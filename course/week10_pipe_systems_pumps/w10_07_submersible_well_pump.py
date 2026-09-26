"""CHME 202 - Week 10 - Example 7: a submersible pump in a borehole.

The pump must lift water from the DYNAMIC water level, which falls as the
pumping rate rises (drawdown), then overcome riser-pipe friction and deliver
into a pressurised main. Pump data are ILLUSTRATIVE, not a specific product.
"""

from fluidmech import Fluid, PumpCurve
from fluidmech import pipe_flow as pf
from fluidmech.constants import G
from fluidmech.solvers import bisect

water = Fluid.water(10)
static_level = 35.0  # depth to water when not pumping [m]
specific_capacity = 2.5  # well yield per metre of drawdown [m3/h per m] (from a pumping test)
riser_d, riser_l = 0.0627, 60.0  # 2-1/2" riser pipe
surface_pipe_l, delivery_pressure = 150.0, 2.0e5  # to a pressurised main at 2 bar(g)


def system_head(q: float) -> float:
    drawdown = q * 3600 / specific_capacity  # m3/s -> m3/h divided by specific capacity [m3/h per m]
    lift = static_level + drawdown
    friction = pf.head_loss(
        max(q, 1e-9), riser_d, riser_l + surface_pipe_l, water, pf.ROUGHNESS["galvanized_iron"], 6.0
    ).total_head_loss
    return lift + friction + delivery_pressure / (water.density * G)


pump = PumpCurve.from_points([0, 0.002, 0.004, 0.006], [120, 112, 95, 68], [0, 0.55, 0.68, 0.60])
q = bisect(lambda x: pump.head(x) - system_head(x), 1e-6, pump.max_flow())  # operating point
drawdown = q * 3600 / specific_capacity
print(f"Operating point: {q * 3600:.1f} m3/h at {pump.head(q):.1f} m, efficiency {pump.efficiency(q):.0%}")
print(f"  dynamic water level {static_level + drawdown:.1f} m below ground (drawdown {drawdown:.1f} m)")
print(f"  shaft power {pump.shaft_power(q, water.density) / 1e3:.2f} kW\n")
print(f"{'Q [m3/h]':>9} {'lift':>6} {'friction':>9} {'pressure':>9} {'system H':>9} {'pump H':>7}")
for qh in [0, 4, 8, 12, 16, 20]:
    qq = qh / 3600  # m3/h -> m3/s
    lift = static_level + qh / specific_capacity
    total = system_head(qq)
    print(
        f"{qh:>9} {lift:>6.1f} {total - lift - delivery_pressure / (water.density * G):>9.1f} "
        f"{delivery_pressure / (water.density * G):>9.1f} {total:>9.1f} {pump.head(qq):>7.1f}"
    )
print("\nDrawdown makes the system curve steeper: pumping harder lowers the water level.")
print("The pump inlet must stay well below the dynamic level; well yield, motor cooling and")
print("installation limits need site- and product-specific checks.")
