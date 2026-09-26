"""CHME 202 - Week 4 - Example 4: potential flow past a cylinder, d'Alembert's paradox and lift.

Uniform stream + doublet = flow past a cylinder; adding a vortex gives lift.
Integrating the surface pressure shows ZERO drag (d'Alembert's paradox) and a
lift equal to rho U Gamma (Kutta-Joukowski). Saves cylinder_flow.png.
Reading: White, Sections 8.3-8.4.

# requires: matplotlib, numpy
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from fluidmech.potential_flow import cylinder, kutta_joukowski_lift

U, R, rho = 10.0, 0.5, 1.2  # free stream [m/s], cylinder radius [m], air density [kg/m3]


def surface_forces(flow, n: int = 720) -> tuple[float, float]:
    drag = lift = 0.0
    for i in range(n):  # integrate surface pressure around the cylinder
        th = 2 * math.pi * (i + 0.5) / n
        x, y = R * math.cos(th), R * math.sin(th)
        p = 0.5 * rho * U**2 * flow.pressure_coefficient(x, y, U)  # gauge pressure
        ds = R * 2 * math.pi / n
        drag += -p * math.cos(th) * ds  # x-component of the pressure force (pressure acts inwards)
        lift += -p * math.sin(th) * ds
    return drag, lift


print(f"Cylinder R = {R} m in a {U} m/s air stream\n")
print(f"{'Gamma [m2/s]':>13} {'drag [N/m]':>11} {'lift [N/m]':>11} {'rho U Gamma':>12}  stagnation points")
for gamma in [0.0, -10.0, -20.0, -4 * math.pi * U * R]:
    flow = cylinder(U, R, gamma)
    d, l_ = surface_forces(flow)
    s = -gamma / (4 * math.pi * U * R)  # sin(theta) of the stagnation points
    where = (
        f"at {math.degrees(math.asin(s)) + 0.0:.0f} and {180 - math.degrees(math.asin(s)):.0f} deg"
        if abs(s) <= 1
        else "off the body"
    )
    print(
        f"{gamma + 0.0:>13.2f} {abs(d):>11.4f} {l_ + 0.0:>11.2f} {kutta_joukowski_lift(rho, U, -gamma) + 0.0:>12.2f}  {where}"
    )
print("\nDrag is zero for every circulation (d'Alembert's paradox): real cylinders have drag because")
print("viscous boundary layers separate (Week 11). The lift matches Kutta-Joukowski.")

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
xs = np.linspace(-2, 2, 300)
ys = np.linspace(-1.5, 1.5, 240)
X, Y = np.meshgrid(xs, ys)
for ax, gamma in zip(axes, [0.0, -20.0]):
    flow = cylinder(U, R, gamma)
    psi = np.vectorize(lambda a, b, f=flow: f.stream_function(a, b) if a * a + b * b > R * R else np.nan)(X, Y)
    ax.contour(X, Y, psi, levels=30, colors="tab:blue", linewidths=0.8)
    ax.add_patch(plt.Circle((0, 0), R, color="grey"))
    ax.set_aspect("equal")
    ax.set_title(f"Gamma = {gamma} m2/s")
fig.tight_layout()
fig.savefig("cylinder_flow.png", dpi=130)
print("Saved cylinder_flow.png")
