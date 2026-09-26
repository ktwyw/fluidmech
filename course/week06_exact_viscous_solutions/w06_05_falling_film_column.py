"""CHME 202 - Week 6 - Example 5: falling liquid films (wetted-wall columns, absorbers, evaporators).

A laminar film on a vertical wall has thickness delta = (3 mu Gamma / rho^2 g)^(1/3)
and a semi-parabolic profile with maximum velocity at the free surface
(1.5 times the mean). Film thickness controls heat and mass transfer.
Reading: Bird, Stewart & Lightfoot, Section 2.2; White, Problem 4.80.
"""

import math

from fluidmech import Fluid
from fluidmech.laminar import film_reynolds, film_thickness, film_velocity

water = Fluid.water(20)
D_col, L_col = 0.025, 1.0  # wetted-wall column diameter and height [m]
perimeter = math.pi * D_col
print(f"Water film inside a vertical tube, D = {D_col * 1000:.0f} mm\n")
print(
    f"{'Q [mL/s]':>9} {'Gamma [kg/m s]':>15} {'Re_film':>8} {'delta [mm]':>11} {'u_surface [m/s]':>16} {'contact time [s]':>17}"
)
for q_ml in [0.1, 0.3, 2, 10, 40]:
    gamma = water.density * q_ml * 1e-6 / perimeter  # mass flow per unit wetted perimeter [kg/(m s)]; mL -> m3
    delta = film_thickness(gamma, water.density, water.dynamic_viscosity)
    u_s = film_velocity(delta, delta, water.density, water.dynamic_viscosity)
    re = film_reynolds(gamma, water.dynamic_viscosity)
    flag = "  smooth laminar" if re < 20 else ("  wavy laminar" if re < 1600 else "  turbulent")
    print(f"{q_ml:>9.1f} {gamma:>15.4f} {re:>8.0f} {delta * 1000:>11.3f} {u_s:>16.3f} {L_col / u_s:>17.2f}{flag}")

gamma = water.density * 10e-6 / perimeter
delta = film_thickness(gamma, water.density, water.dynamic_viscosity)
mean = gamma / (water.density * delta)
print(
    f"\nCheck: u_surface / u_mean = {film_velocity(delta, delta, water.density, water.dynamic_viscosity) / mean:.3f} "
    "(exactly 3/2 for a laminar film)"
)
print("Nusselt's smooth-film theory is exact below Re ~ 20 and a fair estimate for wavy films;")
print("above Re ~ 1600 the film is turbulent and thinner than predicted.")
print("The gas-liquid contact time at the surface sets the absorption rate (penetration theory):")
print("thin, fast films refresh the interface quickly.")
