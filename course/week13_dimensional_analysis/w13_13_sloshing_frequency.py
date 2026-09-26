"""CHME 202 - Week 13 - Example 13: sloshing of liquid in a tank - scaling and the natural frequency.

Dimensional analysis: f = sqrt(g / L) F(h / L) for a tank of length L filled to depth h.
Linear wave theory gives F: omega^2 = (pi g / L) tanh(pi h / L) for the first mode.
Models obey Froude scaling: time scales as sqrt(length scale).
Relevant to road tankers (Week 2, Example 5), ship tanks and seismic design of storage tanks.
"""

import math

from fluidmech.constants import G


def slosh_period(L: float, h: float) -> float:
    # first sloshing mode, linear wave theory
    return 2 * math.pi / math.sqrt(math.pi * G / L * math.tanh(math.pi * h / L))


print(f"{'tank length [m]':>16} {'fill depth [m]':>15} {'period [s]':>11}")
for L, h in [(6.0, 1.6), (6.0, 0.5), (12.0, 1.6), (20.0, 15.0)]:
    print(f"{L:>16} {h:>15} {slosh_period(L, h):>11.2f}")
lam = 1 / 20  # model length scale
T_full = slosh_period(12.0, 1.6)
T_model = slosh_period(12.0 * lam, 1.6 * lam)
print(f"\n1:20 model of the 12 m tanker compartment: model period {T_model:.3f} s, full scale {T_full:.2f} s")
print(
    f"ratio {T_full / T_model:.2f} = sqrt(20) = {math.sqrt(20):.2f} - Froude scaling, as dimensional analysis predicts."
)
print("Braking at intervals close to the slosh period amplifies the waves; baffles split the tank into")
print("shorter compartments with higher natural frequencies.")
