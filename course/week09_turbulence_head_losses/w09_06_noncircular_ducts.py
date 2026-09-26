"""CHME 202 - Week 9 - Example 6: pressure loss in non-circular ducts.

Turbulent flow: the hydraulic diameter D_h = 4A/P works to about +/-15 %.
White's effective-diameter method improves it: D_eff = (64 / fRe_laminar) D_h,
used in the Colebrook equation for the Reynolds number.
Reading: White, Section 6.8.
"""

import math

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.laminar import annulus_fre, rectangular_duct_fre

air = Fluid.air(20)
V, L = 8.0, 20.0  # air velocity [m/s], duct length [m]
print(f"Air at {V} m/s through {L} m of smooth duct\n")
print(f"{'duct':<24} {'D_h [mm]':>9} {'dp (D_h) [Pa]':>14} {'dp (D_eff) [Pa]':>16} {'difference':>11}")
ducts = [
    ("square 300 x 300 mm", 0.3, 0.3, None),
    ("rectangle 600 x 150 mm", 0.6, 0.15, None),
    ("rectangle 1000 x 100 mm", 1.0, 0.1, None),
    ("annulus 200 / 100 mm", 0.2, 0.1, "annulus"),
]
for name, a, b, kind in ducts:
    if kind == "annulus":
        area = math.pi * (a**2 - b**2) / 4  # a, b = outer and inner diameters
        dh = a - b
        fre = annulus_fre(b / a)
    else:
        area = a * b
        dh = pf.hydraulic_diameter(area, 2 * (a + b))
        fre = rectangular_duct_fre(min(a, b) / max(a, b))
    d_eff = 64.0 / fre * dh  # White's effective diameter: corrects D_h using the laminar fRe
    f_h = pf.friction_factor(V * dh / air.kinematic_viscosity, 0.0)
    f_e = pf.friction_factor(V * d_eff / air.kinematic_viscosity, 0.0)
    dp_h = f_h * L / dh * 0.5 * air.density * V**2
    dp_e = f_e * L / dh * 0.5 * air.density * V**2
    print(f"{name:<24} {dh * 1000:>9.0f} {dp_h:>14.1f} {dp_e:>16.1f} {dp_e / dp_h - 1:>+11.1%}")
print("\nNote: D_eff only changes the Reynolds number; D_h is still used in f (L/D_h) V^2/2.")
print("For flat ducts and annuli the correction is several percent - for LAMINAR flow it is essential (Week 6).")
