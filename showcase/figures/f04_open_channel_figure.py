"""Publication figure 4: open-channel flow - specific energy diagram and water-surface profiles.

Demonstrates: annotated curves, shaded regions, and physical-coordinate plots with a shared
style. Saves fig_open_channel.*

# requires: matplotlib
"""

import matplotlib

matplotlib.use("Agg")

from fluidmech import viz  # noqa: E402
from fluidmech.open_channel import RectangularChannel, TrapezoidalChannel, gvf_profile  # noqa: E402

with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("double", aspect=0.36, ncols=2)
    ch = RectangularChannel(3.0)
    for q in (3.0, 6.0, 9.0):
        yc = ch.critical_depth(q)
        ys = [yc * (0.25 + 0.01 * i) for i in range(500)]
        ax1.plot([ch.specific_energy(y, q) for y in ys], ys, label=f"Q = {q:g} m$^3$/s")
        ax1.plot(ch.specific_energy(yc, q), yc, "k.", ms=5, label="critical depth" if q == 9.0 else None)
    ax1.plot([0, 4], [0, 4], ":", color="0.5", lw=0.7)
    ax1.text(3.2, 2.9, "$E = y$", fontsize="small", color="0.4")
    # the region E < y is physically impossible, so it is free space for annotations
    ax1.text(0.12, 3.25, "upper branches: subcritical", fontsize="small")
    ax1.text(0.12, 3.02, "lower branches: supercritical", fontsize="small")
    ax1.set(xlim=(0, 4), ylim=(0, 3.5), xlabel="specific energy $E$ [m]", ylabel="depth $y$ [m]")
    ax1.legend(loc="center right")
    canal = TrapezoidalChannel(4.0, 1.5)
    q, n, s0 = 25.0, 0.012, 0.0008
    yn, yc = canal.normal_depth(q, n, s0), canal.critical_depth(q)
    for label, y0, col in (
        ("M1 (behind a weir)", 2.8, viz.COLORS["blue"]),
        ("M2 (towards a drop)", 1.01 * yc, viz.COLORS["vermillion"]),
    ):
        prof = gvf_profile(canal, q, n, s0, y0, (1.01 if y0 > yn else 0.99) * yn, steps=80)
        # both profiles start at their control section (x = 0) and are computed upstream (x < 0);
        # the bed rises upstream, so water-surface elevation = -S0 x + y
        ax2.plot([p[0] for p in prof], [-s0 * p[0] + p[1] for p in prof], color=col, label=label)
    xs = [-3000 + 30 * i for i in range(101)]
    ax2.plot(xs, [-s0 * x + yn for x in xs], "--", color="0.4", lw=0.8, label="normal depth")
    ax2.plot(xs, [-s0 * x for x in xs], color="saddlebrown", lw=1.5, label="bed")
    ax2.set(xlabel="distance [m] (control at x = 0)", ylabel="elevation [m]", xlim=(-3000, 0))
    ax2.legend(loc="upper right", fontsize="x-small")
    viz.label_panels([ax1, ax2], y=1.04)
    files = viz.savefig(fig, "fig_open_channel", ("pdf", "png", "svg"))
print("Saved", ", ".join(str(f) for f in files))
