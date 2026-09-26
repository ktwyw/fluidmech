"""CHME 202 - Week 2 - Example 11: the stack effect - how a chimney creates draft.

Hot flue gas is lighter than the outside air, so the hydrostatic pressure columns
differ: draft dp = (rho_air - rho_gas) g H. Used by furnaces, boilers and cooling towers;
it also drives air through tall buildings in winter.
"""

from fluidmech.constants import KELVIN_OFFSET, P_ATM, R_AIR, G

H = 40.0  # stack height [m]
T_gas = 200.0
print(f"Stack {H:.0f} m high, flue gas at {T_gas:.0f} degC (treated as air)\n")
print(f"{'outside T [degC]':>17} {'rho air':>8} {'rho gas':>8} {'draft [Pa]':>11}")
rho_gas = P_ATM / (R_AIR * (T_gas + KELVIN_OFFSET))
for T_out in [30, 20, 0, -20, -35]:
    rho_air = P_ATM / (R_AIR * (T_out + KELVIN_OFFSET))
    print(f"{T_out:>17} {rho_air:>8.3f} {rho_gas:>8.3f} {(rho_air - rho_gas) * G * H:>11.1f}")
print("\nDraft is only ~200 Pa (2 cm of water), yet it drives the whole combustion-air flow of a natural-")
print("draft furnace. It is strongest in cold winters (Astana at -35 degC) and weakest on hot days,")
print("so burners are checked for the summer case. Taller stacks give proportionally more draft.")
