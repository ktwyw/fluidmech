"""CHME 202 - Week 2 - Example 14: force needed to hold a hinged inclined gate closed.

A rectangular gate, hinged along its top edge, is held shut by a force P applied
normally at its bottom edge. Moments about the hinge: P L = F (y_cp - y_hinge),
where distances are measured along the gate from the free surface.
Reading: White, Section 2.5 (Examples 2.5-2.6 are of this type).
"""

import math

from fluidmech.hydrostatics import rectangular_gate

width, L, angle = 2.0, 3.0, 60.0  # gate width, length along the slope, angle to horizontal
for hinge_depth in [0.0, 1.0, 2.0, 5.0]:
    g = rectangular_gate(width=width, height=L, top_depth=hinge_depth, angle_deg=angle)
    y_hinge = hinge_depth / math.sin(math.radians(angle))
    arm = g.center_of_pressure_slant - y_hinge
    P = g.force * arm / L
    print(
        f"hinge {hinge_depth:.1f} m deep: F = {g.force / 1e3:7.1f} kN acting {arm:.3f} m below the hinge "
        f"-> hold force P = {P / 1e3:6.1f} kN ({arm / L:.3f} of F)"
    )
print("\nAs the gate goes deeper its centre of pressure approaches the centroid (arm -> L/2), so the")
print("ratio P/F = arm / L falls from 2/3 (hinge at the surface) towards 1/2. The holding force itself")
print("still grows with depth, because the pressure on the gate does.")
