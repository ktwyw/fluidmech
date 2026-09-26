"""CHME 202 - Week 9 - Example 3: how fine must a CFD mesh be near the wall?

Turbulence models either resolve the viscous sublayer (first cell at y+ ~ 1)
or use wall functions (first cell at 30 < y+ < 300). This script estimates the
first-cell height for your COMSOL / CFD lab models from a skin-friction estimate.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech import turbulence as tb
from fluidmech.drag import flat_plate_friction_coefficient

cases = [
    ("water in a 50 mm pipe, 1.5 m/s", Fluid.water(20), 1.5, 0.05, "pipe"),
    ("water in a 200 mm pipe, 2 m/s", Fluid.water(20), 2.0, 0.2, "pipe"),
    ("air in a 300 mm duct, 10 m/s", Fluid.air(20), 10.0, 0.3, "pipe"),
    ("air over a 1 m plate, 20 m/s", Fluid.air(20), 20.0, 1.0, "plate"),
]
print(f"{'case':<33} {'Re':>9} {'u_tau':>7} {'y (y+=1)':>11} {'y (y+=30)':>11}")
for name, fluid, v, length, kind in cases:
    re = v * length / fluid.kinematic_viscosity
    if kind == "pipe":
        f = pf.friction_factor(re, 0.0)
        tau = tb.pipe_wall_shear_stress(f, fluid.density, v)  # tau_w = f rho V^2 / 8
    else:
        cf = flat_plate_friction_coefficient(re, "turbulent")
        tau = cf * 0.5 * fluid.density * v**2  # flat plate: tau_w = Cf rho U^2 / 2
    ut = tb.friction_velocity(tau, fluid.density)
    y1 = tb.wall_distance_for_y_plus(1, ut, fluid.kinematic_viscosity)
    y30 = tb.wall_distance_for_y_plus(30, ut, fluid.kinematic_viscosity)
    print(f"{name:<33} {re:>9.2e} {ut:>7.3f} {y1 * 1e6:>8.1f} um {y30 * 1e3:>8.3f} mm")
print("\nTip: after solving, plot y+ of the first cell in COMSOL and check it is in the intended range.")
print("Wall-resolved meshes need tens of micrometres at the wall - far finer than the core mesh.")
