#!/usr/bin/env python3
"""
Example script demonstrating programmatic use of the thermal analysis tool.

This shows how to configure and run thermal simulations without using the
interactive CLI.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

from thermal_analysis import (
    ThermalConfig, ThermalModel, FlightProfile, InsulationProps,
    ShellMaterial, CapsuleColor, ElectronicsLoad, ElectronicsPreset
)


def example_1_basic_flight():
    """
    Example 1: Basic daytime flight with standard configuration.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Daytime Flight")
    print("="*60)

    # Create a default configuration
    config = ThermalConfig()

    # Customize flight profile
    config.flight_profile = FlightProfile(
        ground_altitude=0.0,
        ascent_rate=5.0,
        float_altitude=25000.0,
        float_duration=7200.0,  # 2 hours
        descent_rate=6.0,
        time_step=20.0
    )

    # Material selection
    config.shell_material = ShellMaterial.ALUMINUM
    config.shell_thickness = 0.002  # 2mm
    config.capsule_color = CapsuleColor.WHITE

    # Insulation
    config.insulation = InsulationProps(
        thickness=0.020,  # 20mm
        density=50.0,
        thermal_cond=0.030,
        specific_heat=1200.0
    )

    # Environmental
    config.sun_on = True
    config.solar_incidence_factor = 0.3

    # Internal loads
    config.num_occupants = 3
    config.metabolic_heat_per_person = 100.0
    config.electronics = ElectronicsLoad.get_preset(ElectronicsPreset.STANDARD)

    # Run simulation
    model = ThermalModel(config)
    model.solve()
    model.print_summary()

    # Save plot
    model.plot_results()
    plt.savefig('example1_basic_flight.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved as: example1_basic_flight.png")

    return model


def example_2_night_flight():
    """
    Example 2: Night flight with radiative cooling.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Night Flight (Radiative Cooling)")
    print("="*60)

    config = ThermalConfig()

    # Flight profile - longer float
    config.flight_profile.float_altitude = 27000.0
    config.flight_profile.float_duration = 14400.0  # 4 hours
    config.flight_profile.time_step=15.0

    # Darker color for contrast (in reality you'd want white)
    config.capsule_color = CapsuleColor.METALLIC

    # No sun
    config.sun_on = False

    # More insulation for night flight
    config.insulation.thickness = 0.030  # 30mm

    # Add auxiliary heating
    config.aux_heating_power = 200.0  # 200W heater

    # Run simulation
    model = ThermalModel(config)
    model.solve()
    model.print_summary()

    model.plot_results()
    plt.savefig('example2_night_flight.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved as: example2_night_flight.png")

    return model


def example_3_comparison():
    """
    Example 3: Compare different shell materials.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Material Comparison")
    print("="*60)

    materials = [
        (ShellMaterial.POLYETHYLENE, "Polyethylene"),
        (ShellMaterial.ALUMINUM, "Aluminum"),
        (ShellMaterial.CARBON_FIBER, "Carbon Fiber")
    ]

    results = {}

    for material, name in materials:
        print(f"\n--- Testing {name} ---")

        config = ThermalConfig()
        config.shell_material = material
        config.shell_thickness = 0.002  # Same thickness for all
        config.capsule_color = CapsuleColor.WHITE
        config.flight_profile.float_altitude = 27000.0
        config.flight_profile.float_duration = 3600.0  # 1 hour for quick test
        config.flight_profile.time_step = 20.0

        model = ThermalModel(config)
        model.solve()

        # Store results
        T_air = model.T[:, 4] - 273.15  # Convert to Celsius
        results[name] = {
            'time': model.time / 3600,  # Convert to hours
            'T_air': T_air,
            'T_min': T_air.min(),
            'T_max': T_air.max(),
            'T_avg': T_air.mean()
        }

        print(f"  Interior air: min={T_air.min():.1f}°C, max={T_air.max():.1f}°C, avg={T_air.mean():.1f}°C")

    # Create comparison plot
    fig, ax = plt.subplots(figsize=(10, 6))

    for name, data in results.items():
        ax.plot(data['time'], data['T_air'], label=name, linewidth=2)

    ax.set_xlabel('Time [hours]')
    ax.set_ylabel('Interior Air Temperature [°C]')
    ax.set_title('Material Comparison: Interior Temperature vs Time')
    ax.axhline(18, color='b', linestyle='--', alpha=0.4, label='Comfort Min')
    ax.axhline(26, color='r', linestyle='--', alpha=0.4, label='Comfort Max')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('example3_material_comparison.png', dpi=150, bbox_inches='tight')
    print("\nComparison plot saved as: example3_material_comparison.png")


def example_4_custom_electronics():
    """
    Example 4: Custom electronics configuration.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Electronics Configuration")
    print("="*60)

    config = ThermalConfig()

    # Create custom electronics load
    config.electronics = ElectronicsLoad({
        "primary_com": 30.0,
        "backup_com": 25.0,
        "gps_navigator": 20.0,
        "flight_computer": 15.0,
        "displays": 40.0,
        "transponder": 20.0,
        "cameras": 35.0,
        "data_logger": 10.0,
        "misc": 15.0
    })

    print(f"Total electronics power: {config.electronics.total_power} W")

    # High-power electronics may require active cooling
    if config.electronics.total_power > 150:
        print("High electronics load detected - consider active cooling!")

    config.flight_profile.float_altitude = 25000.0
    config.flight_profile.float_duration = 5400.0  # 1.5 hours
    config.flight_profile.time_step = 15.0

    model = ThermalModel(config)
    model.solve()
    model.print_summary()

    model.plot_results()
    plt.savefig('example4_custom_electronics.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved as: example4_custom_electronics.png")


def example_5_parameter_sweep():
    """
    Example 5: Parameter sweep - insulation thickness.
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Insulation Thickness Sweep")
    print("="*60)

    insulation_thicknesses = [10, 15, 20, 25, 30]  # [mm]
    results = {}

    for thickness_mm in insulation_thicknesses:
        thickness_m = thickness_mm / 1000.0
        print(f"\n--- Testing {thickness_mm} mm insulation ---")

        config = ThermalConfig()
        config.insulation.thickness = thickness_m
        config.flight_profile.float_altitude = 27000.0
        config.flight_profile.float_duration = 7200.0  # 2 hours
        config.flight_profile.time_step = 20.0
        config.sun_on = False  # Night flight to see insulation effect

        model = ThermalModel(config)
        model.solve()

        T_air = model.T[:, 4] - 273.15
        results[thickness_mm] = {
            'time': model.time / 3600,
            'T_air': T_air,
            'T_min': T_air.min(),
            'T_final': T_air[-1]
        }

        print(f"  Final temperature: {T_air[-1]:.1f}°C (min: {T_air.min():.1f}°C)")

    # Create comparison plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Time series
    for thickness, data in results.items():
        ax1.plot(data['time'], data['T_air'], label=f'{thickness} mm', linewidth=2)

    ax1.set_xlabel('Time [hours]')
    ax1.set_ylabel('Interior Air Temperature [°C]')
    ax1.set_title('Effect of Insulation Thickness (Night Flight)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Summary bar chart
    thicknesses = list(results.keys())
    final_temps = [results[t]['T_final'] for t in thicknesses]
    min_temps = [results[t]['T_min'] for t in thicknesses]

    x = range(len(thicknesses))
    width = 0.35

    ax2.bar([i - width/2 for i in x], final_temps, width, label='Final Temp', alpha=0.8)
    ax2.bar([i + width/2 for i in x], min_temps, width, label='Min Temp', alpha=0.8)

    ax2.set_xlabel('Insulation Thickness [mm]')
    ax2.set_ylabel('Temperature [°C]')
    ax2.set_title('Temperature vs Insulation Thickness')
    ax2.set_xticks(x)
    ax2.set_xticklabels(thicknesses)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('example5_insulation_sweep.png', dpi=150, bbox_inches='tight')
    print("\nSweep plot saved as: example5_insulation_sweep.png")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("THERMAL ANALYSIS TOOL - EXAMPLE SCRIPTS")
    print("="*60)
    print("\nRunning example simulations...")
    print("(Plots will be saved to PNG files)")

    # Run examples
    print("\n\nRunning examples (this may take a minute)...")

    # Example 1: Basic flight
    example_1_basic_flight()

    # Example 2: Night flight
    example_2_night_flight()

    # Example 3: Material comparison
    example_3_comparison()

    # Example 4: Custom electronics
    example_4_custom_electronics()

    # Example 5: Parameter sweep
    example_5_parameter_sweep()

    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  - example1_basic_flight.png")
    print("  - example2_night_flight.png")
    print("  - example3_material_comparison.png")
    print("  - example4_custom_electronics.png")
    print("  - example5_insulation_sweep.png")
    print("\nYou can now examine these plots to understand the thermal behavior")
    print("of the capsule under different conditions.\n")
