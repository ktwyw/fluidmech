"""CHME 202 - Week 1 - Example 3: measuring viscosity.

(a) Concentric-cylinder (Couette) viscometer: torque versus rotation speed.
(b) Falling-ball viscometer: Stokes' law with a wall correction.
Reading: White, Section 1.7 and Problems 1.49-1.56.
"""

import math

from fluidmech.rheology import fit_newtonian

# (a) Couette viscometer: inner cylinder radius Ri rotates at omega inside a fixed cup Ro.
# Exact torque for Newtonian fluid: M = 4 pi mu omega L Ri^2 Ro^2 / (Ro^2 - Ri^2)
Ri, Ro, L = 0.020, 0.021, 0.060
rpm = [10, 20, 50, 100, 200]  # rotation speeds of the inner cylinder
torque_mNm = [0.62, 1.25, 3.10, 6.26, 12.45]  # measured (illustrative lab data)

omega = [n * 2 * math.pi / 60 for n in rpm]  # rpm -> rad/s
geometry = 4 * math.pi * L * Ri**2 * Ro**2 / (Ro**2 - Ri**2)  # M = mu * geometry * omega (exact Couette result)
# Torque is linear in omega for a Newtonian fluid, so fit M = (mu * geometry) * omega
fit = fit_newtonian(omega, [m / 1000 for m in torque_mNm])
mu = fit.mu / geometry
print("(a) Couette viscometer")
print(f"    gap = {(Ro - Ri) * 1000:.1f} mm, bob length {L * 1000:.0f} mm")
print(f"{'rpm':>8} {'omega [rad/s]':>14} {'torque [mN m]':>14} {'shear rate [1/s]':>17}")
for n, w, m in zip(rpm, omega, torque_mNm):
    gamma = w * Ri / (Ro - Ri)  # narrow-gap approximation
    print(f"{n:>8} {w:>14.3f} {m:>14.2f} {gamma:>17.1f}")
print(f"    Fitted viscosity mu = {mu * 1000:.1f} mPa s (torque proportional to speed -> Newtonian)")

# Narrow-gap approximation vs exact
approx = 2 * math.pi * Ri**3 * L / (Ro - Ri)
print(f"    Narrow-gap formula M = 2 pi Ri^3 L mu omega / gap differs from exact by {approx / geometry - 1:+.1%}\n")

# (b) Falling ball: steel ball falling through oil in a tube
d, D_tube = 3.0e-3, 30e-3
rho_ball, rho_oil = 7800.0, 890.0  # steel ball and oil densities [kg/m3]
distance, time = 0.200, 18.4  # m, s
U = distance / time
mu_stokes = (rho_ball - rho_oil) * 9.80665 * d**2 / (18 * U)
ratio = d / D_tube
faxen = 1 - 2.104 * ratio + 2.09 * ratio**3 - 0.95 * ratio**5  # wall correction factor
mu_corrected = mu_stokes * faxen
re = rho_oil * U * d / mu_corrected
print("(b) Falling-ball viscometer")
print(
    f"    ball {d * 1000:.1f} mm in a {D_tube * 1000:.0f} mm tube falls {distance} m in {time} s -> U = {U * 1000:.1f} mm/s"
)
print(f"    Stokes' law                mu = {mu_stokes:.3f} Pa s")
print(f"    with Faxen wall correction mu = {mu_corrected:.3f} Pa s ({faxen - 1:+.0%})")
print(
    f"    check Reynolds number Re = {re:.4f} {'< 0.1: Stokes law valid' if re < 0.1 else '-> too fast for Stokes law!'}"
)
