# Stratospheric Capsule Thermal Analysis Tool

## Overview

A comprehensive Python-based thermal analysis tool for simulating the thermal behavior of a 2.4m diameter spherical capsule carrying 3 people to altitudes of 25-30 km. The tool models conduction, convection, radiation, solar loading, and internal heat generation using a lumped-parameter approach.

**All units are in SI unless otherwise noted.**

## Features

- **ISA 1976 Atmosphere Model**: Accurate temperature, pressure, and density calculations up to 35+ km
- **Lumped-Parameter Thermal Network**: 6-node thermal model with realistic heat transfer mechanisms
- **Multiple Material Options**:
  - Polyethylene shell
  - Aluminum alloy shell
  - Carbon fiber/epoxy composite shell
- **Configurable Parameters**:
  - Shell thickness and material
  - Insulation thickness (polyimide foam)
  - Capsule color (affects solar absorptivity and IR emissivity)
  - Window properties (elliptical, dual-layer polycarbonate with golden mirror coating)
- **Comprehensive Heat Transfer**:
  - Conduction through shell, insulation, and window
  - Exterior convection (altitude-dependent)
  - Interior convection
  - Radiation to space and Earth
  - Solar loading with day/night modes
  - Internal heat generation (humans + electronics)
- **Interactive CLI**: Easy configuration or preset scenarios
- **Visualization**: Time-series plots of temperatures and heat fluxes
- **Risk Assessment**: Automatic checks for material temperature limits

## Installation

### Requirements

- Python 3.7+
- numpy
- matplotlib

### Setup

```bash
# Install dependencies
pip install numpy matplotlib

# Make executable (optional)
chmod +x thermal_analysis.py
```

## Usage

### Quick Start

Run the interactive tool:

```bash
python thermal_analysis.py
```

You'll be presented with options:

1. **Interactive configuration** - Customize all parameters
2. **Preset scenarios** - Pre-configured flight profiles:
   - Standard daytime flight
   - Night flight (cold soak)
   - Hot day with high solar loading
   - Extended duration flight

### Example Session

```
============================================================
STRATOSPHERIC CAPSULE THERMAL ANALYSIS TOOL
============================================================

Select run mode:
  1. Interactive configuration
  2. Preset: Standard daytime flight
  3. Preset: Night flight (cold soak)
  4. Preset: Hot day with high solar loading
  5. Preset: Extended duration flight
  6. Exit

Enter choice [1-6]: 2
```

The tool will then:
1. Display the capsule geometry
2. Run the thermal simulation
3. Print a detailed summary
4. Show interactive plots (optional)

### Output

The tool provides:

1. **Geometry Summary**: Areas, volumes, radii
2. **Simulation Progress**: Real-time updates during computation
3. **Temperature Results**:
   - Interior air temperature (min/max/avg)
   - Shell temperatures
   - Window temperatures
4. **Thermal Comfort Assessment**: Time spent in comfortable range (18-26°C)
5. **Material Risk Assessment**: Warnings if temperatures approach material limits
6. **Plots**:
   - Altitude profile
   - Interior air temperature vs time
   - All node temperatures
   - Heat flux breakdown
   - Temperature vs altitude
   - Interior-ambient temperature difference

## Configuration Parameters

### Geometry

- **Capsule radius**: 1.2 m (default, 2.4m diameter sphere)
- **Shell thickness**: 0.001-0.005 m (typical: 2mm)
- **Insulation thickness**: 0.01-0.03 m (typical: 20mm polyimide foam)

### Materials

#### Shell Materials

| Material | Density (kg/m³) | k (W/m·K) | cp (J/kg·K) |
|----------|----------------|-----------|-------------|
| Polyethylene | 950 | 0.4 | 2300 |
| Aluminum | 2700 | 160 | 900 |
| Carbon Fiber | 1600 | 5.0 | 1000 |

#### Capsule Colors

| Color | Solar α | IR ε | Description |
|-------|---------|------|-------------|
| White | 0.2 | 0.9 | Low heat gain, high cooling |
| Black | 0.95 | 0.95 | High heat gain |
| Metallic | 0.5 | 0.3 | Medium gain, low cooling |
| Custom | User-defined | User-defined | Specify values |

### Flight Profile

- **Ground altitude**: Default 0 m (sea level)
- **Ascent rate**: Typical 3-6 m/s
- **Float altitude**: 25,000-30,000 m
- **Float duration**: Variable (hours)
- **Descent rate**: Typical 5-8 m/s
- **Time step**: 10-30 s (shorter = more accurate but slower)

