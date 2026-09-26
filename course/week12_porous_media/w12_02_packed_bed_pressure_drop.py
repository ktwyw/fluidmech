"""CHME 202 - Week 12 - Example 2: pressure drop through a packed catalyst bed.

Kozeny-Carman (laminar), Burke-Plummer (turbulent) and the Ergun equation which
spans both. Smaller particles give more surface for reaction but a much higher
pressure drop - a central trade-off in reactor design.
"""

from fluidmech import Fluid
from fluidmech import porous as por

gas = Fluid(3.5, 2.5e-5, "reactor gas (5 bar, 300 degC)")
d_p, eps, L = 3e-3, 0.40, 2.0  # particle diameter [m], voidage, bed depth [m]
print(f"Bed of {d_p * 1000:.0f} mm spheres, voidage {eps}, depth {L} m, {gas.name}\n")
print(f"{'u [m/s]':>8} {'Re_p':>8} {'Kozeny-Carman':>14} {'Burke-Plummer':>14} {'Ergun':>9}  [kPa]")
for u in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0]:
    re = por.bed_reynolds(u, d_p, eps, gas.dynamic_viscosity, gas.density)
    kc = por.kozeny_carman_pressure_gradient(u, d_p, eps, gas.dynamic_viscosity) * L
    bp = por.burke_plummer_pressure_gradient(u, d_p, eps, gas.density) * L
    er = por.ergun_pressure_gradient(u, d_p, eps, gas.dynamic_viscosity, gas.density) * L
    print(f"{u:>8.2f} {re:>8.1f} {kc / 1e3:>14.3f} {bp / 1e3:>14.3f} {er / 1e3:>9.3f}")
print("Ergun approaches Kozeny-Carman (x150/180) at low Re_p and Burke-Plummer at high Re_p.\n")

u = 0.5  # superficial gas velocity [m/s]
print(f"Effect of particle size and shape at u = {u} m/s:")
for d in [1e-3, 2e-3, 3e-3, 5e-3]:
    for phi, shape in [(1.0, "spheres"), (0.65, "crushed")]:
        dp = por.ergun_pressure_gradient(u, d, eps, gas.dynamic_viscosity, gas.density, phi) * L
        print(
            f"  d = {d * 1000:.0f} mm {shape:<8} (sphericity {phi}): dp = {dp / 1e3:6.1f} kPa, "
            f"surface area {por.specific_surface(d, phi) * (1 - eps):6.0f} m2/m3 bed"
        )
ratio = ((1 - 0.35) ** 2 / 0.35**3) / ((1 - 0.40) ** 2 / 0.40**3)
print("\nThe voidage enters as (1-eps)^2/eps^3: a denser packing, eps 0.40 -> 0.35, multiplies the")
print(f"viscous pressure drop by {ratio:.2f}. Uniform packing (and loading the catalyst carefully) matters!")
