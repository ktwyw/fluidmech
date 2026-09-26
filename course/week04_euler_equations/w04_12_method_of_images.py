"""CHME 202 - Week 4 - Example 12: a sink near a wall - the method of images.

A plane wall is a streamline if we add a mirror-image sink on the other side.
Model: a suction pipe inlet (line sink) at height a above a tank floor. The flow speeds
up along the floor below the inlet, lowering the pressure there (Bernoulli) - the reason
suction inlets need a minimum floor clearance to avoid vortices and air entrainment.
"""

from fluidmech.potential_flow import Source

m, a, rho = -0.2, 0.3, 1000.0  # sink strength per unit depth [m2/s], height above the floor [m]
flow = Source(m, 0.0, a) + Source(m, 0.0, -a)  # sink and its image below the floor
print(f"Line sink of strength {-m} m2/s at {a} m above the floor\n")
print(f"{'x along floor [m]':>18} {'u [m/s]':>8} {'v [m/s]':>8} {'p drop [Pa]':>12}")
for x in [0.0, 0.1, 0.3, 0.6, 1.0, 2.0]:
    u, v = flow.velocity(x, 0.0)
    print(f"{x:>18} {u:>8.3f} {v:>8.3f} {0.5 * rho * u**2:>12.1f}")
print("\nv = 0 on the floor (no flow through it) - the image enforces the boundary condition exactly.")
print("The floor velocity peaks at x = a, |u| = |m| / (2 pi a): the image doubles the tangential velocity")
print("component that the sink alone would induce there.")
for clearance in [0.1, 0.3, 0.6]:
    f2 = Source(m, 0, clearance) + Source(m, 0, -clearance)
    print(f"  clearance {clearance} m: peak floor speed {abs(f2.velocity(clearance, 0.0)[0]):.3f} m/s")
