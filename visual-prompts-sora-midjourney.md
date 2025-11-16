# Visual Content Prompts for V4 Helistat
## SORA (Video) and Midjourney (Image) Generation - Detailed Technical Specifications

This document provides geometrically precise prompts for generating marketing materials, technical visualizations, and demonstration animations for the V4 Helistat concept.

**CRITICAL:** All prompts include exact dimensions, proportions, materials, and finishes to enable accurate visual reconstruction.

---

## ⚠️ CRITICAL CONFIGURATION CONCEPT ⚠️

**THIS IS A QUADCOPTER DRONE WITH ROTORS INSIDE VERTICAL DONUTS - NOT WHEELS ON A VEHICLE**

Think: **DJI Mavic drone, but each propeller is surrounded by a giant standing donut filled with helium**

### Configuration Overview:
```
         TOP VIEW (Looking Down):

    [Toroid 1]     ←26.16m→    [Toroid 2]
        ⊕                          ⊕
        ↑                          ↑
        |                          |
      Rotor 1                   Rotor 2
        |                          |
        |         PAYLOAD          |
        |           POD            |
        |                          |
      Rotor 3                   Rotor 4
        |                          |
        ↓                          ↓
        ⊕                          ⊕
    [Toroid 3]                 [Toroid 4]

    ⊕ = Rotor (vertical shaft, horizontal spinning blades)
    [Toroid] = Donut standing UPRIGHT (vertical orientation)
```

**Key Points:**
1. **Quadcopter Configuration:** Four rotors in square pattern like any DJI drone
2. **Vertical Rotors:** Rotor shafts point UP (vertical), blades spin horizontally
3. **Toroids Stand Upright:** Donuts are VERTICAL (standing on edge), NOT horizontal like car tires
4. **Rotor Through Center:** Each rotor shaft passes UP through the donut hole of its toroid
5. **View from Side:** You see the donut profile (circular cross-section), rotor spinning inside hole
6. **View from Above:** You see four donuts in square pattern, each with rotor blades visible at center

---

## GEOMETRIC SPECIFICATIONS BY SIZE CLASS

### 20-Ton Heavy Cargo Helistat (Primary Reference)
- **Overall footprint:** 35.5m × 35.5m (square configuration)
- **Overall height:** 9.3m
- **Toroidal envelopes (4 units):**
  - Major radius R: 8.875m (center of toroid to center of tube)
  - Minor radius r: 4.671m (tube cross-section radius)
  - Toroid length: 55.8m (circumference of centerline)
  - Surface area per toroid: 1,637 m²
  - Material: Urethane-coated ripstop nylon, 100 g/m²
  - Color: Metallic silver #C0C0C0 with subtle grid pattern from seams
  - Finish: Semi-gloss, slight translucency showing internal structure
- **Rotors (4 units):**
  - Diameter: 7.14m each
  - Blade count: 4 blades per rotor
  - Blade material: Carbon fiber, matte black #1C1C1C
  - Hub diameter: 0.7m, anodized aluminum #8C8C8C
  - Each rotor passes vertically through center hole of its toroid
- **Structural frame:**
  - Carbon fiber tubular trusses connecting the four toroids
  - Tube diameter: 150mm
  - Color: Matte graphite #2C2C2C
  - Forms square grid pattern between toroids
- **Central payload pod:**
  - Dimensions: 4.0m × 2.5m × 2.0m (L×W×H)
  - Material: Aluminum honeycomb composite
  - Color: White #F5F5F5 with registration markings
  - Suspended 2m below structural frame center
  - Landing gear: 4 telescoping legs, 1.5m extended length
- **Proportions:** Rotors occupy 80% of toroid hole diameter, leaving visible gap

### 1-Ton Medium Cargo Helistat
- **Overall footprint:** 13.1m × 13.1m
- **Overall height:** 3.4m
- **Toroid dimensions:** R=3.27m, r=1.72m
- **Rotor diameter:** 1.60m (4 rotors)
- **Material:** Nylon, same finish as 20-ton
- **Payload pod:** 1.5m × 1.0m × 0.8m

### 100kg Medium UAV Helistat
- **Overall footprint:** 6.1m × 6.1m
- **Overall height:** 1.6m
- **Toroid dimensions:** R=1.52m, r=0.80m
- **Rotor diameter:** 0.50m (4 rotors)
- **Material:** Nylon, same finish
- **Payload pod:** 0.6m × 0.4m × 0.3m

### 10kg Small UAV Helistat
- **Overall footprint:** 2.8m × 2.8m
- **Overall height:** 0.7m
- **Toroid dimensions:** R=0.70m, r=0.37m
- **Rotor diameter:** 0.16m (4 rotors)
- **Material:** Dyneema fabric, 35 g/m²
- **Color:** High-visibility silver with hexagonal ripstop pattern visible
- **Finish:** Matte metallic, technical fabric appearance
- **Payload pod:** 0.25m × 0.15m × 0.10m

### 1kg Micro Demonstrator
- **Overall footprint:** 1.3m × 1.3m
- **Overall height:** 0.3m
- **Toroid dimensions:** R=0.33m, r=0.17m
- **Rotor diameter:** 0.05m (4 rotors)
- **Material:** Dyneema, same finish as 10kg
- **Payload pod:** Minimal 0.10m cube

---

## SORA VIDEO PROMPTS (OpenAI Video Generation)

### 1. Hero Introduction Video (30 seconds)

