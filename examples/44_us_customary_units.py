"""Example 44 - Working in US customary units.

The library computes in SI; ``fluidmech.units`` converts at the boundaries so
you can enter and report data in gpm, ft, psi and hp.
"""

from fluidmech import Fluid, PumpCurve, pumps
from fluidmech import pipe_flow as pf
from fluidmech.units import convert

# Input data as it might appear on a US drawing
flow_gpm = 450.0
length_ft = 1200.0  # pipe length [ft]
diameter_in = 6.065  # 6" Schedule 40 steel, inside diameter
static_lift_ft = 60.0
water_f = 60.0  # degF

water = Fluid.water(convert(water_f, "degF", "degC"))
q = convert(flow_gpm, "gpm", "m3/s")
d = convert(diameter_in, "in", "m")
length = convert(length_ft, "ft", "m")
k_fittings = 0.5 + 6 * 0.3 + 2 * 0.15 + 1.0  # entrance, 6 elbows, 2 gate valves, exit

r = pf.head_loss(q, d, length, water, pf.ROUGHNESS["commercial_steel"], k_fittings)
print(f"{flow_gpm:.0f} gpm through {length_ft:.0f} ft of 6-in Sch 40 steel, water at {water_f:.0f} F")
print(f"  velocity        {convert(r.velocity, 'm/s', 'ft/s'):7.2f} ft/s")
print(f"  Reynolds number {r.reynolds:9.3g}")
print(f"  friction factor {r.friction_factor:9.4f}")
print(
    f"  head loss       {convert(r.total_head_loss, 'm', 'ft'):7.1f} ft "
    f"({convert(r.pressure_drop, 'Pa', 'psi'):.1f} psi)"
)
print(f"  loss per 100 ft {convert(r.major_head_loss, 'm', 'ft') / length_ft * 100:7.2f} ft")

# Pump selection from a catalogue curve given in gpm / ft
cat_gpm = [0, 200, 400, 600]
cat_ft = [120, 116, 103, 80]  # catalogue heads [ft] at cat_gpm
curve = PumpCurve.from_points(
    [convert(x, "gpm", "m3/s") for x in cat_gpm],
    [convert(h, "ft", "m") for h in cat_ft],
    [0.0, 0.62, 0.78, 0.70],
)
system = pumps.system_curve(
    convert(static_lift_ft, "ft", "m"), d, length, water, pf.ROUGHNESS["commercial_steel"], k_fittings
)
op = pumps.operating_point(curve, system, water.density)
print(
    f"\nPump operating point: {convert(op.flow_rate, 'm3/s', 'gpm'):.0f} gpm at "
    f"{convert(op.head, 'm', 'ft'):.0f} ft TDH, efficiency {op.efficiency:.0%}"
)
print(
    f"  brake horsepower {convert(op.shaft_power, 'W', 'hp'):.1f} hp -> choose a "
    f"{next(s for s in (10, 15, 20, 25, 30, 40, 50) if s > convert(op.shaft_power, 'W', 'hp') * 1.15)} hp motor"
)
