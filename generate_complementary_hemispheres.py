"""
Generate two complementary Yoshimura bloom patterns that form nested hemispheres

Design requirements:
- Pattern A (small): Deploys to small hemisphere
- Pattern B (large): Deploys to large hemisphere with cavity
- Both patterns can fit together as complementary halves
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('Bloom_Pattern_Data/Yoshimura Bloom Pattern Computer Program/Yoshimura_bloom_pattern_code.py')
import Bloom_Yoshimura

def calculate_deployed_radius(m, h, s):
    """Calculate deployed radius based on formula from paper (Section 5(b)(i))"""
    beta = np.pi / m
    # Developed circumscribed diameter formula
    diameter = 2 * s * np.sqrt(h**2 + (1/(np.sin(beta)**2))/4 - h * (1/np.sin(beta)) * np.cos(3*beta - 3*np.pi/2))
    return diameter / 2

def generate_pattern(m, h, s, filename_base, title):
    """Generate a bloom pattern with given parameters"""
    bloom = Bloom_Yoshimura.Bloom_Yoshimura(m, h, s)
    bloom.plot_origin = False
    bloom.plot_points = False
    bloom.plot_facets = True  # Show facets to visualize structure
    bloom.plot_lines = True
    bloom.line_width = 1.0
    bloom.line_style = False  # Monochrome
    bloom.crease_is_invert = False

    # Generate
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

    # Plot
    fig = plt.figure(figsize=(8.27, 11.69))  # A4
    bloom.classify_crease()
    bloom.plot_facet_set()
    bloom.plot_monochromatic_crease_set()
    plt.axis('equal')
    plt.axis('off')
    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()

    # Save
    plt.savefig(f'/home/user/z2i/{filename_base}.svg', dpi=300, bbox_inches='tight')
    plt.savefig(f'/home/user/z2i/{filename_base}.png', dpi=300, bbox_inches='tight')
    plt.close()

    return calculate_deployed_radius(m, h, s)

print("=" * 70)
print("COMPLEMENTARY HEMISPHERE BLOOM PATTERNS")
print("=" * 70)
print()

# PATTERN A: Small hemisphere (inner/concave)
print("PATTERN A: Small Hemisphere (Inner)")
print("-" * 70)
m_small = 6   # hexagonal
h_small = 2   # height order 2
s_small = 35  # scale in mm

r_small = generate_pattern(m_small, h_small, s_small,
                          "hemisphere_SMALL_inner_A4",
                          f"Pattern A: Small Hemisphere\nRH-Y-{m_small}.{h_small}(1/2)")

print(f"  Parameters: m={m_small}, h={h_small}, s={s_small}mm")
print(f"  Type: RH-Y-{m_small}.{h_small}(1/2)")
print(f"  Deployed radius: {r_small:.1f}mm")
print(f"  Flat diameter: ~{s_small * 2}mm")
print()

# PATTERN B: Large hemisphere (outer/convex)
# Calculate scale to make inner radius match outer radius of small pattern
print("PATTERN B: Large Hemisphere (Outer)")
print("-" * 70)
m_large = 8    # octagonal (more sides → smoother)
h_large = 3    # higher order → larger deployment
# We want the inner radius of B to equal outer radius of A
# This is approximate - would need iterative calculation for exact fit
s_large = 45   # scaled appropriately

r_large = generate_pattern(m_large, h_large, s_large,
                          "hemisphere_LARGE_outer_A4",
                          f"Pattern B: Large Hemisphere\nRH-Y-{m_large}.{h_large}(1/2)")

print(f"  Parameters: m={m_large}, h={h_large}, s={s_large}mm")
print(f"  Type: RH-Y-{m_large}.{h_large}(1/2)")
print(f"  Deployed radius: {r_large:.1f}mm")
print(f"  Flat diameter: ~{s_large * 2}mm")
print()

# Analysis
print("=" * 70)
print("COMPLEMENTARY FIT ANALYSIS")
print("=" * 70)
gap = r_large - r_small
fit_ratio = r_small / r_large
print(f"Small hemisphere outer radius: {r_small:.1f}mm")
print(f"Large hemisphere outer radius: {r_large:.1f}mm")
print(f"Radial gap (should be ~0 for perfect fit): {gap:.1f}mm")
print(f"Nesting ratio: {fit_ratio:.2f}")
print()

if abs(gap) < 10:
    print("✓ Good complementary fit!")
else:
    print(f"⚠ Gap too large - adjust s_large parameter")
    suggested_s = s_large * (r_small / r_large)
    print(f"  Suggested s_large: {suggested_s:.1f}mm")
print()

print("=" * 70)
print("FOLDING INSTRUCTIONS")
print("=" * 70)
print("""
THREE-STATE DEPLOYMENT:

State 1: FLAT
  - Both patterns fully collapsed
  - Stack together or store separately

State 2: SMALL HEMISPHERE (Pattern A only)
  - Deploy Pattern A fully → creates small dome
  - Pattern B remains flat or partially deployed
  - Dome height ≈ {0:.1f}mm

State 3: LARGE HEMISPHERE (Pattern B only)
  - Deploy Pattern B fully → creates large dome
  - Dome height ≈ {1:.1f}mm
  - Pattern A can nest inside Pattern B cavity

COMPLEMENTARY ASSEMBLY:
  - Deploy both patterns fully
  - Insert small dome (A) into cavity of large dome (B)
  - Should fit together as nested hemispheres
  - Creates approximately spherical closed surface

TIPS:
  - Score creases carefully before folding
  - Deploy slowly to avoid tearing at vertices
  - Patterns may be bistable (snap between states)
  - Use cardstock (120gsm) for better stability
""".format(r_small, r_large))

print("=" * 70)
print("FILES GENERATED:")
print("=" * 70)
print("  hemisphere_SMALL_inner_A4.svg/png - Pattern A (print on A4)")
print("  hemisphere_LARGE_outer_A4.svg/png - Pattern B (print on A4)")
print()
print("✓ Generation complete!")
