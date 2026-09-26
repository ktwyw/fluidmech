"""CHME 202 - Week 9 - Example 11: finding the roughness of an old pipe from a flow test.

Measure Q and the head loss over a length L, compute f from Darcy-Weisbach, then invert
the Colebrook equation for the roughness:
eps / D = 3.7 [10^(-1 / (2 sqrt(f))) - 2.51 / (Re sqrt(f))].
Used to calibrate network models of ageing water mains.
"""

import math

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.constants import G

water = Fluid.water(12)
D, L = 0.200, 500.0  # main diameter and tested length [m]
tests = [(0.03, 4.14), (0.045, 8.96), (0.06, 16.3)]  # (Q [m3/s], measured head loss [m])
print(f"Field test on {L:.0f} m of {D * 1000:.0f} mm cast-iron main (water at 12 degC)\n")
print(f"{'Q [L/s]':>8} {'h_f [m]':>8} {'V [m/s]':>8} {'Re':>9} {'f':>8} {'eps [mm]':>9}")
eps_values = []
for q, hf in tests:
    V = pf.mean_velocity(q, D)
    re = V * D / water.kinematic_viscosity
    f = hf * D / L * 2 * G / V**2  # Darcy-Weisbach solved for f
    rel = 3.7 * (10 ** (-1 / (2 * math.sqrt(f))) - 2.51 / (re * math.sqrt(f)))  # Colebrook solved explicitly for eps/D
    eps_values.append(rel * D)
    print(f"{q * 1000:>8.0f} {hf:>8.2f} {V:>8.2f} {re:>9.3g} {f:>8.4f} {rel * D * 1000:>9.2f}")
eps = sum(eps_values) / len(eps_values)
print(
    f"\nMean effective roughness {eps * 1000:.2f} mm, about {eps / pf.ROUGHNESS['cast_iron']:.0f} times that of new cast iron (0.26 mm):"
)
print(
    f"corrosion nodules (tuberculation) have roughened the main. Check: Colebrook with this eps predicts h_f = "
    f"{pf.head_loss(0.045, D, L, water, eps).major_head_loss:.2f} m at 45 L/s (measured 8.96 m)."
)
print("Small errors in h_f give large errors in eps (f is insensitive to eps): use several flows.")
