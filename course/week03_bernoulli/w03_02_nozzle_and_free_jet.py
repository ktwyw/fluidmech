"""CHME 202 - Week 3 - Example 2: jets from tanks and nozzles.

Torricelli: V = sqrt(2 g h). A free jet leaves at atmospheric pressure and then
follows a ballistic path (Bernoulli along the jet trades speed for height).
Reading: White, Section 3.5.
"""

import math

from fluidmech.bernoulli import torricelli_velocity
from fluidmech.constants import G

# (a) Holes in the side of a tank of height H: which hole squirts furthest?
H = 2.0
print(f"(a) Open tank filled to H = {H} m, holes at height y above the floor (tank on the ground)")
print(f"{'y [m]':>6} {'V [m/s]':>8} {'range [m]':>10}")
for y in [0.2, 0.5, 1.0, 1.5, 1.8]:
    v = torricelli_velocity(H - y)
    t = math.sqrt(2 * y / G)  # time to fall y
    print(f"{y:>6.1f} {v:>8.2f} {v * t:>10.2f}")
print("The maximum range 2 sqrt(y (H - y)) = H occurs for the hole at mid-height.\n")

# (b) A fountain nozzle fed by a pump: how high does it go?
print("(b) Vertical fountain from a nozzle")
for p_gauge_kpa in [50, 100, 200, 400]:
    v = math.sqrt(2 * p_gauge_kpa * 1e3 / 1000)  # V = sqrt(2 p / rho), kPa -> Pa, rho = 1000
    print(f"  nozzle pressure {p_gauge_kpa:>4} kPa -> exit speed {v:5.1f} m/s -> ideal height {v**2 / (2 * G):5.1f} m")
print("  The ideal height equals the pressure head p / (rho g): pressure energy becomes potential energy.")
print("  Real fountains fall short because of air drag and jet break-up.\n")

# (c) Inclined jet: maximum height and range
v0, angle = 12.0, 50.0
vx, vy = v0 * math.cos(math.radians(angle)), v0 * math.sin(math.radians(angle))
print(
    f"(c) Jet at {v0} m/s and {angle:.0f} deg: top of trajectory {vy**2 / (2 * G):.2f} m, range {2 * vx * vy / G:.2f} m"
)
print(
    f"    At the top the jet speed is {vx:.2f} m/s: Bernoulli gives the same height, "
    f"(V0^2 - Vtop^2)/(2g) = {(v0**2 - vx**2) / (2 * G):.2f} m"
)