**Prompt:**
```
Cinematic aerial shot revealing a 20-ton V4 Helistat in flight at golden hour - THIS IS A QUADCOPTER DRONE CONFIGURATION with four rotors surrounded by giant vertical donut-shaped helium envelopes (like DJI drone but each propeller inside a standing donut). Camera begins 100m distant, orbits clockwise showing complete configuration. CONFIGURATION: Four vertical rotor shafts arranged in square pattern (35.5m × 35.5m spacing, quadcopter X layout), each rotor shaft passes UPWARD through center hole of a toroidal envelope standing UPRIGHT (vertical orientation, NOT horizontal like wheels). TOROIDS: Four identical donut-shaped helium envelopes standing vertical (8.875m major radius, 4.671m minor radius, silver metallic #C0C0C0 urethane-coated ripstop nylon, semi-gloss finish, visible seam grid at 2m intervals). From side view: circular toroid cross-section visible with rotor blades spinning inside center hole. From top view: four donuts in square pattern with rotor blades visible at center of each. ROTORS: Four 7.14m diameter propellers (4-blade carbon fiber, matte black #1C1C1C), rotor shafts vertical pointing upward, blades spin horizontally at 350 RPM generating downward thrust through toroid center holes. STRUCTURE: Matte graphite carbon fiber tubes (150mm diameter, #2C2C2C) connect the four toroids in square grid pattern between the rotors. PAYLOAD: White aluminum pod (4.0m × 2.5m × 2.0m, #F5F5F5) suspended 2m below center of quadcopter frame, four telescoping landing legs (1.5m extended). Vehicle hovers 50m altitude above construction site, 11-ton shipping container suspended 10m below on steel cargo cables. Rotors occupy 80% of toroid hole diameter leaving visible gap. Envelope fabric has slight translucency revealing internal catenary curtains. Camera orbit smooth 360°, dramatic god rays through clouds, golden hour lighting (3500K color temp), ultra-realistic 4K. Text overlay at 25 seconds: "V4 HELISTAT - 11.6 TON PAYLOAD" in clean sans-serif white font. CRITICAL: This looks like a giant quadcopter drone with each propeller surrounded by a standing donut, NOT like wheels on a vehicle.
```

**Usage:** Website hero, investor pitch opening, trade show display

---

### 2. Technical Animation: Flight Operations (45 seconds)

**Prompt:**
```
Technical animation sequence of 1-ton helistat complete mission cycle on white background - QUADCOPTER DRONE CONFIGURATION with vertical rotors inside standing donuts. Dimensions: 13.1m × 13.1m footprint (rotor spacing), 3.4m height. [0:00-0:10] GROUND STATE: Four silver nylon toroids (R=3.27m, r=1.72m each) deflated and folded flat on ground, four vertical rotor shafts (1.60m diameter propellers) collapsed alongside, compact 2.5m × 2.5m × 0.8m storage footprint. [0:10-0:20] INFLATION SEQUENCE: Time-lapse showing helium flowing through fill valves, four toroids expand from flat fabric to full standing donut shape (8 min compressed to 10 sec). Toroids rise to VERTICAL orientation (standing upright like donuts on edge), each forming circular tube. Blue translucent helium gas visible filling interior, pressure gauge overlay "1.05 bar". Rotor shafts extend vertically UPWARD, each shaft threading through center hole of its now-standing toroid. [0:20-0:30] ROTOR SPIN-UP: Four 1.60m propellers (4-blade carbon fiber) spin up 0→400 RPM, blades rotating horizontally inside toroid center holes. Thrust vector arrows show downward airflow through donut holes: 200kg rotor thrust + 800kg buoyancy lift = 1,000kg total. Quadcopter frame (carbon fiber tubes connecting four toroid bases) visible. [0:30-0:35] VERTICAL TAKEOFF: Quadcopter configuration lifts smoothly, altitude gauge 0→50m. View clearly shows four vertical donuts in square pattern with propellers spinning inside each center hole. [0:35-0:40] FORWARD FLIGHT: 65 km/h cruise, airflow streamlines (blue) show laminar flow over toroid outer surfaces, Reynolds Re=2.8×10^6 annotation. Side view clearly shows toroid circular cross-sections (vertical donuts) with rotors inside. [0:40-0:43] PRECISION HOVER: Cargo hook lowers 436kg container from central payload pod. [0:43-0:45] DEFLATION: Reverse sequence, toroids deflate back to flat. Clean technical blueprint aesthetic, white background, floating specs in Helvetica (rotor diameter, toroid volume 764.5 m³, power 43.2 kW), photorealistic with CAD overlay. CRITICAL: Show this as quadcopter drone with vertical rotor shafts passing UP through standing donut holes, NOT horizontal wheel configuration.
```

**Usage:** Technical presentations, training materials, certification documentation

---

### 3. Military ISR Mission (60 seconds)

**Prompt:**
```
Military operation: 100kg tactical helistat in matte olive drab paint (#4B5320) launches at dusk from forward operating base. Exact specifications: 6.1m × 6.1m footprint, 1.6m height, four toroids (R=1.52m, r=0.80m), four 0.50m diameter rotors. Envelopes have infrared-suppression coating, non-reflective matte finish. Gimbaled electro-optical/infrared sensor pod (0.6m × 0.4m × 0.3m cylinder, matte black) replaces standard payload box, suspended on 3-axis gimbal 0.8m below frame. Silent flight at 8m/s across rocky desert valley, altitude 100m AGL. Tactical HUD overlay shows telemetry: "SPD 29 km/h | ALT 100m | PWR 4.3 kW | ENDUR 3:47 remain". Split-screen at 30 seconds: left shows helistat maintaining rock-steady hover despite 15 km/h crosswind, right shows thermal imagery from sensor (white-hot人物 signatures 2.3km distant). On-station loiter for 4 hours (time-lapse compression shows sun setting to sunrise). Rotor noise visualization: sound waves at 68 dB vs helicopter comparison at 95 dB. Return to base at dawn, gentle touchdown on 4-point landing gear. Military tactical overlay graphics, desaturated color grading (#8B7D6B earth tones), call-outs: "4 HR ENDURANCE | SILENT OPS 68 dB | 32 KG PAYLOAD". Gritty realistic military cinematography, volumetric dust particles backlit at sunset/sunrise.
```

