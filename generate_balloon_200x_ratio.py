"""
Generate complementary balloon hemisphere patterns
Target: 200:1 volume ratio, desktop size (200mm diameter large state)
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('Bloom_Pattern_Data/Yoshimura Bloom Pattern Computer Program/Yoshimura_bloom_pattern_code.py')
import Bloom_Yoshimura

def calculate_deployed_radius(m, h, s):
    """Calculate deployed radius from bloom pattern parameters"""
    beta = np.pi / m
    diameter = 2 * s * np.sqrt(h**2 + (1/(np.sin(beta)**2))/4 -
                               h * (1/np.sin(beta)) * np.cos(3*beta - 3*np.pi/2))
    return diameter / 2

def find_scale_for_radius(m, h, target_radius):
    """Find scale parameter s to achieve target deployed radius"""
    s_test = 10
    for _ in range(100):
        r_test = calculate_deployed_radius(m, h, s_test)
        if abs(r_test - target_radius) < 0.1:
            return s_test
        s_test = s_test * (target_radius / r_test)
    return s_test

def generate_balloon_half(m, h, s, filename, title, invert_creases=False):
    """Generate one hemisphere of the balloon"""
    bloom = Bloom_Yoshimura.Bloom_Yoshimura(m, h, s)
    bloom.plot_origin = False
    bloom.plot_points = False
    bloom.plot_facets = True
    bloom.plot_lines = True
    bloom.line_width = 0.8
    bloom.line_style = True  # Colored for clarity
    bloom.crease_is_invert = invert_creases

    # Generate pattern
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
    bloom.plot_colored_crease_set()
    plt.axis('equal')
    plt.axis('off')
    plt.title(title, fontsize=11, pad=15, fontweight='bold')

    # Add instruction text
    instr = "BLUE = Mountain fold | RED = Valley fold | BLACK = Edge"
    plt.text(0.5, 0.02, instr, transform=fig.transFigure,
             ha='center', fontsize=8, style='italic')

    plt.tight_layout()

    plt.savefig(f'/home/user/z2i/{filename}.svg', dpi=300, bbox_inches='tight')
    plt.savefig(f'/home/user/z2i/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()

    return calculate_deployed_radius(m, h, s)

print("=" * 80)
print("  200:1 VOLUME RATIO BALLOON - COMPLEMENTARY HEMISPHERE PATTERNS")
print("=" * 80)
print()

# Design parameters
m = 12  # 12-fold symmetry (good sphericity, 30° increments)
h = 6   # Height order 6 (enough complexity for large expansion)
target_radius_large = 100  # 100mm radius = 200mm diameter

print("DESIGN REQUIREMENTS:")
print("-" * 80)
print(f"  Target large balloon diameter: 200mm (desktop size)")
print(f"  Target volume ratio: 200:1")
print(f"  Material: Paper (A4 printable)")
print()

# Calculate dimensions
r_large = target_radius_large
r_small = r_large / (200 ** (1/3))  # Cube root for volume ratio
v_large = (4/3) * np.pi * (r_large ** 3) / 1000  # in liters
v_small = (4/3) * np.pi * (r_small ** 3) / 1000  # in liters
volume_ratio = v_large / v_small

print("CALCULATED DIMENSIONS:")
print("-" * 80)
print(f"  Large balloon radius: {r_large:.1f}mm")
print(f"  Small balloon radius: {r_small:.1f}mm")
print(f"  Radius ratio: {r_large/r_small:.2f}:1")
print(f"  Large volume: {v_large:.2f} liters")
print(f"  Small volume: {v_small*1000:.1f} ml")
print(f"  Volume ratio: {volume_ratio:.1f}:1")
print()

# Find optimal scale
print("PATTERN OPTIMIZATION:")
print("-" * 80)
print(f"  Pattern type: RH-Y-{m}.{h}(1/2) (Yoshimura bloom)")
print(f"  Symmetry: {m}-fold")
print(f"  Complexity: Height order {h}")

s_optimal = find_scale_for_radius(m, h, r_large)
r_actual = calculate_deployed_radius(m, h, s_optimal)
flat_diameter = s_optimal * 2

print(f"  Calculated scale: s = {s_optimal:.1f}mm")
print(f"  Deployed radius: {r_actual:.1f}mm")
print(f"  Flat-folded diameter: ~{flat_diameter:.1f}mm")

if flat_diameter > 200:
    print(f"  ⚠️ Warning: Pattern ({flat_diameter:.0f}mm) larger than A4 width (210mm)")
    print(f"     Consider reducing to fit A4, or print on larger paper")
else:
    print(f"  ✓ Fits on A4 paper with margins")
print()

# Generate both hemispheres
print("GENERATING PATTERNS:")
print("-" * 80)

print("  Generating Pattern A (Top hemisphere)...")
r_a = generate_balloon_half(
    m, h, s_optimal,
    "balloon_200x_TOP_hemisphere",
    f"BALLOON TOP HEMISPHERE (Pattern A)\n" +
    f"RH-Y-{m}.{h}(1/2) | Large: {r_large:.0f}mm | Small: {r_small:.0f}mm | Ratio: 200:1",
    invert_creases=False
)

print("  Generating Pattern B (Bottom hemisphere - inverted creases)...")
r_b = generate_balloon_half(
    m, h, s_optimal,
    "balloon_200x_BOTTOM_hemisphere",
    f"BALLOON BOTTOM HEMISPHERE (Pattern B)\n" +
    f"RH-Y-{m}.{h}(1/2) | Large: {r_large:.0f}mm | Small: {r_small:.0f}mm | Ratio: 200:1",
    invert_creases=True
)

print()
print("=" * 80)
print("  ASSEMBLY & DEPLOYMENT INSTRUCTIONS")
print("=" * 80)
print(f"""
MATERIALS NEEDED:
  • 2× A4 sheets cardstock (120-160gsm recommended)
  • Elastic cord or rubber band (~200mm length)
  • Clear tape for joining hemispheres
  • Scoring tool (bone folder or empty ballpoint pen)

