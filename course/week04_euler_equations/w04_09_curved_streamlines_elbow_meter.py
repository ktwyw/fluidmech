"""CHME 202 - Week 4 - Example 9: pressure across curved streamlines - the elbow flow meter.

Euler's equation normal to a streamline: dp/dn = rho V^2 / R. Pressure rises
towards the outside of a bend, so the pressure difference between the outer and
inner walls of an elbow measures the flow rate. Modelled here as a free vortex
(V = C / r) in a rectangular bend.
Reading: White, Section 3.5 (Bernoulli normal to streamlines).
"""

import math

rho = 1000.0  # water [kg/m3]
r_in, r_out, width = 0.10, 0.20, 0.10  # bend of a 100 mm x 100 mm rectangular duct
print(f"Rectangular bend: inner radius {r_in} m, outer radius {r_out} m, width {width} m\n")
print(f"{'Q [L/s]':>8} {'V inner':>8} {'V outer':>8} {'p_out - p_in [kPa]':>19}")
for q_ls in [5, 10, 20, 30]:
    q = q_ls / 1000  # L/s -> m3/s
    C = q / (width * math.log(r_out / r_in))  # from Q = integral of (C/r) w dr
    dp = 0.5 * rho * C**2 * (1 / r_in**2 - 1 / r_out**2)  # Bernoulli across the bend (free vortex is irrotational)
    print(f"{q_ls:>8} {C / r_in:>8.2f} {C / r_out:>8.2f} {dp / 1e3:>19.3f}")
print("\ndp is proportional to Q^2, just like a Venturi: Q = k sqrt(dp). An existing elbow can be")
print("calibrated as a cheap flow meter with no extra pressure loss.")
print("Consequence for mixing and separation: secondary flows form in bends because the slow fluid")
print("near the walls cannot resist the pressure gradient (Dean vortices).")
