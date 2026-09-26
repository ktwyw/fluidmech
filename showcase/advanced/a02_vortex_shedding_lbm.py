"""Advanced 2: the von Karman vortex street by the lattice-Boltzmann method.

Behind a cylinder at Re = 100 the wake becomes unstable and sheds vortices alternately from
each side, at a frequency given by the Strouhal number St = f D / U. The lattice-Boltzmann
method (LBM) simulates the flow with 'particle populations' streaming and colliding on a grid -
a modern CFD technique that is simple to program. Saves vortex_street.pdf/.png.
The full run takes about 2-3 minutes.

Set FLUIDMECH_QUICK=1 for a short run (shedding not yet developed).
# requires: numpy, matplotlib
"""

import os
import time

import matplotlib

matplotlib.use("Agg")

from fluidmech import cfd, viz  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
steps = 600 if QUICK else 25000  # lattice time steps
t0 = time.time()
last = None
for snap in cfd.lbm_cylinder(nx=300, ny=100, radius=10, u_in=0.06, reynolds=100, steps=steps, snapshot_every=steps):
    last = snap
print(
    f"LBM: 300 x 100 lattice, cylinder D = {last['diameter']} cells, Re = 100, {steps} steps ({time.time() - t0:.0f} s)"
)
if not QUICK:
    st = cfd.strouhal_from_signal(last["probe_v"], last["diameter"], last["u_in"])
    print(f"  Strouhal number St = {st:.3f}")
    print("  Unconfined reference at Re = 100: St = 0.164 (Williamson 1996). This domain is only 5 D wide")
    print("  with periodic sides, which acts like confinement and raises St; a 9 D wide domain gives 0.179.")

with viz.style("paper"):
    fig, ax = viz.figure("double", aspect=0.36)
    vort = last["vorticity"] / (last["u_in"] / last["diameter"])  # vorticity scaled by U / D
    extent = [0, vort.shape[1] / last["diameter"], 0, vort.shape[0] / last["diameter"]]
    im = ax.imshow(vort, origin="lower", cmap="RdBu_r", vmin=-3, vmax=3, extent=extent)
    ax.set(xlabel="$x / D$", ylabel="$y / D$", title=f"Vorticity $\\omega D / U$, Re = 100, step {last['step']}")
    fig.colorbar(im, ax=ax, shrink=0.8)
    files = viz.savefig(fig, "vortex_street")
print("Saved", ", ".join(str(f) for f in files))
