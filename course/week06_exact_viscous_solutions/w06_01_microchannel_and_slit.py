"""CHME 202 - Week 6 - Example 1: pressure-driven flow in a microchannel and a slit.

Plane Poiseuille flow: q = G h^3 / (12 mu) per unit width. Real channels have
finite aspect ratio; the Shah & London f*Re correlation measures the effect of the side walls.
Reading: White, Sections 4.10 and 6.8.
"""

from fluidmech import Fluid
from fluidmech.laminar import plates_flow_rate, plates_velocity, plates_wall_shear, rectangular_duct_fre

water = Fluid.water(25)
h, w, L = 50e-6, 500e-6, 0.02  # microchannel depth, width, length
dp = 20e3  # applied pressure difference [Pa]
G = dp / L
q = plates_flow_rate(h, G, water.dynamic_viscosity)
Q_plates = q * w
print(f"Microchannel {w * 1e6:.0f} x {h * 1e6:.0f} um, length {L * 1000:.0f} mm, dp = {dp / 1e3:.0f} kPa")
print(
    f"  infinite-plates estimate: Q = {Q_plates * 1e9 * 60:.2f} uL/min, "
    f"centre speed {plates_velocity(h / 2, h, G, water.dynamic_viscosity) * 1000:.1f} mm/s"
)
print(
    f"  wall shear stress {plates_wall_shear(h, G, water.dynamic_viscosity)[0]:.1f} Pa (cells are damaged above ~1-10 Pa)"
)

# Correct for side walls with f*Re: dp = f (L/Dh) rho V^2 / 2 and f = fRe / Re
aspect = h / w
dh = 2 * w * h / (w + h)  # hydraulic diameter 4A/P of a rectangle
fre = rectangular_duct_fre(aspect)
V = dp * dh**2 / (fre * water.dynamic_viscosity * L / 2)  # from dp = (fRe / Re) (L/Dh) rho V^2 / 2
Q_true = V * w * h
print(
    f"  rectangular-duct result (aspect {aspect:.2f}, fRe = {fre:.1f}): Q = {Q_true * 1e9 * 60:.2f} uL/min "
    f"({Q_true / Q_plates - 1:+.0%} vs. plates)"
)
print(f"  Re = {V * dh / water.kinematic_viscosity:.2f} -> laminar; flow rate is exactly proportional to dp\n")

print("Aspect-ratio effect on laminar friction (f Re, based on hydraulic diameter):")
for a in [0.0, 0.1, 0.25, 0.5, 1.0]:
    print(f"  h/w = {a:<5} f Re = {rectangular_duct_fre(a):5.1f}")
print("Circular pipe: 64; parallel plates: 96; square duct: 56.9. Using 64 for every shape can be 50 % off.")
print("\nStrong h^3 dependence: halving the depth of a slit die needs 8x the pressure for the same flow.")
