"""CHME 202 - Week 12 - Example 7: the optimum filtration cycle.

A batch filter (filter press) spends time t_f filtering and t_c discharging and
cleaning. Filtering longer collects more filtrate per cycle but at a falling rate.
The average throughput V / (t_f + t_c) has a maximum; with negligible medium
resistance it occurs when t_f = t_c.
"""

from fluidmech import porous as por

mu, dp, A, c = 1e-3, 3e5, 25.0, 30.0  # water, 3 bar [Pa], area [m2], kg solids per m3 filtrate
alpha, r_m = 5e11, 1e11  # specific cake resistance [m/kg], medium resistance [1/m]
t_clean = 20 * 60  # 20 minutes to open, discharge and close the press
print(f"Filter press {A} m2 at {dp / 1e5:.0f} bar, alpha = {alpha:.1e} m/kg, cleaning time {t_clean / 60:.0f} min\n")
print(f"{'filtering time [min]':>21} {'V per cycle [m3]':>17} {'throughput [m3/h]':>18}")
best = (0.0, 0.0, 0.0)
for t_min in [5, 10, 15, 20, 30, 45, 60, 90, 120]:
    t = t_min * 60  # min -> s
    v = por.filtration_volume(t, A, dp, mu, alpha, c, r_m)
    rate = v / (t + t_clean) * 3600  # average throughput over a whole cycle [m3/h]
    best = max(best, (rate, t_min, v))
    print(f"{t_min:>21} {v:>17.2f} {rate:>18.2f}")
print(f"\nBest cycle: ~{best[1]} min filtering, {best[2]:.1f} m3 per cycle, {best[0]:.2f} m3/h average")
print("With negligible medium resistance the optimum is t_f = t_c; medium resistance shifts it slightly")
print("longer. Faster cleaning (automatic plate shifters) raises the throughput of the same press.")
