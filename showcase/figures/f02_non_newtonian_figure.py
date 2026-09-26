"""Publication figure 2: non-Newtonian fluids - flow curves and pipe velocity profiles.

Demonstrates: consistent colours shared between two panels, a log-log inset-free layout,
and profiles normalised by the mean velocity so shapes can be compared. Saves fig_non_newtonian.*

# requires: matplotlib
"""

import math

import matplotlib

matplotlib.use("Agg")

from fluidmech import laminar, rheology, viz  # noqa: E402

models = {  # label: (rheology model, pipe-profile function returning u/u_mean at r/R)
    "Newtonian": rheology.Newtonian(0.5),
    "shear-thinning, n = 0.4": rheology.PowerLaw(2.0, 0.4),
    "shear-thickening, n = 1.6": rheology.PowerLaw(0.1, 1.6),
    "Bingham, $\\tau_y$ = 5 Pa": rheology.Bingham(5.0, 0.2),
}
colors = [viz.COLORS[c] for c in ("black", "blue", "vermillion", "green")]
rates = [10 ** (i / 20 - 1) for i in range(81)]  # 0.1 to 1000 1/s
with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("onehalf", aspect=0.45, ncols=2)
    for (label, model), col in zip(models.items(), colors):
        ax1.loglog(rates, [model.stress(g) for g in rates], color=col, label=label)
    ax1.set(xlabel=r"shear rate $\dot\gamma$ [1/s]", ylabel=r"shear stress $\tau$ [Pa]")
    ax1.legend(loc="upper left", fontsize="x-small")
    R, G = 1.0, 40.0  # dimensionless pipe radius and pressure gradient for the profiles
    rs = [i / 200 for i in range(201)]
    for n, col in ((1.0, colors[0]), (0.4, colors[1]), (1.6, colors[2])):
        q = laminar.power_law_pipe_flow_rate(G, R, 1.0, n)
        u_mean = q / (math.pi * R**2)
        ax2.plot([laminar.power_law_pipe_velocity(r, R, G, 1.0, n) / u_mean for r in rs], rs, color=col)
    tau_y = 0.4 * G * R / 2  # yield stress = 40 % of the wall stress
    q = laminar.bingham_pipe_flow_rate(G, R, tau_y, 1.0)
    u_mean = q / (math.pi * R**2)
    ax2.plot([laminar.bingham_pipe_velocity(r, R, G, tau_y, 1.0) / u_mean for r in rs], rs, color=colors[3])
    ax2.axhspan(0, laminar.bingham_plug_radius(G, tau_y), color=colors[3], alpha=0.1)
    ax2.text(0.05, 0.25, "plug", color=colors[3], fontsize="small")
    ax2.set(
        xlabel=r"$u / \bar u$", ylabel="$r / R$", xlim=(0, 2.4), ylim=(0, 1)
    )  # n = 1.6 peaks at (3n+1)/(n+1) = 2.23
    viz.label_panels([ax1, ax2], y=1.04)
    files = viz.savefig(fig, "fig_non_newtonian", ("pdf", "png", "svg"))
print("Saved", ", ".join(str(f) for f in files))
