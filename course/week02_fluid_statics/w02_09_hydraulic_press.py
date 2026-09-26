"""CHME 202 - Week 2 - Example 9: Pascal's law - the hydraulic press and jack.

Pressure applied to a confined liquid is transmitted undiminished, so
F2 = F1 A2 / A1. Energy is conserved: the large piston moves A1/A2 as far.
Reading: White, Section 2.2.
"""

import math

d1, d2 = 0.02, 0.20  # small and large piston diameters [m]
A1, A2 = math.pi * d1**2 / 4, math.pi * d2**2 / 4
F1, stroke1 = 200.0, 0.10  # force on the small piston [N], its stroke [m]
p = F1 / A1
F2 = p * A2
print(f"Pistons {d1 * 1000:.0f} mm and {d2 * 1000:.0f} mm: area ratio {A2 / A1:.0f}")
print(f"  {F1:.0f} N on the small piston -> pressure {p / 1e5:.1f} bar -> {F2 / 1e3:.1f} kN on the large piston")
print(f"  a {stroke1 * 100:.0f} cm stroke of the small piston lifts the load {stroke1 * A1 / A2 * 1000:.1f} mm")
print(f"  work in {F1 * stroke1:.1f} J = work out {F2 * stroke1 * A1 / A2:.1f} J (no free energy!)\n")

# Height difference between pistons adds a hydrostatic term
dz, rho = 1.5, 870.0
p_big = p + rho * 9.80665 * dz
print(
    f"If the large piston sits {dz} m below the small one (oil, rho = {rho}): extra {rho * 9.80665 * dz / 1e3:.1f} kPa,"
)
print(f"  force {p_big * A2 / 1e3:.2f} kN instead of {F2 / 1e3:.2f} kN - usually negligible at high pressures.\n")

print(
    "Industrial example: a 250 bar hydraulic cylinder of 100 mm bore pushes with "
    f"{250e5 * math.pi * 0.1**2 / 4 / 1e3:.0f} kN (about {250e5 * math.pi * 0.1**2 / 4 / 9.81 / 1000:.0f} tonnes-force)."
)
