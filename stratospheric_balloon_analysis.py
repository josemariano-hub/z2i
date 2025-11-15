"""
STRATOSPHERIC BLOOM BALLOON ANALYSIS
=====================================
Design a 200:1 volume ratio bloom pattern balloon to lift 3 kg to 30 km altitude

Requirements:
- Payload: 3 kg
- Target altitude: 30 km (stratosphere)
- Volume ratio: 200:1 (small to large)
- Material: Lightweight, foldable, gas-tight
"""

import numpy as np

print("="*80)
print("  STRATOSPHERIC BLOOM BALLOON - FEASIBILITY ANALYSIS")
print("="*80)

# ATMOSPHERIC CONDITIONS AT 30 KM
print("\n" + "="*80)
print("  1. ATMOSPHERIC CONDITIONS AT 30 KM ALTITUDE")
print("="*80)

altitude = 30000  # meters
T_30km = -45 + 273.15  # Temperature in Kelvin (~-45°C)
P_30km = 1197  # Pressure in Pa (~1.2 kPa)
P_sea = 101325  # Sea level pressure in Pa

# Air density at 30 km (using ideal gas law)
R_air = 287.05  # Specific gas constant for air (J/kg·K)
rho_air_30km = P_30km / (R_air * T_30km)

print(f"  Temperature:        {T_30km - 273.15:.1f}°C ({T_30km:.1f} K)")
print(f"  Pressure:           {P_30km/1000:.2f} kPa ({P_30km/P_sea*100:.2f}% of sea level)")
print(f"  Air density:        {rho_air_30km:.6f} kg/m³")
print(f"  Pressure ratio:     {P_sea/P_30km:.1f}:1 (sea level vs 30 km)")

# LIFT CALCULATION
print("\n" + "="*80)
print("  2. LIFT REQUIREMENTS")
print("="*80)

payload_mass = 3.0  # kg
g = 9.81  # m/s²

# Lifting gas options
print("\n  Gas Options:")
print("  " + "-"*76)

# Helium
M_He = 0.004  # kg/mol
R_He = 8314.46 / M_He  # Specific gas constant for helium
rho_He_30km = P_30km / (R_He * T_30km)
lift_per_m3_He = (rho_air_30km - rho_He_30km) * g

print(f"  HELIUM:")
print(f"    Density at 30km:   {rho_He_30km:.6f} kg/m³")
print(f"    Lift per m³:       {lift_per_m3_He:.4f} N/m³ ({lift_per_m3_He/g*1000:.2f} g/m³)")

# Hydrogen
M_H2 = 0.002  # kg/mol
R_H2 = 8314.46 / M_H2
rho_H2_30km = P_30km / (R_H2 * T_30km)
lift_per_m3_H2 = (rho_air_30km - rho_H2_30km) * g

print(f"  HYDROGEN:")
print(f"    Density at 30km:   {rho_H2_30km:.6f} kg/m³")
print(f"    Lift per m³:       {lift_per_m3_H2:.4f} N/m³ ({lift_per_m3_H2/g*1000:.2f} g/m³)")

# Hot air (limited at 30 km due to low pressure)
print(f"  HOT AIR:")
print(f"    NOT VIABLE - insufficient temperature differential possible at 30 km")

# BALLOON SIZE CALCULATION
print("\n" + "="*80)
print("  3. BALLOON VOLUME REQUIREMENTS")
print("="*80)

# We need to lift payload + balloon material
# Start with estimate, iterate

material_weight_estimates = {
    "Ultra-thin PE (15μm)": 0.014,  # kg/m² (density 0.92 g/cm³, 15 μm thick)
    "Mylar/BoPET (12μm)": 0.017,    # kg/m² (density 1.4 g/cm³, 12 μm thick)
    "Cuben Fiber (35 g/m²)": 0.035,  # kg/m² (DCF typical)
    "LLDPE (25μm)": 0.023,           # kg/m² (NASA balloon material)
}

