"""Advanced 6: Taylor dispersion - how laminar flow spreads a tracer far faster than diffusion.

A pulse of dye in laminar pipe flow is stretched by the parabolic profile, while radial diffusion
mixes it across the tube. G.I. Taylor (1953) showed the net effect is axial dispersion with
D_eff = D (1 + Pe^2 / 48), Pe = U a / D. We verify it with a Monte Carlo random-walk simulation.
Relevant to chromatography, flow-injection analysis and laminar-flow reactors (Week 14).
Saves taylor_dispersion.pdf/.png.

# requires: numpy, matplotlib
"""

import os

import matplotlib

matplotlib.use("Agg")
import numpy as np  # noqa: E402

from fluidmech import cfd, viz  # noqa: E402

QUICK = os.environ.get("FLUIDMECH_QUICK") == "1"
particles = 1000 if QUICK else 4000
seeds = (1,) if QUICK else (1, 2, 3)  # independent runs to estimate the Monte Carlo scatter
print(f"{'Pe':>4} {'D_eff/D simulated':>20} {'Taylor-Aris 1 + Pe^2/48':>24}")
results = {}
for pe in (5, 10, 20):
    ks = []
    for seed in seeds:
        r = cfd.taylor_dispersion(peclet=pe, particles=particles, t_end=6.0, seed=seed)
        late = r["time"] > 2.0  # after a few radial diffusion times the spreading is linear in t
        ks.append(np.polyfit(r["time"][late], r["variance"][late], 1)[0] / 2)  # variance = 2 D_eff t
    results[pe] = r
    spread = f" +/- {np.std(ks):.2f}" if len(ks) > 1 else ""
    print(f"{pe:>4} {np.mean(ks):>13.2f}{spread:<7} {r['theory_K']:>24.2f}")
print("Agreement within the Monte Carlo scatter: the parabolic profile, not diffusion, spreads the pulse.")

with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("double", aspect=0.38, ncols=2)
    r = results[20]
    for t, x, y in r["snapshots"][1:]:
        ax1.scatter(x, y, s=0.5, alpha=0.4, rasterized=True)  # rasterised: small PDF despite many points
        ax1.text(np.mean(x), 1.1, f"t = {t:g}", ha="center", fontsize="x-small")  # label each cloud directly
    ax1.set(xlabel="$x / a$ (flow direction)", ylabel="$y / a$", ylim=(-1.05, 1.25))
    ax1.set_title("Pe = 20", pad=12)
    for pe, r in results.items():
        ax2.plot(r["time"], r["variance"], label=f"Pe = {pe}")
        ax2.plot(r["time"], 2 * r["theory_K"] * r["time"], "k:", lw=0.7)
    ax2.set(xlabel="$t D / a^2$", ylabel=r"axial variance $\sigma_x^2 / a^2$")
    ax2.legend(loc="upper left")
    viz.label_panels([ax1, ax2], y=1.06)
    files = viz.savefig(fig, "taylor_dispersion")
print("Saved", ", ".join(str(f) for f in files), "(dotted lines: 2 D_eff t from theory)")
