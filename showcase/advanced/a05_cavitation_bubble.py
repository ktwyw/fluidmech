"""Advanced 5: collapse of a cavitation bubble (Rayleigh-Plesset equation).

A 1 mm vapour bubble formed at a pump inlet is carried into liquid at 1 bar. An empty cavity
collapses in Rayleigh's time 0.915 R0 sqrt(rho / dp) with the wall speed growing without limit;
a little non-condensable gas cushions the collapse and makes the bubble rebound. The extreme
wall velocities explain cavitation erosion of impellers (Week 10, NPSH).
Saves cavitation_bubble.pdf/.png.

# requires: matplotlib
"""

import matplotlib

matplotlib.use("Agg")

from fluidmech import cavitation, viz  # noqa: E402

R0, rho, dp = 1e-3, 998.0, 1e5  # initial radius [m], water density, driving pressure difference [Pa]
t_ray = cavitation.rayleigh_collapse_time(R0, rho, dp)
empty = cavitation.rayleigh_plesset(R0, dp + 2.34e3, 2 * t_ray, viscosity=0.0, surface_tension=0.0)
print(f"1 mm cavity, dp = 1 bar: Rayleigh collapse time {t_ray * 1e6:.1f} us, simulated {empty['t'][-1] * 1e6:.1f} us")
i10 = next(k for k, r in enumerate(empty["R"]) if r < 0.1 * R0)
print(f"  wall speed when R = 0.1 R0: {abs(empty['Rdot'][i10]):.0f} m/s; it grows as R^-1.5 without limit.")
print("  Once it approaches the speed of sound in water (~1480 m/s) the incompressible model is no longer")
print("  valid - liquid compressibility, not this equation, limits the collapse (shock waves, erosion).")
cases = {"pure vapour": 0.0, "gas 1 kPa": 1e3, "gas 5 kPa": 5e3}  # initial gas partial pressure
runs = {}
for label, pg in cases.items():
    runs[label] = cavitation.rayleigh_plesset(R0, 1e5, 4 * t_ray, gas_pressure=pg)
    print(f"  {label:<12} minimum radius {min(runs[label]['R']) / R0:.3f} R0")

with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("double", aspect=0.38, ncols=2)
    for label, r in runs.items():
        ax1.plot([t / t_ray for t in r["t"]], [x / R0 for x in r["R"]], label=label)
    ax1.set(xlabel=r"$t / t_\mathrm{Rayleigh}$", ylabel="$R / R_0$", ylim=(0, 1.05))
    ax1.legend(loc="lower left")
    ax2.loglog([x / R0 for x in empty["R"][1:]], [abs(v) for v in empty["Rdot"][1:]], color=viz.COLORS["black"])
    ax2.axhline(1480, ls="--", color=viz.COLORS["vermillion"])  # speed of sound in water
    ax2.text(0.9, 2200, "speed of sound: model invalid above", color=viz.COLORS["vermillion"], fontsize="x-small")
    ax2.set(xlabel="$R / R_0$", ylabel="wall speed $|\\dot R|$ [m/s]", title="empty cavity")
    ax2.invert_xaxis()
    viz.label_panels([ax1, ax2], y=1.06)
    files = viz.savefig(fig, "cavitation_bubble")
print("Saved", ", ".join(str(f) for f in files))
