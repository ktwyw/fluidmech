"""CHME 202 - Week 2 - Example 6: rigid-body rotation - the forced vortex.

Liquid in a tank rotating at omega forms a paraboloid, z = z0 + omega^2 r^2 / (2g).
Relevant to unbaffled stirred tanks, centrifuges and spin coating.
Saves rotating_tank.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech.hydrostatics import RotatingTank

R, h0 = 0.25, 0.40  # tank radius and initial depth [m]
omega_bottom = RotatingTank(R, h0, 1.0).speed_to_expose_bottom()
print(f"Open cylindrical tank R = {R} m, initial depth {h0} m")
print(
    f"The bottom centre is exposed at omega = {omega_bottom:.2f} rad/s ({omega_bottom * 60 / (2 * math.pi):.0f} rpm)\n"
)
print(f"{'rpm':>6} {'omega':>7} {'rise [m]':>9} {'centre depth':>13} {'wall depth':>11} {'p bottom wall [kPa]':>20}")
fig, ax = plt.subplots(figsize=(7, 4.5))
for rpm in [0, 40, 60, 80, 100]:
    tank = RotatingTank(R, h0, rpm * 2 * math.pi / 60)
    p_wall = tank.pressure(R, 0.0)
    print(
        f"{rpm:>6} {tank.omega:>7.2f} {tank.rise:>9.3f} {tank.centre_depth:>13.3f} {tank.wall_depth:>11.3f} "
        f"{p_wall / 1e3:>20.2f}"
    )
    rs = [i * R / 50 for i in range(51)]  # radii for the plotted profile
    ax.plot(rs, [tank.surface_height(r) for r in rs], label=f"{rpm} rpm")
    ax.plot([-r for r in rs], [tank.surface_height(r) for r in rs], color=ax.lines[-1].get_color())
print("\nThe mean surface height stays at the initial depth (volume is conserved): the centre drops")
print("by exactly as much as the wall rises. Pressure at the wall bottom equals rho g (local depth).")

ax.axhline(0, color="k")
ax.plot([-R, -R], [0, 0.8], "k", lw=2)
ax.plot([R, R], [0, 0.8], "k", lw=2)
ax.set(xlabel="r [m]", ylabel="free-surface height [m]", title="Free surface of a liquid in rigid rotation")
ax.legend()
fig.tight_layout()
fig.savefig("rotating_tank.png", dpi=130)
print("Saved rotating_tank.png")
