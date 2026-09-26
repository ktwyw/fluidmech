"""CHME 202 - Week 11 - Example 6: friction drag versus pressure (form) drag - why streamlining works.

Drag = skin friction (shear on the surface) + pressure drag (low pressure in the
separated wake). Bluff bodies are dominated by pressure drag, streamlined bodies
by friction. Compared here at the same frontal area and speed.
Reading: White, Sections 7.1 and 7.6.
"""

from fluidmech import Fluid
from fluidmech.drag import TYPICAL_CD, drag_force, flat_plate_friction_coefficient

air = Fluid.air(20)
V, width, length = 20.0, 1.0, 1.0  # air speed [m/s], plate size [m]
re_L = V * length / air.kinematic_viscosity
cf = flat_plate_friction_coefficient(re_L)
print(f"Air at {V} m/s, body scale 1 m (Re = {re_L:.2e})\n")
print("1 m x 1 m flat plate:")
f_par = drag_force(cf, air.density, V, 2 * width * length)  # both sides, friction only
f_norm = drag_force(TYPICAL_CD["flat_plate_normal_3d"], air.density, V, width * length)
print(f"  parallel to the flow (friction only, both sides): {f_par:7.1f} N")
print(f"  normal to the flow (almost all pressure drag):    {f_norm:7.1f} N  ({f_norm / f_par:.0f}x more)\n")

print("Bodies with 1 m2 frontal area:")
for name in [
    "flat_plate_normal_3d",
    "cube",
    "sphere_subcritical",
    "hemisphere_facing_away",
    "modern_car",
    "streamlined_body",
]:
    cd = TYPICAL_CD[name]
    print(f"  {name.replace('_', ' '):<24} Cd = {cd:5.2f}  drag = {drag_force(cd, air.density, V, 1.0):6.1f} N")
print("\nA streamlined body has more wetted surface (more friction) but its boundary layer stays attached,")
print("so the wake - and the pressure drag - almost disappears. Its total drag is ~1/30 of a plate's.")
print("Process examples: rounded thermowell tips, faired pipe supports, streamlined flow-meter struts.")
