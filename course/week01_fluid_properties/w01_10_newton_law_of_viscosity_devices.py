"""CHME 202 - Week 1 - Example 10: Newton's law of viscosity in simple devices.

For a thin film with a linear velocity profile, tau = mu U / h.
(a) a plate dragged over an oil film; (b) a block sliding down an oiled incline
(terminal velocity); (c) a shaft turning in a lubricated sleeve.
Reading: White, Section 1.7 (Examples 1.8-1.10 are of this type).
"""

import math

from fluidmech.constants import G

mu = 0.29  # SAE 30 oil at 20 degC [Pa s]

# (a) Plate on an oil film
A, h = 0.5, 0.5e-3
for U in [0.1, 0.5, 1.0]:
    print(
        f"(a) plate {A} m2 on a {h * 1000} mm film at {U} m/s: tau = {mu * U / h:6.1f} Pa, "
        f"force {mu * U / h * A:6.1f} N, power {mu * U**2 / h * A:6.1f} W"
    )

# (b) Block sliding down an incline on an oil film reaches terminal speed when
#     W sin(theta) = mu U A / h
m, theta, A_b, h_b = 10.0, 20.0, 0.04, 0.2e-3
U_t = m * G * math.sin(math.radians(theta)) * h_b / (mu * A_b)  # weight component along the slope = viscous force
print(
    f"\n(b) {m} kg block, {theta:.0f} deg incline, {A_b} m2 contact, {h_b * 1000} mm film: terminal speed {U_t:.3f} m/s"
)
print(f"    time constant m h / (mu A) = {m * h_b / (mu * A_b):.3f} s -> terminal speed reached almost at once")

# (c) Shaft in a sleeve
D, L, c, rpm = 0.06, 0.10, 0.1e-3, 1500
U = math.pi * D * rpm / 60  # surface speed of the shaft [m/s]
torque = mu * U / c * math.pi * D * L * D / 2
print(f"\n(c) shaft D = {D * 1000:.0f} mm in a {L * 1000:.0f} mm sleeve, clearance {c * 1000} mm, {rpm} rpm:")
print(
    f"    surface speed {U:.2f} m/s, friction torque {torque:.2f} N m, heat generated {torque * rpm * 2 * math.pi / 60:.0f} W"
)
print("    All that power heats the oil - viscosity then falls (Example 2), a key design coupling.")
