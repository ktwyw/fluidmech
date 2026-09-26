"""CHME 202 - Week 4 - Example 13: the Rankine oval - a closed body from a source-sink pair.

Uniform stream U + source m at x = -a + sink -m at x = +a. The dividing streamline
psi = 0 is a closed oval of half-length l = sqrt(a^2 + m a / (pi U)). We find the
half-width h numerically from the stream function and check the maximum surface speed.
Reading: White, Section 8.3.
"""

import math

from fluidmech.potential_flow import rankine_oval
from fluidmech.solvers import bisect

U, a = 2.0, 1.0  # free stream [m/s], source/sink position [m]
print(f"U = {U} m/s, source and sink at x = -/+{a} m\n")
print(f"{'m [m2/s]':>9} {'half-length l':>14} {'half-width h':>13} {'l/h':>6} {'V_max/U':>8}")
for m in [1.0, 3.0, 6.0, 12.0]:
    flow = rankine_oval(U, m, a)
    half_len = math.sqrt(a**2 + m * a / (math.pi * U))
    # half-width: the dividing streamline psi = 0 crosses x = 0
    h = bisect(lambda y, f=flow: f.stream_function(0.0, y), 1e-6, 20.0)
    v_max = flow.speed(0.0, h) / U
    print(f"{m:>9} {half_len:>14.3f} {h:>13.3f} {half_len / h:>6.2f} {v_max:>8.3f}")
print("\nWeak source-sink pairs give long, slender ovals (V_max -> U, little disturbance); strong pairs")
print("give nearly circular bodies (V_max -> 2U, the cylinder of Example 4). Stagnation points sit at x = -/+l.")
