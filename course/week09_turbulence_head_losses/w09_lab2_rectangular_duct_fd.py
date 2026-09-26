"""CHME 202 - Week 9 - Lab Assignment 2 (Python version): laminar flow in a rectangular duct by finite differences.

Fully developed flow satisfies the Poisson equation  d2u/dy2 + d2u/dz2 = -G / mu
with u = 0 on the walls. We solve it on a grid with successive over-relaxation (SOR),
compute the friction factor, and compare f*Re with the Shah & London correlation
used in pipe_flow/laminar. This is exactly what COMSOL does, on a structured grid.
Saves lab2_duct_velocity.png.

# requires: numpy, matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np

from fluidmech.laminar import rectangular_duct_fre


def solve_duct(aspect: float, n: int = 41, tol: float = 1e-8, mu: float = 1.0, G: float = 1.0):
    """Solve on a duct of width 1 and height = aspect. Returns (u, dy, dz, iterations)."""
    width, height = 1.0, aspect
    ny = n
    nz = max(int(round(n * aspect)), 5)
    dy, dz = width / (ny - 1), height / (nz - 1)
    u = np.zeros((nz, ny))
    omega = 2 / (1 + np.sin(np.pi / max(ny, nz)))  # near-optimal SOR factor
    ay, az = 1 / dy**2, 1 / dz**2
    for it in range(20000):  # SOR sweeps until the largest change is below tol
        max_change = 0.0
        for j in range(1, nz - 1):
            for i in range(1, ny - 1):
                # 5-point discretisation of the Poisson equation
                new = ((u[j, i + 1] + u[j, i - 1]) * ay + (u[j + 1, i] + u[j - 1, i]) * az + G / mu) / (2 * (ay + az))
                change = omega * (new - u[j, i])
                u[j, i] += change
                max_change = max(max_change, abs(change))
        if max_change < tol:
            return u, dy, dz, it + 1
    return u, dy, dz, it + 1


print(f"{'aspect':>7} {'grid':>9} {'iterations':>11} {'fRe (FD)':>9} {'fRe (Shah-London)':>18} {'error':>7}")
results = {}
for aspect in [1.0, 0.5, 0.25]:
    u, dy, dz, its = solve_duct(aspect)
    mean = np.trapezoid(np.trapezoid(u, dx=dy, axis=1), dx=dz) / (1.0 * aspect)
    area, perim = aspect, 2 * (1 + aspect)
    dh = 4 * area / perim  # hydraulic diameter
    # G = f/Dh * rho V^2 / 2 and Re = rho V Dh / mu  ->  fRe = 2 G Dh^2 / (mu V) with G = mu = 1
    fre = 2 * dh**2 / mean  # with G = mu = 1: fRe = 2 G Dh^2 / (mu V)
    ref = rectangular_duct_fre(aspect)
    results[aspect] = u
    print(f"{aspect:>7} {u.shape[1]:>4}x{u.shape[0]:<4} {its:>11} {fre:>9.2f} {ref:>18.2f} {fre / ref - 1:>+7.1%}")
print("\nThe numerical fRe converges to the correlation as the grid is refined (try n = 81).")
print("Questions for the report: how does the error scale with grid spacing? how does the")
print("maximum velocity compare with the mean? where is the wall shear stress largest?")

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
for ax, (aspect, u) in zip(axes, results.items()):
    im = ax.imshow(u / u.max(), origin="lower", extent=[0, 1, 0, aspect], cmap="viridis")
    ax.contour(
        np.linspace(0, 1, u.shape[1]),
        np.linspace(0, aspect, u.shape[0]),
        u / u.max(),
        levels=8,
        colors="w",
        linewidths=0.6,
    )
    ax.set_title(f"aspect ratio {aspect}")
    ax.set_aspect("equal")
fig.colorbar(im, ax=axes, label="u / u_max", shrink=0.8)
fig.savefig("lab2_duct_velocity.png", dpi=130)
print("Saved lab2_duct_velocity.png")
