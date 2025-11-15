# Tri-Stable Complementary Hemispheres Design Analysis

## Problem Statement
Design a single origami pattern with three stable states:
1. **Flat**: Fully collapsed
2. **Small hemisphere**: Partial deployment → 2 copies form complete small sphere
3. **Large hemisphere**: Full deployment → 2 copies form complete large sphere

## Challenges

### Geometric Constraints
- **Perfect hemispheres required**: Standard bloom patterns create conical/dome shapes
- **Flat equatorial edge**: Needed for mating two halves
- **Controlled radii**: r_small and r_large must be precise
- **Tri-stability**: Pattern must be stable in THREE discrete states

### Bloom Pattern Limitations
From Wang et al. (2025) research:
- Yoshimura patterns: Create conical deployment
- Wire patterns: Non-rigidly foldable but unpredictable
- Most patterns: Bistable at best (flat + deployed)

## Proposed Solutions

### Solution 1: High-Order Yoshimura with Mechanical Constraints ⭐ RECOMMENDED

**Pattern**: RH-Y-12.6(1/2) or similar high-order pattern

**Mechanism**:
1. Use **elastic cord deployment limiter**
2. Cord threaded through:
   - Every 2nd vertex at radius = r_small (50% deployment)
   - Outer vertices at radius = r_large (100% deployment)
3. Cord lengths adjustable to lock deployment states

**Advantages**:
- ✅ Uses proven bloom pattern geometry
- ✅ Mechanical simplicity
- ✅ Adjustable deployment radii
- ✅ Can create stable intermediate states

**Disadvantages**:
- ⚠️ Requires added hardware (cord/rings)
- ⚠️ Not pure origami
- ⚠️ Hemispheres are approximate (faceted)

**Implementation Steps**:
```
1. Generate RH-Y-12.h pattern (12-fold symmetry for smoother curve)
2. Identify vertex rings at 50% and 100% radii
3. Add cord channels at these radii
4. Test deployment with adjustable cord tension
```

### Solution 2: Spherical Approximation with Very High m,h

**Pattern**: RH-Y-24.8(1/2) (very high parameters)

**Concept**:
- Many small facets → approximates sphere better
- Higher m (polygon sides) → smoother circumference
- Higher h (height order) → more radial resolution

**Calculation**:
```python
m = 24  # 24-fold symmetry (15° increments)
h = 8   # 8 rings of vertices
→ Creates ~200 facets per hemisphere
→ Approximates sphere to <5% error
```

**Advantages**:
- ✅ Pure origami (no hardware)
- ✅ Better spherical approximation

**Disadvantages**:
- ❌ Extremely complex to fold
- ❌ Very small facets
- ❌ Still needs bistability mechanism
- ❌ May not be hand-foldable

### Solution 3: Water Bomb Base Variant (Alternative Approach)

**Pattern**: Not a bloom pattern, but spherical deployable

**Concept**:
- Water bomb tessellation creates curved surfaces
- Naturally spherical deployment
- Can have multiple stable states with constraints

**References**:
- "Cylindrical waterbomb origami" (Lu et al., 2023)
- Creates more spherical geometry than Yoshimura

**Advantages**:
- ✅ More spherical geometry
- ✅ Natural curvature

**Disadvantages**:
- ❌ Not in bloom pattern family (may not meet your requirements)
- ❌ Complex mathematical model
- ❌ Limited research on tri-stability

## Tri-Stability Mechanisms

### Physical Constraints
1. **Elastic cords** at specific radii
2. **Adjustable rings** that clip at deployment positions
3. **Ratchet mechanism** at vertices
4. **Magnetic stops** at intermediate positions

### Geometric Solutions
1. **Overconstrained vertices**: Add extra creases for bistability
2. **Compliant facets**: Slight panel curvature creates snap-through
3. **Thickness effects**: Panel thickness creates natural stops

## Recommended Design Process

### Phase 1: Proof of Concept
```
1. Generate RH-Y-8.3(1/2) base pattern
2. Add physical deployment limiters (elastic cord)
3. Test three-state deployment
4. Measure hemisphere radii and sphericity
5. Iterate cord positions for better fit
```

### Phase 2: Optimization
```
1. Increase m for smoother curves (try m=12, 16, 20)
2. Adjust h for deployment ratio
3. Test hemisphere mating with 2 identical copies
4. Measure gap/interference at equator
```

### Phase 3: Refinement
```
1. Optimize facet angles for sphericity
2. Add geometric features for snap-through behavior
3. Test with different materials (paper, cardstock, thin plastic)
4. Document reliable deployment procedures
```

## Mathematical Analysis

### Hemisphere Fit Requirements

For two hemispheres to mate perfectly:
```
1. Equatorial diameter must match exactly: d₁ = d₂
2. Equatorial plane must be flat (no warping)
3. Curvature must be spherical: K = 1/r² (constant)
4. Edge must be smooth (no steps/gaps)
```

### Bloom Pattern Geometry
From Wang et al. (2025), Section 5(b)(i):

Developed radius:
```
r = s·√(h² + csc²(β)/4 - h·csc(β)·cos(3β - 3π/2))
where β = π/m
```

This creates **conical** deployment, not spherical!

### Spherical Approximation Error
For Yoshimura pattern with m sides:
```
Sphericity error ≈ 1 - cos(π/m)
m=6:  error ≈ 13.4%
m=12: error ≈ 3.4%
m=24: error ≈ 0.85%
```

**Conclusion**: Need m ≥ 16 for acceptable sphericity

## Feasibility Assessment

### Can Standard Bloom Patterns Achieve This?
**Answer**: Not perfectly, but can approximate with:
1. High m, h parameters (smoother curve)
2. Physical deployment constraints (tri-stability)
3. Accepting ~3-5% sphericity error
4. Flexible mating edges (slight gaps acceptable)

### Alternative: Modify Bloom Pattern Theory
Could extend Wang et al. framework to include:
- **Curved crease bloom patterns** (non-developable)
- **Hybrid rigid/flexible designs**
- **Multi-layer assemblies**

This would require new research beyond current paper.

## Practical Recommendation

**For immediate prototyping**:
1. Use **RH-Y-12.4(1/2)** as base
2. Add **elastic cord limiter** at vertices
3. Create deployment jig with adjustable stops
4. Accept ~3% sphericity error
5. Test with two identical copies at each state

**For research/development**:
1. Collaborate with origami researchers
2. Develop spherical modification to Yoshimura equations
3. Study tri-stable mechanisms in compliant structures
4. Potentially publish extension to Wang et al. work

## Code Implementation Notes

The current `Bloom_Yoshimura.py` generates conical deployment.
To create spherical approximation, would need:
```python
# Modified transformation for spherical projection
def spherical_projection_transformation(self, target_radius):
    # Project points onto sphere of radius r
    # Instead of planar slant transformation
    for point in self.point_set:
        x, y = self.point_map_read(point)
        r_2d = np.sqrt(x**2 + y**2)
        theta = r_2d / target_radius  # Angle from pole
        # Spherical coordinates
        x_sphere = target_radius * np.sin(theta) * (x / r_2d)
        y_sphere = target_radius * np.sin(theta) * (y / r_2d)
        z_sphere = target_radius * np.cos(theta)
        self.point_map_update(point, (x_sphere, y_sphere))
```

This is non-trivial and may violate developability!

## Conclusion

Your requirement is at the **cutting edge** of origami engineering research.

**Achievable with constraints**: Yes, using mechanical limiters
**Pure origami solution**: Requires research beyond current bloom patterns
**Best current approach**: High-order Yoshimura + elastic cord system

Would you like me to generate a prototype with mechanical constraints?
