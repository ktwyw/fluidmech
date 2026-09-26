"""CHME 202 - Week 10 - Example 13: one pump filling two tanks at different levels.

A branching system: the pump feeds a junction from which pipes lead to two tanks. The split
depends on the tank levels and pipe resistances, and it changes as the tanks fill. Solved
with the network solver. Pump data are ILLUSTRATIVE.
"""

from fluidmech import Fluid, Network, PumpCurve
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
eps = pf.ROUGHNESS["commercial_steel"]
pump = PumpCurve.from_points([0, 0.01, 0.02, 0.03], [40, 38.5, 34, 26.5])
print(f"{'tank A level [m]':>17} {'tank B level [m]':>17} {'Q_A [L/s]':>10} {'Q_B [L/s]':>10} {'pump [L/s]':>11}")
for level_a, level_b in [(10.0, 20.0), (15.0, 20.0), (20.0, 20.0), (20.0, 26.0), (25.0, 30.0), (10.0, 38.0)]:
    net = Network(water)
    net.add_reservoir("Sump", 0.0)
    net.add_reservoir("TankA", level_a)
    net.add_reservoir("TankB", level_b)
    net.add_junction("P", 0.0)
    net.add_junction("J", 2.0)
    net.add_pump("Pump", "Sump", "P", pump)  # pump lifts from the sump to the manifold node P
    net.add_pipe("main", "P", "J", 60, 0.10, eps, 3.0)
    net.add_pipe("toA", "J", "TankA", 150, 0.08, eps, 2.0)
    net.add_pipe("toB", "J", "TankB", 80, 0.065, eps, 2.0)
    r = net.solve()
    qa, qb = r.flows["toA"], r.flows["toB"]
    note = "  <- B drains back into A!" if qb < 0 else ""
    print(f"{level_a:>17} {level_b:>17} {qa * 1000:>10.2f} {qb * 1000:>10.2f} {r.flows['Pump'] * 1000:>11.2f}{note}")
print("\nAs tank A fills, more flow goes to B. When the junction head drops below a tank's level, that")
print("tank drains backwards - use check valves or level-controlled valves on each branch.")
