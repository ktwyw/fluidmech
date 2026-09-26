"""CHME 202 - Week 1 - Example 5: introduction to piping systems.

Pipes are specified by nominal size and schedule, not by their inside diameter.
We size a water line using standard Schedule 40 steel pipe and typical velocity
guidelines, and compute mass flow, velocity and Reynolds number.
"""

from fluidmech import Fluid
from fluidmech.pipe_flow import area
from fluidmech.units import convert

# ASME B36.10 Schedule 40: nominal size [in] -> inside diameter [in]
SCHEDULE_40 = {
    "1/2": 0.622,
    "3/4": 0.824,
    "1": 1.049,
    "1-1/2": 1.610,
    "2": 2.067,
    "3": 3.068,
    "4": 4.026,
    "6": 6.065,
    "8": 7.981,
    "10": 10.020,
    "12": 11.938,
}

water = Fluid.water(20)
Q_m3h = 25.0  # design flow [m3/h]
Q = Q_m3h / 3600  # m3/h -> m3/s
print(f"Water at 20 degC, Q = {Q_m3h} m3/h ({Q * 1000:.2f} L/s, mass flow {water.density * Q:.2f} kg/s)\n")
print(f"{'NPS':>6} {'ID [mm]':>8} {'V [m/s]':>8} {'Re':>10}  guideline (1-3 m/s for pump discharge)")
for nps, id_in in SCHEDULE_40.items():
    d = convert(id_in, "in", "m")  # pipe schedules are tabulated in inches
    v = Q / area(d)
    if v < 0.3 or v > 6:
        continue
    note = (
        "OK"
        if 1.0 <= v <= 3.0
        else ("too slow: oversized, costly pipe" if v < 1 else "too fast: high losses, noise, erosion")
    )
    print(f"{nps:>6} {d * 1000:>8.1f} {v:>8.2f} {v * d / water.kinematic_viscosity:>10.3g}  {note}")

print("\nTypical design velocities:")
guide = [
    ("liquid, pump suction", "0.5-1.5 m/s"),
    ("liquid, pump discharge", "1-3 m/s"),
    ("viscous liquid", "0.3-1 m/s"),
    ("gas / vapour, low pressure", "10-30 m/s"),
    ("steam", "20-40 m/s"),
]
for service, v in guide:
    print(f"  {service:<27} {v}")

print("\nWall thickness matters: a '2 inch' pipe is 2.067 in inside for Sch 40 but 1.939 in for Sch 80.")
d40, d80 = convert(2.067, "in", "m"), convert(1.939, "in", "m")
print(
    f"At the same flow, Sch 80 velocity is {(d40 / d80) ** 2 - 1:.0%} higher and friction loss ~{(d40 / d80) ** 5 - 1:.0%} higher."
)