**Usage:** Defense customer presentations, SBIR proposals, military trade shows

---

### 4. Construction Site Cargo Delivery (40 seconds)

**Prompt:**
```
Commercial operation in bright daylight: Full-scale 20-ton helistat approaches downtown high-rise construction site. Precise geometry: 35.5m × 35.5m footprint (wider than city street), 9.3m height. Four massive silver nylon toroids (R=8.875m, r=4.671m each, total volume 15,289 m³) catch sunlight with semi-gloss finish showing subtle wrinkle texture and seam lines every 2m. Each toroid has single 7.14m diameter rotor (four black carbon fiber blades) spinning through center at 340 RPM. Matte graphite carbon fiber frame (150mm tubes) visible connecting toroids in square grid. White payload pod (4.0m × 2.5m × 2.0m) at center with "HELISTAT HEAVY LIFT" decals. Steel cargo cables extend 15m below to standard 20-foot shipping container (6.1m × 2.4m × 2.6m, 11 tons gross weight). Camera low-angle from street level looking up as vehicle maneuvers between glass-facade office towers (gaps as narrow as 45m), showing precise scale. Construction workers on 40th floor steel beams (120m altitude) guide container with tag lines. Close-up shows workers NOT wearing hearing protection, talking normally - noise meter overlay shows "72 dB @ 20m" vs "helicopter: 105 dB". Slow-motion shot of container gentle touchdown (vertical velocity <0.2 m/s). Wide aerial shot shows helistat ascending after release, city skyline background. Text overlays: "$1,000/delivery" fades to "vs $7,200 (helicopter)" with 86% savings graphic. Bright saturated commercial cinematography, deep blue sky (#0077BE), warm sunlight on silver envelopes.
```

**Usage:** Commercial customer demonstrations, construction industry pitches

---

### 5. Comparison: Helistat vs Helicopter (Split Screen, 30 seconds)

**Prompt:**
```
Split-screen comparison, vertical divider line at center. LEFT SIDE - "TRADITIONAL: Sikorsky S-64 Skycrane": Aggressive approach with thunderous rotor noise visualized as red concentric pressure waves radiating from 21.95m main rotor. Camera shake simulated, dust and debris clouds at ground level, workers covering ears (hearing protection visible), sound meter shows "103 dB @ 50m" in warning red. Helicopter dimensions visible: 21.4m fuselage length, 7.9m height, 9.1 ton payload on cargo hook. Pilot visible in cockpit with intense concentration. Scene has warm orange-red color grading (#FF6B35) suggesting danger/legacy. RIGHT SIDE - "V4 HELISTAT": Silent approach with green concentric sound waves (much smaller amplitude), camera stable, minimal ground disturbance, workers talking casually without hearing protection, sound meter shows "70 dB @ 50m" in safe green. Helistat dimensions: 35.5m × 35.5m × 9.3m, 11.6 ton payload. Four silver toroids (R=8.875m, r=4.671m) with 7.14m rotors. Autonomous flight (no visible pilot). Scene has cool blue-green color grading (#00C9A7) suggesting modern/safe. Both deliver identical cargo (shipping container) to same construction site. Final 5 seconds: bar chart animation overlays screen center - "OPERATING COST: S-64 $12,000/hr (red bar full height) vs HELISTAT $2,000/hr (green bar 1/6 height)" with "83% SAVINGS" in bold. Clean professional corporate video style, 4K, side-by-side perfect synchronization.
```

**Usage:** Sales presentations, value proposition demonstrations

---

### 6. Scale Demonstration: Micro to Full-Scale (25 seconds)

**Prompt:**
```
Smooth morphing transition sequence showing helistat family scalability. [0:00-0:05] 1kg micro demonstrator (1.3m × 1.3m × 0.3m footprint) hovers indoors at table height, human hand enters frame for scale comparison (hand 180mm vs vehicle 1,300mm footprint). Four tiny Dyneema toroids (R=0.33m, r=0.17m) shimmer silver with visible hexagonal ripstop pattern, four 50mm rotors spinning. [0:05-0:10] Morph transition to 10kg small UAV (2.8m × 2.8m × 0.7m), outdoor grassy field, person standing 2m away for scale (person 1.75m vs vehicle 2.8m). Dyneema envelopes, 0.16m rotors. [0:10-0:15] Morph to 100kg medium UAV (6.1m × 6.1m × 1.6m), warehouse interior, forklift for scale (forklift 3m vs vehicle 6.1m). Nylon envelopes now, 0.50m rotors. [0:15-0:20] Morph to 1-ton cargo helistat (13.1m × 13.1m × 3.4m), outdoor tarmac, delivery van for scale (van 5m vs vehicle 13.1m). 1.60m rotors. [0:20-0:25] Final morph to 20-ton heavy lift (35.5m × 35.5m × 9.3m), landing at construction site, Sikorsky S-64 helicopter parked beside for scale (S-64 21m fuselage vs helistat 35.5m footprint). 7.14m rotors. All transitions maintain consistent quad-toroid configuration and 1.9:1 aspect ratio (R/r). Floating text morphs with vehicle: "1 kg → 10 kg → 100 kg → 1,000 kg → 20,000 kg" and "PAYLOAD: 0.2kg → 2.2kg → 32kg → 436kg → 11,646kg". Clean white background transitions to contextual environments. Smooth CGI morphing with consistent camera angle (30° elevation, 45° azimuth). Specifications overlay in clean sans-serif.
```

**Usage:** Investor presentations showing scalability, technology demonstrations

---

### 7. Emergency Descent: Fail-Safe Demonstration (20 seconds)

