"""CHME 202 - Week 3 - Example 16: measuring stack-gas velocity - use the density of the ACTUAL gas.

Emission monitoring measures flue-gas velocity with a Pitot (S-type) probe: V = Cp sqrt(2 dp / rho).
The density must be that of the hot, humid flue gas at stack pressure. Using ambient-air density
is a classic error that biases velocity, flow rate and hence reported emissions.
"""

import math

from fluidmech.constants import KELVIN_OFFSET, P_ATM

R_u = 8.314462618  # universal gas constant [J/(mol K)]
Cp = 0.84  # S-type Pitot coefficient (calibrated)
dp = 120.0  # measured velocity pressure [Pa]
D_stack = 1.2
# Flue gas composition (mole fractions) and molar masses [kg/mol]
comp = {"N2": (0.72, 0.028), "CO2": (0.10, 0.044), "H2O": (0.14, 0.018), "O2": (0.04, 0.032)}
M = sum(x * m for x, m in comp.values())  # mean molar mass of the mixture [kg/mol]
T_gas, p_stack = 180.0, P_ATM - 300.0  # stack temperature [degC]; slight draft suction [Pa]
rho_gas = p_stack * M / (R_u * (T_gas + KELVIN_OFFSET))
rho_air = P_ATM * 0.02897 / (R_u * (20 + KELVIN_OFFSET))
print(
    f"Flue gas: molar mass {M * 1000:.1f} g/mol at {T_gas:.0f} degC -> rho = {rho_gas:.3f} kg/m3 "
    f"(ambient air {rho_air:.3f})\n"
)
for label, rho in [("actual flue-gas density", rho_gas), ("ambient-air density (wrong)", rho_air)]:
    V = Cp * math.sqrt(2 * dp / rho)
    Q = V * math.pi * D_stack**2 / 4
    print(f"  {label:<28} V = {V:5.2f} m/s, Q = {Q:5.2f} m3/s actual, mass flow {Q * rho_gas:5.2f} kg/s")
err = math.sqrt(rho_gas / rho_air) - 1
print(f"\nUsing the ambient density underestimates the velocity by {-err:.0%}. Because pollutant mass flow")
print("= concentration x volumetric flow, the reported emissions would be low by the same fraction.")
print("Stack-testing standards therefore require measured temperature, pressure, moisture and composition.")
