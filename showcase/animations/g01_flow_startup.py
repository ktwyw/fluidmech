"""Animation 1: a pressure gradient is switched on and the flow between two plates starts up.

Momentum diffuses in from the walls; after about 0.5 h^2/nu the parabolic Poiseuille profile is
reached (Week 5). Saves flow_startup.gif.

# requires: matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from fluidmech import viz  # noqa: E402
from fluidmech.laminar import plates_velocity  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
nu, h, G, mu = 1e-6, 0.01, 0.1, 1e-3  # water, 10 mm gap, pressure gradient [Pa/m]
n = 41
dy = h / (n - 1)
dt = 0.4 * dy**2 / nu  # explicit stability limit 0.5, with margin
steady = [plates_velocity(i * dy, h, G, mu) for i in range(n)]
frames, u, t = [], [0.0] * n, 0.0
frame_every = 5.0 if not QUICK else 30.0  # (x 1/5) seconds of flow time between frames
next_frame = 0.0
while t <= 60.0:  # most of the development happens in the first ~50 s (0.5 h^2 / nu)
    if t >= next_frame:
        frames.append((t, list(u)))
        next_frame += frame_every / 5
    u = (
        [0.0]
        + [u[i] + dt * (G / 1000 + nu * (u[i + 1] - 2 * u[i] + u[i - 1]) / dy**2) for i in range(1, n - 1)]
        + [0.0]
    )
    t += dt

with viz.style("slides"):
    fig, ax = plt.subplots(figsize=(6, 4.2), constrained_layout=True)
    ys = [i * dy * 1000 for i in range(n)]
    ax.plot([v * 1000 for v in steady], ys, "k--", lw=1.2, label="steady Poiseuille")
    (line,) = ax.plot([], [], color=viz.COLORS["blue"], lw=3, label="u(y, t)")
    label = ax.text(0.05, 0.9, "", transform=ax.transAxes)
    ax.set(
        xlim=(0, max(steady) * 1100), ylim=(0, 10), xlabel="u [mm/s]", ylabel="y [mm]", title="Start-up of channel flow"
    )
    ax.legend(loc="lower right", fontsize=11)

    def draw(k):
        tt, prof = frames[k]
        line.set_data([v * 1000 for v in prof], ys)
        label.set_text(f"t = {tt:4.0f} s")
        return line, label

    anim = FuncAnimation(fig, draw, frames=len(frames), blit=True)
    anim.save("flow_startup.gif", writer=PillowWriter(fps=12), dpi=80)
print(f"Saved flow_startup.gif ({len(frames)} frames)")
