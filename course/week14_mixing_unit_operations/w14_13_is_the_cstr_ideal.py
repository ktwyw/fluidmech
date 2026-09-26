"""CHME 202 - Week 14 - Example 13: is a continuous stirred tank really 'perfectly mixed'?

The ideal-CSTR model assumes the feed is blended instantly. That is reasonable when the
blend time is much shorter than the mean residence time tau = V / Q (and the reaction time).
We check several tanks and throughputs.
"""

from fluidmech import mixing as mx

rho, mu = 1000.0, 1e-3  # water
cases = [
    ("small reactor, slow feed", 0.6, 3.0, 1.0),
    ("small reactor, fast feed", 0.6, 3.0, 40.0),
    ("large tank, 1 h residence", 3.0, 1.0, 50.0),
    ("large tank, 5 min residence", 3.0, 1.0, 600.0),
]
print(f"{'case':<28} {'V [m3]':>7} {'tau [s]':>8} {'t95 [s]':>8} {'t95/tau':>8}  verdict")
for name, T, N, q_m3h in cases:
    tank = mx.StirredTank(T, T / 3)
    r = tank.analyse(N, rho, mu)
    tau = tank.volume / (q_m3h / 3600)  # mean residence time; m3/h -> m3/s
    ratio = r["blend_time_s"] / tau
    verdict = "ideal CSTR OK" if ratio < 0.05 else ("check: partial bypassing" if ratio < 0.2 else "NOT ideal")
    print(f"{name:<28} {tank.volume:>7.2f} {tau:>8.0f} {r['blend_time_s']:>8.1f} {ratio:>8.3f}  {verdict}")
print("\nWhen t95 is not small compared with tau, fresh feed can short-circuit to the outlet: the conversion")
print("is lower than the ideal-CSTR prediction. Position the feed and outlet far apart and near the impeller.")
