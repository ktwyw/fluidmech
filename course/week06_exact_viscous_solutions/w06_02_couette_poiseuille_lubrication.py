"""CHME 202 - Week 6 - Example 2: Couette-Poiseuille flow - lubrication, coating and back-flow.

The upper plate moves at U while a pressure gradient acts. Depending on
the dimensionless pressure gradient P = G h^2 / (2 mu U) the profile is linear
(P = 0), bulges forward (P > 0) or develops back-flow near the fixed wall (P < -1).
Also: viscous torque in a journal bearing (Petroff's equation). Saves couette_poiseuille.png.

# requires: matplotlib
"""

import math

import matplotlib.pyplot as plt

from fluidmech.laminar import plates_flow_rate, plates_velocity

mu, h, U = 0.1, 1e-3, 1.0  # oil, 1 mm gap, plate speed
fig, ax = plt.subplots(figsize=(6.5, 4.5))
print(f"{'P = G h^2/(2 mu U)':>19} {'q [cm2/s]':>10}  profile")
for P in [-3, -1, 0, 1, 3]:
    G = P * 2 * mu * U / h**2  # pressure gradient giving the dimensionless value P
    ys = [i * h / 100 for i in range(101)]
    us = [plates_velocity(y, h, G, mu, U) for y in ys]
    q = plates_flow_rate(h, G, mu, U)
    if min(us) < -1e-12:
        kind = "back-flow near the fixed wall"
    elif P == 0:
        kind = "linear (pure Couette)"
    elif P == -1:
        kind = "zero shear at the fixed wall (onset of back-flow)"
    elif P < 0:
        kind = "flattened by the adverse gradient"
    else:
        kind = "forward bulge"
    print(f"{P:>19} {q * 1e4:>10.3f}  {kind}")
    ax.plot([u / U for u in us], [y / h for y in ys], label=f"P = {P}")
ax.axvline(0, color="k", lw=0.6)
ax.set(xlabel="u / U", ylabel="y / h", title="Couette-Poiseuille flow")
ax.legend()
fig.tight_layout()
fig.savefig("couette_poiseuille.png", dpi=130)
print("\nP = -3 gives zero net flow: this is how a slider bearing builds pressure to carry a load.\n")

# Petroff's equation: lightly loaded journal bearing, thin-gap Couette flow
D, L, c, rpm, mu_oil = 0.05, 0.05, 25e-6, 3000, 0.03
omega = rpm * 2 * math.pi / 60  # rpm -> rad/s
tau = mu_oil * omega * (D / 2) / c  # Couette shear in the thin clearance
torque = tau * math.pi * D * L * D / 2
print(f"Journal bearing D = {D * 1000:.0f} mm, clearance {c * 1e6:.0f} um, {rpm} rpm, oil mu = {mu_oil} Pa s")
print(f"  shear stress {tau / 1e3:.1f} kPa, friction torque {torque:.3f} N m, power loss {torque * omega:.0f} W")
print("Saved couette_poiseuille.png")
