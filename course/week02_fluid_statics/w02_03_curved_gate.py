"""CHME 202 - Week 2 - Example 3: hydrostatic force on a curved (radial) gate.

For a curved surface: F_H = force on its vertical projection;
F_V = weight of the (real or imaginary) water above the surface.
For a circular gate the resultant passes through the centre of curvature.
Reading: White, Section 2.6.
"""

import math

from fluidmech.constants import G
from fluidmech.hydrostatics import curved_surface_force, rectangular_gate

R, width = 3.0, 5.0  # quarter-circle gate radius and width [m]
rho = 1000.0
# Water on the convex side, free surface level with the top of the gate.
horizontal = rectangular_gate(width=width, height=R, top_depth=0.0)
F_H = horizontal.force
# Vertical: water between the quarter circle and the free surface = square minus quarter circle
volume = width * (R**2 - math.pi * R**2 / 4)
F_V = rho * G * volume
F, angle = curved_surface_force(F_H, F_V)
print(f"Quarter-circle gate R = {R} m, width {width} m")
print(f"  horizontal component {F_H / 1e3:8.1f} kN (acts at depth {horizontal.center_of_pressure_depth:.2f} m)")
print(f"  vertical component   {F_V / 1e3:8.1f} kN (weight of {volume:.2f} m3 of water)")
print(f"  resultant            {F / 1e3:8.1f} kN at {angle:.1f} deg below horizontal")

# Case 2: water fills the concave side (under the arc): same F_H, F_V = quarter circle volume, upward
F_V2 = rho * G * width * math.pi * R**2 / 4
print("\nSame gate with water on the concave side:")
print(
    f"  vertical component {F_V2 / 1e3:.1f} kN (quarter-circle of water), resultant "
    f"{curved_surface_force(F_H, F_V2)[0] / 1e3:.1f} kN"
)
print("\nBecause every pressure force is normal to the circular surface, the resultant passes through")
print("the hinge at the centre: the hydrostatic load creates no moment on a radial (Tainter) gate.")
print("That is why radial gates need only a small hoist force to open.")
