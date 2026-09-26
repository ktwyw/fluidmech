"""Example 42 - Skin friction on a ship hull and boundary-layer growth.

Friction drag dominates the resistance of slow, long ships. The hull is
treated as a flat plate with the same length and wetted area (ITTC-style
estimate; wave drag and form factor are ignored).
"""

from fluidmech import Fluid, drag

sea = Fluid(density=1025.0, dynamic_viscosity=1.22e-3, name="sea water 15 degC")
length, wetted = 180.0, 5200.0  # m, m2

print(f"Cargo ship: L = {length} m, wetted area {wetted} m2, {sea.name}")
print(f"{'speed [kn]':>10} {'Re_L':>10} {'C_f':>9} {'F_friction [kN]':>16} {'P_eff [MW]':>11}")
for knots in [8, 10, 12, 14, 16, 18]:
    v = knots * 0.514444
    re = v * length / sea.kinematic_viscosity
    cf = drag.flat_plate_friction_coefficient(re, "schlichting")
    f = drag.skin_friction_drag(length, wetted, v, sea, "schlichting")
    print(f"{knots:>10} {re:>10.2e} {cf:>9.5f} {f / 1e3:>16.1f} {f * v / 1e6:>11.2f}")
print("Slow steaming from 16 to 12 knots cuts friction power to (12/16)^2.8, about 45 % of its value.\n")

# Boundary-layer growth along the hull at 14 knots
v = 14 * 0.514444
print("Boundary-layer thickness along the hull at 14 kn:")
for x in [0.05, 0.5, 5.0, 50.0, 180.0]:
    re_x = v * x / sea.kinematic_viscosity
    state = "laminar" if re_x < drag.TRANSITION_RE else "turbulent"
    delta = drag.boundary_layer_thickness(x, v, sea.kinematic_viscosity)
    print(f"  x = {x:>6.2f} m  Re_x = {re_x:9.2e}  delta = {delta * 1000:8.1f} mm  ({state})")
x_tr = drag.TRANSITION_RE * sea.kinematic_viscosity / v
print(f"Transition occurs only {x_tr * 100:.0f} cm from the bow -> the hull is effectively all turbulent.")

# Same idea for a small sailing dinghy
print("\nCompare: 4.2 m dinghy at 4 knots, wetted area 4 m2")
for method in ["laminar", "mixed", "turbulent"]:
    f = drag.skin_friction_drag(4.2, 4.0, 4 * 0.514444, sea, method)
    print(f"  {method:<10} friction drag {f:6.1f} N")
print(f"(Re_L = {4 * 0.514444 * 4.2 / sea.kinematic_viscosity:.1e}: the 'mixed' formula is the realistic one.)")
