"""Example 20 - Pressure drop in a rectangular HVAC duct (hydraulic diameter).

For non-circular ducts, Re and the friction factor are based on D_h = 4A/P,
while the velocity is still the true mean velocity Q/A.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.constants import G

air = Fluid.air(20)
a, b = 0.40, 0.25  # duct sides [m]
Q, L = 1.2, 30.0  # m3/s, m
eps = pf.ROUGHNESS["galvanized_iron"]

area = a * b
dh = pf.hydraulic_diameter(area, 2 * (a + b))
v = Q / area
re = v * dh / air.kinematic_viscosity
f = pf.friction_factor(re, eps / dh)
dp = f * L / dh * 0.5 * air.density * v**2

print(f"Rectangular duct {a * 1000:.0f} x {b * 1000:.0f} mm, Q = {Q} m3/s of air at 20 degC")
print(f"  hydraulic diameter D_h = {dh * 1000:.1f} mm")
print(f"  V = {v:.2f} m/s, Re = {re:.3g}, f = {f:.4f}")
print(f"  friction pressure drop over {L:.0f} m = {dp:.1f} Pa ({dp / L:.2f} Pa/m)")

# Equivalent round duct (Huebscher): same friction loss and same flow rate
de = 1.30 * (a * b) ** 0.625 / (a + b) ** 0.25
r = pf.head_loss(Q, de, L, air, eps)
print(f"\nEquivalent round duct (Huebscher) D_e = {de * 1000:.0f} mm")
print(f"  gives dp = {r.pressure_drop:.1f} Pa for the same Q (check against {dp:.1f} Pa)")

# Fittings
k_total = 2 * 0.3 + 1.0 + 0.5  # two elbows, a branch tee, a damper
dp_fittings = pf.minor_loss(k_total, v) * air.density * G
print(f"\nFittings (K = {k_total}) add {dp_fittings:.1f} Pa -> total {dp + dp_fittings:.1f} Pa")
print(f"Fan air power = {(dp + dp_fittings) * Q:.0f} W")

print("\nAspect ratio matters: same 0.1 m2 area, different shapes")
for w in [0.316, 0.40, 0.50, 0.80, 1.00]:
    h = area / w
    dh_i = pf.hydraulic_diameter(area, 2 * (w + h))
    re_i = v * dh_i / air.kinematic_viscosity
    dp_i = pf.friction_factor(re_i, eps / dh_i) * L / dh_i * 0.5 * air.density * v**2
    print(f"  {w * 1000:>5.0f} x {h * 1000:>4.0f} mm (AR {max(w, h) / min(w, h):4.1f}): dp = {dp_i:5.1f} Pa")
