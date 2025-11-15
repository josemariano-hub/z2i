"""
DETAILED MASS BUDGET FOR STRATOSPHERIC BLOOM BALLOON
=====================================================
Accounts for ALL components including adhesive tape for joining Mylar
"""

import numpy as np

print("="*80)
print("  DETAILED MASS BUDGET - 2 KG BALLOON CONSTRAINT")
print("="*80)

# SYSTEM PARAMETERS
payload_mass = 3.0  # kg
balloon_material_budget = 2.0  # kg MAX
total_mass = payload_mass + balloon_material_budget

# ATMOSPHERIC CONDITIONS AT 30 KM
T_30km = 228.15  # K (-45°C)
P_30km = 1197  # Pa
R_He = 8314.46 / 0.004
rho_air_30km = 0.018277  # kg/m³
rho_He_30km = P_30km / (R_He * T_30km)
lift_per_m3_He = (rho_air_30km - rho_He_30km) * 9.81

# BALLOON SIZING
V_required = (total_mass * 9.81) / lift_per_m3_He
r_balloon = (3 * V_required / (4 * np.pi)) ** (1/3)
A_balloon = 4 * np.pi * r_balloon**2

# 200:1 ratio
V_small = V_required / 200
r_small = (3 * V_small / (4 * np.pi)) ** (1/3)

print(f"\nBALLOON DIMENSIONS:")
print(f"  Large (deployed):  {2*r_balloon:.2f} m diameter, {V_required:.1f} m³")
print(f"  Small (compact):   {2*r_small:.2f} m diameter, {V_small:.3f} m³")
print(f"  Surface area:      {A_balloon:.1f} m²")
print(f"  Volume ratio:      200:1")

# BLOOM PATTERN GEOMETRY
print("\n" + "="*80)
print("  BLOOM PATTERN GEOMETRY - RH-Y-12.6(1/2)")
print("="*80)

m = 12  # 12-sided polygon
h = 6   # height order 6
facets_per_hemisphere = m * (h**2 + 3*h)  # 648 facets
total_facets = 2 * facets_per_hemisphere

# Pattern dimensions
beta = np.pi / m
r_expansion = np.sqrt(h**2 + (1/np.sin(beta))**2 / 4 -
                     h * (1/np.sin(beta)) * np.cos(3*beta - 3*np.pi/2))
s_scale = r_balloon / r_expansion
flat_diameter = 2 * s_scale * h

print(f"\n  Pattern:           RH-Y-{m}.{h}(1/2)")
print(f"  Polygon sides:     {m}")
print(f"  Height order:      {h}")
print(f"  Scale factor:      {s_scale:.3f} m ({s_scale*1000:.0f} mm)")
print(f"  Facets per half:   {facets_per_hemisphere}")
print(f"  Total facets:      {total_facets}")
print(f"  Flat diameter:     {flat_diameter:.2f} m")

# CREASE LINE CALCULATIONS
# For a hemisphere with m sides and h rings:
# - Central polygon: m sides
# - Each ring adds: m radial creases + m circumferential creases
# - Total creases ≈ m * (2*h + 1) per hemisphere (rough estimate)

# More accurate: Each facet is a quadrilateral with 4 edges
# But edges are shared, so total unique edges ≈ 1.5 * facets
crease_length_per_facet = 2 * s_scale  # Approximate average
total_crease_length = crease_length_per_facet * total_facets * 0.75  # Account for sharing

# Seam length (joining two hemispheres at equator)
equator_circumference = 2 * np.pi * r_balloon

print(f"\n  CREASE & SEAM GEOMETRY:")
print(f"  Total crease length (approx):  {total_crease_length:.0f} m")
print(f"  Equator seam:                  {equator_circumference:.1f} m")

# MASS BREAKDOWN
print("\n" + "="*80)
print("  DETAILED MASS BUDGET")
print("="*80)

# COMPONENT 1: MYLAR SHEETS
mylar_thickness_um = 10  # micrometers
mylar_density = 1.4  # g/cm³ for PET
mylar_weight_per_m2 = (mylar_thickness_um * 1e-6 * 100**2 * mylar_density) / 1000  # kg/m²
mylar_weight_per_m2_g = mylar_weight_per_m2 * 1000  # g/m²

