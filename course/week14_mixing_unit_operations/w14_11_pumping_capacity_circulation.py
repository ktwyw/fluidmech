"""CHME 202 - Week 14 - Example 11: impeller pumping capacity and circulation time.

An impeller discharges Q = N_q N D^3 (flow number N_q). The circulation time t_c = V / Q
is the average time between passes through the impeller; a common rule is that
blend time ~ 4-5 circulation times. We compare this with the Grenville blend-time
correlation used in Example 2. Flow numbers are representative values.
"""

from fluidmech import mixing as mx

flow_numbers = {"rushton_turbine": 0.72, "pitched_blade_45": 0.79, "hydrofoil": 0.56}
T, rho, mu = 1.5, 1000.0, 1e-3  # tank diameter [m], water
N = 2.0  # rev/s
print(f"Tank T = {T} m (V = {3.1416 * T**3 / 4:.2f} m3), water, {N * 60:.0f} rpm\n")
print(
    f"{'impeller':<18} {'D/T':>4} {'Q [m3/s]':>9} {'P [kW]':>7} {'Q/P [m3/s/kW]':>14} {'t_c [s]':>8} {'4-5 t_c [s]':>12} {'Grenville t95':>14}"
)
for name, nq in flow_numbers.items():
    d_ratio = 1 / 3 if name == "rushton_turbine" else 0.4  # typical D/T for each impeller type
    tank = mx.StirredTank(T, d_ratio * T, name)
    D = d_ratio * T
    q = nq * N * D**3  # impeller discharge Q = N_q N D^3
    tc = tank.volume / q
    r = tank.analyse(N, rho, mu)
    print(
        f"{name:<18} {d_ratio:>4.2f} {q:>9.3f} {r['power_W'] / 1e3:>7.2f} {q / (r['power_W'] / 1e3):>14.2f} {tc:>8.1f} "
        f"{f'{4 * tc:.0f}-{5 * tc:.0f}':>12} {r['blend_time_s']:>12.1f} s"
    )
print("\nThe two rules of thumb differ by a factor of 2-5 and even rank the impellers differently: the")
print("circulation-time rule counts only the impeller discharge (ignoring entrained flow), while Grenville's")
print("correlation reflects power input. Treat both as order-of-magnitude estimates and measure blend times")
print("(conductivity or pH tracer) when they matter. The Q/P column shows why axial impellers - and the")
print("hydrofoil above all - are chosen for blending: they move far more liquid per kilowatt.")
