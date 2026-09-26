"""Advanced 4: water hammer by the method of characteristics (MOC).

A valve at the end of a 600 m pipeline closes in 0.5, 2 or 5 s. MOC turns the unsteady
pipe-flow equations into ODEs along the characteristic lines dx/dt = +/- c, which we march on a
grid. Fast closure (< 2L/c) produces the full Joukowsky surge; slow closure lets the reflected
wave relieve the pressure (compare examples 21 and 48). Saves water_hammer.pdf/.png.

# requires: matplotlib
"""

import matplotlib

matplotlib.use("Agg")

from fluidmech import transients, viz  # noqa: E402
from fluidmech.constants import G  # noqa: E402

L, D, c, f, V0, H0 = (
    600.0,
    0.5,
    1200.0,
    0.018,
    1.5,
    100.0,
)  # length, diameter, wave speed, friction, velocity, reservoir head
print(f"Pipe {L:.0f} m, D = {D} m, c = {c:.0f} m/s, V0 = {V0} m/s: pipe period 2L/c = {2 * L / c:.1f} s")
print(f"Joukowsky surge c V0 / g = {c * V0 / G:.0f} m\n")
runs = {}
for tc in (0.5, 2.0, 5.0):
    r = transients.moc_valve_closure(L, D, c, f, V0, H0, closure_time=tc, sections=30, t_end=12.0)
    runs[tc] = r
    rise = max(r["head_valve"]) - r["head_valve"][0]
    print(f"  closure in {tc:3.1f} s: peak head at the valve {max(r['head_valve']):6.1f} m (+{rise:5.1f} m)")

with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("double", aspect=0.38, ncols=2)
    for tc, r in runs.items():
        ax1.plot(r["time"], r["head_valve"], label=f"$t_c$ = {tc} s")
    jouk = runs[0.5]["head_valve"][0] + c * V0 / G
    ax1.axhline(jouk, ls=":", color="0.4")
    ax1.text(7.5, jouk + 5, "Joukowsky", fontsize="small", color="0.3")
    ax1.set(xlabel="time [s]", ylabel="head at the valve [m]", ylim=(-140, 320))
    ax1.legend(loc="lower center", ncol=3)
    r = runs[0.5]
    ax2.fill_between(r["x"], r["head_min"], r["head_max"], color=viz.COLORS["sky"], alpha=0.4, label="envelope")
    ax2.plot(r["x"], [H0 - (H0 - r["head_valve"][0]) * xx / L for xx in r["x"]], "k--", label="steady HGL")
    ax2.set(xlabel="distance from reservoir [m]", ylabel="head [m]", title="$t_c$ = 0.5 s")
    ax2.legend(loc="upper left")
    viz.label_panels([ax1, ax2], y=1.06)
    files = viz.savefig(fig, "water_hammer")
print("\nSaved", ", ".join(str(f) for f in files))
lowest = min(runs[0.5]["head_min"])
if lowest < -10.3:  # heads more than ~10 m below the pipe are impossible: the water would boil
    print(f"The fast closure predicts heads down to {lowest:.0f} m - impossible in reality: the liquid column would")
    print("separate (cavitate) at about -10 m, and the collapse of the vapour cavity causes a second surge.")
