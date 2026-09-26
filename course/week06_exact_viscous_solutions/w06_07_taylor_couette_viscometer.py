"""CHME 202 - Week 6 - Example 7: flow between rotating cylinders (exact) and its stability.

Inner cylinder (R1) rotating at omega, outer (R2) fixed: v_theta = A r + B / r with
A = -omega R1^2 / (R2^2 - R1^2), B = omega R1^2 R2^2 / (R2^2 - R1^2).
Torque M = 4 pi mu omega L R1^2 R2^2 / (R2^2 - R1^2). Above a critical Taylor number
the flow develops Taylor vortices and the viscometer formula no longer holds.
Reading: White, Section 4.10 (flow between long concentric cylinders).
"""

import math

mu, rho = 0.01, 1000.0  # liquid [Pa s], [kg/m3]
R1, R2, L = 0.020, 0.022, 0.08  # cylinder radii and length [m]
d = R2 - R1
A = lambda w: -w * R1**2 / (R2**2 - R1**2)  # noqa: E731
B = lambda w: w * R1**2 * R2**2 / (R2**2 - R1**2)  # noqa: E731
print(f"Cylinders R1 = {R1 * 1000:.0f} mm, R2 = {R2 * 1000:.0f} mm, liquid mu = {mu} Pa s\n")
w = 10.0  # inner-cylinder speed [rad/s]
print(f"Velocity profile at omega = {w} rad/s:")
for i in range(5):
    r = R1 + d * i / 4
    print(
        f"  r = {r * 1000:.1f} mm: v = {abs(A(w) * r + B(w) / r) if abs(A(w) * r + B(w) / r) < 1e-12 else A(w) * r + B(w) / r:.4f} m/s (linear estimate {w * R1 * (R2 - r) / d:.4f})"
    )

print(f"\n{'omega [rad/s]':>14} {'torque [mN m]':>14} {'Taylor number':>14}  state")
for w in [5, 20, 50, 100, 200]:
    M = 4 * math.pi * mu * w * L * R1**2 * R2**2 / (R2**2 - R1**2)
    ta = rho**2 * w**2 * R1 * d**3 / mu**2  # narrow-gap Taylor number
    state = "laminar Couette" if ta < 1708 else "TAYLOR VORTICES - formula invalid"
    print(f"{w:>14} {M * 1000:>14.3f} {ta:>14.0f}  {state}")
print("\nViscometers keep the gap narrow and speeds moderate so that Ta < 1708.")
print("Taylor vortices are also used on purpose: Taylor-Couette reactors give intense, uniform mixing.")
