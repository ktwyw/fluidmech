"""CHME 202 - Week 13 - Example 7: collapsing drag data with dimensionless groups.

Forces measured on spheres of different sizes in different fluids at different
speeds span many decades. Expressed as Cd and Re they fall on ONE curve. Here the
'measurements' are generated from the standard drag curve with 3 % scatter.
"""

import math
import random

from fluidmech import Fluid
from fluidmech.drag import drag_force, sphere_drag_coefficient

random.seed(11)
fluids = [Fluid.water(20), Fluid.air(20), Fluid(1261.0, 1.41, "glycerol"), Fluid(870.0, 0.05, "oil")]
print(f"{'fluid':<16} {'D [mm]':>7} {'V [m/s]':>8} {'F [N]':>11} {'Re':>10} {'Cd':>8}")
points = []
for _ in range(12):  # twelve random 'experiments'
    fl = random.choice(fluids)
    D = random.choice([0.002, 0.01, 0.05])
    V = random.choice([0.01, 0.1, 1.0, 5.0])
    re = fl.density * V * D / fl.dynamic_viscosity
    if re > 2e5:  # skip cases beyond the correlation's range (drag crisis)
        continue
    F = drag_force(sphere_drag_coefficient(re), fl.density, V, math.pi * D**2 / 4) * (1 + random.gauss(0, 0.03))
    cd = F / (0.5 * fl.density * V**2 * math.pi * D**2 / 4)
    points.append((re, cd))
    print(f"{fl.name[:16]:<16} {D * 1000:>7.0f} {V:>8.2f} {F:>11.3e} {re:>10.3g} {cd:>8.3f}")
print("\nSorted by Re, the same points form a single smooth curve:")
for re, cd in sorted(points):
    print(f"  Re = {re:10.3g}   Cd = {cd:8.3f}   (standard curve {sphere_drag_coefficient(re):8.3f})")
print("One dimensionless curve replaces a separate chart for every fluid and size - the power of Pi groups.")
