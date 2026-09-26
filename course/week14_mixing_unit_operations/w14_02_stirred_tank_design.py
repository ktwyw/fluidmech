"""CHME 202 - Week 14 - Example 2: analysing a stirred reactor.

For a 2 m3 reactor we compare impellers at the same power input per volume:
blend time, tip speed, turbulence (Kolmogorov) scale and micromixing time.
"""

from fluidmech import mixing as mx
from fluidmech.solvers import bisect

T = 1.366  # tank diameter for 2 m3 with H = T
rho, mu = 1000.0, 1e-3
target_pv = 500.0  # W/m3, a typical 'vigorous' agitation level
print(f"Tank T = {T} m (V = {3.1416 * T**3 / 4:.2f} m3), water, target P/V = {target_pv} W/m3\n")
print(
    f"{'impeller':<18} {'D/T':>4} {'rpm':>5} {'tip [m/s]':>9} {'blend t95 [s]':>13} {'eta_K [um]':>10} {'t_micro [ms]':>12}"
)
for name, d_ratio in [("rushton_turbine", 1 / 3), ("pitched_blade_45", 0.4), ("hydrofoil", 0.45)]:
    tank = mx.StirredTank(T, d_ratio * T, name)
    # speed [rev/s] that gives the target P/V
    n = bisect(lambda n, tank=tank: tank.analyse(n, rho, mu)["power_per_volume_W_m3"] - target_pv, 0.05, 50)
    r = tank.analyse(n, rho, mu)
    print(
        f"{name:<18} {d_ratio:>4.2f} {n * 60:>5.0f} {r['tip_speed_m_s']:>9.2f} {r['blend_time_s']:>13.1f} "
        f"{r['kolmogorov_length_m'] * 1e6:>10.0f} {r['micromixing_time_s'] * 1000:>12.1f}"
    )
print("\nAt equal P/V, larger low-power-number impellers run slower but blend just as fast or faster;")
print("the Rushton turbine delivers its power as intense shear near the blades (good for gas dispersion).")
print("Kolmogorov and micromixing scales depend only on P/V (mean dissipation) - identical here.")
print("Note: local dissipation near the impeller can be 10-50x the tank average.")
