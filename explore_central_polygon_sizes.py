"""
Explore different central polygon sizes in bloom patterns
Show the trade-offs and options
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

def generate_comparison_pattern(m, h, s, filename, title):
    """Generate pattern for comparison"""
    bloom = Bloom_Yoshimura.Bloom_Yoshimura(m, h, s)
    bloom.plot_origin = False
    bloom.plot_points = False
    bloom.plot_facets = True
    bloom.plot_lines = True
    bloom.line_width = 1.0
    bloom.line_style = True
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

    fig = plt.figure(figsize=(6, 6))
    bloom.classify_crease()
    bloom.plot_facet_set()
    bloom.plot_colored_crease_set()
    plt.axis('equal')
    plt.axis('off')
    plt.title(title, fontsize=10, pad=10, fontweight='bold')
    plt.tight_layout()

    plt.savefig(f'/home/user/z2i/{filename}.png', dpi=200, bbox_inches='tight')
    plt.close()

    central_polygon_side = s
    deployed_r = calculate_deployed_radius(m, h, s)
    ratio = deployed_r / central_polygon_side

    return central_polygon_side, deployed_r, ratio

print("=" * 80)
print("  CENTRAL POLYGON SIZE EXPLORATION")
print("=" * 80)
print()
print("The central polygon size is controlled by THREE parameters:")
print("  m = number of sides (pentagon=5, hexagon=6, octagon=8, etc.)")
print("  h = height order (number of rings)")
print("  s = scale factor (mm)")
print()

print("=" * 80)
print("  OPTION 1: Keep same m, h but REDUCE s (scale down everything)")
print("=" * 80)
print()

configs_option1 = [
    (6, 2, 50, "Same pattern, larger", "LARGE scale"),
    (6, 2, 30, "Same pattern, medium", "MEDIUM scale"),
    (6, 2, 15, "Same pattern, smaller", "SMALL scale"),
]

print("Pattern: RH-Y-6.2(1/2) at different scales")
print("-" * 80)
for m, h, s, desc, label in configs_option1:
    cp_size, deployed_r, ratio = generate_comparison_pattern(m, h, s, desc.replace(" ", "_").replace(",", ""),
                                                              f"{label}\nRH-Y-{m}.{h}(1/2) | s={s}mm")
    print(f"  {label:12} | Central polygon: {cp_size:5.1f}mm | Deployed radius: {deployed_r:6.1f}mm | Ratio: {ratio:5.2f}:1")

print()
print("Result: Everything scales proportionally - central polygon AND deployed size")
print("        Ratio stays the same!")
print()

print("=" * 80)
print("  OPTION 2: INCREASE h (add more rings) - makes center SMALLER relative")
print("=" * 80)
print()

configs_option2 = [
    (6, 1, 30, "Few rings", "h=1 (1 ring)"),
    (6, 2, 30, "Medium rings", "h=2 (2 rings)"),
    (6, 4, 30, "Many rings", "h=4 (4 rings)"),
]

print("Pattern: RH-Y-6.h(1/2) with same scale (s=30mm)")
print("-" * 80)
for m, h, s, desc, label in configs_option2:
    cp_size, deployed_r, ratio = generate_comparison_pattern(m, h, s, desc.replace(" ", "_"),
                                                              f"{label}\nRH-Y-{m}.{h}(1/2) | s={s}mm")
    facets = m * (h**2 + 3*h)
    print(f"  {label:14} | Central: {cp_size:5.1f}mm | Deployed: {deployed_r:6.1f}mm | Ratio: {ratio:5.2f}:1 | Facets: {facets}")

print()
print("Result: Higher h = MORE rings = LARGER deployed radius")
print("        Central polygon stays same size, but becomes SMALLER percentage of total")
print("        ✓ This is what you want for 'smaller central polygon relative to pattern'!")
print()

print("=" * 80)
print("  OPTION 3: CHANGE m (polygon sides) - affects center shape & size")
print("=" * 80)
print()

configs_option3 = [
    (5, 2, 30, "Pentagon", "Pentagon (m=5)"),
    (6, 2, 30, "Hexagon", "Hexagon (m=6)"),
    (8, 2, 30, "Octagon", "Octagon (m=8)"),
]

print("Pattern: RH-Y-m.2(1/2) with same scale (s=30mm)")
print("-" * 80)
for m, h, s, desc, label in configs_option3:
    cp_size, deployed_r, ratio = generate_comparison_pattern(m, h, s, desc,
                                                              f"{label}\nRH-Y-{m}.{h}(1/2) | s={s}mm")
    print(f"  {label:16} | Central: {cp_size:5.1f}mm | Deployed: {deployed_r:6.1f}mm | Ratio: {ratio:5.2f}:1")

print()
print("Result: More sides (higher m) = SMOOTHER circle, slightly different ratios")
print("        Central polygon side length stays same (=s), but perimeter increases")
print()

print("=" * 80)
print("  RECOMMENDATION FOR SMALL CENTRAL POLYGON")
print("=" * 80)
print()
print("To get a SMALL central polygon relative to deployed balloon:")
print()
print("  ✓ INCREASE h (height order) - adds more rings")
print("    Example: h=6 gives you 6 rings of expansion")
print()
print("  ✓ INCREASE m (polygon sides) for smoother sphere")
print("    Example: m=12 (12-sided) is very smooth")
print()
print("  Trade-offs:")
print("    • More rings (high h) = more complex = harder to fold")
print("    • More sides (high m) = more facets = harder to fold")
print("    • But MUCH larger deployment from small center!")
print()

print("=" * 80)
print("  PRACTICAL EXAMPLES")
print("=" * 80)
print()

examples = [
    ("SIMPLE (current)", 6, 2, 30, "Easy to fold, moderate expansion"),
    ("MEDIUM expansion", 8, 3, 25, "Good balance"),
    ("LARGE expansion", 10, 4, 20, "Small center, large balloon"),
    ("EXTREME (200:1)", 12, 6, 13, "Tiny center, huge balloon (complex!)"),
]

print("Comparison of different configurations:")
print("-" * 80)
for name, m, h, s, note in examples:
    cp_size, deployed_r, ratio = s, calculate_deployed_radius(m, h, s), calculate_deployed_radius(m, h, s) / s
    facets = m * (h**2 + 3*h)
    print(f"{name:20} | Center: {cp_size:4.0f}mm | Deployed: {deployed_r:5.0f}mm | Ratio: {ratio:5.1f}:1 | Facets: {facets:3} | {note}")

print()
print("=" * 80)
print("  GENERATE CUSTOM PATTERN WITH SMALL CENTER")
print("=" * 80)
print()

# Generate one example with small center
print("Generating example: SMALL CENTER balloon (m=8, h=4, s=20mm)...")
print()

m_custom, h_custom, s_custom = 8, 4, 20

bloom = Bloom_Yoshimura.Bloom_Yoshimura(m_custom, h_custom, s_custom)
bloom.plot_origin = False
bloom.plot_points = False
bloom.plot_facets = True
bloom.plot_lines = True
bloom.line_width = 1.2
bloom.line_style = True
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

fig = plt.figure(figsize=(8.27, 11.69))  # A4
bloom.classify_crease()
bloom.plot_facet_set()
bloom.plot_colored_crease_set()
plt.axis('equal')
plt.axis('off')

r_deployed = calculate_deployed_radius(m_custom, h_custom, s_custom)
facets = m_custom * (h_custom**2 + 3*h_custom)
ratio_expansion = r_deployed / s_custom

title = f"SMALL CENTER BALLOON - TOP HEMISPHERE\n"
title += f"RH-Y-{m_custom}.{h_custom}(1/2) | Central polygon: {s_custom}mm | Deployed: {r_deployed:.0f}mm\n"
title += f"Expansion ratio: {ratio_expansion:.1f}:1 | Facets: {facets}"

plt.title(title, fontsize=11, pad=15, fontweight='bold')
plt.text(0.5, 0.02, "BLUE = Mountain | RED = Valley | BLACK = Edge",
         transform=fig.transFigure, ha='center', fontsize=8, style='italic')
plt.tight_layout()

plt.savefig('/home/user/z2i/SMALL_center_balloon_TOP.svg', dpi=300, bbox_inches='tight')
plt.savefig('/home/user/z2i/SMALL_center_balloon_TOP.png', dpi=300, bbox_inches='tight')
plt.close()

# Generate inverted bottom
bloom.crease_is_invert = True
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
bloom.plot_colored_crease_set()
plt.axis('equal')
plt.axis('off')

title = f"SMALL CENTER BALLOON - BOTTOM HEMISPHERE\n"
title += f"RH-Y-{m_custom}.{h_custom}(1/2) | Central polygon: {s_custom}mm | Deployed: {r_deployed:.0f}mm\n"
title += f"Expansion ratio: {ratio_expansion:.1f}:1 | Facets: {facets}"

plt.title(title, fontsize=11, pad=15, fontweight='bold')
plt.text(0.5, 0.02, "BLUE = Mountain | RED = Valley | BLACK = Edge",
         transform=fig.transFigure, ha='center', fontsize=8, style='italic')
plt.tight_layout()

plt.savefig('/home/user/z2i/SMALL_center_balloon_BOTTOM.svg', dpi=300, bbox_inches='tight')
plt.savefig('/home/user/z2i/SMALL_center_balloon_BOTTOM.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✓ Generated SMALL_center_balloon_TOP.svg/png")
print(f"✓ Generated SMALL_center_balloon_BOTTOM.svg/png")
print()
print("SPECIFICATIONS:")
print(f"  Central octagon side: {s_custom}mm")
print(f"  Central octagon diameter: ~{s_custom * 2.4:.0f}mm")
print(f"  Deployed radius: {r_deployed:.0f}mm")
print(f"  Deployed diameter: {r_deployed*2:.0f}mm")
print(f"  Expansion ratio: {ratio_expansion:.1f}:1")
print(f"  Facets per hemisphere: {facets}")
print(f"  Complexity: {'MEDIUM' if facets < 100 else 'HIGH' if facets < 150 else 'VERY HIGH'}")
print()
print("This pattern has a SMALL central polygon that expands to a LARGE balloon!")
print()

print("=" * 80)
print("  SUMMARY")
print("=" * 80)
print()
print("To make central polygon SMALLER relative to balloon:")
print()
print("  1. INCREASE h (height order)")
print("     • h=1: minimal expansion")
print("     • h=2-3: moderate (good for beginners)")
print("     • h=4-6: large expansion")
print("     • h=6+: extreme expansion (very complex)")
print()
print("  2. OPTIONALLY increase m (smoother sphere)")
print("     • m=6: hexagon (simple)")
print("     • m=8: octagon (recommended)")
print("     • m=12: dodecagon (very smooth)")
print()
print("  3. Keep s moderate (this is just scale)")
print("     • s=20-30mm works well for A4 paper")
print()
print("Files generated:")
print("  • Comparison images showing different configurations")
print("  • SMALL_center_balloon patterns ready to print!")
print()
print("✓ All files saved!")
