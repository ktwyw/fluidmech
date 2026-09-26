"""CHME 202 - Week 10 - Example 6: a closed heating loop and its circulator pump.

In a closed loop the fluid returns to where it started, so there is NO static
head: the system curve passes through the origin, H = k Q^2. As radiator valves
close, k rises and the duty point moves. Circulators therefore run under
pressure-based control rather than at a fixed speed.
Pump data are ILLUSTRATIVE, not a specific product.
"""

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech import pipe_flow as pf

water = Fluid.water(60)  # heating water
heat_load_kw, dT = 40.0, 20.0  # building load and supply-return temperature difference
cp = 4180.0
q_design = heat_load_kw * 1000 / (water.density * cp * dT)  # Q = heat load / (rho cp dT); kW -> W
print(f"Heat load {heat_load_kw:.0f} kW with a {dT:.0f} K temperature drop -> Q = {q_design * 3600:.2f} m3/h")

loop_length, d = 120.0, 0.028  # total flow + return length, 28 mm copper-like pipe
k_fittings = 35.0  # boiler, radiators, valves, bends
r = pf.head_loss(q_design, d, loop_length, water, pf.ROUGHNESS["drawn_tubing"], k_fittings)
print(f"Loop head at design flow: {r.total_head_loss:.2f} m (all friction - no static head)\n")

circulator = PumpCurve.from_points([0, 0.0003, 0.0006, 0.0009], [6.0, 5.4, 3.6, 0.6], [0, 0.35, 0.45, 0.35])
base = pumps.operating_point(
    circulator, pumps.system_curve(0.0, d, loop_length, water, pf.ROUGHNESS["drawn_tubing"], k_fittings), water.density
)
print(
    f"Selected circulator delivers {base.flow_rate * 3600:.2f} m3/h with all valves open "
    f"({base.flow_rate / q_design - 1:+.0%} margin over the design flow)\n"
)
print(f"{'valve state':<22} {'extra K':>8} {'Q [m3/h]':>9} {'H [m]':>7} {'P shaft [W]':>12}")
for label, extra in [("all valves open", 0), ("half the rooms warm", 60), ("mostly closed", 250)]:
    system = pumps.system_curve(0.0, d, loop_length, water, pf.ROUGHNESS["drawn_tubing"], k_fittings + extra)
    op = pumps.operating_point(circulator, system, water.density)
    print(f"{label:<22} {extra:>8} {op.flow_rate * 3600:>9.2f} {op.head:>7.2f} {op.shaft_power:>12.1f}")
print("\nAt fixed speed the head RISES as valves close (noise, wasted energy). A proportional-pressure")
print("controlled circulator instead lowers its head as the flow falls, saving most of that energy.")
print("Control modes and product limits are covered in manufacturer training.")
