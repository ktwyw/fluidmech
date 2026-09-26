"""CHME 202 - Week 13 - Example 4: model testing and the limits of similarity.

Full dynamic similarity needs ALL Pi groups equal. Usually that is impossible,
so we match the dominant group: Reynolds (pipes, closed conduits, meters) or
Froude (free surfaces, waves, sloshing, surface vortices).
"""

from fluidmech import Fluid
from fluidmech.dimensionless import froude, reynolds

# 1. Flow meter calibrated with water, used for oil: Reynolds similarity
water, oil = Fluid.water(20), Fluid(870.0, 0.012, "light oil")
D, V_oil = 0.1, 2.0  # meter diameter [m], oil velocity [m/s]
re_oil = reynolds(V_oil, D, oil.kinematic_viscosity)
V_water = re_oil * water.kinematic_viscosity / D
print("1) Flow meter for oil (D = 100 mm, V = 2 m/s), calibrated on a water rig:")
print(f"   Re_oil = {re_oil:.0f} -> the water test must run at V = {V_water:.3f} m/s for the same Re")
print(
    f"   Calibrating at the same VELOCITY with water would give Re "
    f"{reynolds(V_oil, D, water.kinematic_viscosity) / re_oil:.0f}x too high and the wrong Cd.\n"
)

# 2. Stirred-tank model with a free surface: can we match both Re and Fr?
T_p, N_p = 3.0, 1.0  # prototype tank diameter [m], speed [rev/s]
scale = 1 / 10
T_m = T_p * scale
N_m_fr = N_p / scale**0.5  # Froude: N^2 D / g equal
nu_needed = water.kinematic_viscosity * scale**1.5  # Reynolds with that speed
print("2) 1:10 model of an unbaffled stirred tank (surface vortex -> Froude matters):")
print(f"   Froude similarity: N_model = {N_m_fr * 60:.0f} rpm (prototype {N_p * 60:.0f} rpm)")
print(f"   Reynolds then also matches only if nu_model = {nu_needed:.2e} m2/s,")
print(f"   {water.kinematic_viscosity / nu_needed:.0f}x less viscous than water - no practical liquid exists.")
print(
    f"   So Re_model = {reynolds(N_m_fr * T_m / 3, T_m / 3, water.kinematic_viscosity):.0f} vs "
    f"Re_prototype = {reynolds(N_p * T_p / 3, T_p / 3, water.kinematic_viscosity):.0f}: accept it if both are turbulent.\n"
)

# 3. Check Froude numbers match
print(f"3) Check: Fr_model = {froude(N_m_fr * T_m, T_m):.3f}, Fr_prototype = {froude(N_p * T_p, T_p):.3f}")
print("Engineering judgement: once flows are fully turbulent, Reynolds effects are weak ('Reynolds")
print("number independence'), so matching the other group is enough.")
