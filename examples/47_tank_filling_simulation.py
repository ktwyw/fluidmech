"""Example 47 - Filling a tank with a pump: time-dependent operating point.

As the tank fills, the static head rises and the pump slides back along its
curve, delivering less flow. We march in time, recomputing the operating
point at every step.
"""

import math

from fluidmech import Fluid, PumpCurve, pumps

water = Fluid.water(20)
pump = PumpCurve.from_points([0.0, 0.02, 0.04, 0.06], [38.0, 36.5, 32.0, 24.5], [0.0, 0.60, 0.80, 0.60])
tank_diameter = 12.0  # [m]
tank_area = math.pi * tank_diameter**2 / 4
z_base = 18.0  # tank floor above the sump level [m]
level, level_full = 0.5, 9.0

dt = 60.0  # time step [s]
t = 0.0
energy = 0.0
print(f"{'time [h]':>8} {'level [m]':>10} {'static H':>9} {'Q [L/s]':>8} {'H [m]':>7} {'eta':>6} {'P [kW]':>7}")
next_report = 0.0
while level < level_full:  # march in time; the operating point is recomputed every step
    system = pumps.system_curve(z_base + level, 0.15, 350.0, water, 0.045e-3, 6.0)
    op = pumps.operating_point(pump, system, water.density)
    if t >= next_report:
        print(
            f"{t / 3600:>8.2f} {level:>10.2f} {z_base + level:>9.2f} {op.flow_rate * 1000:>8.2f} "
            f"{op.head:>7.2f} {op.efficiency:>6.1%} {op.shaft_power / 1e3:>7.2f}"
        )
        next_report += 1800.0
    level += op.flow_rate * dt / tank_area  # level rise = volume pumped / tank area
    energy += op.shaft_power * dt  # energy [J] = power x time
    t += dt

volume = tank_area * (level_full - 0.5)
print(f"\nTank full after {t / 3600:.2f} h; pumped {volume:.0f} m3 using {energy / 3.6e6:.1f} kWh")
print(f"Specific energy: {energy / 3.6e6 / volume * 1000:.0f} Wh/m3")
ideal = water.density * 9.80665 * volume * (z_base + (0.5 + level_full) / 2) / 3.6e6
print(f"(Ideal lifting energy {ideal:.1f} kWh -> overall efficiency {ideal / (energy / 3.6e6):.0%})")
