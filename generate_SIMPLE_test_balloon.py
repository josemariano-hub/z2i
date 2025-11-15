"""
Generate SIMPLE test balloon for A4 paper
- Easy to fold by hand
- Normal paper compatible
- Good for learning the technique
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('Bloom_Pattern_Data/Yoshimura Bloom Pattern Computer Program/Yoshimura_bloom_pattern_code.py')
import Bloom_Yoshimura

def calculate_deployed_radius(m, h, s):
    beta = np.pi / m
    diameter = 2 * s * np.sqrt(h**2 + (1/(np.sin(beta)**2))/4 -
                               h * (1/np.sin(beta)) * np.cos(3*beta - 3*np.pi/2))
    return diameter / 2

def generate_simple_hemisphere(m, h, s, filename, title, invert_creases=False):
    """Generate simplified hemisphere pattern"""
    bloom = Bloom_Yoshimura.Bloom_Yoshimura(m, h, s)
    bloom.plot_origin = False
    bloom.plot_points = True  # Show points for this simple version
    bloom.plot_facets = True
    bloom.plot_lines = True
    bloom.line_width = 1.5
    bloom.line_style = True  # Colored
    bloom.crease_is_invert = invert_creases

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

    # Plot with larger margins
    fig = plt.figure(figsize=(8.27, 11.69))  # A4
    bloom.classify_crease()
    bloom.plot_facet_set()
    bloom.plot_colored_crease_set()
    bloom.plot_point_set()  # Show vertices
    plt.axis('equal')
    plt.axis('off')

    # Title
    plt.title(title, fontsize=13, pad=20, fontweight='bold')

    # Instructions at bottom
    instr = "BLUE lines = Mountain fold (away from you) | RED lines = Valley fold (toward you)\nBLACK thick lines = Edges | Gray dots = Vertices"
    plt.text(0.5, 0.02, instr, transform=fig.transFigure,
             ha='center', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig(f'/home/user/z2i/{filename}.svg', dpi=300, bbox_inches='tight')
    plt.savefig(f'/home/user/z2i/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()

    return calculate_deployed_radius(m, h, s)

print("=" * 80)
print("  SIMPLE TEST BALLOON - A4 PRINTABLE - BEGINNER FRIENDLY")
print("=" * 80)
print()

# SIMPLE parameters for testing
m = 6   # Hexagon (simple, 6-fold symmetry)
h = 2   # Height order 2 (minimal complexity)
s = 50  # 50mm scale (good size for handling)

print("SIMPLIFIED DESIGN:")
print("-" * 80)
print(f"  Pattern: RH-Y-{m}.{h}(1/2) - SIMPLE Yoshimura bloom")
print(f"  Complexity: Only {m*(h**2 + 3*h)} facets per hemisphere (vs 144 in complex version)")
print(f"  Paper: Standard 80gsm A4 paper OK")
print(f"  Folding time: ~15-20 minutes per hemisphere")
print()

r_deployed = calculate_deployed_radius(m, h, s)
flat_diameter = s * 2

v_large = (4/3) * np.pi * (r_deployed ** 3) / 1000
v_small_natural = v_large / 8  # Natural bistable ratio
ratio_natural = 8

print("DIMENSIONS:")
print("-" * 80)
print(f"  Deployed radius: {r_deployed:.1f}mm")
print(f"  Deployed diameter: {r_deployed*2:.1f}mm")
print(f"  Flat-folded diameter: ~{flat_diameter:.0f}mm")
print(f"  Large balloon volume: ~{v_large:.2f} liters")
print(f"  Natural volume ratio (no cord): ~{ratio_natural}:1")
print(f"  ✓ Easily fits on A4 paper (210mm × 297mm)")
print()

print("GENERATING SIMPLIFIED PATTERNS:")
print("-" * 80)

print("  Pattern A (Top hemisphere)...")
r_a = generate_simple_hemisphere(
    m, h, s,
    "SIMPLE_balloon_TOP",
    f"SIMPLE TEST BALLOON - TOP HEMISPHERE (Pattern A)\n" +
    f"Hexagonal Yoshimura RH-Y-{m}.{h}(1/2) | Deployed: {r_deployed:.0f}mm diameter",
    invert_creases=False
)

print("  Pattern B (Bottom hemisphere - inverted)...")
r_b = generate_simple_hemisphere(
    m, h, s,
    "SIMPLE_balloon_BOTTOM",
    f"SIMPLE TEST BALLOON - BOTTOM HEMISPHERE (Pattern B)\n" +
    f"Hexagonal Yoshimura RH-Y-{m}.{h}(1/2) | Deployed: {r_deployed:.0f}mm diameter",
    invert_creases=True
)

facet_count = m * (h**2 + 3*h)

print()
print("=" * 80)
print("  STEP-BY-STEP FOLDING INSTRUCTIONS FOR BEGINNERS")
print("=" * 80)
print(f"""
MATERIALS:
  □ 2× A4 sheets regular printer paper (80gsm) or cardstock (120gsm)
  □ Ruler (metal edge preferred)
  □ Ballpoint pen (empty/dry) or bone folder for scoring
  □ Clear tape or glue stick
  □ Scissors (optional - for trimming edges)

