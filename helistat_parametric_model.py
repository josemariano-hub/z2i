#!/usr/bin/env python3
"""
Helistat Parametric Design Model
=================================

Physics-based engineering model for designing 4-rotor toroidal helistat vehicles
across the full scale range from 1 kg to 20,000 kg MTOW.

Supports:
- Lithium-sulfur battery powered systems (small scale)
- Hybrid kerosene-electric systems (large scale, T700 engines)

Author: Based on V4 Helistat design files
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

G = 9.81  # m/s² - gravitational acceleration
RHO_AIR_SL = 1.225  # kg/m³ - air density at sea level
RHO_HELIUM_SL = 0.1785  # kg/m³ - helium density at sea level
HELIUM_LIFT_SL = RHO_AIR_SL - RHO_HELIUM_SL  # 1.0465 kg/m³

# ============================================================================
# MATERIAL AND COMPONENT PROPERTIES
# ============================================================================

# Envelope materials (scale-dependent)
ENVELOPE_DENSITY_DYNEEMA = 0.035  # kg/m² - Dyneema ripstop + PU coating (for micro/small scale)
ENVELOPE_DENSITY_NYLON = 0.1  # kg/m² - urethane-coated ripstop nylon (for large scale)

# Battery properties
LIPO_ENERGY_DENSITY = 250  # Wh/kg - conventional Li-Po
LISULFUR_ENERGY_DENSITY = 450  # Wh/kg - Lithium-Sulfur (current tech)
BATTERY_DEPTH_OF_DISCHARGE = 0.8  # Use 80% of capacity for safety

# Motor/ESC efficiency
MOTOR_EFFICIENCY = 0.85  # Electric motor efficiency
ESC_EFFICIENCY = 0.95  # Electronic speed controller efficiency
PROP_EFFICIENCY = 0.75  # Propeller efficiency

# Turbine properties (T700 Black Hawk engine)
T700_POWER_KW = 1400  # kW per engine
T700_WEIGHT_KG = 180  # kg per engine
T700_SFC = 0.2  # kg/kWh - specific fuel consumption
GENERATOR_EFFICIENCY = 0.95
KEROSENE_DENSITY = 0.804  # kg/L


# ============================================================================
# SCALING RELATIONSHIPS
# ============================================================================

def estimate_structural_fraction(mtow_kg: float) -> float:
    """
    Estimate structural weight as fraction of MTOW using empirical scaling.

    For helistats, structural weight scales favorably due to buoyancy support.
    Based on V4 data: 10,000 kg structure / 30,000 kg MTOW = 0.33
    """
    # Empirical: smaller vehicles have higher structural fraction
    if mtow_kg < 10:
        return 0.25  # Micro helistats
    elif mtow_kg < 100:
        return 0.28
    elif mtow_kg < 1000:
        return 0.30
    else:
        return 0.33  # Full scale


def get_envelope_material_density(mtow_kg: float) -> float:
    """
    Select appropriate envelope material based on vehicle scale.

    Small vehicles (<100 kg) use Dyneema fabric for weight savings.
    Large vehicles use conventional nylon for cost and durability.

    Args:
        mtow_kg: Maximum takeoff weight

    Returns:
        Envelope material density in kg/m²
    """
    if mtow_kg < 100:
        return ENVELOPE_DENSITY_DYNEEMA
    else:
        return ENVELOPE_DENSITY_NYLON


def estimate_rotor_diameter(mtow_kg: float, num_rotors: int = 4) -> float:
    """
    Estimate rotor diameter based on disk loading and MTOW.

    Helistats operate at much lower disk loading than conventional helicopters
    due to buoyancy support.

    Target disk loading: 20-30 kg/m² (vs 100-150 kg/m² for helicopters)
    """
    # Total rotor thrust required (assuming 20% of MTOW from rotors)
    rotor_thrust_kg = mtow_kg * 0.2
    thrust_per_rotor_kg = rotor_thrust_kg / num_rotors

    # Target disk loading (lower for efficiency)
    disk_loading = 25  # kg/m²

    # Required disk area
    disk_area = thrust_per_rotor_kg / disk_loading

    # Rotor diameter
    diameter = 2 * math.sqrt(disk_area / math.pi)

    return diameter


# ============================================================================
# TOROIDAL ENVELOPE CALCULATIONS
# ============================================================================

@dataclass
class ToroidGeometry:
    """Toroidal envelope geometry parameters"""
    major_radius: float  # R - distance from toroid center to tube center (m)
    minor_radius: float  # r - tube cross-section radius (m)
    envelope_density: float = ENVELOPE_DENSITY_NYLON  # kg/m² - material density

    @property
    def volume(self) -> float:
        """Volume of torus: V = 2π²Rr²"""
        return 2 * math.pi**2 * self.major_radius * self.minor_radius**2

    @property
    def surface_area(self) -> float:
        """Surface area of torus: A = 4π²Rr"""
        return 4 * math.pi**2 * self.major_radius * self.minor_radius

    @property
    def envelope_weight(self) -> float:
        """Weight of envelope material (kg)"""
        return self.surface_area * self.envelope_density

    @property
    def aspect_ratio(self) -> float:
        """R/r - aspect ratio (typically 2-4)"""
        return self.major_radius / self.minor_radius

    @property
    def material_name(self) -> str:
        """Return material name based on density"""
        if self.envelope_density < 0.05:
            return "Dyneema"
        else:
            return "Nylon"


def design_toroid_for_volume(target_volume: float, aspect_ratio: float = 1.9,
                             envelope_density: float = ENVELOPE_DENSITY_NYLON) -> ToroidGeometry:
    """
    Design a toroid with specified volume and aspect ratio.

    Args:
        target_volume: Desired envelope volume (m³)
        aspect_ratio: R/r ratio (default 1.9 from V4 design)
        envelope_density: Material density in kg/m²

    Returns:
        ToroidGeometry with calculated dimensions
    """
    # From V = 2π²Rr² and R = aspect_ratio * r:
    # V = 2π² * (aspect_ratio * r) * r²
    # V = 2π² * aspect_ratio * r³
    # r³ = V / (2π² * aspect_ratio)

    minor_radius = (target_volume / (2 * math.pi**2 * aspect_ratio)) ** (1/3)
    major_radius = aspect_ratio * minor_radius

    return ToroidGeometry(major_radius, minor_radius, envelope_density)


# ============================================================================
# ROTOR PERFORMANCE CALCULATIONS
# ============================================================================

def rotor_hover_power(thrust_kg: float, rotor_diameter: float,
                     rho: float = RHO_AIR_SL) -> float:
    """
    Calculate rotor hover power using momentum theory.

    P = T^(3/2) / sqrt(2ρA)

    Args:
        thrust_kg: Thrust in kg
        rotor_diameter: Rotor diameter in m
        rho: Air density in kg/m³

    Returns:
        Power in Watts
    """
    thrust_N = thrust_kg * G
    disk_area = math.pi * (rotor_diameter / 2)**2

    # Ideal hover power (momentum theory)
    P_ideal = thrust_N**(3/2) / math.sqrt(2 * rho * disk_area)

    # Apply figure of merit (realistic ~0.75)
    FM = 0.75
    P_actual = P_ideal / FM

    return P_actual


def total_system_power(rotor_power_W: float, num_rotors: int = 4,
                       electric: bool = True) -> float:
    """
    Calculate total system power including losses.

    Args:
        rotor_power_W: Mechanical power at rotor (W)
        num_rotors: Number of rotors
        electric: True for electric, False for turbine

    Returns:
        Total electrical/fuel power required (W)
    """
    total_rotor_power = rotor_power_W * num_rotors

    if electric:
        # Account for motor, ESC, and prop losses
        total_power = total_rotor_power / (MOTOR_EFFICIENCY * ESC_EFFICIENCY * PROP_EFFICIENCY)
    else:
        # Account for generator and motor losses
        total_power = total_rotor_power / (GENERATOR_EFFICIENCY * MOTOR_EFFICIENCY * PROP_EFFICIENCY)

    return total_power


# ============================================================================
# PROPULSION SYSTEM SIZING
# ============================================================================

def size_battery_system(power_W: float, endurance_hours: float,
                       use_lisulfur: bool = True) -> Dict[str, float]:
    """
    Size battery system for electric helistat.

    Args:
        power_W: Total power consumption (W)
        endurance_hours: Desired flight time (hours)
        use_lisulfur: True for Li-S, False for Li-Po

    Returns:
        Dictionary with battery specs
    """
    energy_density = LISULFUR_ENERGY_DENSITY if use_lisulfur else LIPO_ENERGY_DENSITY

    # Energy required (Wh)
    energy_required_Wh = power_W * endurance_hours / BATTERY_DEPTH_OF_DISCHARGE

    # Battery weight
    battery_weight_kg = energy_required_Wh / energy_density

    return {
        'energy_Wh': energy_required_Wh,
        'weight_kg': battery_weight_kg,
        'type': 'Li-S' if use_lisulfur else 'Li-Po',
        'energy_density_Wh_kg': energy_density
    }


def size_turbine_system(power_W: float, num_engines: int = 1) -> Dict[str, float]:
    """
    Size turbine-electric system using T700 engines.

    Args:
        power_W: Total power consumption (W)
        num_engines: Number of T700 engines

    Returns:
        Dictionary with turbine system specs
    """
    power_kW = power_W / 1000

    # Check if power is within engine capability
    max_power_kW = num_engines * T700_POWER_KW

    if power_kW > max_power_kW * 0.8:  # Don't run engines above 80% continuously
        required_engines = math.ceil(power_kW / (T700_POWER_KW * 0.8))
    else:
        required_engines = num_engines

    # Engine weight
    engine_weight_kg = required_engines * T700_WEIGHT_KG

    # Generator weight (estimate ~0.5 kg/kW)
    generator_weight_kg = (power_kW / GENERATOR_EFFICIENCY) * 0.5

    # Fuel consumption
    fuel_flow_kg_hr = (power_kW / GENERATOR_EFFICIENCY) * T700_SFC

    # Total system weight (engines + generators + cooling + fuel system)
    system_weight_kg = engine_weight_kg + generator_weight_kg + 100  # +100kg for ancillaries

    return {
        'num_engines': required_engines,
        'engine_weight_kg': engine_weight_kg,
        'generator_weight_kg': generator_weight_kg,
        'system_weight_kg': system_weight_kg,
        'fuel_flow_kg_hr': fuel_flow_kg_hr,
        'power_kW': power_kW,
        'max_power_kW': required_engines * T700_POWER_KW
    }


# ============================================================================
# COMPLETE HELISTAT DESIGN
# ============================================================================

@dataclass
class HelistatDesign:
    """Complete helistat vehicle design"""
    mtow_kg: float
    buoyancy_fraction: float = 0.8  # 80% buoyancy, 20% rotors
    num_rotors: int = 4
    target_endurance_hours: float = 2.0
    use_lisulfur: bool = True  # For small electric systems
    use_turbine: bool = False  # For large hybrid systems

    def __post_init__(self):
        """Calculate all derived parameters"""
        # Determine propulsion type based on size
        if self.mtow_kg < 100:
            self.use_turbine = False
            self.use_lisulfur = True
        else:
            self.use_turbine = True
            self.use_lisulfur = False

        # Weight breakdown
        self.structural_weight_kg = self.mtow_kg * estimate_structural_fraction(self.mtow_kg)

        # Lift breakdown
        self.buoyant_lift_kg = self.mtow_kg * self.buoyancy_fraction
        self.rotor_thrust_kg = self.mtow_kg * (1 - self.buoyancy_fraction)

        # Helium volume required
        self.total_helium_volume_m3 = self.buoyant_lift_kg / HELIUM_LIFT_SL
        self.volume_per_toroid_m3 = self.total_helium_volume_m3 / self.num_rotors

        # Toroid design (with scale-appropriate material)
        envelope_material_density = get_envelope_material_density(self.mtow_kg)
        self.toroid = design_toroid_for_volume(self.volume_per_toroid_m3,
                                               envelope_density=envelope_material_density)
        self.total_envelope_weight_kg = self.toroid.envelope_weight * self.num_rotors

        # Net buoyancy (after envelope weight)
        self.net_buoyant_lift_kg = self.buoyant_lift_kg - self.total_envelope_weight_kg

        # Rotor sizing
        self.rotor_diameter_m = estimate_rotor_diameter(self.mtow_kg, self.num_rotors)
        self.thrust_per_rotor_kg = self.rotor_thrust_kg / self.num_rotors

        # Power calculations
        power_per_rotor_W = rotor_hover_power(self.thrust_per_rotor_kg, self.rotor_diameter_m)
        self.total_rotor_power_W = total_system_power(power_per_rotor_W, self.num_rotors,
                                                      electric=True)

        # Propulsion system
        if self.use_turbine:
            self.propulsion = size_turbine_system(self.total_rotor_power_W)
            self.propulsion_weight_kg = self.propulsion['system_weight_kg']
            # Fuel weight for endurance
            self.fuel_weight_kg = self.propulsion['fuel_flow_kg_hr'] * self.target_endurance_hours
        else:
            self.propulsion = size_battery_system(self.total_rotor_power_W,
                                                  self.target_endurance_hours,
                                                  self.use_lisulfur)
            self.propulsion_weight_kg = self.propulsion['weight_kg']
            self.fuel_weight_kg = 0

        # Total empty weight
        self.empty_weight_kg = (self.structural_weight_kg +
                               self.total_envelope_weight_kg +
                               self.propulsion_weight_kg)

        # Available payload
        self.payload_capacity_kg = self.mtow_kg - self.empty_weight_kg - self.fuel_weight_kg

        # Performance metrics
        self.disk_loading_kg_m2 = self.thrust_per_rotor_kg / (math.pi * (self.rotor_diameter_m/2)**2)
        self.payload_fraction = self.payload_capacity_kg / self.mtow_kg

    def summary(self) -> str:
        """Generate design summary report"""
        report = f"""
{'='*80}
HELISTAT DESIGN SUMMARY - {self.mtow_kg:.1f} kg MTOW
{'='*80}

