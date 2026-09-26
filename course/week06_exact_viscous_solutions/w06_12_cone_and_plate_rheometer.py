"""CHME 202 - Week 6 - Example 12: the cone-and-plate rheometer.

A shallow cone (angle theta) rotating at omega over a flat plate gives the SAME shear
rate everywhere in the gap: gamma_dot = omega / theta (the gap grows with r exactly as the
speed does). The torque gives the shear stress: tau = 3 M / (2 pi R^3). That makes it the
standard instrument for non-Newtonian flow curves.
"""

import math

from fluidmech.rheology import fit_power_law

R, theta = 0.025, math.radians(2.0)  # 50 mm cone, 2 degree angle
omegas = [0.05, 0.2, 0.8, 3.2, 12.8]  # rad/s
torques_mNm = [0.141, 0.305, 0.664, 1.44, 3.13]  # measured (illustrative data)
print(f"Cone R = {R * 1000:.0f} mm, angle {math.degrees(theta):.0f} deg\n")
print(f"{'omega [rad/s]':>14} {'torque [mN m]':>14} {'shear rate [1/s]':>17} {'stress [Pa]':>12} {'mu_app [Pa s]':>14}")
rates, stresses = [], []
for w, m in zip(omegas, torques_mNm):
    rate = w / theta  # uniform shear rate in the cone gap
    tau = 3 * m / 1000 / (2 * math.pi * R**3)  # mN m -> N m; tau = 3 M / (2 pi R^3)
    rates.append(rate)
    stresses.append(tau)
    print(f"{w:>14} {m:>14.3f} {rate:>17.2f} {tau:>12.2f} {tau / rate:>14.3f}")
fit = fit_power_law(rates, stresses)
print(f"\nPower-law fit: K = {fit.K:.2f} Pa s^n, n = {fit.n:.3f} ({fit.behaviour})")
print("A parallel-plate geometry instead has a shear rate that grows with radius (zero at the centre),")
print("so its torque must be corrected before it gives a flow curve (Rabinowitsch-type correction).")