**Prompt:**
```
Safety demonstration split timeline using 1-ton helistat (13.1m × 13.1m, 3.4m height). [0:00-0:05] Normal flight: Four 1.60m rotors spinning at 400 RPM, vehicle hovering at 100m altitude with 400kg cargo. Telemetry overlay shows "POWER: 43.2 kW | BUOYANCY: 800kg (80%) | ROTOR THRUST: 200kg (20%) | ALL SYSTEMS NORMAL" in green. [0:05-0:06] Simulated failure: Screen flashes red, rotors instantly stop spinning (frozen blade positions visible), alarm overlay "TOTAL POWER FAILURE". [0:06-0:15] Instead of crash: Vehicle begins controlled descent at 2.5 m/s (9 km/h) sink rate thanks to 800kg net buoyant lift from four helium toroids (R=3.27m, r=1.72m, total 764.5 m³ volume). Split screen comparison: LEFT shows conventional 1,000kg quadcopter drone (no buoyancy) plummeting at 45 m/s with red motion blur and impact crater at ground; RIGHT shows helistat floating down gently like balloon, cargo and vehicle stable, no spinning. Physics annotations: "Buoyancy = 800kg > Empty weight (557kg) = POSITIVE LIFT". [0:15-0:20] Gentle touchdown on landing gear, cargo safe, no damage. Final message: "FAIL-SAFE BUOYANCY DESIGN | 80% BACKUP LIFT | REDUNDANT SAFETY" in bold green. Professional aerospace safety video aesthetic, clear infographic overlay, dramatic but educational tone, 4K quality.
```

**Usage:** Safety certification materials, investor risk mitigation

---

### 8. Silent Operations: Wildlife/Noise Comparison (35 seconds)

**Prompt:**
```
Nature documentary cinematography: Pristine old-growth forest canopy (Pacific Northwest setting, Douglas fir trees 60m tall). [0:00-0:15] 10kg helistat (2.8m × 2.8m × 0.7m) flies 15m above canopy conducting environmental monitoring. Four Dyneema toroids (R=0.70m, r=0.37m) have matte silver finish blending with morning mist. Four 0.16m rotors barely audible. Wildlife on forest floor 25m below continues normal behavior: black-tailed deer grazing (ears relaxed, not alert), varied thrush singing (spectrogram overlay shows bird vocalization at 4-8 kHz dominant), Douglas squirrels foraging. Sound level meter in corner shows "65 dB @ 15m vertical distance" in green. Mounted atmospheric sensor package (0.25m × 0.15m × 0.10m) hangs below, collecting air samples. Helistat shadow barely visible through canopy. [0:15-0:20] Hard cut to same forest, same altitude: Bell 206 helicopter (3.2m rotor diameter, 1,000kg MTOW) flies over. Immediate chaos: deer bolt away, birds scatter in flocks, squirrels flee to burrows. Trees visibly swaying from rotor downwash (40 m/s tip speed). Sound meter spikes to "98 dB @ 15m" in flashing red. Ground vegetation flattened. [0:20-0:25] Return to helistat: Calm restored, scientist on ground (wearing no hearing protection) reviews data on tablet, makes voice notes clearly audible in footage. Close-up of sensor data showing stable atmospheric readings (no turbulence). [0:25-0:35] Side-by-side comparison bars: "HELISTAT 65 dB | HELICOPTER 98 dB | 85% QUIETER". Beautiful nature cinematography, National Geographic quality, saturated greens (#2D5016 forest, #90EE90 understory), golden morning light shafts, shallow depth of field.
```

**Usage:** Environmental applications, wildlife research customers

---

## MIDJOURNEY IMAGE PROMPTS

### Technical Diagrams & Cutaways

#### Image 1: Technical Cutaway Diagram - 20 Ton Helistat

**Prompt:**
```
Technical cutaway illustration of 20-ton V4 Helistat isometric view 30° elevation - CRITICAL: THIS IS QUADCOPTER DRONE CONFIGURATION with four VERTICAL rotor shafts, each passing UPWARD through center hole of a STANDING (vertical) donut-shaped envelope, NOT wheels on vehicle. CONFIGURATION: Four toroidal envelopes standing VERTICAL like donuts on edge (R=8.875m major radius, r=4.671m minor radius each) positioned at corners of square (35.5m × 35.5m rotor spacing, quadcopter X layout). Front-right toroid rendered 50% transparent showing internal structure: helium gas (translucent pale blue #E6F3FF), internal catenary curtain baffles (ripstop nylon panels every 2m, 28 compartments per toroid), pressure sensors (15 units, 0.05m black boxes), circumferential load tapes (12 per toroid, white webbing 50mm). Three opaque toroids show exterior: silver nylon (#C0C0C0), visible seam welding (2m × 2m panel grid), subtle wrinkle texture, semi-gloss finish. ROTORS: Four 7.14m diameter propellers (four-blade carbon fiber, blade chord 0.35m, black #1C1C1C) shown in exploded view 1m offset from operational position where they normally sit INSIDE toroid center holes. Rotor shafts VERTICAL (pointing up), blades horizontal. Electric motor assemblies visible (0.5m diameter cylinders, brushless DC, 216 kW each) at rotor bases. FRAME: Matte graphite carbon fiber tubes (#2C2C2C, 150mm diameter, 5mm wall) forming square quadcopter frame grid connecting four toroid bases (16 attachment points total). SIDE VIEW INSET: Shows toroid circular cross-section (vertical donut profile) with rotor blades spinning horizontally inside center hole, shaft vertical. TOP VIEW INSET: Shows four donuts in square pattern with rotors at centers (quadcopter layout). PAYLOAD: White aluminum honeycomb pod (4.0m × 2.5m × 2.0m, #F5F5F5) cutaway showing T700 turboshaft (1.2m × 0.8m × 0.7m, 180kg), 450kW generator (0.6m cylinder), fuel tank (500L kerosene), flight computer, cargo floor (11,646kg rated). LANDING GEAR: Four telescoping aluminum legs (1.5m extended, 0.8m retracted, 150mm diameter, silver #A8A8A8, hemispherical rubber feet 0.4m). Detailed annotations with leader lines, component dimensions/specs in clean sans-serif. White background, aerospace engineering aesthetic, precise linework, photorealistic with transparency for cutaways, 8K ultra detail. ORIENTATION CRITICAL: Toroids stand VERTICAL (upright donuts), rotor shafts VERTICAL (pointing up), like giant quadcopter drone NOT vehicle with wheels. --ar 16:9 --style technical --quality 2
```

