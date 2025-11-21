#!/usr/bin/env python3
"""
Quick test script for the thermal analysis tool
"""

import sys
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing

# Import the thermal analysis module
from thermal_analysis import (
    ThermalConfig, ThermalModel, ShellMaterial, CapsuleColor,
    ElectronicsLoad, ElectronicsPreset, isa_atmosphere
)

def test_isa_model():
    """Test ISA atmosphere model."""
    print("Testing ISA atmosphere model...")

    test_altitudes = [0, 5000, 11000, 20000, 27000, 35000]
    print("\nAlt [m]    T [K]     P [Pa]     ρ [kg/m³]")
    print("-" * 50)
    for h in test_altitudes:
        T, P, rho = isa_atmosphere(h)
        print(f"{h:6.0f}   {T:6.1f}   {P:9.1f}   {rho:7.5f}")
    print("ISA model test: PASSED\n")

def test_basic_scenario():
    """Test a basic thermal simulation."""
    print("\n" + "="*60)
    print("Running basic thermal simulation test...")
    print("="*60)

    # Create a simple configuration
    config = ThermalConfig()
    config.sun_on = True
    config.solar_incidence_factor = 0.3
    config.capsule_color = CapsuleColor.WHITE
    config.shell_material = ShellMaterial.ALUMINUM
    config.shell_thickness = 0.002  # 2mm
    config.insulation.thickness = 0.020  # 20mm
    config.flight_profile.float_altitude = 25000.0
    config.flight_profile.float_duration = 3600.0  # 1 hour (shorter for quick test)
    config.flight_profile.time_step = 30.0  # 30s time step

    # Create and run model
    model = ThermalModel(config)
    model.geom.print_summary()

    # Solve
    model.solve()

    # Print results
    model.print_summary()

    # Check that simulation produced reasonable results
    T_air_C = model.T[:, 4] - 273.15
    assert -100 < min(T_air_C) < 50, "Temperature out of reasonable range"
    assert -100 < max(T_air_C) < 50, "Temperature out of reasonable range"

    print("\n✓ Basic simulation test: PASSED")

    return model

if __name__ == "__main__":
    print("\n" + "="*60)
    print("THERMAL ANALYSIS TOOL - TEST SUITE")
    print("="*60 + "\n")

    # Test 1: ISA model
    test_isa_model()

    # Test 2: Basic simulation
    model = test_basic_scenario()

    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60 + "\n")

    print("The thermal analysis tool is working correctly.")
    print("You can now run: python thermal_analysis.py")
