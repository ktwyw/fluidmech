"""Example 29 - Terminal settling velocity of spherical particles.

Force balance: (rho_p - rho) g (pi d^3 / 6) = Cd (rho U^2 / 2) (pi d^2 / 4)
Drag correlation: fluidmech.drag.sphere_drag_coefficient (Brown & Lawler 2003), Re < 2e5
"""

from fluidmech import Fluid
from fluidmech.dimensionless import reynolds
from fluidmech.drag import sphere_drag_coefficient as drag_coefficient
from fluidmech.drag import stokes_velocity, terminal_velocity

water = Fluid.water(20)
rho_sand = 2650.0  # quartz density [kg/m3]
print("Quartz sand settling in water at 20 degC")
print(f"{'d [mm]':>8} {'U [mm/s]':>9} {'Re':>9} {'Cd':>7} {'Stokes U [mm/s]':>16}  time to fall 1 m")
for d_mm in [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
    d = d_mm / 1000  # mm -> m
    u = terminal_velocity(d, rho_sand, water)
    re = reynolds(u, d, water.kinematic_viscosity)
    t = 1.0 / u  # time to fall 1 m [s]
    t_str = f"{t / 3600:.1f} h" if t > 3600 else (f"{t / 60:.1f} min" if t > 60 else f"{t:.1f} s")
    print(
        f"{d_mm:>8} {u * 1000:>9.3f} {re:>9.3g} {drag_coefficient(re):>7.2f} "
        f"{stokes_velocity(d, rho_sand, water) * 1000:>16.3f}  {t_str}"
    )
print("Stokes' law is accurate only for Re < ~0.1-0.3 (silt); it badly overpredicts for sand.")

# Settling tank design: particles must settle before leaving the tank
u_design = terminal_velocity(0.1e-3, rho_sand, water)
Q = 0.05  # flow into the settling tank [m3/s]
print(f"\nSettling tank for 0.1 mm sand, Q = {Q * 1000:.0f} L/s:")
print(f"  required plan area A = Q / U = {Q / u_design:.1f} m2 (independent of depth!)")

air = Fluid.air(20)
print("\nWater droplets falling in air (treated as rigid spheres)")
for d_mm in [0.01, 0.1, 0.5, 1.0, 2.0]:
    u = terminal_velocity(d_mm / 1000, 1000.0, air)  # water droplet (1000 kg/m3), d in m
    print(f"  d = {d_mm:>5} mm: U = {u:6.3f} m/s")
print("(Real raindrops above ~2 mm flatten, so their fall speed levels off near 9 m/s.)")
