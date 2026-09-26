"""Advanced 1: 2D CFD of a lid-driven cavity, validated against Ghia, Ghia & Shin (1982).

The lid of a square cavity slides at speed U and drags the fluid into a large primary vortex
with small counter-rotating corner eddies. This is THE benchmark every CFD code is tested
on. We solve the incompressible Navier-Stokes equations (stream function-vorticity form)
and compare the centreline velocity with the published reference data.
Saves cavity_re100.pdf/.png.

Set FLUIDMECH_QUICK=1 for a fast, coarse run.
# requires: numpy, scipy, matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import numpy as np  # noqa: E402

from fluidmech import cfd, viz  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
n = 33 if QUICK else 65  # grid points per side
res = cfd.lid_driven_cavity(n, reynolds=100.0, t_end=15.0 if QUICK else 30.0)
x, y, psi = res["x"], res["y"], res["psi"]
u_centre = res["u"][:, n // 2]  # u(y) along the vertical centreline x = 0.5

err = max(abs(np.interp(yg, y, u_centre) - ug) for yg, ug in zip(cfd.GHIA_RE100_Y, cfd.GHIA_RE100_U))
j, i = np.unravel_index(np.argmin(psi), psi.shape)
print(f"Lid-driven cavity, Re = 100, {n}x{n} grid, converged after {res['steps']} time steps")
print(f"  primary vortex: psi_min = {psi.min():.4f} at ({x[i]:.3f}, {y[j]:.3f})   Ghia: -0.1034 at (0.617, 0.734)")
print(f"  centreline u: max deviation from Ghia et al. = {err:.4f} (lid speed = 1)")

with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("double", aspect=0.42, ncols=2)
    # streamlines: evenly spaced in the main vortex plus a few weak levels for the corner eddies
    levels = np.sort(np.concatenate([np.linspace(psi.min(), -1e-4, 12), [0.0, 1e-6, 1e-5, 5e-5]]))
    ax1.contour(x, y, psi, levels=levels, colors="k", linewidths=0.5)
    im = ax1.contourf(x, y, res["w"], levels=np.linspace(-5, 5, 41), cmap="RdBu_r", extend="both")
    fig.colorbar(im, ax=ax1, label=r"vorticity $\omega$", shrink=0.85)
    ax1.annotate("", xy=(0.8, 1.035), xytext=(0.2, 1.035), arrowprops={"arrowstyle": "->"}, annotation_clip=False)
    ax1.text(0.5, 1.05, "moving lid, $U = 1$", ha="center", va="bottom")
    ax1.set(aspect="equal", xlabel="$x$", ylabel="$y$", xlim=(0, 1), ylim=(0, 1))
    ax2.plot(u_centre, y, color=viz.COLORS["blue"], label=f"fluidmech ({n}$\\times${n})")
    ax2.plot(
        cfd.GHIA_RE100_U,
        cfd.GHIA_RE100_Y,
        "o",
        mfc="none",
        color=viz.COLORS["vermillion"],
        ms=4,
        label="Ghia et al. (1982)",
    )
    ax2.axvline(0, color="0.6", lw=0.5)
    ax2.set(xlabel="$u$ at $x = 0.5$", ylabel="$y$", ylim=(0, 1))
    ax2.legend(loc="center right")
    viz.label_panels([ax1, ax2], y=1.08)
    files = viz.savefig(fig, "cavity_re100")
print("Saved", ", ".join(str(f) for f in files))
