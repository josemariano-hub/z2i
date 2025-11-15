"""
Generate PROPERLY SCALED complementary Yoshimura bloom patterns
Version 2: With iterative fitting algorithm
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('Bloom_Pattern_Data/Yoshimura Bloom Pattern Computer Program/Yoshimura_bloom_pattern_code.py')
import Bloom_Yoshimura

def calculate_deployed_radius(m, h, s):
    """Calculate deployed radius based on formula from paper"""
    beta = np.pi / m
    diameter = 2 * s * np.sqrt(h**2 + (1/(np.sin(beta)**2))/4 - h * (1/np.sin(beta)) * np.cos(3*beta - 3*np.pi/2))
    return diameter / 2

def find_complementary_scale(m_large, h_large, target_outer_radius):
    """Find scale factor for large pattern to match target outer radius"""
    # Iterative search for correct s_large
    s_test = 10
    for iteration in range(100):
        r_test = calculate_deployed_radius(m_large, h_large, s_test)
        if abs(r_test - target_outer_radius) < 0.1:
            return s_test
        # Adjust proportionally
        s_test = s_test * (target_outer_radius / r_test)
    return s_test

def generate_pattern(m, h, s, filename_base, title):
    """Generate a bloom pattern"""
    bloom = Bloom_Yoshimura.Bloom_Yoshimura(m, h, s)
    bloom.plot_origin = False
    bloom.plot_points = False
    bloom.plot_facets = True
    bloom.plot_lines = True
    bloom.line_width = 1.2
    bloom.line_style = False
    bloom.crease_is_invert = False

    bloom.define_point_set()
    bloom.point_map_initialize()
    bloom.define_crease_set()
    bloom.define_facet_set()
    bloom.slant_linear_transformation()
    bloom.translation_transformation()
    bloom.scale_linear_transformation()
    bloom.define_point_radial_duplicates()
    bloom.define_crease_radial_duplicates()
    bloom.define_facet_radial_duplicates()
    bloom.sequential_rotation_linear_transformation()

    fig = plt.figure(figsize=(8.27, 11.69))
    bloom.classify_crease()
    bloom.plot_facet_set()
    bloom.plot_monochromatic_crease_set()
    plt.axis('equal')
    plt.axis('off')
    plt.title(title, fontsize=12, pad=15)
    plt.tight_layout()

    plt.savefig(f'/home/user/z2i/{filename_base}.svg', dpi=300, bbox_inches='tight')
    plt.savefig(f'/home/user/z2i/{filename_base}.png', dpi=300, bbox_inches='tight')
    plt.close()

    return calculate_deployed_radius(m, h, s)

print("=" * 80)
print(" COMPLEMENTARY HEMISPHERE BLOOM PATTERNS - Properly Scaled")
print("=" * 80)
print()

# DESIGN PHILOSOPHY:
# Pattern A (small) sets the reference size
# Pattern B (large) is calculated to have outer radius = 2× Pattern A outer radius
# This creates nice nesting

# PATTERN A: Small/Inner hemisphere
m_small = 6
h_small = 2
s_small = 40  # Base scale

r_small = calculate_deployed_radius(m_small, h_small, s_small)
print(f"PATTERN A (Small/Inner Hemisphere)")
print(f"  Formula: RH-Y-{m_small}.{h_small}(1/2)")
print(f"  Parameters: m={m_small}, h={h_small}, s={s_small:.1f}mm")
print(f"  Calculated deployed radius: {r_small:.1f}mm")
print()

# PATTERN B: Large/Outer hemisphere
# We want outer radius to be ~2x the small pattern for nice nesting
m_large = 8    # More sides = smoother hemisphere
h_large = 3    # Higher order = more material
target_radius_large = r_small * 2.0  # Double the small radius

print(f"Calculating complementary pattern...")
s_large = find_complementary_scale(m_large, h_large, target_radius_large)
r_large = calculate_deployed_radius(m_large, h_large, s_large)

print(f"PATTERN B (Large/Outer Hemisphere)")
print(f"  Formula: RH-Y-{m_large}.{h_large}(1/2)")
print(f"  Parameters: m={m_large}, h={h_large}, s={s_large:.1f}mm")
print(f"  Calculated deployed radius: {r_large:.1f}mm")
print()

print("=" * 80)
print(" COMPLEMENTARY FIT VERIFICATION")
print("=" * 80)
nesting_gap = r_large - r_small
nesting_ratio = r_small / r_large
print(f"Pattern A outer radius: {r_small:.1f}mm")
print(f"Pattern B outer radius: {r_large:.1f}mm")
print(f"Gap between hemispheres: {nesting_gap:.1f}mm")
print(f"Nesting ratio: {nesting_ratio:.3f} (ideal for 2:1 is 0.500)")
print()

if nesting_ratio > 0.45 and nesting_ratio < 0.55:
    print("✓ EXCELLENT complementary fit!")
elif nesting_ratio > 0.4 and nesting_ratio < 0.6:
    print("✓ Good complementary fit")
else:
    print("⚠ Fit may need adjustment")
print()

# Generate both patterns
print("=" * 80)
print(" GENERATING PATTERNS...")
print("=" * 80)

print("Generating Pattern A...")
r_small_actual = generate_pattern(
    m_small, h_small, s_small,
    "complementary_SMALL_A4",
    f"PATTERN A: Small Hemisphere\nRH-Y-{m_small}.{h_small}(1/2) | Scale: {s_small:.0f}mm | Radius: {r_small:.0f}mm"
)

print("Generating Pattern B...")
r_large_actual = generate_pattern(
    m_large, h_large, s_large,
    "complementary_LARGE_A4",
    f"PATTERN B: Large Hemisphere\nRH-Y-{m_large}.{h_large}(1/2) | Scale: {s_large:.0f}mm | Radius: {r_large:.0f}mm"
)

print()
print("=" * 80)
print(" THREE-STATE ASSEMBLY INSTRUCTIONS")
print("=" * 80)
print("""
STATE 1: FLAT (Both patterns collapsed)
  ├─ Pattern A: Flat hexagon ~{0:.0f}mm diameter
  └─ Pattern B: Flat octagon ~{1:.0f}mm diameter
  Total thickness: ~2-5mm (depending on paper)