# For metallized version, add thin aluminum layer (~30-50 nm)
aluminum_layer_weight = 0.5  # g/m² (very thin)
mylar_total_weight_per_m2_g = mylar_weight_per_m2_g + aluminum_layer_weight

mylar_total_mass = A_balloon * mylar_total_weight_per_m2_g / 1000  # kg

print(f"\n1. MYLAR ENVELOPE (Primary gas barrier)")
print(f"  ────────────────────────────────────────────────────────────────────────")
print(f"  Material:          Metallized BoPET (Mylar)")
print(f"  Thickness:         {mylar_thickness_um} μm PET + 40 nm Al coating")
print(f"  Weight:            {mylar_total_weight_per_m2_g:.1f} g/m²")
print(f"  Surface area:      {A_balloon:.1f} m²")
print(f"  Total mass:        {mylar_total_mass:.3f} kg ({mylar_total_mass/balloon_material_budget*100:.1f}% of budget)")

# COMPONENT 2: SEAM TAPE (Heat-seal tape or adhesive)
# Options:
#   A) Heat-seal overlap (no tape, just doubled Mylar)
#   B) Adhesive tape (polyester tape with acrylic adhesive)

# For heat-seal: Each seam requires ~5mm overlap on each side = 10mm total width
# For bloom pattern, internal seams (joining facets) use heat-seal overlap
# External seam (hemisphere junction) uses reinforced tape

# Internal facet seams (heat-sealed with 10mm overlap)
seam_width_internal = 0.010  # 10 mm overlap
seam_area_internal = total_crease_length * seam_width_internal
seam_mass_internal = seam_area_internal * mylar_total_weight_per_m2_g / 1000  # kg (doubled Mylar)

# Equator seam (reinforced with Mylar tape, 20mm width)
seam_width_equator = 0.020  # 20 mm
seam_area_equator = equator_circumference * seam_width_equator
# Equator uses double-sided reinforcement: 2 layers of tape
seam_mass_equator = seam_area_equator * mylar_total_weight_per_m2_g / 1000 * 2  # kg

total_seam_mass = seam_mass_internal + seam_mass_equator

print(f"\n2. SEAMS & JOINING")
print(f"  ────────────────────────────────────────────────────────────────────────")
print(f"  A) Internal facet seams (heat-seal overlap):")
print(f"     Crease length:     {total_crease_length:.0f} m")
print(f"     Overlap width:     {seam_width_internal*1000:.0f} mm per side")
print(f"     Overlap area:      {seam_area_internal:.2f} m²")
print(f"     Mass:              {seam_mass_internal:.3f} kg")
print(f"  ")
print(f"  B) Equator seam (hemisphere junction, reinforced):")
print(f"     Circumference:     {equator_circumference:.2f} m")
print(f"     Tape width:        {seam_width_equator*1000:.0f} mm (double-sided)")
print(f"     Tape area:         {seam_area_equator:.2f} m²")
print(f"     Mass:              {seam_mass_equator:.3f} kg")
print(f"  ")
print(f"  TOTAL SEAM MASS:     {total_seam_mass:.3f} kg ({total_seam_mass/balloon_material_budget*100:.1f}% of budget)")

# COMPONENT 3: CUBEN FIBER REINFORCEMENT (selective)
# Only at high-stress locations:
#   - Central polygon edges (2 polygons)
#   - Equator seam (already covered by seam tape, but add structural tape)
#   - Deployment constraint attachment points (12 locations)

central_polygon_perimeter = m * s_scale  # Approximate
cuben_strip_width = 0.005  # 5 mm
cuben_weight_per_m2 = 0.035  # 35 g/m² for DCF

# Cuben reinforcement locations:
cuben_length_central = 2 * central_polygon_perimeter  # Both hemispheres
cuben_length_equator = equator_circumference  # Structural reinforcement at junction
cuben_length_attachments = 12 * 0.5  # 12 attachment points, 0.5m each
total_cuben_length = cuben_length_central + cuben_length_equator + cuben_length_attachments

cuben_area = total_cuben_length * cuben_strip_width
cuben_mass = cuben_area * cuben_weight_per_m2

