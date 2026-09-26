"""CHME 202 - Week 3 - Example 12: the rotameter (variable-area flow meter).

A float rises in a tapered tube until the pressure drop across the annular gap
balances its buoyant weight: dp A_f = V_f (rho_f - rho) g. Bernoulli through the gap:
Q = Cd A_gap sqrt(2 dp / rho). Because dp is FIXED by the float, Q grows with the
gap area - almost linearly with height in a conical tube.
"""

import math

from fluidmech.constants import G

d_float, V_float, rho_float = 0.020, 3.0e-6, 7900.0  # stainless float
D0, taper = 0.0205, 0.004  # tube diameter at the bottom, diameter increase per 100 mm
cd = 0.65
A_f = math.pi * d_float**2 / 4


def flow(height_mm: float, rho: float) -> float:
    dp = V_float * (rho_float - rho) * G / A_f  # float's buoyant weight / area: fixed by the float
    D = D0 + taper * height_mm / 100
    gap = math.pi / 4 * (D**2 - d_float**2)
    return cd * gap * math.sqrt(2 * dp / rho)


print(
    f"Float d = {d_float * 1000:.0f} mm, pressure drop across it: "
    f"{V_float * (rho_float - 998) * G / A_f:.0f} Pa (constant, independent of flow)\n"
)
print(f"{'height [mm]':>12} {'water [L/min]':>14} {'ethanol [L/min]':>16}")
for h in [0, 50, 100, 150, 200, 250]:
    print(f"{h:>12} {flow(h, 998.0) * 60000:>14.2f} {flow(h, 789.0) * 60000:>16.2f}")
corr = math.sqrt((rho_float - 789.0) * 998.0 / ((rho_float - 998.0) * 789.0))
print("\nA water-calibrated scale reads ethanol LOW: multiply by sqrt((rho_f - rho) rho_cal / ((rho_f - rho_cal) rho))")
print(f"= {corr:.3f}. Rotameters are cheap, need no power and show flow at a glance - but read only ~2 %.")
