"""Publication figure 1: pipe flow in three panels (Moody chart, velocity profiles, non-circular ducts).

Demonstrates: a double-column multi-panel layout, log axes, direct labelling instead of legends,
panel letters, and export to vector PDF/SVG plus 300-dpi PNG. Saves fig_pipe_flow.*

# requires: matplotlib
"""

import matplotlib

matplotlib.use("Agg")

from fluidmech import laminar, turbulence, viz  # noqa: E402

with viz.style("paper"):
    fig, axes = viz.figure("double", aspect=0.34, ncols=3)
    ax1, ax2, ax3 = axes
    # (a) Moody chart with a few 'measurements' from the Week 9 lab
    viz.moody_chart(ax1, relative_roughness=(0, 1e-4, 1e-3, 1e-2), label=False)
    ax1.plot(
        [1.8e3, 6e3, 2e4, 8e4],
        [0.036, 0.036, 0.026, 0.0195],
        "s",
        mfc="white",
        ms=3.5,
        color=viz.COLORS["black"],
        label="lab data",
    )
    ax1.legend(loc="upper right")
    # (b) laminar parabola vs turbulent power-law and log-law profiles
    rs = [i / 200 for i in range(201)]  # r / R
    ax2.plot([1 - r**2 for r in rs], rs, label="laminar")
    for re in (1e4, 1e6):
        n = turbulence.power_law_exponent(re)
        ax2.plot([(1 - r) ** (1 / n) for r in rs], rs, label=f"turbulent, Re = {re:.0e}")
    ax2.set(xlabel=r"$u / U_{max}$", ylabel="$r / R$", xlim=(0, 1.02), ylim=(0, 1))
    ax2.legend(loc="lower left")
    # (c) laminar friction constant for rectangular ducts and annuli
    ks = [0.01 + 0.98 * i / 100 for i in range(101)]
    ax3.plot(ks, [laminar.rectangular_duct_fre(k) for k in ks], label="rectangle, aspect ratio")
    ax3.plot(ks, [laminar.annulus_fre(k) for k in ks], label="annulus, $R_i/R_o$")
    ax3.axhline(64, ls=":", color="0.4")
    ax3.text(0.5, 65.5, "circular pipe, 64", ha="center", fontsize="small", color="0.3")
    ax3.set(xlabel="shape parameter", ylabel=r"$f\,Re$ (laminar, based on $D_h$)", ylim=(50, 100))
    ax3.legend(loc="center right")
    viz.label_panels(axes, y=1.04)
    files = viz.savefig(fig, "fig_pipe_flow", ("pdf", "png", "svg"))
print("Saved", ", ".join(str(f) for f in files))
