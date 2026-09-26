"""Advanced 3: the Blasius boundary layer - a similarity solution by the shooting method.

Prandtl's boundary-layer equations for a flat plate reduce, with eta = y sqrt(U / nu x), to one
ODE: f''' + (1/2) f f'' = 0. Its solution gives the famous numbers delta_99 = 4.91 x / sqrt(Re_x)
and C_f = 0.664 / sqrt(Re_x) used in Weeks 9 and 11. Saves blasius.pdf/.png.

# requires: matplotlib
"""

import matplotlib

matplotlib.use("Agg")

from fluidmech import laminar, viz  # noqa: E402

b = laminar.blasius()
print("Blasius similarity solution (shooting + RK4):")
print(f"  f''(0) = {b['fpp0']:.5f}   (literature 0.33206)  ->  C_f,x = {2 * b['fpp0']:.3f} / sqrt(Re_x)")
print(f"  delta_99 = {b['delta99']:.2f} x / sqrt(Re_x)     (4.91)")
print(f"  displacement thickness = {b['delta_star']:.4f} x / sqrt(Re_x)   (1.7208)")
print(f"  momentum thickness     = {b['theta']:.4f} x / sqrt(Re_x)   (0.6641)")

with viz.style("paper"):
    fig, (ax1, ax2) = viz.figure("double", aspect=0.38, ncols=2)
    ax1.plot(b["fp"], b["eta"], label=r"$u/U = f'(\eta)$")
    ax1.plot(b["fpp"], b["eta"], "--", label=r"shear $f''(\eta)$")
    ax1.axhline(b["delta99"], color="0.6", lw=0.6)
    ax1.text(0.03, b["delta99"] + 0.15, r"$\delta_{99}$", fontsize="small")
    ax1.set(xlabel="dimensionless value", ylabel=r"$\eta = y\sqrt{U/\nu x}$", ylim=(0, 8))
    ax1.legend(loc="center right")
    U, nu = 5.0, 1.5e-5  # air at 5 m/s: the same profile in physical units grows like sqrt(x)
    for x in (0.1, 0.4, 0.9):
        scale = (nu * x / U) ** 0.5  # y = eta sqrt(nu x / U)
        ax2.plot([f * U for f in b["fp"]], [e * scale * 1000 for e in b["eta"]], label=f"x = {x} m")
    ax2.set(xlabel="$u$ [m/s]", ylabel="$y$ [mm]", ylim=(0, 12), title="air, $U$ = 5 m/s")
    ax2.legend()
    viz.label_panels([ax1, ax2], y=1.06)
    files = viz.savefig(fig, "blasius")
print("Saved", ", ".join(str(f) for f in files))
