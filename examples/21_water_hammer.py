"""Example 21 - Water hammer: pressure surge from sudden valve closure.

Wave speed in an elastic pipe:  c = sqrt( (K/rho) / (1 + K D / (E e)) )
Joukowsky surge:                dp = rho c dV          (closure faster than 2L/c)
Slow closure (Michaud):         dp ~ 2 rho L V / t_c   (closure slower than 2L/c)
"""

import math

from fluidmech import Fluid

water = Fluid.water(15)
K_water = 2.15e9  # bulk modulus [Pa]
D, V0, L = 0.30, 2.0, 1200.0  # diameter, velocity, pipe length

materials = {  # (Young's modulus [Pa], wall thickness [m])
    "steel": (200e9, 0.008),
    "ductile iron": (170e9, 0.008),
    "concrete": (30e9, 0.050),
    "PVC": (3.0e9, 0.015),
    "HDPE": (0.9e9, 0.027),
}

c_rigid = math.sqrt(K_water / water.density)
print(f"Speed of sound in water (rigid pipe): {c_rigid:.0f} m/s")
print(f"Pipe D = {D * 1000:.0f} mm, L = {L:.0f} m, V0 = {V0} m/s, instantaneous closure\n")
print(f"{'material':<13} {'c [m/s]':>8} {'dp [bar]':>9} {'surge head [m]':>15} {'2L/c [s]':>9}")
for name, (E, e) in materials.items():
    # Korteweg wave speed (pipe-wall elasticity lowers it)
    c = math.sqrt((K_water / water.density) / (1 + K_water * D / (E * e)))
    dp = water.density * c * V0
    print(f"{name:<13} {c:>8.0f} {dp / 1e5:>9.1f} {dp / (water.density * 9.80665):>15.0f} {2 * L / c:>9.2f}")

print("\nFlexible plastic pipes have much lower wave speeds and hence lower surges.")

# Effect of closure time for the steel pipe
E, e = materials["steel"]
c = math.sqrt((K_water / water.density) / (1 + K_water * D / (E * e)))
t_crit = 2 * L / c  # time for a pressure wave to travel to the reservoir and back
print(f"\nSteel pipe, critical closure time 2L/c = {t_crit:.2f} s")
print(f"{'closure time [s]':>17} {'dp [bar]':>9}")
for tc in [0.5, t_crit, 5, 10, 20, 60]:
    dp = water.density * c * V0 if tc <= t_crit else 2 * water.density * L * V0 / tc
    print(f"{tc:>17.2f} {dp / 1e5:>9.1f}")
print("Closing valves slowly (>> 2L/c) is the simplest surge protection.")
