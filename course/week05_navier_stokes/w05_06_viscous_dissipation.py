"""CHME 202 - Week 5 - Example 6: viscous dissipation - friction turns flow work into heat.

The dissipation function for simple shear is Phi = mu (du/dy)^2 [W/m3]. Over a whole
pipe or valve, all the pressure drop ends up as heat: temperature rise dT = dp / (rho cp)
if no heat is lost. The Brinkman number Br = mu U^2 / (k dT) says when this matters.
Reading: White, Section 4.5 (energy equation).
"""

# Couette flow in a lubricating film
mu, U, h = 0.05, 10.0, 50e-6  # oil viscosity [Pa s], sliding speed [m/s], film [m]
phi = mu * (U / h) ** 2  # dissipation per unit volume [W/m3]
print(f"Oil film mu = {mu} Pa s, sliding speed {U} m/s, thickness {h * 1e6:.0f} um:")
print(f"  dissipation {phi / 1e9:.1f} GW/m3 -> {phi * h / 1e3:.1f} kW per m2 of bearing surface")
k_oil = 0.14  # thermal conductivity of oil [W/(m K)]
print(
    f"  Brinkman number for a 10 K temperature difference: Br = {mu * U**2 / (k_oil * 10):.1f}  (> 1: heating dominates)\n"
)

print("Temperature rise of a liquid throttled through a valve (adiabatic, all dp -> heat):")
for name, rho, cp in [("water", 998.0, 4180.0), ("light oil", 870.0, 1900.0)]:
    for dp_bar in [5, 20, 100]:
        print(f"  {name:<10} dp = {dp_bar:>3} bar: dT = {dp_bar * 1e5 / (rho * cp):5.2f} K")
print("Small for water in normal lines, but hydraulic systems with 200 bar relief valves heat")
print("their oil quickly - hence oil coolers. In pipelines of viscous crude this heating is used on purpose.")
