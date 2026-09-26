"""CHME 202 - Week 11 - Example 2: terminal settling velocity of particles.

Force balance: weight - buoyancy = drag, with Cd depending on the unknown
velocity - an iterative problem. The Archimedes number Ar = rho (rho_p - rho) g d^3 / mu^2
contains only known quantities and tells the regime in advance.
Applications: sedimentation tanks, cyclones, catalyst elutriation, spray towers.
"""

from fluidmech import Fluid
from fluidmech.drag import stokes_velocity, terminal_velocity
from fluidmech.porous import archimedes_number

cases = [
    ("clay/silt in water", 5e-6, 2650, Fluid.water(20)),
    ("fine sand in water", 100e-6, 2650, Fluid.water(20)),
    ("coarse sand in water", 1e-3, 2650, Fluid.water(20)),
    ("FCC catalyst in air", 70e-6, 1500, Fluid.air(500)),
    ("fine dust in air", 10e-6, 2000, Fluid.air(20)),
    ("spray droplet in air", 200e-6, 1000, Fluid.air(20)),
]
print(f"{'particle':<22} {'d [um]':>7} {'Ar':>10} {'U_t [m/s]':>10} {'Re':>8} {'Stokes U':>9}")
for name, d, rho_p, fluid in cases:
    u = terminal_velocity(d, rho_p, fluid)  # solves weight - buoyancy = drag(Re(u)) for u
    re = fluid.density * u * d / fluid.dynamic_viscosity
    ar = archimedes_number(d, rho_p, fluid.density, fluid.dynamic_viscosity)
    print(f"{name:<22} {d * 1e6:>7.0f} {ar:>10.3g} {u:>10.4g} {re:>8.3g} {stokes_velocity(d, rho_p, fluid):>9.3g}")
print("\nRule of thumb: Ar < 3.6 -> Stokes regime (Re < 0.2); Ar > 1e5 -> Newton regime.")
print("Stokes' law is only valid for the smallest particles; it grossly overpredicts U for coarse sand.")
print("Note the catalyst in HOT air: the higher gas viscosity at 500 degC slows settling.")
