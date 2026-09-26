"""Example 28 - Scale models and dynamic similarity.

Free-surface models (spillways, ships) match the Froude number;
closed-conduit models (pipes, valves) match the Reynolds number.
"""

from fluidmech import Fluid
from fluidmech.dimensionless import froude, reynolds

# --- Froude scaling: spillway model -------------------------------------- #
Lr = 1 / 25  # model : prototype length ratio
Q_p, V_p, h_p = 800.0, 12.0, 4.0  # prototype discharge, velocity, depth
scales = {
    "length": Lr,
    "velocity": Lr**0.5,
    "time": Lr**0.5,
    "discharge": Lr**2.5,
    "force": Lr**3,
    "power": Lr**3.5,
}
print(f"Spillway model at 1:{1 / Lr:.0f} (Froude similarity, same fluid)")
for name, s in scales.items():
    print(f"  {name:<10} scale = {s:.3e}  (1:{1 / s:,.0f})")
V_m, h_m = V_p * scales["velocity"], h_p * Lr
print(f"  prototype Q = {Q_p} m3/s -> model Q = {Q_p * scales['discharge'] * 1000:.1f} L/s")
print(f"  Fr prototype = {froude(V_p, h_p):.3f}, Fr model = {froude(V_m, h_m):.3f}  (equal)")

water = Fluid.water(15)
re_p = reynolds(V_p, h_p, water.kinematic_viscosity)
re_m = reynolds(V_m, h_m, water.kinematic_viscosity)
print(f"  but Re prototype = {re_p:.2e}, Re model = {re_m:.2e} -> viscous 'scale effects'")
print("  Keep model Re above ~1e4-1e5 so the model flow stays fully turbulent.\n")

# --- Reynolds scaling: valve tested in air ------------------------------- #
oil = Fluid(density=870.0, dynamic_viscosity=0.035, name="oil")
air = Fluid.air(20)
D_p, V_p = 0.40, 2.0  # prototype diameter [m] and velocity [m/s]
D_m = 0.10  # model diameter [m]
V_m = V_p * (D_p / D_m) * air.kinematic_viscosity / oil.kinematic_viscosity  # equal Reynolds numbers
print(f"Oil valve (D = {D_p} m, V = {V_p} m/s) modelled at D = {D_m} m in AIR (Reynolds similarity)")
print(f"  required air velocity = {V_m:.1f} m/s")
print(
    f"  Re prototype = {reynolds(V_p, D_p, oil.kinematic_viscosity):.0f}, "
    f"Re model = {reynolds(V_m, D_m, air.kinematic_viscosity):.0f}"
)

dp_m = 150.0  # measured model pressure drop [Pa]
dp_p = dp_m * (oil.density * V_p**2) / (air.density * V_m**2)  # equal Euler numbers
print(f"  model dp = {dp_m} Pa  ->  prototype dp = {dp_p / 1e3:.1f} kPa (equal Euler number)\n")

# --- Why ship models can't match both ----------------------------------- #
print("Ship model 1:50 in water: Froude similarity needs V_m = V_p/sqrt(50), Reynolds needs")
print("V_m = 50 V_p -- impossible together, so wave drag (Froude) and friction drag (Reynolds)")
print("are scaled separately (Froude's method).")