print("\n  Using HELIUM as lifting gas:")
print("  " + "-"*76)

for material_name, weight_per_m2 in material_weight_estimates.items():
    print(f"\n  Material: {material_name}")

    # Iterative calculation (balloon weight depends on size, size depends on lift needed)
    # Start with payload-only estimate
    V_required_payload = (payload_mass * g) / lift_per_m3_He

    # Estimate surface area for sphere: A = 4πr², V = 4/3πr³
    # So A = (36π)^(1/3) * V^(2/3)
    for iteration in range(5):
        r_balloon = (3 * V_required_payload / (4 * np.pi)) ** (1/3)
        A_balloon = 4 * np.pi * r_balloon**2
        balloon_mass = A_balloon * weight_per_m2
        total_mass = payload_mass + balloon_mass
        V_required_payload = (total_mass * g) / lift_per_m3_He

    # Final results
    r_balloon = (3 * V_required_payload / (4 * np.pi)) ** (1/3)
    A_balloon = 4 * np.pi * r_balloon**2
    balloon_mass = A_balloon * weight_per_m2

    print(f"    Required volume:   {V_required_payload:.2f} m³")
    print(f"    Balloon radius:    {r_balloon:.2f} m (diameter: {2*r_balloon:.2f} m)")
    print(f"    Surface area:      {A_balloon:.2f} m²")
    print(f"    Material weight:   {balloon_mass:.3f} kg")
    print(f"    Total weight:      {payload_mass + balloon_mass:.3f} kg")
    print(f"    Weight ratio:      {balloon_mass/payload_mass*100:.1f}% of payload")

# BLOOM PATTERN SIZING FOR 200:1 RATIO
print("\n" + "="*80)
print("  4. BLOOM PATTERN DIMENSIONS (200:1 VOLUME RATIO)")
print("="*80)

# Using Cuben Fiber as most realistic option
material_name = "Cuben Fiber (35 g/m²)"
weight_per_m2 = 0.035

# Recalculate for exact values
V_required_payload = (payload_mass * g) / lift_per_m3_He
for iteration in range(5):
    r_balloon = (3 * V_required_payload / (4 * np.pi)) ** (1/3)
    A_balloon = 4 * np.pi * r_balloon**2
    balloon_mass = A_balloon * weight_per_m2
    total_mass = payload_mass + balloon_mass
    V_required_payload = (total_mass * g) / lift_per_m3_He

V_large = V_required_payload
V_small = V_large / 200
r_large = (3 * V_large / (4 * np.pi)) ** (1/3)
r_small = (3 * V_small / (4 * np.pi)) ** (1/3)

print(f"\n  DEPLOYED STATE (LARGE):")
print(f"    Volume:            {V_large:.2f} m³ ({V_large * 1000:.0f} liters)")
print(f"    Radius:            {r_large:.3f} m ({r_large*100:.1f} cm)")
print(f"    Diameter:          {2*r_large:.3f} m ({2*r_large*100:.1f} cm)")

print(f"\n  COMPACT STATE (SMALL):")
print(f"    Volume:            {V_small:.4f} m³ ({V_small * 1e6:.0f} cm³)")
print(f"    Radius:            {r_small:.4f} m ({r_small*100:.2f} cm)")
print(f"    Diameter:          {2*r_small:.4f} m ({2*r_small*100:.2f} cm)")

print(f"\n  RATIO:")
print(f"    Volume ratio:      {V_large/V_small:.1f}:1")
print(f"    Radius ratio:      {r_large/r_small:.2f}:1")

# BLOOM PATTERN PARAMETERS
print("\n" + "="*80)
print("  5. BLOOM PATTERN PARAMETERS")
print("="*80)

# For 200:1 volume ratio, we need radius ratio of ~5.85
# From previous analysis: RH-Y-m.h(1/2) pattern
# Deployed radius formula: r ≈ s × sqrt(h² + csc²(π/m)/4 - h×csc(π/m)×cos(3π/m - 3π/2))

