"""CHME 202 - Week 10 - Example 5: multiple-pipe systems - series, parallel and branching.

Series: same flow, head losses add.  Parallel: same head loss, flows add.
Branching (three reservoirs): the junction head sets the direction of every flow.
Reading: White, Section 6.10.
"""

from fluidmech import Fluid, Network
from fluidmech import pipe_flow as pf
from fluidmech.solvers import bisect

water = Fluid.water(15)
eps = pf.ROUGHNESS["cast_iron"]

# Series
q = 0.02
pipes = [(200, 0.15), (150, 0.10)]
losses = [pf.head_loss(q, d, length, water, eps).major_head_loss for length, d in pipes]
print(f"1) Series: Q = {q * 1000:.0f} L/s through 200 m of 150 mm then 150 m of 100 mm")
print(f"   losses {losses[0]:.2f} m + {losses[1]:.2f} m = {sum(losses):.2f} m (smaller pipe dominates)\n")

# Parallel: split 60 L/s between two pipes
branches = [(400, 0.20), (300, 0.15)]
total = 0.06  # total flow to be shared [m3/s]
h = bisect(
    lambda hh: sum(pf.flow_rate_for_head_loss(hh, d, length, water, eps) for length, d in branches) - total, 1e-3, 100
)
print(f"2) Parallel: {total * 1000:.0f} L/s shared by two pipes; common head loss {h:.2f} m")
for length, d in branches:
    qb = pf.flow_rate_for_head_loss(h, d, length, water, eps)
    print(f"   {length} m of {d * 1000:.0f} mm carries {qb * 1000:.1f} L/s ({qb / total:.0%})")

# Branching: three reservoirs
print("\n3) Three reservoirs at 100, 80 and 50 m joined at one junction")
net = Network(water)
for name, head in [("R1", 100.0), ("R2", 80.0), ("R3", 50.0)]:
    net.add_reservoir(name, head)
net.add_junction("J", 40.0)
net.add_pipe("P1", "R1", "J", 1000, 0.30, eps)
net.add_pipe("P2", "R2", "J", 800, 0.20, eps)
net.add_pipe("P3", "J", "R3", 1200, 0.25, eps)
res = net.solve()
print(f"   junction head {res.heads['J']:.2f} m")
for p, (a, b) in {"P1": ("R1", "J"), "P2": ("R2", "J"), "P3": ("J", "R3")}.items():
    qf = res.flows[p]
    print(f"   {p}: {abs(qf) * 1000:6.1f} L/s  {a + ' -> ' + b if qf > 0 else b + ' -> ' + a}")
print("   Because the junction head is above R2's level, reservoir R2 is being FILLED.")