STEP 1: PRINT & PREPARE
  1. Print both patterns on cardstock
  2. Score all creases carefully with ruler
  3. Pre-fold all creases (this is important!)
  4. Fold flat and unfold several times to "break in" the creases

STEP 2: INSTALL CONSTRAINT SYSTEM (for small balloon state)
  For 200:1 ratio, we need mechanical constraint:

  Pattern A (Top):
    • Thread elastic cord through vertices at ~{r_small:.0f}mm radius
    • Mark this as "small balloon ring"
    • Tie cord into adjustable loop

  Pattern B (Bottom):
    • Repeat same process
    • Ensure cord length matches Pattern A

STEP 3: ASSEMBLY
  1. Deploy both patterns to desired size
  2. Align equatorial edges (the outer polygon)
  3. Join with small pieces of clear tape on inside
  4. Work around circumference for complete seal

DEPLOYMENT STATES:

  STATE 1: FLAT (Storage)
    • Both patterns fully collapsed
    • Stack together or store separately
    • Thickness: ~5-10mm
    • Footprint: ~{flat_diameter:.0f}mm diameter

  STATE 2: SMALL BALLOON (Constrained)
    • Deploy until elastic cord is taut
    • Radius: ~{r_small:.0f}mm
    • Volume: ~{v_small*1000:.0f}ml
    • Cord holds this stable state

  STATE 3: LARGE BALLOON (Full deployment)
    • Loosen/remove elastic cord
    • Deploy fully to maximum radius
    • Radius: ~{r_large:.0f}mm
    • Volume: ~{v_large:.2f} liters
    • Pattern naturally wants this state

VOLUME RATIO: {volume_ratio:.0f}:1 🎈

TIPS:
  • The elastic cord is ESSENTIAL for the small stable state
  • Without constraint, pattern will only be bistable (flat ↔ large)
  • Adjust cord length to fine-tune small balloon size
  • Use thicker paper for better shape retention
  • Pattern has {m*h*2} triangular facets per hemisphere - be patient!

PURE ORIGAMI ALTERNATIVE:
  If you want no hardware, you could:
  • Hold small state manually
  • Use friction/interference fit
  • Accept only 2 states: flat and large (~8:1 ratio naturally)
""")

print("=" * 80)
print("  FILES GENERATED")
print("=" * 80)
print("  balloon_200x_TOP_hemisphere.svg/.png     - Pattern A (normal creases)")
print("  balloon_200x_BOTTOM_hemisphere.svg/.png  - Pattern B (inverted creases)")
print()
print("✓ Generation complete!")
print()
print("=" * 80)
print("  CONSTRAINT SYSTEM DETAILS")
print("=" * 80)
print(f"""
To achieve 200:1 ratio, elastic cord must limit deployment:

CORD PLACEMENT:
  • Thread through vertices at approximately ring #{h//2} from center
  • This should be at radius ≈ {r_small:.0f}mm when deployed
  • Tie with adjustable knot (bowline or taut-line hitch)

CORD LENGTH CALCULATION:
  • Small balloon circumference: 2π × {r_small:.0f}mm ≈ {2*np.pi*r_small:.0f}mm
  • Add 20-30mm for knot and adjustment
  • Total cord needed: ~{2*np.pi*r_small + 25:.0f}mm per hemisphere

ADJUSTMENT:
  • Too tight → balloon won't deploy to small size
  • Too loose → balloon deploys past small size
  • Test and adjust cord length until {r_small:.0f}mm radius achieved

REMOVAL FOR LARGE STATE:
  • Slip cord over vertices to outside
  • Or untie and remove completely
  • Pattern will naturally deploy to ~{r_large:.0f}mm radius
""")
