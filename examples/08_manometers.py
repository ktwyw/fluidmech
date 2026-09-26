"""Example 8 - Manometers: piezometer, U-tube and inclined manometer."""

import math

from fluidmech.constants import G
from fluidmech.hydrostatics import manometer_pressure_difference, pressure_at_depth

rho_water, rho_mercury, rho_gauge_oil = 1000.0, 13_600.0, 827.0  # densities [kg/m3]

# 1. Piezometer: water rises 1.35 m above a pipe centreline
h = 1.35
print("1) Piezometer tube")
print(f"   Water column of {h} m -> gauge pressure = {pressure_at_depth(h) / 1e3:.2f} kPa\n")

# 2. U-tube mercury manometer across an orifice plate in a water line
reading = 0.180
dp = manometer_pressure_difference(reading, rho_mercury, rho_water)
print("2) Mercury U-tube across an orifice plate (water flowing)")
print(f"   Reading {reading * 1000:.0f} mm Hg -> dp = {dp / 1e3:.2f} kPa")
print(f"   Equivalent water head = {dp / (rho_water * G):.2f} m\n")

# 3. Inclined manometer for a small air-duct pressure difference
angle = 15.0
length_along_tube = 0.120  # liquid displacement read along the inclined tube [m]
vertical = length_along_tube * math.sin(math.radians(angle))
dp_air = manometer_pressure_difference(vertical, rho_gauge_oil, flowing_density=1.2)
print(f"3) Inclined manometer at {angle:.0f} deg with gauge oil (SG 0.827), air above")
print(f"   Reading along tube {length_along_tube * 1000:.0f} mm = {vertical * 1000:.1f} mm vertical")
print(f"   dp = {dp_air:.1f} Pa")
print(f"   Amplification vs. a vertical tube: x{1 / math.sin(math.radians(angle)):.2f}\n")

# 4. Which gauge liquid for a target resolution?
print("4) Deflection produced by dp = 500 Pa (gas above the gauge liquid)")
for name, rho in [("water", 1000.0), ("gauge oil", 827.0), ("mercury", 13_600.0)]:
    print(f"   {name:<10} {500.0 / (rho * G) * 1000:7.1f} mm")
