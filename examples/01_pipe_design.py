"""Example 1 - Pipe design: the three classic pipe-flow problems.

Water at 20 degC flows through 200 m of commercial-steel pipe with a sharp
entrance, four regular 90-degree elbows, an open gate valve and an exit.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
eps = pf.ROUGHNESS["commercial_steel"]
k_total = (
    pf.MINOR_LOSS_K["sharp_entrance"]
    + 4 * pf.MINOR_LOSS_K["elbow_90_regular"]
    + pf.MINOR_LOSS_K["gate_valve_open"]
    + pf.MINOR_LOSS_K["exit"]
)
L = 200.0  # pipe length [m]

print(f"Fluid: {water.name}, rho = {water.density:.1f} kg/m3, nu = {water.kinematic_viscosity:.3e} m2/s")
print(f"Sum of minor-loss coefficients K = {k_total:.2f}\n")

# Type 1: head loss for given Q and D
res = pf.head_loss(flow_rate=0.02, diameter=0.1, length=L, fluid=water, roughness=eps, k_total=k_total)
print("Type 1 - head loss for Q = 20 L/s, D = 100 mm")
print(f"  V = {res.velocity:.2f} m/s, Re = {res.reynolds:.3g} ({res.regime}), f = {res.friction_factor:.4f}")
print(f"  major loss = {res.major_head_loss:.2f} m, minor loss = {res.minor_head_loss:.2f} m")
print(f"  total = {res.total_head_loss:.2f} m, dp = {res.pressure_drop / 1e3:.1f} kPa")
print(f"  pump power at 75 % efficiency = {res.pumping_power(0.75) / 1e3:.2f} kW\n")

# Type 2: flow rate for a given available head
q = pf.flow_rate_for_head_loss(8.0, diameter=0.1, length=L, fluid=water, roughness=eps, k_total=k_total)
print(f"Type 2 - flow rate with 8 m of head available: Q = {q * 1000:.2f} L/s\n")

# Type 3: diameter for a maximum head loss
d = pf.diameter_for_head_loss(0.02, head_loss_allowed=5.0, length=L, fluid=water, roughness=eps, k_total=k_total)
print(f"Type 3 - diameter so that Q = 20 L/s loses only 5 m: D = {d * 1000:.1f} mm")
print("  -> choose the next standard pipe size up.")
