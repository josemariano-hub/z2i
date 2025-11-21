#!/usr/bin/env python3
"""
Stratospheric Capsule Thermal Analysis Tool

A comprehensive thermal model for a 2.4m diameter spherical capsule carrying 3 people
to altitudes of 25-30 km. Models conduction, convection, radiation, solar loading,
and internal heat generation using a lumped-parameter approach.

All units in SI unless otherwise noted.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
from enum import Enum
import sys


# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# Stefan-Boltzmann constant [W/(m²·K⁴)]
SIGMA_SB = 5.670374419e-8

# Solar constant at Earth orbit [W/m²]
SOLAR_CONSTANT = 1360.0

# Universal gas constant for dry air [J/(kg·K)]
R_AIR = 287.05

# Specific heat of air at constant pressure [J/(kg·K)]
CP_AIR = 1005.0

# Gravitational acceleration at sea level [m/s²]
G0 = 9.80665

# ISA sea level conditions
T0_ISA = 288.15  # [K]
P0_ISA = 101325.0  # [Pa]
RHO0_ISA = 1.225  # [kg/m³]


# ============================================================================
# ISA ATMOSPHERE MODEL (1976 International Standard Atmosphere)
# ============================================================================

# ISA layer definitions: (base_altitude [m], lapse_rate [K/m], base_temp [K], base_pressure [Pa])
ISA_LAYERS = [
    (0, -0.0065, 288.15, 101325.0),      # Troposphere
    (11000, 0.0, 216.65, 22632.1),        # Tropopause
    (20000, 0.001, 216.65, 5474.89),      # Stratosphere 1
    (32000, 0.0028, 228.65, 868.019),     # Stratosphere 2
    (47000, 0.0, 270.65, 110.906),        # Stratopause
    (51000, -0.0028, 270.65, 66.9389),    # Mesosphere 1
    (71000, -0.002, 214.65, 3.95642),     # Mesosphere 2
]


def isa_atmosphere(altitude: float) -> Tuple[float, float, float]:
    """
    Compute temperature, pressure, and density at a given altitude using ISA 1976.

    Args:
        altitude: Geometric altitude above sea level [m]

    Returns:
        Tuple of (temperature [K], pressure [Pa], density [kg/m³])
    """
    # Find the appropriate layer
    for i, (h_base, lapse, T_base, P_base) in enumerate(ISA_LAYERS):
        if i < len(ISA_LAYERS) - 1:
            h_next = ISA_LAYERS[i + 1][0]
            if altitude < h_next:
                break
        else:
            break

    # Height above layer base
    dh = altitude - h_base

    # Temperature calculation
    if abs(lapse) < 1e-10:  # Isothermal layer
        T = T_base
        # Barometric formula for isothermal layer
        P = P_base * np.exp(-G0 * dh / (R_AIR * T_base))
    else:  # Gradient layer
        T = T_base + lapse * dh
        # Barometric formula for gradient layer
        P = P_base * (T / T_base) ** (-G0 / (lapse * R_AIR))

    # Density from ideal gas law
    rho = P / (R_AIR * T)

    return T, P, rho


# ============================================================================
# ENUMS AND CONFIGURATION TYPES
# ============================================================================

class ShellMaterial(Enum):
    """Material options for the capsule shell."""
    POLYETHYLENE = "polyethylene"
    ALUMINUM = "aluminum"
    CARBON_FIBER = "carbon_fiber"


class CapsuleColor(Enum):
    """Color options affecting solar absorptivity and IR emissivity."""
    WHITE = "white"
    BLACK = "black"
    METALLIC = "metallic"
    CUSTOM = "custom"


class ElectronicsPreset(Enum):
    """Preset electronics configurations."""
    MINIMAL = "minimal"
    STANDARD = "standard"
    HEAVY = "heavy"
    CUSTOM = "custom"


# ============================================================================
# DATACLASSES FOR CONFIGURATION
# ============================================================================

@dataclass
class MaterialProps:
    """Thermal and physical properties of a material."""
    name: str
    density: float          # [kg/m³]
    thermal_cond: float     # [W/(m·K)]
    specific_heat: float    # [J/(kg·K)]
    emissivity: float       # [-] (IR emissivity)
    solar_absorptivity: float  # [-] (solar spectrum absorptivity)


@dataclass
class WindowProps:
    """Properties of the window assembly."""
    major_axis: float = 1.9              # [m]
    minor_axis: float = 1.19             # [m]
    layer_thickness: float = 0.003       # [m] (3mm per polycarbonate layer)
    gap_thickness: float = 0.010         # [m] (10mm air gap)
    pc_thermal_cond: float = 0.20        # [W/(m·K)] polycarbonate
    pc_density: float = 1200.0           # [kg/m³]
    pc_specific_heat: float = 1250.0     # [J/(kg·K)]
    pc_emissivity: float = 0.90          # [-]

    # Optical properties with golden mirror coating
    solar_transmittance: float = 0.15    # [-] (mostly reflected by coating)
    solar_absorptance: float = 0.10      # [-] (absorbed in coating/layers)
    solar_reflectance: float = 0.75      # [-] (reflected by golden mirror)

    @property
    def area(self) -> float:
        """Compute elliptical window area [m²]."""
        return np.pi * (self.major_axis / 2) * (self.minor_axis / 2)

    @property
    def total_thickness(self) -> float:
        """Total window stack thickness [m]."""
        return 2 * self.layer_thickness + self.gap_thickness


@dataclass
class InsulationProps:
    """Properties of interior insulation (polyimide foam)."""
    thickness: float = 0.020             # [m] (20mm default)
    density: float = 50.0                # [kg/m³]
    thermal_cond: float = 0.030          # [W/(m·K)]
    specific_heat: float = 1200.0        # [J/(kg·K)]


@dataclass
class ElectronicsLoad:
    """Electronic devices and their power consumption."""
    devices: Dict[str, float] = field(default_factory=dict)  # {device_name: power [W]}

    @property
    def total_power(self) -> float:
        """Total power dissipated by all devices [W]."""
        return sum(self.devices.values())

    @staticmethod
    def get_preset(preset: ElectronicsPreset) -> 'ElectronicsLoad':
        """Get a preset electronics configuration."""
        if preset == ElectronicsPreset.MINIMAL:
            return ElectronicsLoad({
                "com_radio": 15.0,
                "gps": 10.0,
                "transponder": 15.0,
            })
        elif preset == ElectronicsPreset.STANDARD:
            return ElectronicsLoad({
                "com_radio": 25.0,
                "nav_gps": 15.0,
                "pfd_mfd": 30.0,
                "transponder": 20.0,
                "adsb": 15.0,
                "audio_panel": 10.0,
                "misc_instruments": 20.0,
            })
        elif preset == ElectronicsPreset.HEAVY:
            return ElectronicsLoad({
                "com_radio_1": 25.0,
                "com_radio_2": 25.0,
                "nav_gps": 15.0,
                "pfd_mfd": 40.0,
                "transponder": 20.0,
                "adsb": 15.0,
                "audio_panel": 10.0,
                "misc_instruments": 25.0,
                "cameras": 30.0,
                "datalogger": 15.0,
            })
        else:  # CUSTOM
            return ElectronicsLoad({})


@dataclass
class FlightProfile:
    """Definition of the flight trajectory."""
    ground_altitude: float = 0.0         # [m]
    ground_temperature: float = 288.15   # [K] (15°C)

    ascent_rate: float = 5.0             # [m/s]
    float_altitude: float = 27000.0      # [m]
    float_duration: float = 7200.0       # [s] (2 hours)
    descent_rate: float = 6.0            # [m/s]

    time_step: float = 10.0              # [s]

    def generate_profile(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate time and altitude arrays for the flight.

        Returns:
            Tuple of (time_array [s], altitude_array [m])
        """
        # Ascent phase
        t_ascent = (self.float_altitude - self.ground_altitude) / self.ascent_rate
        n_ascent = int(t_ascent / self.time_step)
        t_asc = np.linspace(0, t_ascent, n_ascent)
        h_asc = self.ground_altitude + self.ascent_rate * t_asc

        # Float phase
        n_float = int(self.float_duration / self.time_step)
        t_flt = np.linspace(t_ascent, t_ascent + self.float_duration, n_float)
        h_flt = np.full(n_float, self.float_altitude)

        # Descent phase
        t_descent = (self.float_altitude - self.ground_altitude) / self.descent_rate
        n_descent = int(t_descent / self.time_step)
        t_end = t_ascent + self.float_duration + t_descent
        t_desc = np.linspace(t_ascent + self.float_duration, t_end, n_descent)
        h_desc = self.float_altitude - self.descent_rate * (t_desc - (t_ascent + self.float_duration))

        # Concatenate
        time = np.concatenate([t_asc, t_flt, t_desc])
        altitude = np.concatenate([h_asc, h_flt, h_desc])

        return time, altitude