---

#### Image 2: Quad Configuration Top View - Engineering Drawing

**Prompt:**
```
Precision top-down orthographic technical view (bird's eye view looking DOWN) of 20-ton helistat - QUADCOPTER DRONE CONFIGURATION clearly visible from above, CRITICAL: Four VERTICAL rotors (shafts pointing up toward camera) inside four VERTICAL standing donuts (looking down INTO the donut holes). Four toroidal envelopes rendered as blue wireframe mesh (#0066CC lines, 0.1m grid spacing) showing toroid surface geometry when viewed from above (looking down at standing donuts). Each toroid positioned at corners of perfect square (quadcopter X layout): coordinates relative to center origin (0,0) are toroid centers at (+13.08m, +13.08m), (-13.08m, +13.08m), (-13.08m, -13.08m), (+13.08m, -13.08m). Each toroid from TOP VIEW shows: major radius R=8.875m (red dimension line from toroid center to tube centerline), minor radius r=4.671m (green dimension showing tube thickness). When looking DOWN at vertical standing donut, toroid appears as two concentric circles: outer circle diameter 18.67m (outer edge of donut tube), inner circle diameter 0.54m (center hole where rotor sits). Four rotors visible at center of each toroid hole: 7.14m diameter propellers, four-blade configuration at 90° intervals (quadcopter standard), blade planform showing tapered geometry (0.5m root chord → 0.2m tip chord, twisted airfoil profile). Rotor blades shown in white (#FFFFFF) contrasting against blue wireframe toroids, rotor hubs shown as small circles. QUADCOPTER FRAME: Carbon fiber tubes connecting four toroid bases shown as yellow lines (#FFD700, 150mm diameter), square grid pattern connecting nearest attachment points (like DJI drone arms). PAYLOAD POD: Central white dashed rectangle (4.0m × 2.5m footprint) at quadcopter center. DIMENSION ANNOTATIONS in clean sans-serif: "OVERALL SPAN: 35.5m × 35.5m", "TOROID SPACING (center-to-center): 26.16m", "ROTOR DIAMETER: 7.14m", "TOROID MAJOR RADIUS (R): 8.875m", "TOROID MINOR RADIUS (r): 4.671m", "CONFIGURATION: QUADCOPTER X LAYOUT". Grid background 5m intervals (light gray #CCCCCC), dark background (#1A1A1A), dimension lines with arrowheads, CAD software aesthetic (SolidWorks/CATIA), architectural precision (ANSI Y14.5). ORIENTATION NOTE: "TOP VIEW - Looking down at quadcopter with four vertical donuts, rotors inside holes pointing UP toward camera". --ar 1:1 --style technical --quality 2
```

---

#### Image 3: Scale Comparison Poster - Museum Exhibit Quality

**Prompt:**
```
Professional comparison poster showing V4 Helistat family arranged left to right by ascending size against pure white seamless background (#FFFFFF) with soft studio lighting from 45° above creating subtle shadows beneath each vehicle. Six vehicles perfectly aligned at ground level, shot from eye height (1.7m camera elevation), slight wide-angle lens (28mm equivalent) to capture full lineup. LEFT TO RIGHT with scale references:

[1] 1kg MICRO: 1.3m × 1.3m × 0.3m footprint, silver Dyneema toroids (R=0.33m, r=0.17m) with hexagonal ripstop pattern visible, 0.05m rotors. Human hand (adult, 180mm length) positioned 0.5m in front for scale comparison.

[2] 10kg SMALL: 2.8m × 2.8m × 0.7m, silver Dyneema toroids (R=0.70m, r=0.37m), 0.16m rotors. Standing person (1.75m height, business casual attire) positioned 1m in front.

[3] 100kg MEDIUM: 6.1m × 6.1m × 1.6m, silver nylon toroids (R=1.52m, r=0.80m), 0.50m rotors. Sedan car (4.8m length, 1.4m height, silver) positioned beside.

[4] 1-TON: 13.1m × 13.1m × 3.4m, silver nylon toroids (R=3.27m, r=1.72m), 1.60m rotors. Semi truck (6.0m length, 2.5m height, red cab) positioned beside.

[5] 5-TON: 22.4m × 22.4m × 5.9m, silver nylon toroids (R=5.59m, r=2.94m), 3.57m rotors. Two-story building (8m width, 7m height, modern glass facade) positioned beside.

[6] 20-TON: 35.5m × 35.5m × 9.3m, silver nylon toroids (R=8.875m, r=4.671m), 7.14m rotors. Sikorsky S-64 Skycrane helicopter (21.4m fuselage length, 7.9m height, orange/red livery) positioned beside for direct comparison.

All helistats identical quad-toroid configuration, 1.9:1 aspect ratio (R/r), consistent silver metallic color (#C0C0C0), four black carbon fiber rotors (#1C1C1C). Floating specification text above each vehicle in clean Helvetica font: "1 kg | 0.2 kg payload" ... "20,000 kg | 11,646 kg payload". Subtle depth of field: closest (1kg) in sharp focus, furthest (20-ton) very slight softness. Perfect studio lighting (soft boxes, no harsh shadows), museum exhibit photography quality, 16K resolution, ultra-sharp detail, professional product photography. --ar 21:9 --quality 2 --style raw
```

