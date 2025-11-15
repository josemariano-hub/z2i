"""Generate a printable bloom pattern for A4 paper"""

import sys
sys.path.append('Bloom_Pattern_Data/Yoshimura Bloom Pattern Computer Program/Yoshimura_bloom_pattern_code.py')
import Bloom_Yoshimura
import matplotlib.pyplot as plt

# Settings for A4 paper (210mm x 297mm)
# We'll use about 180mm diameter to leave margins
m = 6  # hexagon
h = 1  # height order 1 (simple)
s = 60  # scale in mm - will create ~120mm diameter pattern

bloom = Bloom_Yoshimura.Bloom_Yoshimura(m, h, s)
bloom.plot_origin = False
bloom.plot_points = False
bloom.plot_facets = False  # No fill, just creases
bloom.plot_lines = True
bloom.line_width = 1.5
bloom.line_style = False  # Monochrome for printing
bloom.crease_is_invert = False

# Generate the pattern
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
plt.figure(figsize=(8.27, 11.69))  # A4 in inches
bloom.classify_crease()
bloom.plot_monochromatic_crease_set()
plt.axis('equal')
plt.axis('off')
plt.tight_layout()

# Save as SVG
plt.savefig('/home/user/z2i/bloom_pattern_A4_printable.svg', dpi=300, bbox_inches='tight')
plt.savefig('/home/user/z2i/bloom_pattern_A4_printable.png', dpi=300, bbox_inches='tight')
print("✓ Generated bloom_pattern_A4_printable.svg")
print("✓ Generated bloom_pattern_A4_printable.png")
print("\nPattern: RH-Y-6.1 (Hexagonal Yoshimura, height order 1)")
print("Scale: ~120mm diameter (fits A4 with margins)")
print("\nFolding guide:")
print("- SOLID lines = Mountain folds (fold away from you)")
print("- DASHED lines = Valley folds (fold toward you)")
print("- THICK lines = Edges (cut or leave as border)")