STATE 2: SMALL HEMISPHERE (Pattern A deployed, B flat)
  ├─ Deploy Pattern A fully → dome shape
  │  ├─ Deployed radius: ~{2:.0f}mm
  │  └─ Height: ~{3:.0f}mm (approximate hemisphere)
  └─ Pattern B remains flat (stored or unused)

STATE 3: LARGE HEMISPHERE (Pattern B deployed, A flat)
  ├─ Deploy Pattern B fully → larger dome
  │  ├─ Deployed radius: ~{4:.0f}mm
  │  └─ Height: ~{5:.0f}mm
  └─ Pattern A remains flat (stored or unused)

COMPLEMENTARY ASSEMBLY: (Both deployed)
  ├─ Deploy both Pattern A and Pattern B
  ├─ Pattern A forms inner hemisphere (radius {2:.0f}mm)
  ├─ Pattern B forms outer hemisphere (radius {4:.0f}mm)
  ├─ Nest A inside B's cavity
  └─ Gap between shells: ~{6:.0f}mm
     → Creates double-walled spherical structure!

ALTERNATIVE: Side-by-side complementary
  Instead of nesting, place convex sides together:
  ├─ Pattern A convex side
  ├─ Pattern B concave side (inverted)
  └─ Should create closed spheroid

""".format(
    s_small * 2,  # 0: flat diameter A
    s_large * 2,  # 1: flat diameter B
    r_small_actual,  # 2: deployed radius A
    r_small_actual * 0.8,  # 3: height A (approx)
    r_large_actual,  # 4: deployed radius B
    r_large_actual * 0.8,  # 5: height B (approx)
    nesting_gap  # 6: gap
))

print("=" * 80)
print(" FILES GENERATED (ready to print on A4)")
print("=" * 80)
print("  complementary_SMALL_A4.svg/png  - Pattern A (small hemisphere)")
print("  complementary_LARGE_A4.svg/png  - Pattern B (large hemisphere)")
print()
print("✓ Generation complete!")
print()
print("=" * 80)
print(" FOLDING TIPS")
print("=" * 80)
print("""
1. Print both patterns on 120gsm cardstock
2. Score all fold lines with ruler and bone folder
3. Fold slowly - these larger patterns need gentle deployment
4. For bistable behavior: fold completely flat first, then deploy
5. Patterns may resist at first - be patient and persistent
6. Once creased properly, should snap between flat and deployed states

EXPERIMENT:
- Try deploying Pattern A to different intermediate states
- See if you can find stable positions between flat and full deployment
- This could give you additional "states" beyond the three designed!
""")
