"""Example 30 - Aerodynamic drag: wind loads and the power to move through air.

F_D = Cd (1/2) rho V^2 A
"""

import math

from fluidmech import Fluid
from fluidmech.dimensionless import reynolds

air = Fluid.air(15)
q_dyn = lambda v: 0.5 * air.density * v**2  # noqa: E731  dynamic pressure

# --- Wind load on structures --------------------------------------------- #
print("Wind loads at 35 m/s (storm)")
V = 35.0  # storm wind speed [m/s]
structures = [
    # name, Cd, frontal area [m2], characteristic length [m]
    ("Billboard 10 m x 4 m (flat plate)", 1.2, 40.0, 4.0),
    ("Chimney D = 2 m, H = 40 m (cylinder)", 0.7, 80.0, 2.0),
    ("Lattice tower face", 2.0, 25.0, 0.1),
    ("Hemispherical dome D = 20 m", 0.4, 157.0, 20.0),
]
for name, cd, area, length in structures:
    f = cd * q_dyn(V) * area
    re = reynolds(V, length, air.kinematic_viscosity)
    print(f"  {name:<40} Re = {re:8.2e}  F = {f / 1e3:7.1f} kN")
print(f"  (dynamic pressure q = {q_dyn(V):.0f} Pa; doubling wind speed quadruples the load)\n")

# --- Drag power of vehicles ---------------------------------------------- #
vehicles = [
    ("Upright cyclist", 0.9, 0.50),
    ("Racing cyclist, tuck", 0.7, 0.35),
    ("Family car", 0.30, 2.2),
    ("SUV", 0.40, 2.8),
    ("Truck / lorry", 0.65, 9.5),
]
speeds_kmh = [20, 50, 90, 120]  # vehicle speeds [km/h]
print("Power needed to overcome aerodynamic drag, P = F_D V [kW]")
print(f"{'vehicle':<22} {'CdA [m2]':>8} " + "".join(f"{s:>8} km/h" for s in speeds_kmh))
for name, cd, area in vehicles:
    powers = [cd * area * q_dyn(s / 3.6) * s / 3.6 / 1e3 for s in speeds_kmh]  # P = F V; km/h -> m/s, W -> kW
    print(f"{name:<22} {cd * area:>8.2f} " + "".join(f"{p:>13.2f}" for p in powers))
print(f"\nDrag power grows with V^3: going from 90 to 120 km/h needs {(120 / 90) ** 3:.2f}x the aerodynamic power.")

# --- Drag crisis of a sphere --------------------------------------------- #
print("\nGolf ball vs. smooth sphere (D = 42.7 mm) at 70 m/s:")
d, v = 0.0427, 70.0  # golf-ball diameter [m] and launch speed [m/s]
re = reynolds(v, d, air.kinematic_viscosity)
area = math.pi * d**2 / 4  # frontal area of the ball [m2]
for name, cd in [("smooth sphere (subcritical, Cd ~ 0.47)", 0.47), ("dimpled golf ball (Cd ~ 0.25)", 0.25)]:
    print(f"  Re = {re:.2e}  {name:<40} F = {cd * q_dyn(v) * area:.2f} N")
print("Dimples trip the boundary layer to turbulence, delaying separation and halving drag.")
