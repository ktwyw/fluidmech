"""CHME 202 - Week 3 - Example 11: Bernoulli with a free surface - flow under a sluice gate.

Between the upstream pool (depth y1) and the jet downstream (depth y2) the pressure
is hydrostatic and the surface is at atmospheric pressure, so Bernoulli plus
continuity gives  q = y2 sqrt( 2 g (y1 - y2) / (1 - (y2/y1)^2) )  per unit width.
Reading: White, Section 10.4 and Problem 3.x (sluice gate).
"""

import math

from fluidmech.constants import G

y1, width = 2.0, 3.0  # upstream depth [m], channel width [m]
print(f"Upstream depth {y1} m, channel width {width} m\n")
print(f"{'gate opening [m]':>17} {'y2 = 0.61 a':>12} {'Q [m3/s]':>9} {'V2 [m/s]':>9} {'Fr2':>6}")
for a in [0.1, 0.2, 0.4, 0.6]:
    y2 = 0.61 * a  # contraction coefficient for a sharp gate
    q = y2 * math.sqrt(2 * G * (y1 - y2) / (1 - (y2 / y1) ** 2))
    v2 = q / y2
    print(f"{a:>17} {y2:>12.3f} {q * width:>9.3f} {v2:>9.2f} {v2 / math.sqrt(G * y2):>6.2f}")
print("\nThe flow leaving the gate is fast and shallow (supercritical, Fr > 1); it usually returns to")
print("deep, slow flow through a hydraulic jump (see examples/24 and the open_channel module).")
worst = 1 / math.sqrt(1 - (0.61 * 0.6 / y1) ** 2) - 1  # effect of the (y2/y1)^2 term at the largest opening
print(f"Neglecting the upstream velocity head (the (y2/y1)^2 term) underestimates Q by up to {worst:.1%} here.")
