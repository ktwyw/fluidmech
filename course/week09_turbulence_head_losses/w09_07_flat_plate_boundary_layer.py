"""CHME 202 - Week 9 - Example 7: boundary layer on a flat plate.

Laminar (Blasius): delta = 4.91 x / Re_x^0.5, displacement thickness 1.72 x / Re_x^0.5.
Turbulent: delta = 0.37 x / Re_x^0.2. Transition near Re_x = 5e5.
Reading: White, Sections 7.3-7.4.
"""

import math

from fluidmech import Fluid
from fluidmech.drag import TRANSITION_RE, boundary_layer_thickness, flat_plate_friction_coefficient

for fluid, U in [(Fluid.air(20), 10.0), (Fluid.water(20), 1.0)]:
    nu = fluid.kinematic_viscosity
    x_tr = TRANSITION_RE * nu / U
    print(f"{fluid.name}, U = {U} m/s: transition at x = {x_tr * 100:.1f} cm")
    print(f"  {'x [m]':>6} {'Re_x':>9} {'delta [mm]':>11} {'delta* [mm]':>12} {'state':>10}")
    for x in [0.01, 0.1, 0.5, 1.0, 2.0]:
        re_x = U * x / nu
        d = boundary_layer_thickness(x, U, nu)
        # displacement thickness: Blasius, or delta/8 for the 1/7 power law
        d_star = 1.721 * x / math.sqrt(re_x) if re_x < TRANSITION_RE else d / 8
        state = "laminar" if re_x < TRANSITION_RE else "turbulent"
        print(f"  {x:>6.2f} {re_x:>9.2e} {d * 1000:>11.2f} {d_star * 1000:>12.3f} {state:>10}")
    re_l = U * 1.0 / nu
    print(
        f"  drag coefficient of a 1 m plate: laminar {flat_plate_friction_coefficient(re_l, 'laminar'):.5f}, "
        f"mixed {flat_plate_friction_coefficient(re_l, 'mixed'):.5f}, "
        f"fully turbulent {flat_plate_friction_coefficient(re_l, 'turbulent'):.5f}\n"
    )
print("Boundary layers are THIN compared with the body (delta/x ~ Re^-1/2): this is why the")
print("inviscid Euler solutions of Week 4 work outside them.")
print("(delta* for turbulent flow uses the 1/7-power-law value delta/8. The turbulent formula assumes")
print(" turbulence from the leading edge, which is why delta appears to jump at transition.)")
