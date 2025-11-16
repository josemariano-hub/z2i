#!/usr/bin/env python3
"""
Helistat Forward Flight Performance Analysis
============================================

Analyzes cruise speed, range, and efficiency in forward flight.
Accounts for envelope drag, rotor tilting, and power requirements.
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Tuple

# Import constants from parametric model
import sys
sys.path.insert(0, '/home/user/z2i')
from helistat_parametric_model import (
    HelistatDesign, G, RHO_AIR_SL, HELIUM_LIFT_SL,
    MOTOR_EFFICIENCY, ESC_EFFICIENCY, PROP_EFFICIENCY
)

# ============================================================================
# AERODYNAMIC DRAG MODELS
# ============================================================================

def toroid_drag_coefficient(reynolds_number: float) -> float:
    """
    Estimate drag coefficient for toroidal envelope.

    Torus has complex flow separation. CD varies with:
    - Reynolds number
    - Aspect ratio
    - Surface roughness

    Typical range: CD = 0.4 to 1.2
    """
    # Simplified model based on sphere/cylinder data
    # Actual value needs wind tunnel testing
    if reynolds_number < 1e4:
        return 1.2  # Low Re, laminar flow
    elif reynolds_number < 1e5:
        return 0.8  # Transition
    else:
        return 0.6  # High Re, turbulent (smoother fabric)


def calculate_reynolds_number(velocity_ms: float, characteristic_length: float) -> float:
    """Calculate Reynolds number for flow around envelope"""
    kinematic_viscosity = 1.5e-5  # m²/s for air at sea level
    return velocity_ms * characteristic_length / kinematic_viscosity


def envelope_drag_force(velocity_ms: float, toroid_minor_radius: float,
                       num_toroids: int = 4) -> float:
    """
    Calculate drag force on all toroidal envelopes in forward flight.

    Uses frontal area projection and drag coefficient.

    Args:
        velocity_ms: Forward flight speed (m/s)
        toroid_minor_radius: Minor radius of each toroid (m)
        num_toroids: Number of toroids

    Returns:
        Total drag force (N)
    """
    # Frontal area of one toroid (approximation: circular cross-section)
    frontal_area_one = math.pi * toroid_minor_radius**2
    total_frontal_area = frontal_area_one * num_toroids

    # Reynolds number (use toroid minor diameter as characteristic length)
    Re = calculate_reynolds_number(velocity_ms, 2 * toroid_minor_radius)

    # Drag coefficient
    Cd = toroid_drag_coefficient(Re)

    # Drag force: D = 0.5 * rho * v² * Cd * A
    drag_force = 0.5 * RHO_AIR_SL * velocity_ms**2 * Cd * total_frontal_area

    return drag_force


def frame_drag_force(velocity_ms: float, mtow_kg: float) -> float:
    """
    Estimate drag from structural frame, payload pod, landing gear.

    Simplified model: scales with vehicle size
    """
    # Estimate exposed frame area based on vehicle size
    # Rough approximation: 0.5 m² per ton MTOW
    exposed_area = 0.5 * (mtow_kg / 1000)

    # Structural components: Cd ≈ 1.0 (non-streamlined)
    Cd_frame = 1.0

    drag_force = 0.5 * RHO_AIR_SL * velocity_ms**2 * Cd_frame * exposed_area

    return drag_force


# ============================================================================
# PROPULSION IN FORWARD FLIGHT
# ============================================================================

def rotor_forward_flight_power(thrust_N: float, velocity_ms: float,
                               rotor_diameter: float) -> float:
    """
    Calculate rotor power in forward flight using momentum theory.

    Power = Induced power + Profile power + Parasit power

    Simplified model - ignores many effects:
    - Rotor tilt
    - Advancing/retreating blade dynamics
    - Wake skew
    """
    # Rotor disk area
    A = math.pi * (rotor_diameter / 2)**2

    # Induced velocity in hover
    v_hover = math.sqrt(thrust_N / (2 * RHO_AIR_SL * A))

    # Induced velocity in forward flight (simplified)
    # v_induced = v_hover / sqrt(1 + (V/v_hover)²)
    if velocity_ms < 0.1:
        v_induced = v_hover
    else:
        v_induced = v_hover / math.sqrt(1 + (velocity_ms / v_hover)**2)

    # Induced power
    P_induced = thrust_N * v_induced

    # Profile power (blade drag)
    # Rough estimate: constant fraction of induced power
    P_profile = 0.2 * P_induced

    # Parasit power (rotor hub drag)
    # Negligible compared to envelope drag

    # Total power
    P_total = P_induced + P_profile

    # Apply figure of merit
    FM = 0.75
    P_actual = P_total / FM

    return P_actual


def total_forward_flight_power(helistat: HelistatDesign, velocity_ms: float) -> float:
    """
    Calculate total power required for forward flight at given speed.

    Power components:
    1. Rotor thrust power (to overcome drag + maintain altitude)
    2. Propulsive power (to overcome drag)
    """
    # Drag forces
    envelope_drag_N = envelope_drag_force(velocity_ms, helistat.toroid.minor_radius,
                                         helistat.num_rotors)
    frame_drag_N = frame_drag_force(velocity_ms, helistat.mtow_kg)
    total_drag_N = envelope_drag_N + frame_drag_N

    # Weight in Newtons
    weight_N = helistat.mtow_kg * G

    # Buoyant force in Newtons
    buoyant_force_N = helistat.buoyant_lift_kg * G

    # Net vertical force needed from rotors
    vertical_thrust_N = weight_N - buoyant_force_N

    # In forward flight, rotors must provide:
    # - Vertical component to support weight
    # - Horizontal component to overcome drag

    # Total thrust vector
    # T² = T_vert² + T_horiz²
    thrust_horizontal_N = total_drag_N
    thrust_vertical_N = vertical_thrust_N

    total_thrust_N = math.sqrt(thrust_horizontal_N**2 + thrust_vertical_N**2)

    # Thrust per rotor
    thrust_per_rotor_N = total_thrust_N / helistat.num_rotors

    # Power per rotor
    power_per_rotor_W = rotor_forward_flight_power(
        thrust_per_rotor_N,
        velocity_ms,
        helistat.rotor_diameter_m
    )

    # Total rotor power
    total_rotor_power_W = power_per_rotor_W * helistat.num_rotors

    # Account for motor/ESC/prop losses
    system_power_W = total_rotor_power_W / (MOTOR_EFFICIENCY * ESC_EFFICIENCY * PROP_EFFICIENCY)

    return system_power_W


# ============================================================================
# PERFORMANCE CURVES
# ============================================================================

def find_max_speed(helistat: HelistatDesign, max_power_W: float = None) -> float:
    """
    Find maximum achievable cruise speed.

    Limited by either:
    1. Maximum available power
    2. Structural limits (envelope stress)

    Args:
        helistat: HelistatDesign object
        max_power_W: Maximum continuous power (if None, uses rated power)

    Returns:
        Maximum speed in m/s
    """
    if max_power_W is None:
        # Assume max continuous power = hover power × 2.5
        max_power_W = helistat.total_rotor_power_W * 2.5

    # Iterate to find speed where power required = power available
    speeds_ms = np.linspace(0, 50, 200)  # 0 to 180 km/h

    for v in speeds_ms:
        power_required = total_forward_flight_power(helistat, v)
        if power_required >= max_power_W:
            return v

    # If we didn't hit power limit, return max tested speed
    return speeds_ms[-1]


def calculate_range(helistat: HelistatDesign, cruise_speed_ms: float) -> float:
    """
    Calculate maximum range at given cruise speed.

    Range = (Available energy / Power consumption) × Speed

    Args:
        helistat: HelistatDesign object
        cruise_speed_ms: Cruise speed (m/s)

    Returns:
        Range in meters
    """
    # Power at cruise
    cruise_power_W = total_forward_flight_power(helistat, cruise_speed_ms)

    # Energy available (from fuel/battery)
    if helistat.use_fuel_cell:
        # H2 fuel cells
        energy_available_Wh = (helistat.propulsion['h2_fuel_kg'] * 33.3 * 1000 *
                              helistat.propulsion['fc_efficiency'])
    elif helistat.use_turbine:
        # Turbine
        energy_available_Wh = (helistat.fuel_weight_kg * 11.9 * 1000)  # kerosene: 11.9 kWh/kg
    else:
        # Battery
        energy_available_Wh = helistat.propulsion['energy_Wh'] * 0.8  # 80% usable

    # Endurance at cruise
    endurance_hours = energy_available_Wh / cruise_power_W

    # Range
    range_m = endurance_hours * cruise_speed_ms * 3600

    return range_m


def performance_summary(helistat: HelistatDesign) -> str:
    """Generate forward flight performance summary"""

    # Max speed
    max_speed_ms = find_max_speed(helistat)
    max_speed_kmh = max_speed_ms * 3.6

    # Optimal cruise (typically 60-70% of max speed for efficiency)
    cruise_speed_ms = max_speed_ms * 0.65
    cruise_speed_kmh = cruise_speed_ms * 3.6

    # Cruise power
    cruise_power_W = total_forward_flight_power(helistat, cruise_speed_ms)
    cruise_power_kW = cruise_power_W / 1000

    # Range at cruise
    range_m = calculate_range(helistat, cruise_speed_ms)
    range_km = range_m / 1000

    # Drag breakdown at cruise
    envelope_drag_N = envelope_drag_force(cruise_speed_ms, helistat.toroid.minor_radius,
                                         helistat.num_rotors)
    frame_drag_N = frame_drag_force(cruise_speed_ms, helistat.mtow_kg)
    total_drag_N = envelope_drag_N + frame_drag_N

    # Power breakdown
    hover_power_kW = helistat.total_rotor_power_W / 1000
    cruise_power_increase = (cruise_power_W / helistat.total_rotor_power_W - 1) * 100

    report = f"""
{'='*80}
FORWARD FLIGHT PERFORMANCE - {helistat.mtow_kg:.0f} kg MTOW
{'='*80}

