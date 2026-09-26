"""CHME 202 - Week 2 - Example 5: rigid-body motion - a road tanker accelerating and braking.

In uniform acceleration the liquid moves as a rigid body: the free surface tilts
with slope dz/dx = -a_x / (g + a_z) and pressure is still linear in position.
Reading: White, Section 2.9.
"""

import math

from fluidmech.constants import G
from fluidmech.hydrostatics import accelerating_pressure, accelerating_surface_slope

L, H, fill = 6.0, 2.0, 1.6  # open-top tank length, height, initial depth [m]
rho = 1000.0
print(f"Open tank {L} m long, {H} m high, filled to {fill} m\n")
print(f"{'a_x [m/s2]':>11} {'surface angle':>14} {'rear depth':>11} {'front depth':>12} {'p rear bottom [kPa]':>20}")
for a in [0.0, 1.0, 2.0, 3.0, 4.0]:
    slope = accelerating_surface_slope(a)
    rise = -slope * L / 2  # the surface pivots about the tank centre
    rear, front = fill + rise, fill - rise
    p_rear = accelerating_pressure(-L / 2, 0.0, a, density=rho, reference_pressure=rho * G * fill)
    flag = "  SPILLS" if rear > H else ""
    print(
        f"{a:>11.1f} {math.degrees(math.atan(-slope)):>13.1f}d {rear:>11.2f} {front:>12.2f} {p_rear / 1e3:>20.2f}{flag}"
    )

a_max = 2 * (H - fill) / L * G  # surface may rise by (H - fill) at the rear: tan(theta) = a/g
print(f"\nMaximum acceleration before spilling: {a_max:.2f} m/s2 ({a_max / G:.2f} g)")
print("Braking is the same problem with the liquid surging forward - baffles limit the sloshing.\n")

print("Vertical acceleration (a lift accelerating upwards) simply changes the effective gravity:")
for az in [-4.9, 0.0, 4.9]:
    p = accelerating_pressure(0.0, -1.0, 0.0, az, density=rho)
    print(f"  a_z = {az:+.1f} m/s2: pressure 1 m below the surface = {p / 1e3:.2f} kPa")
