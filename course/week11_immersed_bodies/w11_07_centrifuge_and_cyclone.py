"""CHME 202 - Week 11 - Example 7: separating particles faster than gravity - centrifuges and cyclones.

In a centrifugal field the settling velocity is multiplied by omega^2 r / g (Stokes regime).
Cyclones use a spinning gas stream; Lapple's model gives the cut size (50 % efficiency)
d50 = sqrt(9 mu W / (2 pi N_e V_i (rho_p - rho))) and efficiency 1 / (1 + (d50/d)^2).
"""

import math

from fluidmech import Fluid
from fluidmech.drag import stokes_velocity

# Decanter centrifuge for fine solids in water
water = Fluid.water(20)
d, rho_p = 5e-6, 2000.0  # particle diameter [m] and density [kg/m3]
ut = stokes_velocity(d, rho_p, water)
print(
    f"{d * 1e6:.0f} um particles (rho = {rho_p:.0f}) in water: gravity settling {ut * 1e6:.1f} um/s "
    f"(1 m takes {1 / ut / 3600:.0f} h)"
)
for rpm, r in [(1500, 0.2), (3000, 0.2), (6000, 0.15)]:
    w = rpm * 2 * math.pi / 60  # rpm -> rad/s
    g_factor = w**2 * r / 9.80665  # centrifugal acceleration in multiples of g
    print(f"  centrifuge {rpm} rpm at r = {r} m: {g_factor:6.0f} g -> settling {ut * g_factor * 1000:.2f} mm/s")

# Lapple cyclone for dust in air
air = Fluid.air(20)
D = 0.5  # cyclone body diameter [m]
W, Vi, Ne, rho_dust = D / 4, 15.0, 6, 2500.0  # inlet width [m], inlet velocity [m/s], effective turns, dust density
d50 = math.sqrt(9 * air.dynamic_viscosity * W / (2 * math.pi * Ne * Vi * (rho_dust - air.density)))  # Lapple cut size
print(f"\nLapple cyclone D = {D} m, inlet width {W} m, inlet velocity {Vi} m/s: cut size d50 = {d50 * 1e6:.1f} um")
print(f"{'d [um]':>7} {'efficiency':>11}")
for dp in [1, 2, 5, 10, 20, 50]:
    print(f"{dp:>7} {1 / (1 + (d50 / (dp * 1e-6)) ** 2):>11.1%}")
print("Smaller cyclones (or higher inlet velocity) catch finer dust, at the cost of pressure drop;")
print("particles below ~2 um need bag filters or electrostatic precipitators.")