@dataclass
class ThermalConfig:
    """Complete thermal analysis configuration."""
    # Geometry
    capsule_radius: float = 1.2          # [m]
    shell_thickness: float = 0.002       # [m] (2mm default)

    # Materials
    shell_material: ShellMaterial = ShellMaterial.ALUMINUM
    insulation: InsulationProps = field(default_factory=InsulationProps)
    window: WindowProps = field(default_factory=WindowProps)

    # Color/optical
    capsule_color: CapsuleColor = CapsuleColor.WHITE
    custom_solar_absorptivity: float = 0.2
    custom_ir_emissivity: float = 0.9

    # Flight
    flight_profile: FlightProfile = field(default_factory=FlightProfile)

    # Environmental
    sun_on: bool = True
    solar_incidence_factor: float = 0.3  # [-] effective sun angle and orientation

    # Convection
    interior_h_conv: float = 5.0         # [W/(m²·K)] interior natural convection

    # Internal loads
    num_occupants: int = 3
    metabolic_heat_per_person: float = 100.0  # [W]
    electronics: ElectronicsLoad = field(default_factory=lambda: ElectronicsLoad.get_preset(ElectronicsPreset.STANDARD))

    # Additional heating/cooling
    aux_heating_power: float = 0.0       # [W]

    # Initial conditions
    initial_temp_interior: float = 288.15  # [K] (15°C)
    initial_temp_shell: float = 288.15
    initial_temp_window: float = 288.15

    # Radiative environment
    effective_sky_temp: float = 220.0    # [K] effective radiative temperature of sky at altitude
    earth_view_factor: float = 0.5       # [-] fraction of capsule "seeing" Earth vs space


# ============================================================================
# MATERIAL PROPERTIES DATABASE
# ============================================================================

def get_shell_material_props(material: ShellMaterial, color: CapsuleColor,
                             custom_alpha: float = 0.2, custom_epsilon: float = 0.9) -> MaterialProps:
    """
    Get thermal properties for a shell material with specified color.

    Args:
        material: Shell material type
        color: Capsule color (affects solar absorptivity and IR emissivity)
        custom_alpha: Custom solar absorptivity (used if color is CUSTOM)
        custom_epsilon: Custom IR emissivity (used if color is CUSTOM)

    Returns:
        MaterialProps with complete thermal properties
    """
    # Base material properties
    if material == ShellMaterial.POLYETHYLENE:
        density = 950.0
        k = 0.4
        cp = 2300.0
        base_name = "Polyethylene"
    elif material == ShellMaterial.ALUMINUM:
        density = 2700.0
        k = 160.0
        cp = 900.0
        base_name = "Aluminum"
    elif material == ShellMaterial.CARBON_FIBER:
        density = 1600.0
        k = 5.0  # Through-thickness (lower than in-plane)
        cp = 1000.0
        base_name = "Carbon Fiber/Epoxy"
    else:
        raise ValueError(f"Unknown material: {material}")

    # Color-dependent optical properties
    if color == CapsuleColor.WHITE:
        alpha = 0.2  # Low solar absorptivity
        epsilon = 0.9  # High IR emissivity
        color_name = "White"
    elif color == CapsuleColor.BLACK:
        alpha = 0.95  # High solar absorptivity
        epsilon = 0.95  # High IR emissivity
        color_name = "Black"
    elif color == CapsuleColor.METALLIC:
        alpha = 0.5  # Medium solar absorptivity
        epsilon = 0.3  # Low IR emissivity (polished metal)
        color_name = "Metallic"
    elif color == CapsuleColor.CUSTOM:
        alpha = custom_alpha
        epsilon = custom_epsilon
        color_name = "Custom"
    else:
        raise ValueError(f"Unknown color: {color}")

    return MaterialProps(
        name=f"{base_name} ({color_name})",
        density=density,
        thermal_cond=k,
        specific_heat=cp,
        emissivity=epsilon,
        solar_absorptivity=alpha
    )


