"""CHME 202 - Week 2 - Example 4: buoyancy - hydrometers and the stability of a floating drum.

Reading: White, Sections 2.8-2.9.
"""

import math

from fluidmech.constants import G
from fluidmech.hydrostatics import buoyant_force

# (a) Hydrometer: bulb volume V0, stem area A. Immersion depth h of the stem in a liquid of SG s:
# m = rho_w s (V0 + A h)  ->  h = (m / (rho_w s) - V0) / A
m, V0, d_stem = 0.020, 18e-6, 6e-3
A = math.pi * d_stem**2 / 4
print("(a) Hydrometer (mass 20 g, bulb 18 cm3, stem 6 mm)")
for sg in [0.85, 0.90, 1.00, 1.05, 1.10]:
    h = (m / (1000 * sg) - V0) / A
    print(f"  SG = {sg:.2f}: stem immersed {h * 1000:6.1f} mm")
print("  Equal steps in SG give UNEQUAL spacing on the stem - the scale is compressed at high SG.\n")

# (b) A floating steel drum: is it stable upright?
D, H, mass = 0.6, 0.9, 60.0  # empty drum with ballast, centre of gravity height KG
print("(b) Cylindrical drum floating upright in water (D = 0.6 m, H = 0.9 m, mass 60 kg)")
draft = mass / (1000 * math.pi * D**2 / 4)
print(f"  draft {draft * 100:.1f} cm; buoyancy {buoyant_force(math.pi * D**2 / 4 * draft) / G:.1f} kg-force")
for kg in [0.10, 0.30, 0.45]:
    KB = draft / 2
    BM = (math.pi * D**4 / 64) / (math.pi * D**2 / 4 * draft)  # I / V_displaced
    GM = KB + BM - kg
    print(f"  CG at {kg:.2f} m: GM = {GM:+.3f} m -> {'stable' if GM > 0 else 'UNSTABLE (tips over)'}")
print("  A tall body floating upright is stable only if its centre of gravity is kept low.")
