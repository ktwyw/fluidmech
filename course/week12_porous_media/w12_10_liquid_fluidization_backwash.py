"""CHME 202 - Week 12 - Example 10: expanding a sand filter bed by backwashing (liquid fluidisation).

Liquid-fluidised beds expand smoothly: the Richardson-Zaki relation u = u_t eps^n gives
the voidage at each superficial velocity, and mass conservation gives the height
L = L_0 (1 - eps_0) / (1 - eps). Water-treatment sand filters are cleaned this way.
"""

from fluidmech import Fluid
from fluidmech import porous as por
from fluidmech.drag import richardson_zaki_exponent, terminal_velocity

water = Fluid.water(15)
d, rho_p = 0.8e-3, 2650.0  # sand diameter [m], density [kg/m3]
L0, eps0 = 0.8, 0.42  # settled bed depth and voidage
ut = terminal_velocity(d, rho_p, water)
re_t = water.density * ut * d / water.dynamic_viscosity
n = richardson_zaki_exponent(re_t)
u_mf = por.minimum_fluidization_velocity(d, rho_p, water.density, water.dynamic_viscosity, voidage_mf=eps0)
print(
    f"Filter sand d = {d * 1000} mm: u_t = {ut * 100:.1f} cm/s (Re_t = {re_t:.0f}), n = {n:.2f}, "
    f"u_mf = {u_mf * 100:.2f} cm/s\n"
)
print(f"{'u [cm/s]':>9} {'u [m/h]':>8} {'voidage':>8} {'bed height [m]':>15} {'expansion':>10}")
for u_cm in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]:
    u = u_cm / 100
    if u < u_mf:
        print(f"{u_cm:>9} {u * 3600:>8.0f} {eps0:>8.2f} {L0:>15.2f} {'fixed bed':>10}")
        continue
    eps = (u / ut) ** (1 / n)  # Richardson-Zaki solved for voidage
    if eps <= eps0:
        print(f"{u_cm:>9} {u * 3600:>8.0f} {eps0:>8.2f} {L0:>15.2f} {'incipient':>10}")
        continue
    L = L0 * (1 - eps0) / (1 - eps)  # sand volume is conserved as the bed expands
    print(f"{u_cm:>9} {u * 3600:>8.0f} {eps:>8.2f} {L:>15.2f} {L / L0 - 1:>10.0%}")
print("\nFor this fairly coarse 0.8 mm sand, 20-40 % expansion - enough to scour off trapped dirt - needs")
print("~70-110 m/h; finer sand expands at lower rates. The velocity stays well below u_t, so the sand")
print("is not washed out of the filter.")
u_rz = ut * eps0**n
print(f"Note: Richardson-Zaki predicts expansion only above u = u_t eps0^n = {u_rz * 100:.2f} cm/s, while Ergun")
print(f"gives u_mf = {u_mf * 100:.2f} cm/s - between the two the bed is fluidised but hardly expanded.")
