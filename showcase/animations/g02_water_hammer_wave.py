"""Animation 2: a water-hammer pressure wave racing up and down a pipeline.

The valve at the right closes in 0.5 s; the method of characteristics (fluidmech.transients)
tracks the pressure wave as it travels to the reservoir at 1200 m/s, reflects, and returns.
Saves water_hammer.gif.

# requires: matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from fluidmech import transients, viz  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
r = transients.moc_valve_closure(
    600, 0.5, 1200, 0.018, 1.5, 100, closure_time=0.5, sections=60, t_end=1.5 if QUICK else 4.0, snapshot_every=1
)
snaps = r["snapshots"][::2]  # every second time step keeps the GIF small

with viz.style("slides"):
    fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
    ax.fill_between(r["x"], r["head_min"], r["head_max"], color=viz.COLORS["sky"], alpha=0.25, lw=0, label="envelope")
    ax.axhline(0, color="0.5", lw=0.8)
    (line,) = ax.plot([], [], color=viz.COLORS["vermillion"], lw=3, label="head H(x, t)")
    label = ax.text(0.02, 0.92, "", transform=ax.transAxes)
    ax.text(0, -115, "reservoir", fontsize=11)
    ax.text(600, -115, "valve", fontsize=11, ha="right")
    ax.set(
        xlim=(0, 600),
        ylim=(-130, 320),
        xlabel="distance along pipe [m]",
        ylabel="head [m]",
        title="Water hammer after rapid valve closure",
    )
    ax.legend(loc="upper right", fontsize=11)

    def draw(k):
        t, heads = snaps[k]
        line.set_data(r["x"], heads)
        label.set_text(f"t = {t:4.2f} s")
        return line, label

    anim = FuncAnimation(fig, draw, frames=len(snaps), blit=True)
    anim.save("water_hammer.gif", writer=PillowWriter(fps=20), dpi=75)
print(f"Saved water_hammer.gif ({len(snaps)} frames)")