SPEED PERFORMANCE:
  Maximum speed: {max_speed_kmh:.1f} km/h ({max_speed_ms:.1f} m/s)
  Optimal cruise: {cruise_speed_kmh:.1f} km/h ({cruise_speed_ms:.1f} m/s)
  Hover power: {hover_power_kW:.2f} kW
  Cruise power: {cruise_power_kW:.2f} kW (+{cruise_power_increase:.0f}% vs hover)

DRAG ANALYSIS AT CRUISE ({cruise_speed_kmh:.0f} km/h):
  Envelope drag: {envelope_drag_N:.1f} N ({envelope_drag_N/total_drag_N*100:.0f}%)
  Frame drag: {frame_drag_N:.1f} N ({frame_drag_N/total_drag_N*100:.0f}%)
  Total drag: {total_drag_N:.1f} N
  L/D ratio: {(helistat.mtow_kg * G) / total_drag_N:.1f}

RANGE PERFORMANCE:
  Cruise range: {range_km:.1f} km
  Cruise endurance: {range_km / cruise_speed_kmh:.2f} hours
  Specific range: {range_km / helistat.mtow_kg:.2f} km/kg

COMPARISON TO HOVER:
  Cruise power vs hover: +{cruise_power_increase:.0f}%
  Range vs hovering in place: {(cruise_speed_ms * 3.6) / (helistat.total_rotor_power_W / 1000):.1f} km per kW

{'='*80}
"""

    return report


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("HELISTAT FORWARD FLIGHT PERFORMANCE ANALYSIS")
    print("="*80)

    # Analyze each size class
    designs = [
        HelistatDesign(mtow_kg=10, target_endurance_hours=3),
        HelistatDesign(mtow_kg=100, target_endurance_hours=4),
        HelistatDesign(mtow_kg=1000, target_endurance_hours=3),
        HelistatDesign(mtow_kg=5000, target_endurance_hours=2),
        HelistatDesign(mtow_kg=20000, target_endurance_hours=2),
    ]

    for design in designs:
        print(performance_summary(design))
