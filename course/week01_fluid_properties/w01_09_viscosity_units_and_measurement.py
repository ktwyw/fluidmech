"""CHME 202 - Week 1 - Example 9: viscosity units and kinematic viscometers.

Data sheets quote viscosity in cP (dynamic) or cSt (kinematic). 1 cP = 1 mPa s,
1 cSt = 1 mm2/s. Glass capillary (Ubbelohde) viscometers give nu = C t directly.
"""

from fluidmech.units import convert

print("Unit conversions:")
for value, a, b in [
    (1.0, "cP", "Pa*s"),
    (1.0, "cSt", "m2/s"),
    (350.0, "cP", "Pa*s"),
    (1.0, "P", "cP"),
    (46.0, "cSt", "m2/s"),
]:
    print(f"  {value:g} {a} = {convert(value, a, b):.4g} {b}")

# Ubbelohde viscometer: nu = C * t (C from the calibration certificate)
C = 0.01  # mm2/s per second (cSt/s)
print(f"\nUbbelohde viscometer, constant C = {C} cSt/s:")
for liquid, t_flow, rho in [
    ("water, 20 degC", 100.5, 998.2),
    ("ethanol, 20 degC", 152.0, 789.0),
    ("light oil", 2950.0, 870.0),
]:
    nu = C * t_flow
    print(f"  {liquid:<16} efflux time {t_flow:7.1f} s -> nu = {nu:6.2f} cSt, mu = rho nu = {nu * rho / 1000:6.3f} cP")
print("Choose a capillary so the efflux time exceeds ~200 s (small timing error, negligible kinetic energy).\n")

print("ISO viscosity grades are the kinematic viscosity at 40 degC in cSt:")
for grade in [10, 32, 68, 220, 460]:
    mu = convert(grade, "cSt", "m2/s") * 870
    print(f"  ISO VG {grade:<4} nu = {grade} cSt, mu ~ {mu * 1000:6.1f} mPa s (rho = 870 kg/m3)")
