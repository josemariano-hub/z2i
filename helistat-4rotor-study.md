# 4-Rotor Helistat Study
## Toroidal Envelope Multicopter Hybrid Aircraft

### Concept Overview
A helistat is a hybrid aircraft that combines:
- **Heavier-than-air** propulsion (rotorcraft)
- **Lighter-than-air** buoyancy (aerostatic lift)

This study focuses on a 4-rotor quadcopter configuration with toroidal (donut-shaped) lighter-than-air envelopes surrounding each rotor.

---

## Design Concept

### Configuration
- **4 rotors** in quadcopter X or + configuration
- **4 toroidal envelopes** - one surrounding each rotor
- **Central payload bay** suspended below rotors
- **Lightweight frame** connecting rotor assemblies

### Toroidal Envelope Advantages
1. **Rotor Integration**: Torus allows rotor shaft to pass through center
2. **Aerodynamic Flow**: Rotor wash can flow through center hole
3. **Structural Efficiency**: Distributes lift around each rotor
4. **Crashworthiness**: Envelopes provide impact protection
5. **Deployability**: Can be collapsed for transport (bloom patterns applicable)

---

## Key Design Parameters

### Envelope Specifications
```
Toroidal Parameters:
- Major radius (R): Distance from torus center to tube center
- Minor radius (r): Radius of the tube cross-section
- Aspect ratio: R/r (typically 2-4 for stability)
- Volume: 2π²Rr²
```

### Lift Gas Options
1. **Helium**
   - Lift: ~1.0 kg/m³ at sea level
   - Safe, non-flammable
   - Expensive, limited supply

2. **Hydrogen**
   - Lift: ~1.1 kg/m³ at sea level
   - Flammable (safety concerns)
   - Abundant, cheap

3. **Heated Air**
   - Lift: ~0.3 kg/m³ (depends on temperature)
   - Safe, no gas required
   - Requires continuous heating

### Weight Budget Analysis
For effective hybrid design, buoyant lift should offset 30-70% of total weight:

```
Target Specifications (Example):
- Total mass: 10 kg
- Desired buoyant lift: 5 kg (50%)
- Required gas volume: 5 m³ (helium)
- Volume per toroid: 1.25 m³
```

---

## Performance Benefits

### 1. Extended Flight Time
- Buoyancy reduces power needed to hover
- Rotors only need to provide control and translation forces
- Potential 2-5x increase in endurance

### 2. Efficiency Improvements
- Reduced rotor disk loading
- Lower induced power losses
- Quiet operation at low speeds

### 3. Stability Enhancements
- Higher inertia provides damping
- Resistance to wind gusts
- Gentle failure mode (soft landing if power lost)

### 4. Payload Capacity
- Buoyancy can offset vehicle weight
- All rotor thrust available for payload
- Heavy lift capability

---

## Technical Challenges

### 1. Envelope Design
**Requirements:**
- Lightweight gastight material (mylar, ripstop nylon with coating)
- UV resistance
- Abrasion resistance near rotors
- Minimal gas permeability

**Bloom Pattern Application:**
- Flat-foldable toroidal structures for deployment
- Yoshimura or Miura-ori patterns for radial expansion
- Collapsible design for transport and storage
- Could enable inflatable deployment in field

### 2. Structural Integration
**Challenges:**
- Envelope attachment to rotor mounts
- Managing envelope deformation under thrust
- Preventing rotor blade contact with envelope
- Frame must handle both tension (from buoyancy) and compression

### 3. Aerodynamic Interactions
**Considerations:**
- Rotor downwash interaction with toroid surface
- Vortex ring state behavior
- Ground effect modifications
- Translational flight drag

### 4. Control Systems
**Unique aspects:**
- Large moment of inertia (slow rotation)
- Buoyancy varies with altitude and temperature
- Wind sensitivity due to large surface area
- May need active ballast or gas valving

### 5. Practical Operations
- Ground handling of large envelopes
- Inflation/deflation procedures
- Weather limitations (wind, storms)
- Storage and transport
- Gas containment and top-off

---

## Design Calculations

### Toroid Volume
For a toroidal envelope:
```
V = 2π²Rr²

Example: R = 0.5m, r = 0.2m
V = 2π² × 0.5 × 0.2² = 0.395 m³ per toroid
Total volume (4 toroids) = 1.58 m³
Helium lift ≈ 1.58 kg
```

### Rotor Sizing
Assuming 50% buoyant support:
```
Total weight: W = 10 kg
Buoyant force: B = 5 kg
Rotor thrust required: T = W - B = 5 kg (49 N)
Thrust per rotor: 12.25 N (1.25 kg)
```

