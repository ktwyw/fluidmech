"""Example 19 - Laminar vs. turbulent velocity profiles and wall shear stress.

Laminar (Hagen-Poiseuille):  u/U_max = 1 - (r/R)^2,        V = U_max / 2
Turbulent (power law):       u/U_max = (1 - r/R)^(1/n),    V = 2 n^2 U_max / ((n+1)(2n+1))
"""

import math

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
D = 0.05  # pipe diameter [m]
R = D / 2


def describe(q: float) -> None:
    r = pf.head_loss(q, D, 1.0, water, 0.0)
    v = r.velocity
    tau_w = r.friction_factor * water.density * v**2 / 8.0
    u_star = math.sqrt(tau_w / water.density)
    print(f"\nQ = {q * 1000:.3f} L/s -> V = {v:.3f} m/s, Re = {r.reynolds:.0f} ({r.regime})")
    if r.regime == "laminar":
        u_max = 2.0 * v  # laminar: centreline velocity is twice the mean
        profile = [1 - (y / 10) ** 2 for y in range(11)]  # parabola u/U_max = 1 - (r/R)^2 at r/R = 0, 0.1, ..., 1
    else:
        n = -1.7 + 1.8 * math.log10(r.reynolds)  # power-law exponent correlation
        u_max = v * (n + 1) * (2 * n + 1) / (2 * n**2)
        profile = [(1 - y / 10) ** (1 / n) for y in range(11)]  # power-law profile at the same radii
        print(f"   power-law exponent n = {n:.2f}")
    print(f"   U_max = {u_max:.3f} m/s (U_max/V = {u_max / v:.2f})")
    print(f"   wall shear stress = {tau_w:.4f} Pa, friction velocity u* = {u_star:.4f} m/s")
    print("   r/R    u/U_max")
    for i, u in enumerate(profile):
        bar = "#" * int(40 * u)
        print(f"   {i / 10:>4.1f}   {u:>6.3f}  {bar}")


describe(0.045e-3)  # laminar
describe(5.0e-3)  # turbulent
print("\nThe turbulent profile is much flatter, with steep gradients (and high shear) at the wall.")