---

### Marketing & Promotional Images

#### Image 4: Hero Marketing Shot - Golden Hour Construction Site

**Prompt:**
```
Stunning cinematic hero shot of 20-ton V4 Helistat at golden hour (30 minutes before sunset), hovering gracefully at 80m altitude above coastal construction site. Vehicle specifications: 35.5m × 35.5m square footprint, 9.3m height, four toroidal silver nylon envelopes (R=8.875m, r=4.671m each) catching warm golden sunlight (color temperature 3500K) creating brilliant highlights on semi-gloss fabric surface, seam lines visible creating subtle 2m grid pattern. Envelopes show slight translucency with backlight revealing internal structure shadows. Four 7.14m diameter rotors (four carbon fiber blades each, matte black #1C1C1C) spinning, slight motion blur on blade tips suggesting 340 RPM rotation. Matte graphite structural frame (150mm carbon fiber tubes #2C2C2C) connecting toroids visible in silhouette against bright envelope backlighting. White payload pod (4.0m × 2.5m × 2.0m) at center. Standard 20-foot shipping container (6.1m × 2.4m × 2.6m, weathered blue Maersk livery) suspended 15m below on steel cargo cables, swaying very slightly. Background: Pacific coastal construction site with gentle turquoise ocean waves (#40E0D0) below, partially completed high-rise building (30 stories, glass and steel), dramatic cloud formations (cumulus mediocris) with golden backlighting creating god rays (crepuscular rays) streaming through gaps, deep blue sky gradient from #87CEEB at horizon to #191970 at zenith. Camera angle: 15° below horizon looking up at vehicle from 100m horizontal distance, rule of thirds composition (helistat at right third intersection, ocean at left third). Shallow depth of field: helistat in sharp focus, background building and clouds with slight bokeh. Volumetric atmospheric haze suggesting coastal air. Branded text overlay at bottom third: "V4 HELISTAT - THE FUTURE OF HEAVY LIFT" in clean white sans-serif (Helvetica Neue Ultra Light, 72pt, 20% transparency). National Geographic/Apple product photography quality, shot on medium format digital (Hasselblad H6D equivalent), 8K, HDR (14 stops dynamic range), stunning. --ar 16:9 --style cinematic --quality 2
```

---

#### Image 5: Military Stealth Operations - Tactical Realism

**Prompt:**
```
Dramatic military tactical scene: 100kg V4 Helistat (6.1m × 6.1m × 1.6m) in full tactical paint scheme flying NOE (nap-of-earth) at 50m AGL over mountainous desert terrain at twilight (civil twilight, 20 minutes after sunset). Vehicle specifications: Four toroidal envelopes (R=1.52m, r=0.80m) coated in matte olive drab infrared-suppression paint (#4B5320 base with #3D3D29 shadow disruptive pattern camouflage), non-reflective flat finish absorbing remaining ambient light. Four 0.50m diameter rotors spinning (four blades each, sound-dampened composite material). Electro-optical/infrared sensor turret (0.6m × 0.4m × 0.3m cylinder, matte black #0A0A0A) suspended below on 3-axis gimbal, lens glint visible. Vehicle following terrain contours over winding canyon, altitude maintaining 50m above rocks. Terrain: Mojave Desert style rocky mountains, tan sandstone (#D2B48C) with desert scrub vegetation (creosote bush, Joshua trees), deep shadows in ravines (#1C1410). Sky: Deep blue twilight gradient (#1C2841 to #0F1419) with first stars visible, thin crescent moon 10° above horizon. Tactical HUD overlay in lower-left: monospace font (Courier New) in bright green (#00FF00) showing "MISSION TIME: 03:47:22 | ALT AGL: 51m | SPD: 32 km/h | PWR: 4.1 kW | FUEL: 68% | COORDINATES: 35.0°N 116.5°W | MODE: AUTO-TERRAIN-FOLLOW | SENSOR: ACTIVE TRACK". Thermal imagery inset picture-in-picture in upper-right corner (320×240px): white-hot thermal view showing distant vehicle signatures 2,800m range (bright white silhouettes #FFFFFF against gray landscape #7F7F7F). Gritty realistic military photography style, desaturated color palette (reduced saturation 30%, earth tones dominant), dust particles in air catching last light, volumetric atmospheric scattering, shot with cinéma vérité aesthetic. Subtle film grain (ISO 6400 equivalent), Tom Clancy/Lone Survivor cinematography, tactical realism, intense but professional. --ar 16:9 --style military --quality 2
```

---

#### Image 6: Clean Energy Vision - Environmental Harmony

