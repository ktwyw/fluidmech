"""Animation 4: a tracer pulse in laminar pipe flow - stretched by the parabolic profile, smoothed by diffusion.

Viewed in a frame moving with the mean velocity, the cloud first shears into an arrowhead,
then spreads into a Gaussian that grows much faster than by diffusion alone (Taylor dispersion).
Saves taylor_dispersion.gif.

# requires: numpy, matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from fluidmech import cfd  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
pe = 20.0
times = np.round(np.linspace(0.01, 0.6 if QUICK else 2.5, 12 if QUICK else 60), 3)
res = cfd.taylor_dispersion(peclet=pe, particles=1500, t_end=float(times[-1]) + 0.01, snapshot_times=tuple(times))

fig, ax = plt.subplots(figsize=(7, 3.2), constrained_layout=True)
scat = ax.scatter([], [], s=2, c=[], cmap="viridis", vmin=0, vmax=1)
label = ax.text(0.02, 0.88, "", transform=ax.transAxes)
ax.set(
    xlim=(-30, 30),
    ylim=(-1.05, 1.05),
    xlabel="x - U t  (moving with the mean flow) / a",
    ylabel="y / a",
    title=f"Taylor dispersion, Pe = {pe:g}",
)


def draw(k):
    t, x, y = res["snapshots"][k]
    scat.set_offsets(np.c_[x - pe * t, y])  # subtract the mean displacement U t (U = Pe in these units)
    scat.set_array(np.abs(y))  # colour by distance from the axis: fast core, slow wall
    label.set_text(f"t = {t:.2f} a$^2$/D")
    return scat, label


anim = FuncAnimation(fig, draw, frames=len(res["snapshots"]), blit=True)
anim.save("taylor_dispersion.gif", writer=PillowWriter(fps=12), dpi=80)
print(f"Saved taylor_dispersion.gif ({len(res['snapshots'])} frames)")
