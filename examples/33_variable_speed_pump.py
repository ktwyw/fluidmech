"""Example 33 - Variable-speed drive vs. throttling: pump energy savings.

A pump sized for 80 L/s must sometimes deliver only 50 L/s. Compare closing a
valve (throttling) with slowing the pump using the affinity laws.
"""

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech.solvers import bisect

water = Fluid.water(20)
pump = PumpCurve.from_points(
    # catalogue flow rates [m3/s]
    flow_rates=[0.0, 0.04, 0.08, 0.12],
    # heads at those flows [m]
    heads=[42.0, 40.0, 33.5, 22.5],
    # efficiencies (fractions)
    efficiencies=[0.0, 0.62, 0.80, 0.68],
)
system = pumps.system_curve(static_head=12.0, diameter=0.25, length=800.0, fluid=water, roughness=0.26e-3, k_total=8.0)

full = pumps.operating_point(pump, system, water.density)
print(
    f"Full speed: Q = {full.flow_rate * 1000:.1f} L/s, H = {full.head:.1f} m, "
    f"eta = {full.efficiency:.1%}, P = {full.shaft_power / 1e3:.1f} kW\n"
)

print(f"{'Q target':>9} | {'throttled: H_pump':>17} {'P [kW]':>7} | {'VFD: speed':>10} {'H':>6} {'P [kW]':>7} | saving")
for q_target in [0.075, 0.065, 0.055, 0.045, 0.035]:
    # Throttling: the pump stays on its full-speed curve, the valve burns the excess head
    h_throttle = pump.head(q_target)
    p_throttle = water.density * 9.80665 * q_target * h_throttle / pump.efficiency(q_target)

    # Variable speed: find the speed ratio whose curve passes through (Q, H_system)
    h_needed = system(q_target)
    # speed ratio whose curve passes through the duty point
    ratio = bisect(lambda r, q=q_target, h=h_needed: pump.scaled(speed_ratio=r).head(q) - h, 0.3, 1.0)
    slow = pump.scaled(speed_ratio=ratio)
    p_vfd = water.density * 9.80665 * q_target * h_needed / slow.efficiency(q_target)
    print(
        f"{q_target * 1000:>6.0f} L/s | {h_throttle:>15.1f} m {p_throttle / 1e3:>7.1f} | "
        f"{ratio:>9.1%} {h_needed:>6.1f} {p_vfd / 1e3:>7.1f} | {1 - p_vfd / p_throttle:>5.0%}"
    )

hours, price = 4000, 0.12  # operating hours per year, electricity price [$/kWh]
q = 0.050  # part-load flow [m3/s]
h_t = pump.head(q)
p_t = water.density * 9.80665 * q * h_t / pump.efficiency(q)
r = bisect(lambda r: pump.scaled(speed_ratio=r).head(q) - system(q), 0.3, 1.0)
p_v = water.density * 9.80665 * q * system(q) / pump.scaled(speed_ratio=r).efficiency(q)
print(
    f"\nRunning {hours} h/yr at 50 L/s saves {(p_t - p_v) / 1e3 * hours * price:,.0f} $/yr "
    f"at {price} $/kWh (ignoring drive losses of ~3 %)."
)
