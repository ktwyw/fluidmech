"""CHME 202 - Week 2 - Example 10: hydrostatic load on a storage tank shell.

Pressure rises linearly with depth, so the hoop stress in a vertical tank is
highest at the bottom: sigma = p D / (2 t). Tank shells are built of courses
that get thicker towards the base.
"""

from fluidmech.constants import G

D, H = 20.0, 15.0  # tank diameter and liquid height [m]
rho = 1050.0  # product density
sigma_allow = 160e6  # allowable stress [Pa]
corrosion = 1.5e-3  # corrosion allowance [m]
course_height = 2.5
print(f"Tank D = {D} m filled to {H} m with liquid of density {rho} kg/m3\n")
print(f"{'course':>7} {'bottom depth [m]':>17} {'p [kPa]':>8} {'t required [mm]':>16}")
depth = H
course = 1
while depth > 0:  # one shell course per pass, from the bottom up
    p = rho * G * depth
    t_req = p * D / (2 * sigma_allow) + corrosion  # hoop stress sigma = p D / (2 t) solved for t
    print(f"{course:>7} {depth:>17.1f} {p / 1e3:>8.1f} {t_req * 1000:>16.1f}")
    depth -= course_height
    course += 1
print(
    f"\nThe stress-based thickness (excluding corrosion allowance) of the bottom course is "
    f"{H / course_height:.0f}x that of the top course: it scales with depth."
)
print("(Real design codes such as API 650 also impose minimum thicknesses and a hydrotest case with water.)")
force_bottom = rho * G * H * 3.14159 * D**2 / 4
print(f"Total load on the tank floor: {force_bottom / 1e6:.1f} MN = weight of the liquid.")
