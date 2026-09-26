"""Example 5 - Property tables for water and air.

Prints the kind of property table found in the appendix of a fluid mechanics
textbook, generated from the correlations in ``fluidmech.properties``.
"""

from fluidmech.properties import (
    air_density,
    air_dynamic_viscosity,
    air_kinematic_viscosity,
    water_density,
    water_dynamic_viscosity,
    water_kinematic_viscosity,
)

print("Liquid water at atmospheric pressure")
print(f"{'T [degC]':>9} {'rho [kg/m3]':>12} {'mu [Pa s]':>12} {'nu [m2/s]':>12}")
for t in range(0, 101, 10):  # 0-100 degC in 10 K steps (liquid-water range)
    print(f"{t:>9} {water_density(t):>12.2f} {water_dynamic_viscosity(t):>12.4e} {water_kinematic_viscosity(t):>12.4e}")

print("\nDry air at 1 atm")
print(f"{'T [degC]':>9} {'rho [kg/m3]':>12} {'mu [Pa s]':>12} {'nu [m2/s]':>12}")
for t in range(-40, 201, 20):  # -40 to 200 degC
    print(f"{t:>9} {air_density(t):>12.4f} {air_dynamic_viscosity(t):>12.4e} {air_kinematic_viscosity(t):>12.4e}")

print("\nNote: water viscosity falls with temperature while air viscosity rises.")
print(f"Water: mu(80)/mu(20) = {water_dynamic_viscosity(80) / water_dynamic_viscosity(20):.2f}")
print(f"Air:   mu(80)/mu(20) = {air_dynamic_viscosity(80) / air_dynamic_viscosity(20):.2f}")
