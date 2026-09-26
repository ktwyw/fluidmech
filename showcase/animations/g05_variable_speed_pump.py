"""Animation 5: slowing a pump down - the operating point slides along the system curve.

As the speed falls, the pump curve shrinks by the affinity laws (H ~ N^2, Q ~ N); the power
falls roughly as N^3. Pump data are ILLUSTRATIVE. Saves variable_speed_pump.gif.

# requires: matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from fluidmech import Fluid, PumpCurve, pumps, viz  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
water = Fluid.water(20)
pump = PumpCurve.from_points([0.0, 0.04, 0.08, 0.12], [42.0, 40.0, 33.5, 22.5], [0.0, 0.62, 0.80, 0.68])
system = pumps.system_curve(12.0, 0.25, 800.0, water, 0.26e-3, 8.0)
speeds = [1.0 - 0.4 * k / (8 if QUICK else 40) for k in range((8 if QUICK else 40) + 1)]
speeds += speeds[::-1]  # slow down, then speed up again
qs = [0.14 * i / 100 for i in range(101)]
full = pumps.operating_point(pump, system, water.density)

with viz.style("slides"):
    fig, ax = plt.subplots(figsize=(6.5, 4.3), constrained_layout=True)
    ax.plot([q * 1000 for q in qs], [system(q) for q in qs], color=viz.COLORS["green"], lw=3, label="system curve")
    ax.plot([q * 1000 for q in qs], [pump.head(q) for q in qs], color="0.75", lw=1.5, label="pump, 100 % speed")
    (curve,) = ax.plot([], [], color=viz.COLORS["blue"], lw=3, label="pump at speed N")
    (point,) = ax.plot([], [], "o", color=viz.COLORS["vermillion"], ms=11)
    label = ax.text(0.03, 0.06, "", transform=ax.transAxes, fontsize=12, family="monospace")
    ax.set(xlim=(0, 140), ylim=(0, 48), xlabel="flow [L/s]", ylabel="head [m]", title="Variable-speed pump")
    ax.legend(loc="upper right", fontsize=11)

    def draw(k):
        s = speeds[k]
        c = pump.scaled(speed_ratio=s)
        op = pumps.operating_point(c, system, water.density)
        curve.set_data([q * 1000 for q in qs], [max(c.head(q), -1) for q in qs])
        point.set_data([op.flow_rate * 1000], [op.head])
        label.set_text(
            f"N = {s:4.0%}   Q = {op.flow_rate * 1000:5.1f} L/s   P = {op.shaft_power / 1e3:5.1f} kW\n"
            f"(full speed: {full.shaft_power / 1e3:.1f} kW)"
        )
        return curve, point, label

    anim = FuncAnimation(fig, draw, frames=len(speeds), blit=True)
    anim.save("variable_speed_pump.gif", writer=PillowWriter(fps=12), dpi=80)
print(f"Saved variable_speed_pump.gif ({len(speeds)} frames)")