CONFIGURATION:
  Number of rotors: {self.num_rotors}
  Rotor diameter: {self.rotor_diameter_m:.2f} m
  Vehicle footprint: ~{self.toroid.major_radius * 4:.1f} m × {self.toroid.major_radius * 4:.1f} m
  Vehicle height: ~{self.toroid.minor_radius * 2:.1f} m

WEIGHT BREAKDOWN:
  MTOW: {self.mtow_kg:.1f} kg
  Empty weight: {self.empty_weight_kg:.1f} kg ({self.empty_weight_kg/self.mtow_kg*100:.1f}%)
    - Structure: {self.structural_weight_kg:.1f} kg
    - Envelopes: {self.total_envelope_weight_kg:.1f} kg
    - Propulsion: {self.propulsion_weight_kg:.1f} kg
  Fuel/battery: {self.fuel_weight_kg:.1f} kg
  Payload: {self.payload_capacity_kg:.1f} kg ({self.payload_fraction*100:.1f}%)

LIFT DISTRIBUTION:
  Buoyant lift: {self.buoyant_lift_kg:.1f} kg ({self.buoyancy_fraction*100:.0f}%)
    - Gross helium lift: {self.buoyant_lift_kg:.1f} kg
    - Envelope weight: -{self.total_envelope_weight_kg:.1f} kg
    - Net buoyancy: {self.net_buoyant_lift_kg:.1f} kg
  Rotor thrust: {self.rotor_thrust_kg:.1f} kg ({(1-self.buoyancy_fraction)*100:.0f}%)
    - Per rotor: {self.thrust_per_rotor_kg:.1f} kg
    - Disk loading: {self.disk_loading_kg_m2:.1f} kg/m²

