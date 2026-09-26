"""CHME 202 - Week 14 - Example 4: macro-, meso- and micromixing versus reaction speed.

Mixing happens on several scales: the tank circulates fluid (blend time), turbulent
eddies break it up, and finally molecular-scale mixing occurs within the Kolmogorov
eddies (micromixing, t_E ~ 17 (nu/eps)^1/2). A reaction is 'mixing sensitive'
when its characteristic time is comparable to or shorter than the relevant mixing time.
"""

from fluidmech import mixing as mx
from fluidmech.turbulence import kolmogorov_scales

rho, mu = 1000.0, 1e-3  # water
nu = mu / rho
tank = mx.StirredTank(2.0, 2.0 / 3)
r = tank.analyse(1.5, rho, mu)
eps_mean = r["dissipation_W_kg"]
print(f"6.3 m3 tank at 90 rpm: mean dissipation {eps_mean:.3f} W/kg, blend time {r['blend_time_s']:.0f} s\n")
print(f"{'location':<22} {'eps [W/kg]':>11} {'eta_K [um]':>11} {'t_micro [ms]':>13}")
for where, factor in [("bulk (far from blades)", 0.2), ("tank average", 1.0), ("impeller discharge", 20.0)]:
    eps = eps_mean * factor
    eta, _, _ = kolmogorov_scales(eps, nu)
    print(f"{where:<22} {eps:>11.3f} {eta * 1e6:>11.0f} {mx.micromixing_time(eps, nu) * 1000:>13.1f}")
print("\nFeeding a fast reagent into the impeller discharge rather than the quiet surface")
print("shortens its micromixing time ~10x.\n")

t_micro = mx.micromixing_time(eps_mean, nu)
print(f"{'reaction half-life':>19} {'Da_micro':>9} {'Da_macro':>9}  verdict")
for t_half in [100.0, 1.0, 0.01, 1e-4]:
    t_r = t_half / 0.693  # first-order reaction time 1/k from the half-life
    da_mi = mx.damkohler(t_micro, t_r)
    da_ma = mx.damkohler(r["blend_time_s"], t_r)
    if da_ma < 0.1:
        verdict = "slow: kinetics control, tank is well mixed"
    elif da_mi < 0.1:
        verdict = "blend time matters (feed position, macromixing)"
    else:
        verdict = "MIXING SENSITIVE: micromixing sets selectivity"
    print(f"{t_half:>17g} s {da_mi:>9.3g} {da_ma:>9.3g}  {verdict}")
