"""CHME 202 - Week 13 - Example 11: dimensional analysis plus ONE experiment gives a design formula.

Flow over a rectangular weir: q = Q / b depends only on g and the head H (viscosity and surface
tension negligible for large weirs). Dimensional analysis leaves one group, q / (sqrt(g) H^1.5),
which must be a constant C. A few lab measurements fix C; the formula then works at any scale.
"""

import math

from fluidmech import dimensional as dim

groups = dim.pi_groups({"q": "L^2 T^-1", "g": "gravity", "H": "length"})
print("Pi group:", dim.format_group(groups[0]), " -> q = C sqrt(g) H^(3/2)\n")

b = 0.30  # lab weir crest length [m]
lab = [(0.04, 0.0043), (0.06, 0.0081), (0.08, 0.01237), (0.1, 0.01724)]  # (H [m], Q [m3/s]) measured
Cs = [Q / b / (math.sqrt(9.80665) * H**1.5) for H, Q in lab]  # the single Pi group, evaluated for each test
C = sum(Cs) / len(Cs)
print(f"{'H [mm]':>7} {'Q [L/s]':>8} {'C':>7}")
for (H, Q), c in zip(lab, Cs):
    print(f"{H * 1000:>7.0f} {Q * 1000:>8.2f} {c:>7.3f}")
print(
    f"\nMean C = {C:.3f}  (theory for a sharp-crested weir with Cd = 0.62: 0.62 x (2/3) x sqrt(2) = "
    f"{0.62 * 2 / 3 * math.sqrt(2):.3f})"
)
print("\nPrediction for a full-scale spillway weir, b = 12 m:")
for H in [0.3, 0.6, 1.0]:
    print(f"  H = {H} m: Q = {C * 12 * math.sqrt(9.80665) * H**1.5:.2f} m3/s")
print("Caution: at very small heads surface tension and viscosity (ignored above) become important.")
