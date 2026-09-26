"""CHME 202 - Week 6 - Example 13: draining a tank through a long laminar tube.

With Hagen-Poiseuille in the outlet tube, Q = pi rho g h R^4 / (8 mu L) is PROPORTIONAL to
the level h, so the level falls exponentially: h = h0 exp(-t / T), T = 8 mu L A / (rho g pi R^4).
Compare Torricelli draining (Week 3), where Q ~ sqrt(h) and the tank empties in finite time.
This is the principle of efflux-cup and capillary viscometers.
"""

import math

from fluidmech.constants import G

A_tank, h0 = 0.01, 0.30  # tank area [m2], initial level [m]
R, L = 3.0e-3, 0.1  # outlet tube radius and length
for name, rho, mu in [("glycerol", 1261.0, 1.41), ("oil", 880.0, 0.10)]:
    T = 8 * mu * L * A_tank / (rho * G * math.pi * R**4)  # time constant of the exponential decay
    q0 = math.pi * rho * G * h0 * R**4 / (8 * mu * L)
    re0 = rho * (q0 / (math.pi * R**2)) * 2 * R / mu
    print(f"{name}: time constant T = {T / 60:.1f} min, initial Re = {re0:.2f} (laminar: formula valid)")
    for frac in [0.5, 0.1, 0.01]:
        print(f"    level falls to {frac:.0%} of h0 after {T * math.log(1 / frac) / 60:6.1f} min")
print("\nExponential decay never quite reaches zero; halving the level always takes the same time")
print("(T ln 2). Measuring that half-time with a known tube gives the kinematic viscosity.")
