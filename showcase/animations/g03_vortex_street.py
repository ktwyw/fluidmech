"""Animation 3: the von Karman vortex street behind a cylinder (lattice-Boltzmann CFD).

Uses fluidmech.cfd.lbm_cylinder. The full animation needs about 2-3 minutes of computing.
Saves vortex_street.gif.

Set FLUIDMECH_QUICK=1 for a very short test run.
# requires: numpy, matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from fluidmech import cfd  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
steps, start, every = (400, 200, 100) if QUICK else (22000, 14000, 160)  # record only the developed wake
frames = [s["vorticity"].copy() for s in cfd.lbm_cylinder(steps=steps, snapshot_every=every) if s["step"] >= start]

fig, ax = plt.subplots(figsize=(7.5, 2.8), constrained_layout=True)
im = ax.imshow(frames[0], origin="lower", cmap="RdBu_r", vmin=-0.012, vmax=0.012)
ax.set_axis_off()
ax.set_title("Von Karman vortex street, Re = 100 (lattice Boltzmann)", fontsize=11)


def draw(k):
    im.set_data(frames[k])
    return (im,)


anim = FuncAnimation(fig, draw, frames=len(frames), blit=True)
anim.save("vortex_street.gif", writer=PillowWriter(fps=15), dpi=80)
print(f"Saved vortex_street.gif ({len(frames)} frames)")
