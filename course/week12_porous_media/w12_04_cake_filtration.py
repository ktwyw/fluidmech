"""CHME 202 - Week 12 - Example 4: constant-pressure cake filtration.

Ruth equation: t / V = (mu alpha c / 2 A^2 dp) V + mu R_m / (A dp).
Plotting t/V against V gives a straight line: the slope gives the specific cake
resistance alpha, the intercept the filter-medium resistance R_m.
Lab-scale results are then scaled up to a filter press.
"""

from fluidmech import porous as por

mu, dp, A, c = 1.0e-3, 2.0e5, 0.05, 25.0  # water, 2 bar, 0.05 m2 leaf filter, 25 kg solids / m3 filtrate
times = [18.0, 44.0, 78.0, 121.0, 170.0, 228.0]  # s (laboratory data)
volumes = [0.5e-3, 1.0e-3, 1.5e-3, 2.0e-3, 2.5e-3, 3.0e-3]  # m3
alpha, r_m, kp, b = por.filtration_constants_from_data(times, volumes, A, dp, mu, c)
print("Leaf-filter test at 2 bar:")
print(f"{'V [L]':>6} {'t [s]':>6} {'t/V [s/L]':>10}")
for t, v in zip(times, volumes):
    print(f"{v * 1000:>6.1f} {t:>6.0f} {t / v / 1000:>10.1f}")
print(f"\nSpecific cake resistance alpha = {alpha:.2e} m/kg")
print(f"Filter-medium resistance   R_m = {r_m:.2e} 1/m")

# Scale up to a filter press: 20 m2 area, collect 3 m3 of filtrate
A_press, V_batch = 20.0, 3.0
t_batch = por.filtration_time(V_batch, A_press, dp, mu, alpha, c, r_m)
print(f"\nFilter press, {A_press:.0f} m2 at the same pressure: {V_batch} m3 of filtrate takes {t_batch / 60:.1f} min")
print(
    f"  cake mass {c * V_batch:.0f} kg; at 4 bar the time would be "
    f"{por.filtration_time(V_batch, A_press, 2 * dp, mu, alpha, c, r_m) / 60:.1f} min (incompressible cake)"
)
print("  Real cakes are compressible (alpha rises with dp), so doubling pressure gains less than this.")
print("  Filtration rate falls as the cake grows: the optimum cycle balances filtering and cleaning time.")
