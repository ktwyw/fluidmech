"""CHME 202 - Week 2 - Example 15: rigid-body rotation in a U-tube (a liquid tachometer).

A U-tube with arms at radii R1 and R2 from a vertical axis spins at omega. The free
surfaces lie on the same paraboloid, so their height difference is
dh = omega^2 (R2^2 - R1^2) / (2 g). Measuring dh measures the speed.
Reading: White, Section 2.9 (Problems 2.150-2.160 are of this type).
"""

import math

from fluidmech.constants import G

R1, R2 = 0.05, 0.25  # arm radii [m]
print(f"U-tube arms at {R1} m and {R2} m from the axis\n")
print(f"{'rpm':>5} {'omega [rad/s]':>14} {'dh [mm]':>8}")
for rpm in [30, 60, 90, 120]:
    w = rpm * 2 * math.pi / 60  # rpm -> rad/s
    print(f"{rpm:>5} {w:>14.2f} {w**2 * (R2**2 - R1**2) / (2 * G) * 1000:>8.1f}")
dh = 0.120  # measured level difference [m]
w = math.sqrt(2 * G * dh / (R2**2 - R1**2))
print(f"\nMeasured dh = {dh * 1000:.0f} mm -> omega = {w:.2f} rad/s = {w * 60 / (2 * math.pi):.0f} rpm")
print("If one arm is ON the axis (R1 = 0) the formula reduces to the rotating-tank paraboloid of Example 6.")
print("The same balance sets the liquid levels in the arms of rotating separators and spin-coaters.")
