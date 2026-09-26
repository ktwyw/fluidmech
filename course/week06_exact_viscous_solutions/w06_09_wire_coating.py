"""CHME 202 - Week 6 - Example 9: wire coating - annular Couette flow.

A wire of radius R1 is pulled at speed U through a die of radius R2 filled with
coating liquid (no pressure gradient). The exact solution is
u(r) = U ln(r/R2) / ln(R1/R2). Flow rate and coating thickness follow.
Reading: White, Problem 4.x (wire coating); Bird, Stewart & Lightfoot, Problem 2B.
"""

import math

R1, R2, L_die = 0.5e-3, 1.5e-3, 0.02  # wire radius, die radius, die length [m]
mu = 1.2  # enamel/polymer coating [Pa s]
U = 2.0  # wire speed [m/s]


def u(r):
    return U * math.log(r / R2) / math.log(R1 / R2)


n = 4000
Q = sum(2 * math.pi * r * u(r) * (R2 - R1) / n for r in [R1 + (i + 0.5) * (R2 - R1) / n for i in range(n)])
# Coating thickness: Q = pi ((R1 + t)^2 - R1^2) U far downstream (coating moves with the wire)
t = math.sqrt(Q / (math.pi * U) + R1**2) - R1  # downstream the coating moves with the wire at speed U
tau_w = mu * U / (R1 * math.log(R2 / R1))  # shear at the wire surface, mu |du/dr| at r = R1
F = tau_w * 2 * math.pi * R1 * L_die
print(f"Wire r = {R1 * 1000} mm pulled at {U} m/s through a die r = {R2 * 1000} mm, coating mu = {mu} Pa s")
print(f"  coating flow {Q * 1e6 * 60:.2f} mL/min, wet coating thickness {t * 1e6:.0f} um")
print(f"  wall shear on the wire {tau_w / 1e3:.1f} kPa -> pulling force {F:.2f} N")
print(f"\n{'r [mm]':>7} {'u [m/s]':>8}")
for i in range(6):
    r = R1 + (R2 - R1) * i / 5
    print(f"{r * 1000:>7.2f} {(0.0 if abs(u(r)) < 1e-12 else u(r)):>8.3f}")
print("\nThe profile is logarithmic, not linear: curvature matters when the gap is not thin.")
print("A pressure gradient in the die (pumped coating) would add a Poiseuille part and thicken the coat.")
