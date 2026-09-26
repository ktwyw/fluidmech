"""CHME 202 - Week 12 - Example 13: concentration polarisation in reverse osmosis.

Water passing through the membrane leaves salt behind, which accumulates at the surface:
c_m = c_b exp(J / k) (film model, perfect rejection). The higher surface concentration
raises the osmotic pressure and lowers the flux, so the flux must be solved iteratively:
J = (dp - pi(c_m)) / (mu R_m). Better cross-flow mixing (larger k) helps.
"""

import math

from fluidmech import porous as por
from fluidmech.solvers import bisect

mu, R_m, dp = 1e-3, 1.0e14, 40e5  # brackish-water RO membrane at 40 bar
c_b = 200.0  # mol/m3 NaCl (~12 g/L)
print(f"Feed {c_b:.0f} mol/m3 NaCl, applied pressure {dp / 1e5:.0f} bar\n")
print(f"{'k [um/s]':>9} {'flux [LMH]':>11} {'c_m / c_b':>10} {'pi at membrane [bar]':>21}")
J_ideal = (dp - por.vant_hoff_osmotic_pressure(c_b, 25, 2)) / (mu * R_m)
for k_um in [5, 10, 20, 50, 1e6]:
    k = k_um * 1e-6

    def residual(J, k=k):
        pi_m = por.vant_hoff_osmotic_pressure(c_b * math.exp(J / k), 25, 2)
        return J - por.membrane_flux(dp, mu, R_m, osmotic_pressure_difference=pi_m)

    J = bisect(residual, 0.0, J_ideal)  # residual increases with J: a unique root
    c_m = c_b * math.exp(J / k)
    label = "no polarisation" if k_um >= 1e6 else f"{k_um:.0f}"
    print(
        f"{label:>9} {por.lmh(J):>11.1f} {c_m / c_b:>10.2f} {por.vant_hoff_osmotic_pressure(c_m, 25, 2) / 1e5:>21.1f}"
    )
print("\nPoor mixing (small k) raises the salt concentration at the wall several-fold and cuts the")
print("flux; it also promotes scaling and fouling. Spacers and higher cross-flow velocity raise k.")
