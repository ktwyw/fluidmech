"""CHME 202 - Week 6 - Example 14: leakage past a piston or valve spool (narrow annular gap).

A thin annular clearance c around a piston of diameter D behaves like parallel plates of
width pi D: Q = pi D c^3 dp / (12 mu L). If the piston sits off-centre (eccentricity e,
epsilon = e / c) the leakage rises by the factor (1 + 1.5 epsilon^2) - up to 2.5x.
"""

import math

D, L, dp = 0.05, 0.04, 200e5  # piston diameter, sealing length, pressure difference (200 bar)
mu = 0.03  # hydraulic oil
print(f"Piston D = {D * 1000:.0f} mm, sealing length {L * 1000:.0f} mm, dp = {dp / 1e5:.0f} bar, oil mu = {mu} Pa s\n")
print(f"{'clearance [um]':>15} {'concentric [mL/min]':>20} {'fully eccentric':>16} {'Re':>6}")
for c_um in [5, 10, 20, 40]:
    c = c_um * 1e-6
    q = math.pi * D * c**3 * dp / (12 * mu * L)  # narrow annulus = parallel plates of width pi D
    v = q / (math.pi * D * c)
    re = 870 * v * 2 * c / mu  # Re with oil density 870 kg/m3 and hydraulic diameter 2c
    print(f"{c_um:>15} {q * 6e7:>20.2f} {q * 2.5 * 6e7:>16.2f} {re:>6.1f}")
print("\nThe c^3 law makes machining tolerance critical (Week 5, the cubic law). Side loads that push the")
print("piston against one wall increase leakage 2.5x - one reason for centring grooves on spools.")
print("The leakage flow also heats the oil: power lost = Q dp.")
