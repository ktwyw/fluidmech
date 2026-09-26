"""CHME 202 - Week 6 - Example 10: flow maldistribution among parallel laminar channels.

In laminar flow Q ~ d^4 at a fixed pressure drop (Hagen-Poiseuille). Small
differences in channel diameter therefore give large differences in flow -
a design problem for microreactors ('numbering-up'), hollow-fibre membrane
modules and monolith catalysts.
"""

import math
import random

from fluidmech.laminar import pipe_flow_rate

random.seed(3)
mu, L, dp = 1e-3, 0.1, 5e3  # water [Pa s], channel length [m], pressure drop [Pa]
d_nom = 500e-6  # nominal channel diameter [m]
n = 20  # number of parallel channels
print(f"{n} parallel channels, nominal d = {d_nom * 1e6:.0f} um, L = {L * 100:.0f} cm, dp = {dp / 1e3:.0f} kPa\n")
for tol in [0.01, 0.03, 0.05, 0.10]:
    ds = [d_nom * (1 + random.gauss(0, tol)) for _ in range(n)]  # manufactured diameters with random scatter
    qs = [pipe_flow_rate(dp / L, d / 2, mu) for d in ds]
    mean = sum(qs) / n
    sd = (sum((q - mean) ** 2 for q in qs) / (n - 1)) ** 0.5
    residence = [L / (q / (math.pi * d**2 / 4)) for q, d in zip(qs, ds)]
    print(
        f"diameter scatter {tol:4.0%} (1 sigma): flow scatter {sd / mean:4.0%} (1 sigma), "
        f"max/min flow {max(qs) / min(qs):4.2f}, residence time {min(residence):.2f}-{max(residence):.2f} s"
    )
print("\nFlow scales with d^4 and residence time with 1/d^2: a 5 % diameter scatter gives ~20 % scatter")
print("in flow (4 x 5 %) and a broad residence-time distribution (Week 14) - lower conversion and selectivity.")
print("Remedies: tight manufacturing tolerances or a large flow restriction at each channel inlet.")
