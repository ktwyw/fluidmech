"""CHME 202 - Week 14 - Example 1: power curves of stirred-tank impellers.

Power number Np = P / (rho N^3 D^5) versus impeller Reynolds number Re = rho N D^2 / mu.
Laminar: Np = Kp / Re (P ~ mu N^2 D^3); turbulent: Np ~ constant (P ~ rho N^3 D^5).
Saves power_curves.png. Impeller constants are representative values for baffled tanks.
Reading: McCabe, Smith & Harriott (agitation and mixing of liquids).

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import mixing as mx

fig, ax = plt.subplots(figsize=(7, 4.5))
res = [10 ** (i / 20) for i in range(0, 121)]  # Re 1 to 1e6
for name in mx.IMPELLERS:
    ax.loglog(res, [mx.power_number(r, name) for r in res], label=name.replace("_", " "))
ax.axvspan(10, 1e4, color="grey", alpha=0.1)
ax.text(100, 200, "transitional", ha="center")
ax.set(xlabel="impeller Reynolds number", ylabel="power number Np", title="Power curves (baffled tanks)")
ax.grid(alpha=0.3, which="both")
ax.legend()
fig.tight_layout()
fig.savefig("power_curves.png", dpi=130)

tank_d = 1.0  # tank diameter [m]
d = tank_d / 3
print(f"Rushton turbine D = {d:.2f} m in a {tank_d} m baffled tank (H = T, V = {3.1416 / 4:.2f} m3)\n")
print(f"{'liquid':<14} {'rpm':>5} {'Re':>9} {'regime':>12} {'Np':>6} {'P [W]':>8} {'P/V [W/m3]':>11}")
for name, rho, mu in [("water", 1000, 0.001), ("syrup", 1300, 0.5), ("polymer melt", 1000, 50.0)]:
    for rpm in (60, 180):
        n = rpm / 60  # rpm -> rev/s
        re = mx.impeller_reynolds(n, d, rho, mu)
        np_ = mx.power_number(re)
        p = mx.impeller_power(np_, rho, n, d)
        print(f"{name:<14} {rpm:>5} {re:>9.3g} {mx.mixing_regime(re):>12} {np_:>6.2f} {p:>8.1f} {p / 0.785:>11.1f}")
print("\nTripling the speed multiplies turbulent power by 27 but laminar power by only 9.")
print("Saved power_curves.png")