# ============================================================================
# GEOMETRY CALCULATIONS
# ============================================================================

class CapsuleGeometry:
    """Geometric properties of the capsule."""

    def __init__(self, radius: float, shell_thickness: float,
                 insulation_thickness: float, window: WindowProps):
        self.r_outer = radius  # [m]
        self.shell_thickness = shell_thickness  # [m]
        self.insulation_thickness = insulation_thickness  # [m]
        self.window = window

        # Radii
        self.r_shell_inner = self.r_outer - shell_thickness
        self.r_insul_inner = self.r_shell_inner - insulation_thickness

        # Surface areas
        self.area_shell_outer = 4 * np.pi * self.r_outer ** 2  # [m²]
        self.area_window = window.area  # [m²]
        self.area_shell_outer_net = self.area_shell_outer - self.area_window  # [m²]

        # Inner surface area (approximate as sphere at inner radius)
        self.area_shell_inner = 4 * np.pi * self.r_shell_inner ** 2  # [m²]
        self.area_insul_inner = 4 * np.pi * self.r_insul_inner ** 2  # [m²]

        # Volumes
        self.volume_shell = (4/3) * np.pi * (self.r_outer**3 - self.r_shell_inner**3)  # [m³]
        self.volume_insulation = (4/3) * np.pi * (self.r_shell_inner**3 - self.r_insul_inner**3)  # [m³]
        self.volume_interior = (4/3) * np.pi * self.r_insul_inner**3  # [m³]

    def print_summary(self):
        """Print geometric summary."""
        print("\n=== Capsule Geometry ===")
        print(f"Outer radius: {self.r_outer:.3f} m")
        print(f"Shell thickness: {self.shell_thickness*1000:.1f} mm")
        print(f"Insulation thickness: {self.insulation_thickness*1000:.1f} mm")
        print(f"Inner radius: {self.r_insul_inner:.3f} m")
        print(f"\nOuter shell area (total): {self.area_shell_outer:.2f} m²")
        print(f"Window area: {self.area_window:.2f} m²")
        print(f"Outer shell area (net): {self.area_shell_outer_net:.2f} m²")
        print(f"Interior volume: {self.volume_interior:.2f} m³")


# ============================================================================
# HEAT TRANSFER FUNCTIONS
# ============================================================================

def exterior_convection_coefficient(altitude: float, velocity: float,
                                    char_length: float = 2.4) -> float:
    """
    Estimate exterior convective heat transfer coefficient.

    Uses a simplified empirical correlation based on Reynolds number and
    atmospheric density variation with altitude.

    Args:
        altitude: Current altitude [m]
        velocity: Relative velocity (vertical rate or wind) [m/s]
        char_length: Characteristic length (capsule diameter) [m]

    Returns:
        Convective heat transfer coefficient [W/(m²·K)]
    """
    T_amb, P_amb, rho_amb = isa_atmosphere(altitude)

    # Avoid division by zero at very high altitudes
    if rho_amb < 1e-6:
        return 0.1  # Negligible convection in near-vacuum

    # Dynamic viscosity of air (Sutherland's law approximation)
    mu_ref = 1.716e-5  # [Pa·s] at 273K
    T_ref = 273.15
    S = 110.4  # Sutherland constant [K]
    mu = mu_ref * (T_amb / T_ref)**1.5 * (T_ref + S) / (T_amb + S)

    # Reynolds number
    Re = rho_amb * velocity * char_length / mu

    # Thermal conductivity of air (approximate)
    k_air = 0.024 * (T_amb / 273.15)**0.8  # [W/(m·K)]

    # Nusselt number correlation for sphere (forced convection)
    # Nu = 2 + 0.6 * Re^0.5 * Pr^(1/3)
    Pr = 0.71  # Prandtl number for air
    if Re > 1:
        Nu = 2.0 + 0.6 * Re**0.5 * Pr**(1/3)
    else:
        Nu = 2.0  # Minimum Nusselt (pure conduction limit)

    h = Nu * k_air / char_length

    return max(h, 0.1)  # Minimum threshold


def conduction_resistance(thickness: float, area: float, thermal_cond: float) -> float:
    """
    Compute thermal resistance for planar conduction.

    Args:
        thickness: Material thickness [m]
        area: Heat transfer area [m²]
        thermal_cond: Thermal conductivity [W/(m·K)]

    Returns:
        Thermal resistance [K/W]
    """
    return thickness / (thermal_cond * area)


def radiation_heat_transfer(T_surface: float, T_environment: float,
                           emissivity: float, area: float, view_factor: float = 1.0) -> float:
    """
    Compute net radiative heat transfer (positive = heat loss from surface).

    Args:
        T_surface: Surface temperature [K]
        T_environment: Environment radiative temperature [K]
        emissivity: Surface emissivity [-]
        area: Surface area [m²]
        view_factor: View factor to environment [-]

    Returns:
        Net radiative heat loss [W]
    """
    # Clamp temperatures to reasonable physical bounds to avoid overflow
    T_surf_clamped = np.clip(T_surface, 1.0, 1500.0)  # [K]
    T_env_clamped = np.clip(T_environment, 1.0, 1500.0)  # [K]

    return view_factor * emissivity * area * SIGMA_SB * (T_surf_clamped**4 - T_env_clamped**4)


def effective_earth_temperature(altitude: float) -> float:
    """
    Estimate effective radiative temperature of Earth as seen from altitude.

    At low altitudes, Earth appears warm (~280-290K).
    At high altitudes, still sees Earth but cooler effective temperature.

    Args:
        altitude: Current altitude [m]

    Returns:
        Effective Earth radiative temperature [K]
    """
    T_ground = 288.15  # [K] typical ground temperature
    T_cloud_top = 220.0  # [K] typical cloud-top/tropopause temperature

    # Simple interpolation: at ground, see ground; at 15km+, see cloud tops
    h_transition = 15000.0  # [m]
    if altitude < h_transition:
        factor = altitude / h_transition
        T_eff = T_ground * (1 - factor) + T_cloud_top * factor
    else:
        T_eff = T_cloud_top

    return T_eff


# ============================================================================
# THERMAL NETWORK MODEL
# ============================================================================

