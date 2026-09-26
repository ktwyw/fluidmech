"""Example 37 - The classic three-reservoir problem.

Three reservoirs are joined by pipes meeting at one junction. Which way does
the water flow in each pipe? The answer depends on the junction head, which
the network solver finds automatically.
"""

from fluidmech import Fluid, Network
from fluidmech import pipe_flow as pf

water = Fluid.water(15)
eps = pf.ROUGHNESS["cast_iron"]

for z2 in [110.0, 95.0, 80.0]:
    net = Network(water)
    net.add_reservoir("R1", 120.0)
    net.add_reservoir("R2", z2)
    net.add_reservoir("R3", 70.0)
    net.add_junction("J", elevation=50.0)
    net.add_pipe("P1", "R1", "J", 2000, 0.30, eps)
    net.add_pipe("P2", "R2", "J", 1500, 0.25, eps)
    net.add_pipe("P3", "J", "R3", 2500, 0.30, eps)
    res = net.solve()
    print(f"Middle reservoir R2 at {z2:.0f} m -> junction head {res.heads['J']:.2f} m")
    for name, frm, to in [("P1", "R1", "J"), ("P2", "R2", "J"), ("P3", "J", "R3")]:
        q = res.flows[name]
        direction = f"{frm} -> {to}" if q > 0 else f"{to} -> {frm}"
        print(f"   {name}: {abs(q) * 1000:6.1f} L/s  ({direction})")
    print(f"   continuity error {res.max_continuity_error:.1e} m3/s\n")

print("When the junction head is above R2, the middle reservoir is being FILLED;")
print("when it is below, R2 supplies water together with R1.")