PREPARATION (15 minutes):

1. PRINT
   • Print Pattern A (top) on one sheet
   • Print Pattern B (bottom) on another sheet
   • Print at 100% scale (no scaling!)
   • Color printing recommended but not required

2. SCORE ALL CREASES (Important!)
   • Place ruler along EACH colored line
   • Run empty pen firmly along line (don't tear paper!)
   • Blue lines = score on one side
   • Red lines = score on opposite side
   • This takes time but makes folding much easier

3. PRE-FOLD
   • Gently fold along each scored line
   • BLUE lines: fold AWAY from you (mountain ⛰️)
   • RED lines: fold TOWARD you (valley 🌊)
   • Don't crease hard yet, just "break in" the folds

FOLDING SEQUENCE (20 minutes per hemisphere):

STEP 1: Fold the center
  • Start with the hexagon in the center
  • Fold all 6 creases connected to hexagon edges
  • Work gently - paper will resist at first

STEP 2: Work outward in rings
  • This pattern has {h} rings from center to edge
  • Complete one ring before moving to next
  • Be patient - each ring gets easier

STEP 3: Flatten completely
  • Once all creases are folded, press flat
  • Should collapse into flat hexagonal shape
  • Flat diameter: ~{flat_diameter:.0f}mm

STEP 4: Deployment test
  • Gently pull center and edge apart
  • Pattern should "pop" open into dome
  • Diameter when deployed: ~{r_deployed*2:.0f}mm

STEP 5: Repeat for second hemisphere
  • Fold Pattern B (bottom) the same way
  • Note: creases are inverted (opposite colors)
  • This is correct! They're complementary halves

ASSEMBLY (10 minutes):

1. DEPLOY BOTH HEMISPHERES
   • Unfold both patterns to dome shape
   • Make sure both are same size

2. ALIGN EDGES
   • The outer hexagon edges should match
   • Place hemispheres edge-to-edge
   • One convex up, one convex down

3. JOIN WITH TAPE
   • Small pieces of clear tape on INSIDE
   • Work around the 6 edges
   • Don't tape too tightly - allow slight flex

4. TEST DEPLOYMENT
   • Gently squeeze balloon flat
   • Should collapse to ~{flat_diameter:.0f}mm diameter
   • Release - should spring back to ~{r_deployed*2:.0f}mm

NATURAL BEHAVIOR:

This simple version has TWO natural stable states:
  • FLAT: Fully collapsed
  • DEPLOYED: ~{r_deployed*2:.0f}mm diameter

Volume ratio: ~{ratio_natural}:1 (natural, no hardware needed!)

To get 200:1 ratio, you'd need the complex version with elastic cord.
But this simple version is GREAT for learning the technique!

TROUBLESHOOTING:

□ "Won't fold flat"
   → Re-score creases more firmly
   → Make sure mountain/valley assignments are correct

□ "Pattern tears at vertices"
   → Use thicker paper (120gsm cardstock)
   → Score more gently
   → Reinforce with clear tape on back

□ "Creases won't stay folded"
   → Pre-fold each crease back and forth several times
   → Use sharper creases (crease firmly along ruler)

□ "Hemispheres don't match"
   → Check that both printed at same scale (100%)
   → Verify Pattern B creases are inverted

□ "Too difficult"
   → Try even simpler: m=5, h=1 (only {5*(1+3)} facets!)
   → Practice with just one hemisphere first

WHAT TO EXPECT:

  Facets per hemisphere: {facet_count}
  Total creases to fold: ~{facet_count * 3} (manageable!)
  Folding time: 15-20 min per hemisphere
  Assembly time: 10 min
  Total project time: ~1 hour

NEXT STEPS:

Once you've mastered this simple version:
  1. Try higher complexity (m=8, h=3)
  2. Try the 200:1 ratio version (m=12, h=6)
  3. Experiment with different sizes (change s value)
  4. Try different paper types (cardstock, thin plastic)

TIPS FOR SUCCESS:

  ✓ Work slowly and carefully
  ✓ Score EVERY crease before folding
  ✓ Start from center, work outward
  ✓ Be patient with first few folds
  ✓ Paper will become easier to fold after "breaking in"
  ✓ Good lighting helps see the creases
  ✓ Take breaks if fingers get tired

This is a real origami engineering project - be proud when you finish! 🎈
""")

print("=" * 80)
print("  FILES GENERATED")
print("=" * 80)
print("  SIMPLE_balloon_TOP.svg/.png     - Pattern A (normal creases)")
print("  SIMPLE_balloon_BOTTOM.svg/.png  - Pattern B (inverted creases)")
print()
print("✓ SIMPLE test patterns ready to print!")
print()
print("These are MUCH easier than the 200:1 version - perfect for learning!")