### Power Estimation
```
Hover power per rotor (simplified):
P = T^(3/2) / (2ρA)^(1/2)

Where:
- T = thrust (N)
- ρ = air density (1.225 kg/m³)
- A = rotor disk area (m²)

For 10" propeller (A = 0.0507 m²):
P ≈ 15-20 W per rotor
Total hover power ≈ 60-80 W

Compare to conventional quadcopter (no buoyancy):
Total hover power ≈ 120-160 W
```

**Efficiency gain: 40-50% reduction in hover power**

---

## Bloom Pattern Integration

### Relevance to Toroidal Design

The bloom pattern research in this repository could enable:

1. **Deployable Toroids**
   - Flat-packed for transport
   - Radially expansive deployment
   - Yoshimura patterns for circumferential expansion
   - Helical folding matches toroidal geometry

2. **Manufacturing**
   - Generate cutting patterns for envelope fabrication
   - Optimize material usage
   - Create segmented designs for assembly

3. **Variable Geometry**
   - Active shape control for flight regimes
   - Partial deflation for landing
   - Compact stowed configuration

### Yoshimura Pattern Application
The Yoshimura bloom pattern (available in code) is particularly relevant:
- Circular/radial symmetry matches toroid
- Can model circumferential folding
- Developable surface (can be cut from flat material)
- Could generate gore patterns for toroid fabrication

---

## Development Roadmap

### Phase 1: Analysis & Simulation
- [ ] Detailed CAD model of toroidal geometry
- [ ] CFD analysis of rotor-envelope interaction
- [ ] Structural analysis of envelope under thrust
- [ ] Flight dynamics simulation with buoyancy
- [ ] Use Yoshimura code to generate toroid patterns

### Phase 2: Prototype Envelope
- [ ] Select envelope material
- [ ] Generate gore patterns using bloom pattern tools
- [ ] Fabricate single toroid prototype
- [ ] Pressure and leak testing
- [ ] Wind tunnel testing (if available)

### Phase 3: Scale Model
- [ ] Build 1/4 scale demonstrator
- [ ] Integrate simple flight controller
- [ ] Tethered flight tests
- [ ] Characterize flight performance
- [ ] Validate lift and power models

### Phase 4: Full Scale Development
- [ ] Design full-scale vehicle (target specs)
- [ ] Fabricate 4 production toroids
- [ ] Integrate with flight controller
- [ ] Flight testing program
- [ ] Performance validation

---

## Reference Designs

### Similar Concepts
1. **Hybrid Air Vehicles (HAV)**
   - Large airship-aircraft hybrids
   - Proven concept at large scale

2. **Skyship Multicopter**
   - Research projects combining drones with balloons
   - Typically single balloon above rotors

3. **Helikite**
   - Kite-balloon hybrid
   - Different but related principle

### Novel Aspects of This Design
- **Distributed buoyancy** around each rotor
- **Toroidal geometry** for rotor integration
- **Bloom pattern** deployable structures
- **Small-scale** multicopter form factor

---

## Safety Considerations

### Failure Modes
1. **Envelope puncture**: Gradual descent, still has rotor power
2. **Rotor failure**: Partial buoyancy enables controlled descent
3. **Complete power loss**: Buoyant descent like a balloon
4. **Over-pressure**: Relief valves required

### Operational Safety
- Use helium for crewed or public operations
- Redundant gas cells within each toroid
- Rotor guards integrated with envelope structure
- Emergency ballast release (if needed)

---

## Next Steps

1. **Review bloom pattern code** for toroid pattern generation
2. **Create parametric CAD model** of toroidal envelope
3. **Calculate detailed weight/lift budget** for target vehicle
4. **Research envelope materials** and suppliers
5. **Develop simplified simulation** for flight dynamics
6. **Design test rig** for rotor-envelope interaction

---

## Appendices

### A. Useful Formulas

**Toroid Geometry:**
- Volume: V = 2π²Rr²
- Surface Area: A = 4π²Rr
- Major circumference: C = 2πR
- Minor circumference: c = 2πr

**Buoyant Force:**
- F = ρ_air × V × g - ρ_gas × V × g
- F ≈ (1.225 - ρ_gas) × V × 9.81

**Rotor Theory:**
- Thrust: T = ρAv²
- Induced velocity: v = √(T/(2ρA))
- Ideal hover power: P = T^(3/2)/√(2ρA)

### B. Material Properties

**Candidate Envelope Materials:**
- Mylar: 12-50 μm, gastight, stiff
- Ripstop Nylon + PU coating: Lightweight, flexible
- Tedlar (PVF): Excellent gas barrier, UV resistant
- Urethane-coated fabrics: Good balance of properties

**Typical densities:**
- Mylar film: 25-50 g/m²
- Coated ripstop: 30-60 g/m²
- Requires sealing/welding compatible materials

---

**Document Version:** 1.0
**Date:** 2025-11-15
**Project:** 4-Rotor Helistat with Toroidal LTA Envelopes