**Prompt:**
```
Aspirational sustainability image showcasing 1-ton V4 Helistat (13.1m × 13.1m × 3.4m) in pristine white livery hovering 100m above lush green temperate rainforest canopy, embodying zero-emissions aviation future. Vehicle specifications: Four toroidal envelopes (R=3.27m, r=1.72m) in brilliant white nylon fabric (#FAFAFA) with semi-gloss UV-resistant coating reflecting blue sky, seam pattern visible. Monocrystalline solar panels (total 45 m², blue-black #1C2833) mounted on top surfaces of all four toroids providing supplemental power, visible rectangular cell grid pattern (156mm cells). Four 1.60m rotors (carbon fiber, white painted blades #F0F0F0) spinning silently. White structural frame and payload pod matching envelope color creating cohesive clean aesthetic. Beneath vehicle, translucent infographic overlay (50% opacity) showing system diagram: green hydrogen generation from solar farm (yellow sun icon → blue H2 molecule symbols), "ZERO EMISSIONS" in bold green text (#2ECC71), "SUSTAINABLE AVIATION" subtitle. Forest below: Dense old-growth temperate rainforest (Pacific Northwest Sitka spruce/Western hemlock), extremely saturated vibrant greens (#228B22 canopy, #90EE90 sun-dappled areas, #2D5016 shadows), morning mist wisps (#F0F8FF) rising from valleys. Background: Distant solar farm visible on hillside (regular grid of blue photovoltaic panels, 2 hectares), small hydrogen production facility (white industrial building with H2 storage tanks). Sky: Bright daylight (noon, 5500K color temperature), clear blue (#87CEEB) with scattered cumulus clouds (#FFFFFF), excellent visibility. Camera angle: Low angle 20° elevation from forest floor, vehicle centered, surrounded by nature, technology in harmony with environment. Composition suggests hope, clean future, environmental responsibility. National Geographic Earth Day cover quality, deeply saturated color (saturation +40%), HDR processing, inspirational tone, photorealistic but slightly idealized, beautiful. --ar 4:5 --style environmental --quality 2
```

---

### Operational Scenarios

#### Image 7: Construction Site Operations - Urban Heavy Lift

**Prompt:**
```
Dramatic wide-angle documentary shot of active urban construction site, ground perspective looking upward 60° elevation angle, emphasizing massive scale of 20-ton V4 Helistat positioning steel I-beam between skyscrapers. Camera positioned on construction site ground level (120m building altitude), ultra-wide 16mm equivalent lens creating forced perspective. Helistat specifications: 35.5m × 35.5m overall span, 9.3m height, four silver nylon toroids (R=8.875m, r=4.671m, metallic #C0C0C0 with sun highlights creating bright spots and shadow areas showing toroid curvature), four 7.14m black carbon fiber rotors at each toroid center. Vehicle maneuvering slowly (2 m/s) between two glass-facade office towers with narrow 47m gap clearance (vehicle 35.5m + 6m margins each side). Structural steel I-beam (W36×300 wide-flange, 11m length, 900kg mass, rusty orange primer coating #CC5500) suspended on 4-point cable bridle, currently being guided by three ironworkers on 40th floor steel deck. Workers wearing: yellow hard hats, safety orange high-vis vests (#FF6700), blue jeans, leather work gloves, safety harnesses. Workers using tag lines (12mm rope) to control beam rotation, one worker with hand raised in directional signal to crane operator/helistat pilot. Notable detail: Workers NOT wearing hearing protection - two workers talking to each other, mouths visible in conversation, one worker on radio. Foreground: Ground level showing construction materials (rebar bundles, plywood stacks), concrete and steel textures, construction debris. Background buildings: Modern downtown architecture with glass curtain walls reflecting blue sky and clouds. Environmental conditions: Bright midday sun creating strong shadows, slight heat shimmer rising from sun-heated concrete. Blue collar industrial aesthetic emphasizing real work, safety culture, precision operations. Documentary photography style (photojournalism), natural lighting with harsh direct sun contrast, gritty texture, conveys capability and precision, architectural photography composition quality. Shot on full-frame DSLR (Canon 5D Mark IV equivalent), f/8 for deep depth of field (everything sharp), ISO 200, 1/500s shutter. Photorealistic, authentic, compelling. --ar 3:2 --quality 2 --style raw
```

---

#### Image 8: Disaster Relief Operations - Humanitarian Impact

**Prompt:**
```
Emotionally impactful humanitarian photojournalism: 1-ton V4 Helistat (13.1m × 13.1m × 3.4m) delivering emergency supplies to remote mountain village 72 hours after major earthquake. Vehicle: Four silver nylon toroids (R=3.27m, r=1.72m) with "UN HUMANITARIAN RELIEF" decals (blue UN logo on white roundels, 1.5m diameter, positioned on toroid sides), white payload pod carrying emergency cargo net (4m × 4m × 2m) loaded with: blue UNHCR tarps, white rice sacks, red medical supply boxes, bottled water pallets (total 400kg cargo). Vehicle in final approach descent at 5m altitude above village square, rotor downwash (minimal at low disk loading) gently disturbing dust. Village setting: Remote Himalayan mountain village (altitude 2,800m), traditional stone houses (2-story, slate roofs) with earthquake damage visible: collapsed walls, rubble piles (#8B7355 stone, #654321 earth), damaged roofs. Village square: Packed earth cleared for landing zone (15m × 15m), dust color #C19A6B. Relief workers coordinating: 4 people in bright orange NGO vests with "RELIEF" printed on back, directing landing with hand signals, one person on radio. Local villagers: Group of 12-15 grateful villagers (men, women, children, wearing traditional Himalayan clothing - colorful wool garments, prayer scarves) gathered at safe distance (20m perimeter), expressions showing relief and hope, some with hands in prayer position (namaste), children pointing at helistat with wonder. Background: Dramatic Himalayan peaks (5,000m+ altitude, snow-covered #FAFAFA summits) with deep blue sky (#003366), scattered clouds, morning golden light (7:00 AM, side-lighting creating texture on mountains and rubble). Collapsed building in mid-ground showing earthquake destruction severity. Composition: Rule of thirds - helistat upper-left third, villagers lower-right third, damaged buildings middle ground providing context. Emotional tone: Hope amid tragedy, accessibility of aid, technology serving humanity, grateful human connection. Photojournalistic style (Pulitzer Prize-winning aesthetic): natural lighting, authentic moment (not posed), emotional resonance, documentary truth, award-winning composition. Shot on professional photojournalist gear (Nikon D6 equivalent), 35mm lens, f/4, ISO 400, capturing decisive moment. Photorealistic, emotionally authentic. --ar 16:9 --style documentary --quality 2
```

---

#### Image 9: Maritime Operations - Offshore Heavy Lift

