"""CHME 202 - Week 5 - Example 7: creeping flow around a sphere (Stokes 1851).

Dropping the inertia terms of Navier-Stokes (Re << 1) leads to Stokes' law
F = 3 pi mu d U: one third from pressure (form) drag, two thirds from viscous
shear. Oseen's correction extends it slightly: Cd = 24/Re (1 + 3 Re / 16).
Reading: White, Section 7.6.
"""

import math

from fluidmech import Fluid
from fluidmech.drag import sphere_drag_coefficient

water = Fluid.water(20)
d, U = 50e-6, 1e-3  # sphere diameter [m], speed [m/s]
F = 3 * math.pi * water.dynamic_viscosity * d * U  # Stokes' law
print(
    f"Sphere d = {d * 1e6:.0f} um moving at {U * 1000} mm/s in water: Re = {water.density * U * d / water.dynamic_viscosity:.3f}"
)
print(f"  Stokes drag {F * 1e9:.3f} nN = pressure {F / 3 * 1e9:.3f} nN + viscous {2 * F / 3 * 1e9:.3f} nN\n")

print(f"{'Re':>6} {'Stokes 24/Re':>13} {'Oseen':>8} {'correlation':>12} {'Stokes error':>13}")
for re in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]:
    stokes = 24 / re
    oseen = 24 / re * (1 + 3 * re / 16)  # Oseen's first inertia correction
    corr = sphere_drag_coefficient(re)
    print(f"{re:>6} {stokes:>13.2f} {oseen:>8.2f} {corr:>12.2f} {stokes / corr - 1:>+13.0%}")
e01 = 1 - 240 / sphere_drag_coefficient(0.1)
e1 = 1 - 24 / sphere_drag_coefficient(1.0)
print(f"\nStokes' law underestimates drag by ~{e01:.0%} at Re = 0.1 and ~{e1:.0%} at Re = 1;")
print("Re < ~0.1-0.3 is the usual limit for using it.")
print("Creeping flow is reversible: run it backwards and it retraces its path (G.I. Taylor's demonstration).")
