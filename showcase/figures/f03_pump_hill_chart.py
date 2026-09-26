"""Publication figure 3: a pump 'hill chart' - efficiency contours over the whole operating map.

For every (Q, H) point we find the speed at which the pump passes through it (affinity laws) and
the efficiency there; contours of efficiency form the hill. Overlaid: constant-speed curves and
the system curve. Demonstrates contour plots with labelled levels. Pump data are ILLUSTRATIVE.
Saves fig_pump_hill_chart.*

# requires: matplotlib, numpy
"""

import matplotlib

matplotlib.use("Agg")
import numpy as np  # noqa: E402

from fluidmech import Fluid, PumpCurve, pumps, viz  # noqa: E402
from fluidmech.solvers import bisect  # noqa: E402

pump = PumpCurve.from_points([0.0, 0.04, 0.08, 0.12], [42.0, 40.0, 33.5, 22.5], [0.0, 0.62, 0.80, 0.68])
system = pumps.system_curve(12.0, 0.25, 800.0, Fluid.water(20), 0.26e-3, 8.0)
qs = np.linspace(0.002, 0.14, 120)
hs = np.linspace(1.0, 50.0, 120)
eta = np.full((hs.size, qs.size), np.nan)
for i, h in enumerate(hs):
    for j, q in enumerate(qs):
        # speed ratio r at which the scaled curve passes through (q, h): h = r^2 H(q / r)
        f = lambda r, q=q, h=h: pump.scaled(speed_ratio=r).head(q) - h  # noqa: E731
        if f(0.3) * f(1.2) < 0:
            r = bisect(f, 0.3, 1.2)
            eta[i, j] = pump.efficiency(q / r)  # efficiency is unchanged at corresponding points
with viz.style("paper"):
    fig, ax = viz.figure("single", aspect=0.85)
    # top band must include the peak efficiency, otherwise contourf leaves the best-efficiency ridge blank
    top = max(82.0, float(np.nanmax(eta)) * 100 + 0.5)
    cs = ax.contourf(qs * 1000, hs, eta * 100, levels=[40, 50, 60, 65, 70, 75, 78, 80, top], cmap="Blues")
    lines = ax.contour(qs * 1000, hs, eta * 100, levels=[50, 60, 70, 75, 78], colors="k", linewidths=0.4)
    ax.clabel(lines, fmt="%d %%", fontsize=6)
    for s in (0.6, 0.7, 0.8, 0.9, 1.0):
        c = pump.scaled(speed_ratio=s)
        ax.plot(qs * 1000, [c.head(q) for q in qs], color="0.25", lw=0.6)
        ax.text(3, c.head(0.002) + 0.8, f"{s:.0%}", fontsize=6, color="0.25")
    ax.plot(qs * 1000, [system(q) for q in qs], color=viz.COLORS["vermillion"], lw=1.4, label="system curve")
    ax.set(xlabel="flow [L/s]", ylabel="head [m]", xlim=(0, 140), ylim=(0, 50))
    ax.legend(loc="upper right")
    fig.colorbar(cs, ax=ax, label="efficiency [%]", format="%.0f")
    files = viz.savefig(fig, "fig_pump_hill_chart", ("pdf", "png", "svg"))
print("Saved", ", ".join(str(f) for f in files))
print("Reading the chart: the system curve cuts the efficiency contours - running slower moves the duty")
print("along it into regions of lower efficiency, a trade-off that the energy calculation must include.")
