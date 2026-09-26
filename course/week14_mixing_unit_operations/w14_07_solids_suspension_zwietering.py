"""CHME 202 - Week 14 - Example 7: suspending solids - the just-suspended speed (Zwietering 1958).

N_js = S nu^0.1 (g drho / rho_L)^0.45 X^0.13 d_p^0.2 D^-0.85
(N in rev/s, nu in m2/s, X = solids mass per 100 kg liquid, d_p and D in m; S depends
on impeller type and geometry, ~6 used here as an illustration.)
Catalyst slurries, crystallisers and leaching tanks are designed around N_js.
"""

from fluidmech import mixing as mx
from fluidmech.constants import G

rho_l, mu = 1000.0, 1e-3  # water
nu = mu / rho_l
S = 6.0  # Zwietering geometry constant (illustrative)
rho_s, X = 2500.0, 10.0  # sand-like solids, 10 kg per 100 kg liquid


def n_js(d_p, D):
    return S * nu**0.1 * (G * (rho_s - rho_l) / rho_l) ** 0.45 * X**0.13 * d_p**0.2 * D ** (-0.85)


print("Just-suspended speed in a 1 m tank with a D = T/3 impeller:")
for d_um in [50, 100, 200, 500]:
    n = n_js(d_um * 1e-6, 1 / 3)
    tank = mx.StirredTank(1.0, 1 / 3, "pitched_blade_45")
    p = tank.analyse(n, rho_l, mu)
    print(f"  d_p = {d_um:>3} um: N_js = {n * 60:5.0f} rpm, P/V = {p['power_per_volume_W_m3']:6.0f} W/m3")
print("\nScale-up at constant geometry (d_p = 200 um):")
for T in [0.3, 1.0, 3.0]:
    n = n_js(200e-6, T / 3)
    pv = mx.StirredTank(T, T / 3, "pitched_blade_45").analyse(n, rho_l, mu)["power_per_volume_W_m3"]
    print(f"  T = {T} m: N_js = {n * 60:5.0f} rpm, P/V = {pv:6.0f} W/m3")
print("N_js ~ D^-0.85, so P/V ~ N^3 D^2 ~ D^-0.55: large tanks need LESS power per volume to suspend")
print("solids than constant-P/V scale-up would give. Axial-flow impellers suspend solids most efficiently.")