class ThermalModel:
    """
    Lumped-parameter thermal model of the capsule.

    Nodes:
        0: Shell outer surface
        1: Shell inner surface
        2: Insulation inner surface
        3: Window (simplified single node)
        4: Interior air
        5: Interior mass (optional - seats, equipment, floor)
    """

    def __init__(self, config: ThermalConfig):
        self.config = config

        # Get material properties
        self.shell_props = get_shell_material_props(
            config.shell_material,
            config.capsule_color,
            config.custom_solar_absorptivity,
            config.custom_ir_emissivity
        )

        # Geometry
        self.geom = CapsuleGeometry(
            config.capsule_radius,
            config.shell_thickness,
            config.insulation.thickness,
            config.window
        )

        # Generate flight profile
        self.time, self.altitude = config.flight_profile.generate_profile()
        self.n_steps = len(self.time)

        # Number of thermal nodes
        self.n_nodes = 6

        # Initialize temperature arrays (all nodes at initial interior temp)
        self.T = np.zeros((self.n_steps, self.n_nodes))
        self.T[0, :] = config.initial_temp_interior
        self.T[0, 0] = config.initial_temp_shell  # Shell outer
        self.T[0, 3] = config.initial_temp_window  # Window

        # Compute node thermal masses [J/K]
        self.thermal_mass = self._compute_thermal_masses()

        # Storage for heat flux components (for analysis)
        self.heat_fluxes = {
            'solar_shell': np.zeros(self.n_steps),
            'solar_window': np.zeros(self.n_steps),
            'conv_exterior': np.zeros(self.n_steps),
            'rad_exterior': np.zeros(self.n_steps),
            'internal_gen': np.zeros(self.n_steps),
            'conv_interior': np.zeros(self.n_steps),
        }

    def _compute_thermal_masses(self) -> np.ndarray:
        """Compute thermal mass for each node [J/K]."""
        masses = np.zeros(self.n_nodes)

        # Node 0: Shell outer surface (use half shell mass)
        m_shell = self.shell_props.density * self.geom.volume_shell
        masses[0] = 0.5 * m_shell * self.shell_props.specific_heat

        # Node 1: Shell inner surface (other half)
        masses[1] = 0.5 * m_shell * self.shell_props.specific_heat

        # Node 2: Insulation inner surface
        m_insul = self.config.insulation.density * self.geom.volume_insulation
        masses[2] = m_insul * self.config.insulation.specific_heat

        # Node 3: Window (two polycarbonate layers)
        V_window = self.config.window.area * 2 * self.config.window.layer_thickness
        m_window = self.config.window.pc_density * V_window
        masses[3] = m_window * self.config.window.pc_specific_heat

        # Node 4: Interior air
        T_init = self.config.initial_temp_interior
        P_init, _, _ = isa_atmosphere(self.config.flight_profile.ground_altitude)
        rho_air_init = P_init / (R_AIR * T_init)
        m_air = rho_air_init * self.geom.volume_interior
        masses[4] = m_air * CP_AIR

        # Node 5: Interior solid mass (estimate ~200 kg of seats, floor, equipment)
        m_internal_solids = 200.0  # [kg]
        cp_internal = 900.0  # [J/(kg·K)] average for aluminum/composites
        masses[5] = m_internal_solids * cp_internal

        # Apply minimum thermal mass to avoid numerical instability
        # (at least 1000 J/K per node for stability)
        min_thermal_mass = 1000.0  # [J/K]
        masses = np.maximum(masses, min_thermal_mass)

        return masses

    def compute_heat_balance(self, i: int, T_current: np.ndarray) -> np.ndarray:
        """
        Compute dT/dt for each node at time step i.

        Args:
            i: Time step index
            T_current: Current temperatures [K] for all nodes

        Returns:
            Array of dT/dt [K/s] for each node
        """
        # Unpack current temperatures
        T_shell_out = T_current[0]
        T_shell_in = T_current[1]
        T_insul_in = T_current[2]
        T_window = T_current[3]
        T_air = T_current[4]
        T_mass = T_current[5]

        # Current altitude and ambient conditions
        h = self.altitude[i]
        T_amb, P_amb, rho_amb = isa_atmosphere(h)

        # Velocity (vertical rate) for exterior convection
        if i > 0:
            dt = self.time[i] - self.time[i-1]
            if dt > 0:
                v_vertical = abs((self.altitude[i] - self.altitude[i-1]) / dt)
            else:
                v_vertical = self.config.flight_profile.ascent_rate
        else:
            v_vertical = self.config.flight_profile.ascent_rate

        # Add some residual wind (especially at float)
        v_wind = 5.0  # [m/s] assumed wind speed
        v_rel = np.sqrt(v_vertical**2 + v_wind**2)

        # Exterior convection coefficient
        h_ext = exterior_convection_coefficient(h, v_rel, char_length=2*self.geom.r_outer)

        # Interior convection coefficient
        h_int = self.config.interior_h_conv

        # Initialize heat flows to each node [W]
        Q_dot = np.zeros(self.n_nodes)

        # ========================================
        # NODE 0: SHELL OUTER SURFACE
        # ========================================

        # Solar heating on shell (if sun is on)
        Q_solar_shell = 0.0
        if self.config.sun_on:
            # Solar flux on shell area (excluding window)
            A_shell_solar = self.geom.area_shell_outer_net
            Q_solar_shell = (self.config.solar_incidence_factor *
                           SOLAR_CONSTANT *
                           self.shell_props.solar_absorptivity *
                           A_shell_solar)
            self.heat_fluxes['solar_shell'][i] = Q_solar_shell

        # Exterior convection (shell to ambient)
        Q_conv_ext_shell = h_ext * self.geom.area_shell_outer_net * (T_amb - T_shell_out)

        # Exterior radiation from shell
        # View factors: fraction to space vs Earth
        T_space = 3.0  # [K] deep space
        T_earth = effective_earth_temperature(h)
        f_space = 0.5  # Approximate: half-sphere sees space, half sees Earth
        f_earth = 0.5

        Q_rad_space = radiation_heat_transfer(T_shell_out, T_space,
                                             self.shell_props.emissivity,
                                             self.geom.area_shell_outer_net,
                                             view_factor=f_space)
        Q_rad_earth = radiation_heat_transfer(T_shell_out, T_earth,
                                             self.shell_props.emissivity,
                                             self.geom.area_shell_outer_net,
                                             view_factor=f_earth)
        Q_rad_ext_shell = Q_rad_space + Q_rad_earth

        self.heat_fluxes['conv_exterior'][i] += Q_conv_ext_shell
        self.heat_fluxes['rad_exterior'][i] += Q_rad_ext_shell

        # Conduction through shell (node 0 to node 1)
        R_shell = conduction_resistance(self.config.shell_thickness,
                                       self.geom.area_shell_inner,
                                       self.shell_props.thermal_cond)
        Q_cond_shell = (T_shell_out - T_shell_in) / R_shell

        # Net heat to node 0
        Q_dot[0] = Q_solar_shell + Q_conv_ext_shell - Q_rad_ext_shell - Q_cond_shell

        # ========================================
        # NODE 1: SHELL INNER SURFACE
        # ========================================

        # Conduction from shell outer (node 0)
        Q_dot[1] += Q_cond_shell

        # Conduction through insulation (node 1 to node 2)
        R_insul = conduction_resistance(self.config.insulation.thickness,
                                       self.geom.area_insul_inner,
                                       self.config.insulation.thermal_cond)
        Q_cond_insul = (T_shell_in - T_insul_in) / R_insul
        Q_dot[1] -= Q_cond_insul

        # ========================================
        # NODE 2: INSULATION INNER SURFACE
        # ========================================

        # Conduction from shell inner
        Q_dot[2] += Q_cond_insul

        # Convection to interior air (node 2 to node 4)
        Q_conv_insul_air = h_int * self.geom.area_insul_inner * (T_insul_in - T_air)
        Q_dot[2] -= Q_conv_insul_air

        # Radiation to interior (simplified: insulation to air/internal mass)
        # Approximate as small correction, can be refined
        epsilon_insul = 0.8  # Typical foam emissivity
        Q_rad_insul_air = radiation_heat_transfer(T_insul_in, T_air,
                                                  epsilon_insul,
                                                  self.geom.area_insul_inner,
                                                  view_factor=0.5)
        Q_dot[2] -= Q_rad_insul_air

        # ========================================
        # NODE 3: WINDOW
        # ========================================

        # Solar heating on window
        Q_solar_window = 0.0
        if self.config.sun_on:
            Q_solar_window = (self.config.solar_incidence_factor *
                            SOLAR_CONSTANT *
                            self.config.window.solar_absorptance *
                            self.geom.area_window)
            self.heat_fluxes['solar_window'][i] = Q_solar_window

        # Exterior convection (window to ambient)
        Q_conv_ext_window = h_ext * self.geom.area_window * (T_amb - T_window)

        # Exterior radiation from window
        Q_rad_space_win = radiation_heat_transfer(T_window, T_space,
                                                 self.config.window.pc_emissivity,
                                                 self.geom.area_window,
                                                 view_factor=f_space)
        Q_rad_earth_win = radiation_heat_transfer(T_window, T_earth,
                                                 self.config.window.pc_emissivity,
                                                 self.geom.area_window,
                                                 view_factor=f_earth)
        Q_rad_ext_window = Q_rad_space_win + Q_rad_earth_win

        self.heat_fluxes['conv_exterior'][i] += Q_conv_ext_window
        self.heat_fluxes['rad_exterior'][i] += Q_rad_ext_window

        # Interior convection (window to air)
        Q_conv_window_air = h_int * self.geom.area_window * (T_window - T_air)

        # Net heat to window
        Q_dot[3] = Q_solar_window + Q_conv_ext_window - Q_rad_ext_window - Q_conv_window_air

        # ========================================
        # NODE 4: INTERIOR AIR
        # ========================================

        # Convection from insulation
        Q_dot[4] += Q_conv_insul_air

        # Radiation from insulation (approximate)
        Q_dot[4] += Q_rad_insul_air

        # Convection from window
        Q_dot[4] += Q_conv_window_air

        # Convection between air and internal mass (node 4 to node 5)
        A_mass_conv = 5.0  # [m²] effective area of internal surfaces
        Q_conv_air_mass = h_int * A_mass_conv * (T_air - T_mass)
        Q_dot[4] -= Q_conv_air_mass

        # Internal heat generation
        Q_internal = (self.config.num_occupants * self.config.metabolic_heat_per_person +
                     self.config.electronics.total_power +
                     self.config.aux_heating_power)
        Q_dot[4] += Q_internal
        self.heat_fluxes['internal_gen'][i] = Q_internal

        self.heat_fluxes['conv_interior'][i] = Q_conv_insul_air + Q_conv_window_air - Q_conv_air_mass

        # ========================================
        # NODE 5: INTERIOR MASS
        # ========================================

        # Convection from air
        Q_dot[5] += Q_conv_air_mass

        # Compute dT/dt for each node
        dT_dt = Q_dot / self.thermal_mass

        return dT_dt

    def solve(self):
        """Solve the thermal model over the entire flight profile using forward Euler."""
        print("\n=== Running Thermal Simulation ===")
        print(f"Total time steps: {self.n_steps}")
        print(f"Time step: {self.config.flight_profile.time_step} s")

        max_dT_per_step = 5.0  # [K] maximum temperature change per time step (stability limit)

        for i in range(1, self.n_steps):
            dt = self.time[i] - self.time[i-1]
            if dt <= 0:
                dt = self.config.flight_profile.time_step

            # Compute heat balance at previous step
            dT_dt = self.compute_heat_balance(i-1, self.T[i-1, :])

            # Limit temperature rate of change for stability
            dT_dt = np.clip(dT_dt, -max_dT_per_step/dt, max_dT_per_step/dt)

            # Forward Euler integration
            self.T[i, :] = self.T[i-1, :] + dT_dt * dt

            # Clamp temperatures to physically reasonable bounds [K]
            self.T[i, :] = np.clip(self.T[i, :], 150.0, 450.0)

            # Progress indicator
            if i % (self.n_steps // 10) == 0:
                progress = 100 * i / self.n_steps
                h_current = self.altitude[i]
                T_air_current = self.T[i, 4] - 273.15  # Convert to Celsius
                print(f"  Progress: {progress:.0f}% | Alt: {h_current/1000:.1f} km | T_interior: {T_air_current:.1f} °C")

        print("Simulation complete!\n")

    def print_summary(self):
        """Print summary of thermal analysis results."""
        print("\n" + "="*60)
        print("THERMAL ANALYSIS SUMMARY")
        print("="*60)

        # Convert temperatures to Celsius for readability
        T_air_C = self.T[:, 4] - 273.15
        T_shell_out_C = self.T[:, 0] - 273.15
        T_shell_in_C = self.T[:, 1] - 273.15
        T_window_C = self.T[:, 3] - 273.15

        print("\nMaterial Configuration:")
        print(f"  Shell: {self.shell_props.name}")
        print(f"  Shell thickness: {self.config.shell_thickness*1000:.1f} mm")
        print(f"  Insulation thickness: {self.config.insulation.thickness*1000:.1f} mm")
        print(f"  Solar absorptivity: {self.shell_props.solar_absorptivity:.2f}")
        print(f"  IR emissivity: {self.shell_props.emissivity:.2f}")

        print("\nFlight Profile:")
        print(f"  Max altitude: {np.max(self.altitude)/1000:.1f} km")
        print(f"  Total duration: {self.time[-1]/3600:.2f} hours")
        print(f"  Sun: {'ON' if self.config.sun_on else 'OFF'}")

        print("\nInternal Heat Generation:")
        print(f"  Occupants: {self.config.num_occupants} × {self.config.metabolic_heat_per_person:.0f} W = {self.config.num_occupants * self.config.metabolic_heat_per_person:.0f} W")
        print(f"  Electronics: {self.config.electronics.total_power:.0f} W")
        print(f"  Auxiliary: {self.config.aux_heating_power:.0f} W")
        total_internal = (self.config.num_occupants * self.config.metabolic_heat_per_person +
                         self.config.electronics.total_power +
                         self.config.aux_heating_power)
        print(f"  TOTAL: {total_internal:.0f} W")

        print("\n" + "-"*60)
        print("TEMPERATURE RESULTS (°C)")
        print("-"*60)

        print("\nInterior Air:")
        print(f"  Initial:  {T_air_C[0]:6.1f} °C")
        print(f"  Minimum:  {np.min(T_air_C):6.1f} °C  (at t={self.time[np.argmin(T_air_C)]/3600:.2f} h)")
        print(f"  Maximum:  {np.max(T_air_C):6.1f} °C  (at t={self.time[np.argmax(T_air_C)]/3600:.2f} h)")
        print(f"  Final:    {T_air_C[-1]:6.1f} °C")

        print("\nShell Outer Surface:")
        print(f"  Minimum:  {np.min(T_shell_out_C):6.1f} °C")
        print(f"  Maximum:  {np.max(T_shell_out_C):6.1f} °C")

        print("\nWindow:")
        print(f"  Minimum:  {np.min(T_window_C):6.1f} °C")
        print(f"  Maximum:  {np.max(T_window_C):6.1f} °C")

        # Thermal comfort assessment (rough guidelines)
        print("\n" + "-"*60)
        print("THERMAL COMFORT ASSESSMENT")
        print("-"*60)

        comfort_min = 18.0  # °C
        comfort_max = 26.0  # °C

        too_cold = T_air_C < comfort_min
        too_hot = T_air_C > comfort_max
        comfortable = ~too_cold & ~too_hot

        total_time_hours = self.time[-1] / 3600
        time_comfortable = np.sum(comfortable) * self.config.flight_profile.time_step / 3600
        time_cold = np.sum(too_cold) * self.config.flight_profile.time_step / 3600
        time_hot = np.sum(too_hot) * self.config.flight_profile.time_step / 3600

        print(f"\nComfortable range: {comfort_min}–{comfort_max} °C")
        print(f"  Comfortable: {time_comfortable:5.2f} h ({100*time_comfortable/total_time_hours:5.1f}%)")
        print(f"  Too cold:    {time_cold:5.2f} h ({100*time_cold/total_time_hours:5.1f}%)")
        print(f"  Too hot:     {time_hot:5.2f} h ({100*time_hot/total_time_hours:5.1f}%)")

        # Material risk assessment
        print("\n" + "-"*60)
        print("MATERIAL RISK ASSESSMENT")
        print("-"*60)

        # Polycarbonate glass transition / softening
        T_pc_soften = 150.0  # °C (approximate)
        if np.max(T_window_C) > T_pc_soften:
            print(f"\n⚠ WARNING: Window temperature exceeds polycarbonate softening point!")
            print(f"  Max window temp: {np.max(T_window_C):.1f} °C")
            print(f"  Softening point: {T_pc_soften:.1f} °C")
        else:
            print(f"\n✓ Window temperature OK (max: {np.max(T_window_C):.1f} °C < {T_pc_soften:.1f} °C)")

        # Polyimide foam max temp
        T_foam_max = 200.0  # °C (typical for polyimide)
        T_insul_max_C = np.max(self.T[:, 2]) - 273.15
        if T_insul_max_C > T_foam_max:
            print(f"\n⚠ WARNING: Insulation temperature exceeds max rating!")
            print(f"  Max insulation temp: {T_insul_max_C:.1f} °C")
            print(f"  Max rating: {T_foam_max:.1f} °C")
        else:
            print(f"✓ Insulation temperature OK (max: {T_insul_max_C:.1f} °C < {T_foam_max:.1f} °C)")

        # Polyethylene melting
        if self.config.shell_material == ShellMaterial.POLYETHYLENE:
            T_pe_melt = 130.0  # °C (HDPE melting point)
            if np.max(T_shell_out_C) > T_pe_melt:
                print(f"\n⚠ WARNING: Shell temperature approaches polyethylene melting point!")
                print(f"  Max shell temp: {np.max(T_shell_out_C):.1f} °C")
                print(f"  Melting point: {T_pe_melt:.1f} °C")
            else:
                print(f"✓ Shell temperature OK (max: {np.max(T_shell_out_C):.1f} °C < {T_pe_melt:.1f} °C)")

        print("\n" + "="*60 + "\n")

    def plot_results(self):
        """Generate plots of thermal analysis results."""
        # Convert time to hours
        time_hours = self.time / 3600

        # Convert temperatures to Celsius
        T_air_C = self.T[:, 4] - 273.15
        T_shell_out_C = self.T[:, 0] - 273.15
        T_shell_in_C = self.T[:, 1] - 273.15
        T_insul_in_C = self.T[:, 2] - 273.15
        T_window_C = self.T[:, 3] - 273.15
        T_mass_C = self.T[:, 5] - 273.15

        # Altitude in km
        altitude_km = self.altitude / 1000

        # Ambient temperature
        T_amb = np.array([isa_atmosphere(h)[0] for h in self.altitude]) - 273.15

        # Create figure with subplots
        fig = plt.figure(figsize=(14, 10))

        # Subplot 1: Altitude profile
        ax1 = plt.subplot(3, 2, 1)
        ax1.plot(time_hours, altitude_km, 'b-', linewidth=2)
        ax1.set_xlabel('Time [h]')
        ax1.set_ylabel('Altitude [km]')
        ax1.set_title('Flight Profile')
        ax1.grid(True, alpha=0.3)

        # Subplot 2: Interior air temperature
        ax2 = plt.subplot(3, 2, 2)
        ax2.plot(time_hours, T_air_C, 'r-', linewidth=2, label='Interior Air')
        ax2.axhline(18, color='b', linestyle='--', alpha=0.5, label='Comfort Min')
        ax2.axhline(26, color='orange', linestyle='--', alpha=0.5, label='Comfort Max')
        ax2.set_xlabel('Time [h]')
        ax2.set_ylabel('Temperature [°C]')
        ax2.set_title('Interior Air Temperature')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Subplot 3: All temperatures
        ax3 = plt.subplot(3, 2, 3)
        ax3.plot(time_hours, T_shell_out_C, label='Shell Outer', linewidth=1.5)
        ax3.plot(time_hours, T_shell_in_C, label='Shell Inner', linewidth=1.5)
        ax3.plot(time_hours, T_insul_in_C, label='Insulation Inner', linewidth=1.5)
        ax3.plot(time_hours, T_window_C, label='Window', linewidth=1.5)
        ax3.plot(time_hours, T_air_C, label='Interior Air', linewidth=2)
        ax3.plot(time_hours, T_amb, 'k--', label='Ambient', linewidth=1, alpha=0.6)
        ax3.set_xlabel('Time [h]')
        ax3.set_ylabel('Temperature [°C]')
        ax3.set_title('All Node Temperatures')
        ax3.legend(loc='best', fontsize=8)
        ax3.grid(True, alpha=0.3)

        # Subplot 4: Heat flux breakdown
        ax4 = plt.subplot(3, 2, 4)
        ax4.plot(time_hours, self.heat_fluxes['solar_shell'] + self.heat_fluxes['solar_window'],
                label='Solar Absorbed', linewidth=1.5)
        ax4.plot(time_hours, self.heat_fluxes['internal_gen'],
                label='Internal Generation', linewidth=1.5)
        ax4.plot(time_hours, -self.heat_fluxes['rad_exterior'],
                label='Radiative Loss', linewidth=1.5)
        ax4.plot(time_hours, self.heat_fluxes['conv_exterior'],
                label='Convective Exchange', linewidth=1.5)
        ax4.set_xlabel('Time [h]')
        ax4.set_ylabel('Heat Flow [W]')
        ax4.set_title('Heat Flux Components')
        ax4.legend(loc='best', fontsize=8)
        ax4.grid(True, alpha=0.3)

        # Subplot 5: Temperature vs altitude
        ax5 = plt.subplot(3, 2, 5)
        ax5.plot(T_air_C, altitude_km, 'r-', linewidth=2, label='Interior Air')
        ax5.plot(T_amb, altitude_km, 'k--', linewidth=1, alpha=0.6, label='Ambient')
        ax5.set_xlabel('Temperature [°C]')
        ax5.set_ylabel('Altitude [km]')
        ax5.set_title('Temperature vs Altitude')
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # Subplot 6: Temperature difference (interior - ambient)
        ax6 = plt.subplot(3, 2, 6)
        delta_T = T_air_C - T_amb
        ax6.plot(time_hours, delta_T, 'g-', linewidth=2)
        ax6.axhline(0, color='k', linestyle='-', alpha=0.3)
        ax6.set_xlabel('Time [h]')
        ax6.set_ylabel('ΔT [°C]')
        ax6.set_title('Interior - Ambient Temperature Difference')
        ax6.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


# ============================================================================
# INTERACTIVE CLI
# ============================================================================

def get_float_input(prompt: str, default: float) -> float:
    """Get float input from user with default value."""
    while True:
        user_input = input(f"{prompt} [{default}]: ").strip()
        if not user_input:
            return default
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int_input(prompt: str, default: int) -> int:
    """Get integer input from user with default value."""
    while True:
        user_input = input(f"{prompt} [{default}]: ").strip()
        if not user_input:
            return default
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_bool_input(prompt: str, default: bool) -> bool:
    """Get boolean input from user with default value."""
    default_str = "y" if default else "n"
    while True:
        user_input = input(f"{prompt} (y/n) [{default_str}]: ").strip().lower()
        if not user_input:
            return default
        if user_input in ['y', 'yes', 'true', '1']:
            return True
        if user_input in ['n', 'no', 'false', '0']:
            return False
        print("Invalid input. Please enter y or n.")


def select_enum(prompt: str, enum_class, default):
    """Select an enum value from a list."""
    options = list(enum_class)
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        marker = " (default)" if option == default else ""
        print(f"  {i}. {option.value}{marker}")

    while True:
        user_input = input(f"Select [1-{len(options)}] or press Enter for default: ").strip()
        if not user_input:
            return default
        try:
            idx = int(user_input) - 1
            if 0 <= idx < len(options):
                return options[idx]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def configure_interactive() -> ThermalConfig:
    """Interactive configuration of thermal analysis."""
    print("\n" + "="*60)
    print("STRATOSPHERIC CAPSULE THERMAL ANALYSIS")
    print("="*60)
    print("\nInteractive Configuration")
    print("(Press Enter to accept default values shown in brackets)\n")

    config = ThermalConfig()

    # Flight profile
    print("\n--- Flight Profile ---")
    config.flight_profile.ground_altitude = get_float_input(
        "Ground altitude [m]", config.flight_profile.ground_altitude)
    config.flight_profile.ascent_rate = get_float_input(
        "Ascent rate [m/s]", config.flight_profile.ascent_rate)
    config.flight_profile.float_altitude = get_float_input(
        "Float altitude [m]", config.flight_profile.float_altitude)
    float_duration_hours = get_float_input(
        "Time at float [hours]", config.flight_profile.float_duration / 3600)
    config.flight_profile.float_duration = float_duration_hours * 3600
    config.flight_profile.descent_rate = get_float_input(
        "Descent rate [m/s]", config.flight_profile.descent_rate)

    # Materials
    print("\n--- Material Configuration ---")
    config.shell_material = select_enum(
        "Select shell material:", ShellMaterial, ShellMaterial.ALUMINUM)

    config.shell_thickness = get_float_input(
        "Shell thickness [mm]", config.shell_thickness * 1000) / 1000

    config.insulation.thickness = get_float_input(
        "Insulation thickness [mm]", config.insulation.thickness * 1000) / 1000

    config.capsule_color = select_enum(
        "Select capsule color:", CapsuleColor, CapsuleColor.WHITE)

    if config.capsule_color == CapsuleColor.CUSTOM:
        config.custom_solar_absorptivity = get_float_input(
            "Custom solar absorptivity (0-1)", 0.2)
        config.custom_ir_emissivity = get_float_input(
            "Custom IR emissivity (0-1)", 0.9)

    # Environmental
    print("\n--- Environmental Conditions ---")
    config.sun_on = get_bool_input("Sun ON (daytime flight)?", config.sun_on)
    if config.sun_on:
        config.solar_incidence_factor = get_float_input(
            "Solar incidence factor (0-1)", config.solar_incidence_factor)

    # Internal loads
    print("\n--- Internal Heat Generation ---")
    config.num_occupants = get_int_input(
        "Number of occupants", config.num_occupants)
    config.metabolic_heat_per_person = get_float_input(
        "Metabolic heat per person [W]", config.metabolic_heat_per_person)

    electronics_preset = select_enum(
        "Select electronics configuration:",
        ElectronicsPreset, ElectronicsPreset.STANDARD)
    config.electronics = ElectronicsLoad.get_preset(electronics_preset)

    if electronics_preset == ElectronicsPreset.CUSTOM:
        print("\nEnter custom electronics loads (Enter 0 to finish):")
        while True:
            device_name = input("  Device name (or press Enter to finish): ").strip()
            if not device_name:
                break
            power = get_float_input(f"  Power for {device_name} [W]", 10.0)
            config.electronics.devices[device_name] = power

    print(f"\nTotal electronics power: {config.electronics.total_power:.0f} W")

    config.aux_heating_power = get_float_input(
        "Additional heating/cooling power [W]", config.aux_heating_power)

    # Convection
    print("\n--- Heat Transfer Parameters ---")
    config.interior_h_conv = get_float_input(
        "Interior convection coefficient [W/(m²·K)]", config.interior_h_conv)

    return config


def run_preset_scenario(scenario_name: str) -> ThermalConfig:
    """Run a predefined scenario."""
    config = ThermalConfig()

    if scenario_name == "day_standard":
        print("\n=== SCENARIO: Standard Daytime Flight ===")
        config.sun_on = True
        config.solar_incidence_factor = 0.3
        config.capsule_color = CapsuleColor.WHITE
        config.shell_material = ShellMaterial.ALUMINUM
        config.shell_thickness = 0.002  # 2mm
        config.insulation.thickness = 0.020  # 20mm
        config.flight_profile.float_altitude = 27000.0
        config.flight_profile.float_duration = 7200.0  # 2 hours

    elif scenario_name == "night_cold":
        print("\n=== SCENARIO: Night Flight (Cold Soak) ===")
        config.sun_on = False
        config.capsule_color = CapsuleColor.BLACK
        config.shell_material = ShellMaterial.ALUMINUM
        config.shell_thickness = 0.002
        config.insulation.thickness = 0.030  # Thicker insulation
        config.flight_profile.float_altitude = 27000.0
        config.flight_profile.float_duration = 14400.0  # 4 hours

    elif scenario_name == "hot_day":
        print("\n=== SCENARIO: Hot Day, High Solar Loading ===")
        config.sun_on = True
        config.solar_incidence_factor = 0.6  # High sun angle
        config.capsule_color = CapsuleColor.BLACK  # Worst case
        config.shell_material = ShellMaterial.POLYETHYLENE
        config.shell_thickness = 0.001  # Thin PE film
        config.insulation.thickness = 0.015
        config.flight_profile.float_altitude = 25000.0
        config.flight_profile.float_duration = 3600.0  # 1 hour
        config.aux_heating_power = 500.0  # Extra heat load

    elif scenario_name == "long_flight":
        print("\n=== SCENARIO: Extended Duration Flight ===")
        config.sun_on = True
        config.solar_incidence_factor = 0.25
        config.capsule_color = CapsuleColor.WHITE
        config.shell_material = ShellMaterial.CARBON_FIBER
        config.shell_thickness = 0.003  # 3mm CFRP
        config.insulation.thickness = 0.025
        config.flight_profile.float_altitude = 30000.0
        config.flight_profile.float_duration = 21600.0  # 6 hours
        config.flight_profile.ascent_rate = 4.0  # Slower ascent
        config.flight_profile.descent_rate = 5.0

    else:
        raise ValueError(f"Unknown scenario: {scenario_name}")

    return config


def main():
    """Main entry point for thermal analysis tool."""
    print("\n" + "="*60)
    print("STRATOSPHERIC CAPSULE THERMAL ANALYSIS TOOL")
    print("="*60)
    print("\nSelect run mode:")
    print("  1. Interactive configuration")
    print("  2. Preset: Standard daytime flight")
    print("  3. Preset: Night flight (cold soak)")
    print("  4. Preset: Hot day with high solar loading")
    print("  5. Preset: Extended duration flight")
    print("  6. Exit")

    choice = input("\nEnter choice [1-6]: ").strip()

    if choice == '1':
        config = configure_interactive()
    elif choice == '2':
        config = run_preset_scenario("day_standard")
    elif choice == '3':
        config = run_preset_scenario("night_cold")
    elif choice == '4':
        config = run_preset_scenario("hot_day")
    elif choice == '5':
        config = run_preset_scenario("long_flight")
    elif choice == '6':
        print("\nExiting.")
        return
    else:
        print("\nInvalid choice. Exiting.")
        return

    # Create and run thermal model
    model = ThermalModel(config)
    model.geom.print_summary()

    # Solve
    model.solve()

    # Results
    model.print_summary()

    # Plot
    plot_choice = input("\nShow plots? (y/n) [y]: ").strip().lower()
    if not plot_choice or plot_choice in ['y', 'yes']:
        model.plot_results()

    print("\nThank you for using the Stratospheric Capsule Thermal Analysis Tool!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