TOROIDAL ENVELOPE (per envelope):
  Volume: {self.volume_per_toroid_m3:.3f} m³
  Major radius (R): {self.toroid.major_radius:.3f} m
  Minor radius (r): {self.toroid.minor_radius:.3f} m
  Aspect ratio (R/r): {self.toroid.aspect_ratio:.2f}
  Surface area: {self.toroid.surface_area:.2f} m²
  Material: {self.toroid.material_name} ({self.toroid.envelope_density*1000:.0f} g/m²)
  Weight: {self.toroid.envelope_weight:.2f} kg

TOTAL HELIUM:
  Volume: {self.total_helium_volume_m3:.2f} m³
  Weight: {self.total_helium_volume_m3 * RHO_HELIUM_SL:.2f} kg

POWER SYSTEM:
  Total hover power: {self.total_rotor_power_W/1000:.2f} kW
  Power per rotor: {self.total_rotor_power_W/self.num_rotors/1000:.2f} kW
"""

        if self.use_turbine:
            report += f"""
PROPULSION: Turbine-Electric (T700 engines)
  Number of engines: {self.propulsion['num_engines']}
  Engine weight: {self.propulsion['engine_weight_kg']:.1f} kg
  Generator weight: {self.propulsion['generator_weight_kg']:.1f} kg
  System weight: {self.propulsion['system_weight_kg']:.1f} kg
  Fuel flow: {self.propulsion['fuel_flow_kg_hr']:.1f} kg/hr
  Endurance: {self.target_endurance_hours:.1f} hours
  Fuel capacity: {self.fuel_weight_kg:.1f} kg
