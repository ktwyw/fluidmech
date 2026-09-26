"""CHME 202 - Week 3 - Example 1: stagnation pressure and a Pitot-tube traverse.

A Pitot-static probe measures V = sqrt(2 dp / rho) at a point. Traversing it
across a duct and integrating the velocity profile gives the flow rate.
Reading: White, Section 3.5 (Bernoulli) and 6.12 (flow measurement).
"""

import math

from fluidmech import Fluid
from fluidmech.bernoulli import pitot_velocity

air = Fluid.air(25)
D = 0.30  # duct diameter [m]
R = D / 2
# Traverse: radial position [mm] and manometer reading dp [Pa] (illustrative lab data)
r_mm = [0, 20, 40, 60, 80, 100, 120, 135, 145]
dp_pa = [98.0, 97.1, 95.2, 91.8, 87.0, 79.6, 68.3, 55.1, 38.6]  # Pitot readings [Pa] at r_mm

print(f"Air at 25 degC, rho = {air.density:.3f} kg/m3, duct D = {D * 1000:.0f} mm\n")
print(f"{'r [mm]':>7} {'dp [Pa]':>8} {'V [m/s]':>8}")
v = [pitot_velocity(dp, air.density) for dp in dp_pa]
for r, p, vi in zip(r_mm, dp_pa, v):
    print(f"{r:>7} {p:>8.1f} {vi:>8.2f}")

# Integrate Q = integral 2 pi r V(r) dr with the trapezoidal rule, V = 0 at the wall
rs = [x / 1000 for x in r_mm] + [R]  # mm -> m, plus the wall point where V = 0
vs = v + [0.0]
# trapezoidal rule for Q = integral of 2 pi r V dr
Q = sum(math.pi * (rs[i + 1] * vs[i + 1] + rs[i] * vs[i]) * (rs[i + 1] - rs[i]) for i in range(len(rs) - 1))
V_mean = Q / (math.pi * R**2)
print(f"\nFlow rate Q = {Q:.3f} m3/s, mean velocity {V_mean:.2f} m/s")
print(f"Ratio V_mean / V_centre = {V_mean / v[0]:.3f} (about 0.82 for turbulent pipe flow, 0.5 for laminar)")
re = V_mean * D / air.kinematic_viscosity
print(f"Reynolds number {re:.3g} -> turbulent, consistent with the flat profile")
print("\nNote: the last interval assumes V falls linearly to zero at the wall, which UNDERestimates Q")
print("slightly for a turbulent profile. Standard traverses use equal-area positions to avoid this.")