print(f"\n3. CUBEN FIBER REINFORCEMENT (High-stress areas only)")
print(f"  ────────────────────────────────────────────────────────────────────────")
print(f"  Strip width:       {cuben_strip_width*1000:.0f} mm")
print(f"  Weight:            {cuben_weight_per_m2*1000:.0f} g/m²")
print(f"  ")
print(f"  Locations:")
print(f"    Central polygons:   {cuben_length_central:.1f} m")
print(f"    Equator junction:   {cuben_length_equator:.1f} m")
print(f"    Attachment points:  {cuben_length_attachments:.1f} m")
print(f"  ")
print(f"  Total length:      {total_cuben_length:.1f} m")
print(f"  Total area:        {cuben_area:.3f} m²")
print(f"  Total mass:        {cuben_mass:.3f} kg ({cuben_mass/balloon_material_budget*100:.1f}% of budget)")

# COMPONENT 4: FITTINGS & HARDWARE
# - Fill valve (helium inlet with self-sealing valve)
# - Payload attachment ring
# - Deployment mechanism (dissolvable cord + triggers)
# - GPS tracker mount

valve_mass = 0.030  # kg (30g for small lightweight valve)
attachment_ring_mass = 0.050  # kg (50g for Kevlar cord loop)
deployment_mechanism_mass = 0.020  # kg (20g for dissolvable cord + small heat element)
tracker_mount_mass = 0.010  # kg (10g for mount bracket)

hardware_total_mass = valve_mass + attachment_ring_mass + deployment_mechanism_mass + tracker_mount_mass

print(f"\n4. HARDWARE & FITTINGS")
print(f"  ────────────────────────────────────────────────────────────────────────")
print(f"  Fill valve:            {valve_mass*1000:.0f} g")
print(f"  Payload attachment:    {attachment_ring_mass*1000:.0f} g")
print(f"  Deployment mechanism:  {deployment_mechanism_mass*1000:.0f} g")
print(f"  Tracker mount:         {tracker_mount_mass*1000:.0f} g")
print(f"  ")
print(f"  TOTAL HARDWARE:        {hardware_total_mass:.3f} kg ({hardware_total_mass/balloon_material_budget*100:.1f}% of budget)")

# TOTAL MASS
total_balloon_mass = mylar_total_mass + total_seam_mass + cuben_mass + hardware_total_mass

print(f"\n" + "="*80)
print(f"  TOTAL BALLOON MASS BUDGET")
print(f"="*80)

print(f"\n  Component                          Mass (kg)    % of Budget")
print(f"  ────────────────────────────────────────────────────────────────────────")
print(f"  Mylar envelope                     {mylar_total_mass:8.3f}     {mylar_total_mass/balloon_material_budget*100:5.1f}%")
print(f"  Seams & joining tape               {total_seam_mass:8.3f}     {total_seam_mass/balloon_material_budget*100:5.1f}%")
print(f"  Cuben Fiber reinforcement          {cuben_mass:8.3f}     {cuben_mass/balloon_material_budget*100:5.1f}%")
print(f"  Hardware & fittings                {hardware_total_mass:8.3f}     {hardware_total_mass/balloon_material_budget*100:5.1f}%")
print(f"  ────────────────────────────────────────────────────────────────────────")
print(f"  TOTAL                              {total_balloon_mass:8.3f}     {total_balloon_mass/balloon_material_budget*100:5.1f}%")
print(f"  ")
print(f"  BUDGET                             {balloon_material_budget:8.3f}    100.0%")
print(f"  MARGIN                             {balloon_material_budget - total_balloon_mass:8.3f}     {(balloon_material_budget - total_balloon_mass)/balloon_material_budget*100:5.1f}%")

# ASSESSMENT
print(f"\n" + "="*80)
print(f"  BUDGET ASSESSMENT")
print(f"="*80)

if total_balloon_mass <= balloon_material_budget:
    margin_pct = (balloon_material_budget - total_balloon_mass) / balloon_material_budget * 100
    if margin_pct > 10:
        status = "✓ EXCELLENT - Good margin for safety"
    elif margin_pct > 0:
        status = "✓ ACCEPTABLE - Tight but feasible"
    else:
        status = "⚠ CRITICAL - No margin for error"
    print(f"\n  Status: {status}")
    print(f"  Margin: {balloon_material_budget - total_balloon_mass:.3f} kg ({margin_pct:.1f}%)")