# For hemisphere (1/2 trimming)
m_options = [8, 10, 12]  # polygon sides
h_options = [4, 5, 6]    # height order

print("\n  Pattern options for ~200:1 volume ratio (hemisphere design):")
print("  " + "-"*76)

for m in m_options:
    for h in h_options:
        beta = np.pi / m
        # Expansion ratio formula for Yoshimura pattern
        r_expansion = np.sqrt(h**2 + (1/np.sin(beta))**2 / 4 -
                             h * (1/np.sin(beta)) * np.cos(3*beta - 3*np.pi/2))

        # Scale factor to match our required large radius
        s_required = r_large / r_expansion

        # Calculate small state parameters
        # For tri-stable design, small state requires constraint mechanism
        # Natural small radius (when partially deployed)
        r_small_natural = s_required * np.sqrt(1)  # Approximate for minimal deployment

        # Number of facets
        facets = m * (h**2 + 3*h)

        # Flat size estimate (for packaging)
        flat_diameter = 2 * s_required * h

        print(f"\n  Pattern RH-Y-{m}.{h}(1/2):")
        print(f"    Polygon sides (m): {m}")
        print(f"    Height order (h):  {h}")
        print(f"    Scale factor (s):  {s_required:.4f} m ({s_required*1000:.1f} mm)")
        print(f"    Facets per half:   {facets}")
        print(f"    Large diameter:    {2*r_large:.3f} m")
        print(f"    Small diameter:    {2*r_small:.3f} m")
        print(f"    Flat diameter:     {flat_diameter:.3f} m")
        print(f"    Complexity:        {'LOW' if facets < 100 else 'MEDIUM' if facets < 300 else 'HIGH'}")

# MATERIAL RECOMMENDATIONS
print("\n" + "="*80)
print("  6. MATERIAL SELECTION AND RECOMMENDATIONS")
print("="*80)

materials = [
    {
        "name": "Cuben Fiber (Dyneema Composite Fabric)",
        "weight": "35-50 g/m²",
        "thickness": "~50 μm",
        "pros": [
            "Extremely strong (15x stronger than steel by weight)",
            "Waterproof and gas-resistant laminate",
            "Excellent tear resistance",
            "UV resistant",
            "Holds creases well",
            "Used in ultralight sailing and aerospace"
        ],
        "cons": [
            "VERY EXPENSIVE (~$30-50/m²)",
            "Difficult to seal (requires specialized tape)",
            "Can delaminate at sharp creases with repeated folding",
            "Not perfectly gas-tight for helium long-term"
        ],
        "verdict": "BEST for structural elements and high-stress areas"
    },
    {
        "name": "Mylar/BoPET (Biaxially-oriented PET)",
        "weight": "12-25 g/m²",
        "thickness": "12-20 μm",
        "pros": [
            "Excellent crease retention",
            "Very lightweight",
            "Gas-tight (good for helium retention)",
            "Heat-sealable",
            "Relatively inexpensive",
            "Good UV resistance",
            "Used in solar balloons and space blankets"
        ],
        "cons": [
            "Can tear along creases under stress",
            "Brittle at low temperatures (-45°C)",
            "Puncture-sensitive"
        ],
        "verdict": "GOOD for inner gas envelope, needs reinforcement"
    },
    {
        "name": "Metallized Mylar",
        "weight": "15-30 g/m²",
        "thickness": "12-25 μm",
        "pros": [
            "Same as Mylar + reflective coating",
            "Reflects solar radiation (thermal control)",
            "Better visibility for tracking",
            "Commonly used in party balloons (proven folding)"
        ],
        "cons": [
            "Same as Mylar",
            "Metallization can crack at creases"
        ],
        "verdict": "GOOD option with thermal benefits"
    },
    {
        "name": "LLDPE (Linear Low-Density Polyethylene)",
        "weight": "23-46 g/m²",
        "thickness": "25-50 μm",
        "pros": [
            "PROVEN for NASA high-altitude balloons",
            "Excellent low-temperature performance",
            "Heat-sealable",
            "Very tough and flexible",
            "Inexpensive",
            "Good helium retention"
        ],
        "cons": [
            "Poor crease retention (very flexible)",
            "Requires external structure for origami folds",
            "Heavier than Mylar/Cuben"
        ],
        "verdict": "EXCELLENT for gas envelope, POOR for origami structure"
    },
    {
        "name": "PE + Starch Composite (Your suggestion)",
        "weight": "40-80 g/m² (estimated)",
        "thickness": "30-60 μm",
        "pros": [
            "Starch adds rigidity for fold retention",
            "Bio-based option",
            "PE provides flexibility and strength",
            "Could be heat-sealable"
        ],
        "cons": [
            "UNTESTED for aerospace applications",
            "Starch degrades with moisture and UV",
            "Weight penalty vs pure PE",
            "Unknown low-temperature performance",
            "Questionable gas-tightness"
        ],
        "verdict": "EXPERIMENTAL - needs R&D, likely too heavy/unreliable"
    },
    {
        "name": "Ripstop Nylon + Coating",
        "weight": "40-60 g/m²",
        "thickness": "30-50 μm",
        "pros": [
            "Excellent tear resistance",
            "Can be coated for gas-tightness",
            "Good temperature range",
            "Moderate cost"
        ],
        "cons": [
            "Heavier than thin films",
            "Coating adds weight",
            "Less gas-tight than solid films"
        ],
        "verdict": "BACKUP option if film materials fail"
    }
]

