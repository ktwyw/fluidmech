"""CHME 202 - Week 5 - Example 11: radial flow between parallel discs.

Navier-Stokes in cylindrical coordinates, thin gap h, creeping flow outward from r1 to r2:
u_r(r, z) = (1 / (2 mu)) (-dp/dr) z (h - z) and continuity makes Q = 2 pi r q(r) constant, so
p(r1) - p(r2) = 6 mu Q ln(r2 / r1) / (pi h^3). Found in filter plates, radial diffusers,
hydrostatic thrust bearings and disc-type heat exchangers.
"""

import math

mu, h = 0.05, 0.5e-3  # oil, gap
r1, r2 = 0.01, 0.10
Q = 5e-6  # m3/s
dp_total = 6 * mu * Q * math.log(r2 / r1) / (math.pi * h**3)
print(f"Oil mu = {mu} Pa s between discs {h * 1000} mm apart, from r = {r1} to {r2} m, Q = {Q * 1e6:.0f} mL/s")
print(f"Total pressure drop {dp_total / 1e3:.1f} kPa\n")
print(f"{'r [m]':>6} {'p - p_out [kPa]':>16} {'mean velocity [mm/s]':>21}")
for r in [0.01, 0.02, 0.04, 0.06, 0.08, 0.10]:
    p = 6 * mu * Q * math.log(r2 / r) / (math.pi * h**3)  # pressure above the outlet pressure at radius r
    v = Q / (2 * math.pi * r * h)  # mean radial velocity: same Q through a growing circumference
    print(f"{r:>6} {p / 1e3:>16.2f} {v * 1000:>21.2f}")
print("\nThe pressure falls logarithmically: most of the drop happens near the inlet, where the fluid is")
print("fastest. A hydrostatic thrust bearing uses exactly this pressure field to carry a load:")
load = (
    sum(
        2 * math.pi * r * 6 * mu * Q * math.log(r2 / r) / (math.pi * h**3) * (r2 - r1) / 1000
        for r in [r1 + (i + 0.5) * (r2 - r1) / 1000 for i in range(1000)]
    )
    + math.pi * r1**2 * dp_total
)
print(f"  load carried = {load:.0f} N for the flow above (plus the pocket r < r1 at full pressure)")
print(f"Check laminar: Re = rho V h / mu at the inlet = {900 * Q / (2 * math.pi * r1 * h) * h / mu:.2f}")
