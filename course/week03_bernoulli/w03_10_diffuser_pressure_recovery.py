"""CHME 202 - Week 3 - Example 10: diffusers - turning velocity back into pressure.

In an ideal diffuser from area A1 to A2, Bernoulli gives the pressure-recovery
coefficient Cp = (p2 - p1) / (0.5 rho V1^2) = 1 - (A1/A2)^2. Real diffusers
achieve 60-85 % of this if the angle is small; wide angles separate (a sudden
expansion loses the Borda-Carnot head instead).
Reading: White, Section 6.9 (diffuser performance).
"""

rho, V1 = 1000.0, 6.0  # water [kg/m3], inlet velocity [m/s]
q_dyn = 0.5 * rho * V1**2  # inlet dynamic pressure [Pa]
print(f"Inlet velocity {V1} m/s, dynamic pressure {q_dyn / 1e3:.1f} kPa\n")
print(f"{'area ratio':>11} {'ideal Cp':>9} {'good diffuser':>14} {'sudden expansion':>17}   [kPa recovered]")
for ar in [1.5, 2.0, 3.0, 4.0]:
    cp_ideal = 1 - 1 / ar**2  # Bernoulli + continuity
    cp_real = 0.8 * cp_ideal  # well-designed conical diffuser, ~7 deg total angle
    # sudden expansion: momentum balance gives Cp = 2 (A1/A2) (1 - A1/A2)
    cp_sudden = 2 / ar * (1 - 1 / ar)
    print(f"{ar:>11} {cp_ideal:>9.3f} {cp_real * q_dyn / 1e3:>14.2f} {cp_sudden * q_dyn / 1e3:>17.2f}")
print("\nEven a sudden expansion recovers some pressure (momentum theorem, Week 9), but a gentle diffuser")
print("recovers much more. Pump casings, Venturi meters and ejector outlets all rely on diffusers.")