else:
    overmass = total_balloon_mass - balloon_material_budget
    print(f"\n  Status: ✗ OVER BUDGET")
    print(f"  Overmass: {overmass:.3f} kg ({overmass/balloon_material_budget*100:.1f}% over)")
    print(f"\n  REQUIRED OPTIMIZATIONS:")

# OPTIMIZATION STRATEGIES if over budget
if total_balloon_mass > balloon_material_budget:
    print(f"  1. Reduce Mylar thickness to 8 μm (saves ~{(mylar_total_mass * 0.2):.3f} kg)")
    print(f"  2. Simplify pattern to RH-Y-8.4 (fewer facets = less seam tape)")
    print(f"  3. Use lighter hardware (titanium valve, carbon fiber fittings)")
    print(f"  4. Minimize Cuben reinforcement (only critical points)")
else:
    print(f"\n  RECOMMENDATIONS:")
    print(f"  1. Use margin for additional Cuben reinforcement at stress points")
    print(f"  2. Add redundant sealing at equator junction")
    print(f"  3. Include emergency venting system (~20-50g)")
    print(f"  4. Buffer for manufacturing tolerances and waste")

# ALTERNATIVE SCENARIOS
print(f"\n" + "="*80)
print(f"  ALTERNATIVE MATERIAL SCENARIOS")
print(f"="*80)

scenarios = [
    ("Ultra-thin Mylar (7 μm)", 7, "Lighter but more fragile"),
    ("Current design (10 μm)", 10, "Good balance"),
    ("Thicker Mylar (12 μm)", 12, "More durable, heavier"),
]

print(f"\n  Mylar Thickness    Envelope Mass    Total Mass    Margin      Status")
print(f"  ────────────────────────────────────────────────────────────────────────")

for name, thickness, notes in scenarios:
    mylar_weight = (thickness * 1e-6 * 100**2 * mylar_density + aluminum_layer_weight/1000) * 1000  # g/m²
    envelope_mass = A_balloon * mylar_weight / 1000
    seam_mass_alt = (seam_area_internal + seam_area_equator * 2) * mylar_weight / 1000
    total_alt = envelope_mass + seam_mass_alt + cuben_mass + hardware_total_mass
    margin = balloon_material_budget - total_alt
    margin_pct = margin / balloon_material_budget * 100

    status = "✓ OK" if margin > 0 else "✗ OVER"

    print(f"  {name:18} {envelope_mass:8.3f} kg   {total_alt:8.3f} kg   {margin:+7.3f} kg  {status}")

# SENSITIVITY ANALYSIS
print(f"\n" + "="*80)
print(f"  SENSITIVITY ANALYSIS - What if we use thinner Mylar?")
print(f"="*80)

print(f"\n  The seam tape mass scales with Mylar thickness!")
print(f"  Current design: 10 μm Mylar")
print(f"  Seam mass: {total_seam_mass:.3f} kg ({total_seam_mass/total_balloon_mass*100:.1f}% of total)")
print(f"\n  Seams are a MAJOR mass component - they scale with base material weight.")
print(f"  Going thinner helps BOTH envelope AND seams!")

print(f"\n" + "="*80)
print(f"  FINAL RECOMMENDATION")
print(f"="*80)

if total_balloon_mass <= balloon_material_budget * 0.9:
    print(f"\n  ✓ Current design (10 μm Mylar) is FEASIBLE with good margin.")
    print(f"  ")
    print(f"  Use the {(balloon_material_budget - total_balloon_mass)*1000:.0f}g margin for:")
    print(f"    • Additional reinforcement at high-stress points")
    print(f"    • Manufacturing waste allowance (~10%)")
    print(f"    • Emergency systems (pressure relief valve, etc.)")
elif total_balloon_mass <= balloon_material_budget:
    print(f"\n  ⚠ Current design is TIGHT but feasible.")
    print(f"  Recommend precision manufacturing and testing before scaling.")
else:
    print(f"\n  ✗ Need to reduce mass by {(total_balloon_mass - balloon_material_budget)*1000:.0f}g")
    print(f"  Switch to 7-8 μm Mylar or simplify pattern complexity.")

print(f"\n" + "="*80)
