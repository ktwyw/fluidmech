"""CHME 202 - Week 4 - Example 5: the Rankine half-body (flow around a blunt nose).

A source in a uniform stream: the dividing streamline psi = m/2 forms a body
of asymptotic width m / U. Useful model of flow approaching a hill, a pier
nose or a Pitot probe.
Reading: White, Section 8.3.
"""

import math

from fluidmech.potential_flow import rankine_half_body

U = 5.0  # m/s
width = 2.0  # desired asymptotic body width [m]
m = U * width  # source strength
flow = rankine_half_body(U, m)
x_stag = -m / (2 * math.pi * U)
print(f"Half-body of asymptotic width {width} m in a {U} m/s stream: m = {m} m2/s")
print(f"Stagnation point at x = {x_stag:.3f} m\n")

# Surface: psi = m/2 -> r = m (pi - theta) / (2 pi U sin theta)
print(f"{'theta [deg]':>12} {'x [m]':>7} {'y [m]':>7} {'V/U':>6} {'Cp':>6}")
best = (0.0, 0.0)  # (largest V/U, angle) found so far
for deg in [170, 150, 130, 115, 100, 90, 70, 50, 30, 10]:
    th = math.radians(deg)
    r = m * (math.pi - th) / (2 * math.pi * U * math.sin(th))  # body surface: psi = m/2 solved for r(theta)
    x, y = r * math.cos(th), r * math.sin(th)
    ratio = flow.speed(x, y) / U
    best = max(best, (ratio, deg))
    print(f"{deg:>12} {x:>7.3f} {y:>7.3f} {ratio:>6.3f} {1 - ratio**2:>6.3f}")
print(f"\nMaximum surface speed {best[0]:.3f} U near theta = {best[1]} deg (exact: 1.26 U at theta = 63 deg)")
print("Downstream the surface speed returns to U and the half-width approaches m / (2U).")
print("Engineering use: a Pitot-static probe's static holes are placed several diameters behind the nose,")
print("where the surface pressure has recovered to the free-stream static pressure.")
