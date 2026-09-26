"""CHME 202 - Week 11 - Example 8: how quickly does a falling sphere reach terminal velocity?

Unsteady momentum balance including the added (virtual) mass of fluid carried along:
(m + 0.5 rho V) dU/dt = (rho_p - rho) V g - Cd(Re) 0.5 rho U^2 A.
Checks the Lab 3 assumption that spheres fall at terminal speed between the marks.
"""

import math

from fluidmech import Fluid
from fluidmech.constants import G
from fluidmech.drag import sphere_drag_coefficient, terminal_velocity

liquid = Fluid(1210.0, 0.060, "80 % glycerol")
air = Fluid.air(20)
cases = [
    ("glass 3 mm in glycerol", 3e-3, 2500.0, liquid),
    ("steel 8 mm in glycerol", 8e-3, 7800.0, liquid),
    ("water drop 2 mm in air", 2e-3, 1000.0, air),
    ("sand 0.2 mm in air", 0.2e-3, 2650.0, air),
]
print(f"{'case':<26} {'U_t [m/s]':>10} {'t99 [s]':>8} {'distance to 99% [m]':>20}")
for name, d, rho_p, fl in cases:
    vol, area = math.pi * d**3 / 6, math.pi * d**2 / 4
    m_eff = rho_p * vol + 0.5 * fl.density * vol  # particle mass + added mass (half the displaced fluid)
    ut = terminal_velocity(d, rho_p, fl)
    u = x = t = 0.0
    dt = 1e-5  # initial time step [s]; grows as the motion settles
    while u < 0.99 * ut:  # integrate until 99 % of the terminal velocity
        re = max(fl.density * u * d / fl.dynamic_viscosity, 1e-9)
        drag = sphere_drag_coefficient(re) * 0.5 * fl.density * u**2 * area
        u += dt * ((rho_p - fl.density) * vol * G - drag) / m_eff  # (net weight - drag) / effective mass
        x += u * dt
        t += dt
        dt = min(dt * 1.001, 1e-3)
    print(f"{name:<26} {ut:>10.3f} {t:>8.3f} {x:>20.3f}")
print("\nIn viscous liquids small spheres reach terminal speed within millimetres, but large dense ones")
print("need ~20 cm: in Lab 3, place the first timing mark at least 25 cm below the release point.")
print("In air, drops need metres - measuring their terminal velocity requires a free-fall tower.")
