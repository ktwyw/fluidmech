"""CHME 202 - Week 13 - Example 14: bubble size from a sparger orifice - a force balance in Pi groups.

At low gas rates a bubble grows until buoyancy overcomes the surface-tension force at the
orifice rim: (pi/6) d_b^3 drho g = pi d_o sigma  ->  d_b = (6 d_o sigma / (drho g))^(1/3).
In dimensionless form: d_b / d_o = (6 / Eo_o)^(1/3), Eo_o = drho g d_o^2 / sigma (Eotvos number).
"""

from fluidmech.properties import water_density, water_surface_tension

sigma, rho = water_surface_tension(25), water_density(25)
print(f"{'orifice [mm]':>13} {'Eo_o':>8} {'bubble d [mm]':>14} {'d_b / d_o':>10}")
for d_o_mm in [0.2, 0.5, 1.0, 2.0, 4.0]:
    d_o = d_o_mm / 1000  # mm -> m
    eo = rho * 9.80665 * d_o**2 / sigma
    d_b = (6 * d_o * sigma / (rho * 9.80665)) ** (1 / 3)  # buoyancy (pi/6 d_b^3 rho g) = surface tension (pi d_o sigma)
    print(f"{d_o_mm:>13} {eo:>8.4f} {d_b * 1000:>14.2f} {d_b / d_o:>10.2f}")
print("\nBubble size grows only as d_o^(1/3): even a 0.2 mm hole gives ~2 mm bubbles in water.")
print("This quasi-static result holds at low gas rates; at higher rates bubbles grow faster than they")
print("detach and become larger. Surfactants (lower sigma) and porous spargers give finer bubbles -")
print("more interfacial area for gas-liquid mass transfer (Week 11, Example 10; Week 14).")