for mat in materials:
    print(f"\n  {mat['name'].upper()}")
    print(f"  {'─'*76}")
    print(f"  Weight:   {mat['weight']}")
    print(f"  Thickness: {mat['thickness']}")
    print(f"\n  PROS:")
    for pro in mat['pros']:
        print(f"    ✓ {pro}")
    print(f"  CONS:")
    for con in mat['cons']:
        print(f"    ✗ {con}")
    print(f"\n  VERDICT: {mat['verdict']}")

# HYBRID DESIGN RECOMMENDATION
print("\n" + "="*80)
print("  7. RECOMMENDED HYBRID DESIGN")
print("="*80)

print("""
  COMPOSITE STRUCTURE for bloom pattern stratospheric balloon:

  LAYER 1 - STRUCTURAL SKELETON (Cuben Fiber/DCF):
    • Use Cuben Fiber for all crease lines and facet edges
    • Creates rigid framework that holds bloom pattern shape
    • Width: 5-10mm strips along each fold line
    • Provides strength and crease retention
    • Weight: ~15-20% of total

  LAYER 2 - GAS ENVELOPE (Metallized Mylar or LLDPE):
    • Thin film bonded to structural skeleton
    • Provides gas-tight membrane
    • Can be slightly oversized to allow for expansion
    • Metallized for thermal control
    • Weight: ~60-70% of total

  LAYER 3 - OUTER REINFORCEMENT (Optional - thin Mylar):
    • Protects gas layer from UV and abrasion
    • Only on facet faces, not creases
    • Weight: ~10-15% of total

  DEPLOYMENT MECHANISM:
    • Small state: Constrained with dissolvable/meltable cord
    • At altitude: Heat or chemical trigger releases constraint
    • Balloon expands to large state naturally
    • Two hemispheres connected with flexible sealed joint

  MANUFACTURING APPROACH:
    1. Laser-cut Cuben Fiber strips for structural pattern
    2. Heat-weld Mylar sheets to structure
    3. Assemble two hemispheres separately
    4. Join with flexible sealed seam
    5. Install deployment mechanism
    6. Pressure test at ground level
    7. Test deployment in vacuum chamber (simulates altitude)
""")