**Prompt:**
```
Dramatic offshore industrial scene: 5-ton V4 Helistat (22.4m × 22.4m × 5.9m) approaching offshore oil platform helipad in challenging North Sea weather conditions, demonstrating superior stability in harsh environment. Vehicle specifications: Four silver-gray nylon toroids (R=5.59m, r=2.94m, weathered appearance with salt spray staining, darker gray #A9A9A9 compared to pristine silver) with high-visibility orange safety markings (diagonal stripes, 0.5m width, fluorescent orange #FF4500) on toroid leading edges. Four 3.57m rotors maintaining stable hover despite crosswind. Industrial equipment cargo: Heavy oilfield valve assembly (2,500kg mass, yellow painted steel #FFD700, cylindrical 3m × 1.5m diameter) suspended on certified lifting sling, approaching platform helipad (marked with white circle and "H", 25m diameter painted on steel deck). Oil platform: Massive offshore production platform (North Sea type, steel structure painted industrial safety yellow #F4C430 with rust streaks #8B4513, total platform 80m × 80m footprint, 40m deck height above water) with visible details: drilling derrick, accommodation block, helideck, safety railings, cranes, flare stack with flame visible. Platform workers: 4 personnel in orange coveralls and white hard hats on helideck coordinating cargo delivery, holding guide ropes. Weather conditions: Dramatic stormy sky with dark cumulonimbus clouds (#36454F) backlit by breaks of sunlight creating dramatic lighting, wind indicated by whitecaps on ocean surface and flag on platform showing 25 kt wind. Ocean: Rough North Sea waters with 2-3m wave height, dark blue-gray (#2F4F4F) with white foam crests (#F5F5F5), visible swell pattern. Environmental challenge visual cues: Vehicle maintaining rock-steady hover (stable despite wind - no tilt), slight spray visible from wave action below, workers bracing against wind but helistat unaffected (demonstrating buoyancy stability advantage). Lighting: Overcast with dramatic cloud breaks creating shafts of sunlight (volumetric god rays) illuminating vehicle and platform while surrounding sea remains dark. Gritty offshore petroleum industry aesthetic: industrial textures (rust, weathered paint, salt corrosion), harsh environment, operational capability focus. Industrial photography style similar to offshore energy sector marketing materials, shot with professional telephoto lens (200mm equivalent) from nearby support vessel, f/5.6, ISO 800, fast shutter 1/1000s to freeze motion in wind. Conveys: capability in extreme conditions, industrial strength, maritime operations, weather independence. Cinematic dramatic lighting, photorealistic detail, compelling. --ar 16:9 --style industrial --quality 2
```

---

## ADDITIONAL SPECIFICATIONS FOR ALL PROMPTS

### Color Palette Reference:
- **Envelope silver:** #C0C0C0 (metallic, semi-gloss on nylon) / Hexagonal shimmer on Dyneema
- **Rotor blades:** #1C1C1C (matte black carbon fiber)
- **Structural frame:** #2C2C2C (matte graphite)
- **Payload pod:** #F5F5F5 (white aluminum)
- **Landing gear:** #A8A8A8 (anodized aluminum)
- **Helium gas (when visible):** #E6F3FF (pale translucent blue, 30% opacity)

### Material Finish Specifications:
- **Nylon envelopes (≥100kg):** Semi-gloss urethane coating, subtle wrinkle texture, seam lines visible every 2m forming grid pattern
- **Dyneema envelopes (<100kg):** Matte metallic finish, hexagonal ripstop pattern visible (12mm repeat), technical fabric appearance
- **Carbon fiber components:** Matte finish with visible weave pattern (2×2 twill, 3K tow)

### Aspect Ratio Consistency:
All helistats maintain R/r = 1.9:1 aspect ratio across all size classes

### Configuration Geometry:
- **QUADCOPTER LAYOUT:** Four toroids arranged in perfect square pattern (like DJI drone layout)
- **VERTICAL ORIENTATION:** Toroids stand UPRIGHT (vertical, like donuts on edge), NOT horizontal like wheels
- **ROTOR POSITION:** Each rotor shaft passes VERTICALLY UPWARD through center hole of its toroid
- **ROTOR SIZE:** Rotors occupy 80% of hole diameter (20% clearance margin for safety)
- **FRAME:** Structural frame connects toroid bases at 4 attachment points each (16 total connections)
- **SIDE VIEW:** See circular toroid cross-section (donut profile) with rotor blades inside center hole
- **TOP VIEW:** See four concentric circles (looking down into standing donuts) with rotors at centers

---

**RENDERING PARAMETERS:**

### SORA Recommended Settings:
```
--duration: 30-60 seconds
--aspect-ratio: 16:9 (landscape), 9:16 (vertical social)
--style: cinematic | realistic | documentary | technical (match application)
--quality: maximum
--camera-movement: smooth orbits, dolly, crane (cinematically motivated)
```

### Midjourney Recommended Settings:
```
--ar [specified in each prompt]
--quality 2 (maximum quality)
--style [raw | technical | cinematic | etc. as specified]
--stylize 25-50 (low stylization for technical accuracy)
--version 6 (latest for photorealism)
```

---

**USAGE GUIDE:**

1. **Copy prompts exactly** - geometric specifications are precise
2. **Maintain consistency** - use same color/material specs across all visuals
3. **Scale context** - always include appropriate scale references (humans, vehicles, buildings)
4. **Material accuracy** - Dyneema for <100kg (matte, hexagonal ripstop), Nylon for ≥100kg (semi-gloss, seam grid)
5. **Verify geometry** - R/r = 1.9:1 ratio, square configuration, 80% rotor-to-hole sizing

---

**Document Version:** 2.0
**Date:** 2025-11-16
**Revision:** Complete geometric specification overhaul with precise dimensions, materials, and finishes
