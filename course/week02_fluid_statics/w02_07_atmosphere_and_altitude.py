"""CHME 202 - Week 2 - Example 7: pressure variation in the atmosphere.

Hydrostatics for a compressible fluid: dp/dz = -rho g with rho = p / (R T).
Compares the incompressible, isothermal and standard-atmosphere (linear
temperature) models, and shows why altitude matters for pumps (NPSH).
Reading: White, Section 2.3.
"""

import math

from fluidmech.constants import P_ATM, R_AIR, G
from fluidmech.properties import standard_atmosphere, water_vapor_pressure

rho0, T0 = 1.225, 288.15  # sea-level air density [kg/m3] and temperature [K]
print(f"{'z [m]':>7} {'incompressible':>15} {'isothermal':>11} {'ISA':>9}   [kPa]")
for z in [0, 500, 1000, 2000, 4000, 8000, 11000]:
    p_inc = P_ATM - rho0 * G * z
    p_iso = P_ATM * math.exp(-G * z / (R_AIR * T0))
    _, p_isa, _ = standard_atmosphere(z)
    print(f"{z:>7} {p_inc / 1e3:>15.1f} {p_iso / 1e3:>11.1f} {p_isa / 1e3:>9.1f}")
print("The incompressible model is fine for a few hundred metres (tanks, buildings) but badly wrong")
print("for the atmosphere as a whole.\n")

print("Why it matters for chemical plants and pumps:")
for place, z in [
    ("sea level", 0),
    ("Astana (~350 m)", 350),
    ("Almaty (~800 m)", 800),
    ("mountain site (2500 m)", 2500),
]:
    _, p, _ = standard_atmosphere(z)
    # boiling point of water where vapour pressure = local pressure
    lo, hi = 50.0, 100.0
    for _ in range(50):  # bisection: find T where the vapour pressure equals the local air pressure
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if water_vapor_pressure(mid) < p else (lo, mid)
    atm_head = p / (1000 * G)
    print(
        f"  {place:<24} p_atm = {p / 1e3:6.1f} kPa, water boils at {mid:5.1f} degC, atmospheric head {atm_head:5.2f} m"
    )
print("Lower atmospheric pressure reduces the suction head available to a pump (NPSHa, Week 10).")