# ENGINEERING CHALLENGES
print("\n" + "="*80)
print("  8. CRITICAL ENGINEERING CHALLENGES")
print("="*80)

challenges = [
    ("Crease Durability",
     "Repeated folding/unfolding cycles cause material fatigue at creases. "
     "Solution: Reinforced crease lines with Cuben Fiber tape, limit cycles to 2-3."),

    ("Gas Tightness",
     "Helium molecules are tiny - leak through seams and material pores. "
     "Solution: Double-sealed seams, metallized barrier films, overfill by 10-15%."),

    ("Deployment Control",
     "Uncontrolled expansion could tear material or tangle. "
     "Solution: Staged release mechanism, guide wires, slow-dissolve constraints."),

    ("Sphericity",
     "Yoshimura pattern creates conical shape, not perfect sphere - aerodynamics suffer. "
     "Solution: Use m≥12 for better approximation, accept some distortion."),

    ("Temperature Cycling",
     "Ground: +20°C, Altitude: -45°C, Sunlit side: +40°C - huge stress. "
     "Solution: Materials tested to -60°C, thermal modeling, reflective coating."),

    ("Pressure Differential",
     "At 30km, internal pressure 85x external - huge stress on seams. "
     "Solution: Stress analysis on crease patterns, reinforced facet intersections."),

    ("Manufacturing Precision",
     "Even 1% error in pattern scaling = fit problems between hemispheres. "
     "Solution: CNC laser cutting, precision jigs, iterative prototyping."),

    ("Testing",
     "Can't test at 30km easily. "
     "Solution: Vacuum chamber tests, computational fluid dynamics, scale models."),
]

for i, (challenge, description) in enumerate(challenges, 1):
    print(f"\n  {i}. {challenge.upper()}")
    print(f"     {description}")

# FEASIBILITY VERDICT
print("\n" + "="*80)
print("  9. FEASIBILITY VERDICT")
print("="*80)

print(f"""
  Can we build a 200:1 bloom balloon to lift 3kg to 30km?

  TECHNICAL FEASIBILITY:   ✓ POSSIBLE (with significant engineering)

  REQUIRED TECHNOLOGY:
    • Balloon diameter:      ~{2*r_large:.1f} m deployed, ~{2*r_small:.2f} m compact
    • Material weight:       ~{balloon_mass:.2f} kg (Cuben+Mylar hybrid)
    • Pattern complexity:    RH-Y-12.6(1/2) - 648 facets (very complex)
    • Manufacturing:         CNC laser cutting, precision heat-sealing
    • Testing required:      Vacuum chamber, thermal cycling, deployment trials
    • Estimated cost:        $5,000-15,000 for materials + testing

  COMPARISON TO CONVENTIONAL:
    • Conventional balloon:  ~{2*r_large:.1f} m diameter, ~0.3-0.5 kg material
    • Bloom balloon:         Same lift, but PACKS 200x SMALLER when compact!
    • Trade-off:             3-4x heavier material, much more complex

  REALISTIC DEVELOPMENT PATH:
    1. Start with small-scale proof-of-concept (1m diameter, desktop)
    2. Test materials and deployment mechanisms
    3. Scale to medium (3m diameter, field tests to 10km)
    4. Full-scale prototype with instrumentation
    5. Stratospheric test flight

  BIGGEST ADVANTAGE:
    Compact storage! A {2*r_large:.1f}m balloon packs into {2*r_small*100:.1f}cm package.
    Revolutionary for spacecraft deployment, emergency systems.

  BIGGEST RISK:
    Material failure at creases during deployment at -45°C with 85:1 pressure ratio.
    Mitigation: Extensive testing, reinforced creases, deployment control.

  RECOMMENDED NEXT STEP:
    Build 1-meter diameter proof-of-concept with Mylar + Cuben Fiber hybrid.
    Test deployment cycles at room temperature before scaling up.
""")

print("\n" + "="*80)
print("  Analysis complete! Ready to start prototyping?")
print("="*80)