### Environmental

- **Sun on/off**: Enable/disable solar heating
- **Solar incidence factor**: 0-1 (accounts for sun angle and capsule orientation)
  - 0 = no solar heating
  - 0.3 = typical oblique angle
  - 0.6-1.0 = near-perpendicular sun

### Internal Loads

#### Human Heat Generation

- Default: 100 W per person (seated, moderate activity)
- Range: 90-150 W depending on activity level

#### Electronics Presets

**Minimal** (~40 W):
- COM radio: 15 W
- GPS: 10 W
- Transponder: 15 W

**Standard** (~135 W):
- COM radio: 25 W
- NAV/GPS: 15 W
- PFD/MFD: 30 W
- Transponder: 20 W
- ADS-B: 15 W
- Audio panel: 10 W
- Misc instruments: 20 W

**Heavy Avionics** (~220 W):
- Dual COM radios: 50 W
- NAV/GPS: 15 W
- PFD/MFD: 40 W
- Transponder: 20 W
- ADS-B: 15 W
- Audio panel: 10 W
- Misc instruments: 25 W
- Cameras: 30 W
- Data logger: 15 W

**Custom**: Specify individual devices

### Heat Transfer Parameters

- **Interior convection coefficient**: 3-10 W/(m²·K)
  - 3-5 W/(m²·K): Natural convection, still air
  - 5-10 W/(m²·K): Some air movement, ventilation

## Thermal Model Details

### Node Structure

The lumped-parameter model uses 6 thermal nodes:

0. **Shell Outer Surface**: Exchanges heat with ambient via convection and radiation
1. **Shell Inner Surface**: Conducts heat through shell
2. **Insulation Inner Surface**: Interface between insulation and cabin
3. **Window**: Simplified single-node window assembly
4. **Interior Air**: Well-mixed cabin air
5. **Interior Mass**: Seats, floor, equipment (~200 kg equivalent)

### Heat Transfer Mechanisms

1. **Conduction**:
   - Through shell: Q = (T_out - T_in) / R_shell
   - Through insulation: Q = (T_shell - T_cabin) / R_insul
   - Through window: Simplified 1D conduction

2. **Convection - Exterior**:
   - Altitude-dependent coefficient using empirical correlations
   - Reynolds number based on vertical velocity and wind
   - Approaches zero at very high altitudes (near-vacuum)

3. **Convection - Interior**:
   - Constant coefficient (user-configurable)
   - Natural convection in cabin

4. **Radiation - Exterior**:
   - Split view factor: 50% to deep space (3K), 50% to Earth
   - Earth effective temperature varies with altitude
   - Stefan-Boltzmann law: Q = ε·σ·A·(T⁴_surface - T⁴_environment)

5. **Solar Loading**:
   - Solar constant: 1360 W/m²
   - User-specified incidence factor for sun angle
   - Separate treatment for shell and window
   - Window has golden mirror coating (high reflectance)

6. **Internal Generation**:
   - Metabolic heat from occupants
   - Electronics waste heat
   - Optional auxiliary heating/cooling

### Numerical Integration

- **Method**: Forward Euler with stability constraints
- **Time step**: User-configurable (default 10-30 s)
- **Stability**:
  - Maximum dT/dt limiter (5 K/s)
  - Temperature clamping (150-450 K)
  - Minimum thermal mass per node (1000 J/K)

## Example Results

### Standard Daytime Flight

- **Configuration**: White aluminum shell, 2mm thick, 20mm insulation, sun on
- **Profile**: Ascent to 27 km, 2-hour float, descent
- **Results**:
  - Interior temperature: 15-20°C
  - Comfortable for majority of flight
  - Shell outer: -20°C at altitude (radiative cooling)
  - Window: -20 to 15°C

### Night Flight

- **Configuration**: Black aluminum, sun off
- **Results**:
  - Significant cooling at altitude due to radiation
  - Interior may require auxiliary heating
  - Shell can reach -60°C or colder

### Hot Day, High Solar

- **Configuration**: Black polyethylene, sun on, high incidence
- **Results**:
  - Rapid heating during ascent
  - May exceed comfort range
  - Risk of PE softening if extreme

## Material Limits

The tool automatically checks against these limits:

- **Polycarbonate window**: Softening point ~150°C
- **Polyimide foam insulation**: Max continuous temp ~200°C
- **Polyethylene shell**: Melting point ~130°C (if used)

Warnings are displayed if temperatures approach these limits.

## Physical Constants

All defined at the top of `thermal_analysis.py`:

- Stefan-Boltzmann constant: 5.67e-8 W/(m²·K⁴)
- Solar constant: 1360 W/m²
- Gas constant (air): 287.05 J/(kg·K)
- Specific heat (air): 1005 J/(kg·K)
- Standard gravity: 9.80665 m/s²

## ISA Atmosphere Model

Implements the 1976 International Standard Atmosphere with piecewise layers:

| Layer | Alt (m) | Lapse Rate (K/m) | Description |
|-------|---------|------------------|-------------|
| Troposphere | 0-11,000 | -0.0065 | Standard lapse |
| Tropopause | 11,000-20,000 | 0 | Isothermal |
| Stratosphere 1 | 20,000-32,000 | +0.001 | Warming |
| Stratosphere 2 | 32,000-47,000 | +0.0028 | Warming |
| Stratopause | 47,000+ | 0 | Isothermal |

## Testing

Run the included test suite:

```bash
python test_thermal.py
```

This verifies:
- ISA atmosphere model accuracy
- Basic thermal simulation
- Numerical stability
- Reasonable temperature ranges

## Tips for Use

1. **Start with presets**: Use preset scenarios to understand typical behavior
2. **Time step selection**:
   - 10-30 s: Good balance of speed and accuracy
   - <10 s: More accurate but slower
   - >30 s: May have stability issues
3. **Insulation thickness**: 20-30mm provides good thermal protection
4. **Color choice**: White is optimal for minimizing solar heating
5. **Electronics**: Be realistic about power consumption (everything becomes heat!)
6. **Float duration**: Longer floats allow thermal equilibrium to establish

## Customization

### Adding New Materials

Edit the `get_shell_material_props()` function in `thermal_analysis.py`:

```python
elif material == ShellMaterial.YOUR_MATERIAL:
    density = XXX  # kg/m³
    k = YYY       # W/(m·K)
    cp = ZZZ      # J/(kg·K)
```

### Modifying Electronics

Edit the `get_preset()` method in the `ElectronicsLoad` class, or use custom mode in the CLI.

### Changing Window Properties

Modify the `WindowProps` dataclass defaults.

## Limitations and Assumptions

1. **Lumped-parameter model**: Does not capture spatial temperature gradients within nodes
2. **Spherical geometry**: Assumes perfect sphere (simplified)
3. **Well-mixed interior**: No temperature stratification in cabin
4. **Simplified window**: Single effective node vs. detailed multilayer model
5. **Constant properties**: Material properties don't vary with temperature
6. **View factors**: Simplified 50/50 space/Earth approximation
7. **External convection**: Empirical correlation, not high-fidelity CFD
8. **No phase change**: Assumes all materials remain solid
9. **No moisture**: Humidity effects not modeled
10. **No ventilation**: Assumes sealed capsule

## Validation

The tool has been validated against:
- ISA 1976 standard atmosphere tables
- Basic energy balance checks
- Physical reasonableness of results
- Stability under various configurations

For critical applications, results should be verified with higher-fidelity tools or experimental data.

## Troubleshooting

**Problem**: Temperatures seem unrealistic (too hot or too cold)
- Check solar settings (sun on/off, incidence factor)
- Verify material properties and color
- Check internal heat generation (humans + electronics)
- Ensure adequate insulation thickness

**Problem**: Simulation is slow
- Increase time step (carefully, watch for instability)
- Reduce total simulation time

**Problem**: Results oscillate or diverge
- Reduce time step
- Check for unrealistic material properties
- Ensure thermal masses are reasonable

**Problem**: Program crashes or errors
- Verify all parameters are positive
- Check that file paths are correct
- Ensure numpy and matplotlib are installed

## References

- 1976 U.S. Standard Atmosphere (NOAA/NASA/USAF)
- Heat Transfer principles: Incropera & DeWitt, "Fundamentals of Heat and Mass Transfer"
- Thermal properties: Engineering toolbox and material databases
- Spherical geometry: Basic calculus and geometry

## Author

Created for aerospace thermal analysis applications.

## License

This tool is provided as-is for educational and engineering analysis purposes.

---

**For questions or issues, please refer to the code comments and docstrings within `thermal_analysis.py`.**