"""
        else:
            report += f"""
PROPULSION: Battery-Electric ({self.propulsion['type']})
  Battery capacity: {self.propulsion['energy_Wh']:.0f} Wh
  Battery weight: {self.propulsion['weight_kg']:.2f} kg
  Energy density: {self.propulsion['energy_density_Wh_kg']:.0f} Wh/kg
  Endurance: {self.target_endurance_hours:.1f} hours
"""

        report += f"""
PERFORMANCE ESTIMATES:
  Hover endurance: {self.target_endurance_hours:.1f} hours
  Power loading: {self.mtow_kg / (self.total_rotor_power_W/1000):.2f} kg/kW
  Compared to helicopter: ~{80:.0f}% power reduction in hover

{'='*80}
"""
        return report


# ============================================================================
# DESIGN EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("HELISTAT FAMILY PARAMETRIC DESIGN TOOL")
    print("="*80)

    # Design family of helistats
    designs = [
        HelistatDesign(mtow_kg=1, target_endurance_hours=2),      # Micro demonstrator
        HelistatDesign(mtow_kg=10, target_endurance_hours=3),     # Small UAV
        HelistatDesign(mtow_kg=100, target_endurance_hours=4),    # Medium UAV
        HelistatDesign(mtow_kg=1000, target_endurance_hours=3),   # Light cargo
        HelistatDesign(mtow_kg=5000, target_endurance_hours=2),   # Medium cargo
        HelistatDesign(mtow_kg=20000, target_endurance_hours=2),  # Heavy cargo
    ]

    for design in designs:
        print(design.summary())
