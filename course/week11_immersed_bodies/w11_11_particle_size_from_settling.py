"""CHME 202 - Week 11 - Example 11: sedimentation analysis - particle size from settling speed.

Measuring how fast particles settle gives their 'Stokes diameter' d = sqrt(18 mu U / (drho g)).
This is the basis of the hydrometer and pipette methods for soils and powders. For larger
particles Stokes' law fails and the drag curve must be inverted numerically.
"""

import math

from fluidmech import Fluid
from fluidmech.constants import G
from fluidmech.drag import terminal_velocity
from fluidmech.solvers import bisect

water = Fluid.water(20)
rho_p = 2650.0  # quartz [kg/m3]
print(f"{'measured U [mm/s]':>18} {'Stokes d [um]':>14} {'Re (Stokes)':>12} {'true d [um]':>12} {'Stokes error':>13}")
for u_mm in [0.01, 0.1, 1.0, 5.0, 20.0, 60.0]:
    U = u_mm / 1000  # mm/s -> m/s
    d_stokes = math.sqrt(18 * water.dynamic_viscosity * U / ((rho_p - water.density) * G))  # Stokes' law solved for d
    re = water.density * U * d_stokes / water.dynamic_viscosity
    # invert the full drag curve numerically
    d_true = bisect(lambda d, U=U: terminal_velocity(d, rho_p, water) - U, 1e-7, 0.01)
    print(
        f"{u_mm:>18} {d_stokes * 1e6:>14.2f} {re:>12.3f} {d_true * 1e6:>12.2f} {(0.0 if abs(d_stokes / d_true - 1) < 5e-4 else d_stokes / d_true - 1):>+13.1%}"
    )
print("\nStokes' law is fine for silt and clay (U < ~1 mm/s, Re < 0.1) - the range of sedimentation")
print("analysis. For sand, inverting the full drag curve is essential; Stokes underestimates d badly.")
print("The result is an equivalent SPHERE diameter: flaky clay particles are larger than it suggests.")
