"""Example 38 - Scenario analysis: peak demand, fire flow and a pipe break.

Engineers rarely solve a network once. This example reruns one network under
several operating scenarios and compares the minimum pressures.
"""

from fluidmech import Fluid, Network

water = Fluid.water(15)
RHO_G = water.density * 9.80665
ROUGHNESS = 0.1e-3  # cement-lined ductile iron [m]

base_demand = {"A": 10.0, "B": 15.0, "C": 12.0, "D": 18.0, "E": 8.0, "F": 14.0}  # L/s
elevation = {"A": 20.0, "B": 24.0, "C": 30.0, "D": 22.0, "E": 26.0, "F": 34.0}
pipes = [  # name, from, to, length, diameter
    ("S1", "Res", "A", 800, 0.35),
    ("AB", "A", "B", 500, 0.25),
    ("BC", "B", "C", 600, 0.20),
    ("AD", "A", "D", 450, 0.25),
    ("BE", "B", "E", 450, 0.20),
    ("CF", "C", "F", 450, 0.15),
    ("DE", "D", "E", 500, 0.20),
    ("EF", "E", "F", 600, 0.15),
]


def build(demand_factor=1.0, extra=None, closed=()):
    net = Network(water)
    net.add_reservoir("Res", 85.0)
    for node, q in base_demand.items():
        q_total = q * demand_factor + (extra or {}).get(node, 0.0)
        net.add_junction(node, elevation=elevation[node], demand=q_total / 1000)  # L/s -> m3/s
    for name, a, b, length, d in pipes:
        if name not in closed:
            net.add_pipe(name, a, b, length, d, ROUGHNESS)
    return net


scenarios = {
    "Average day": build(1.0),
    "Peak hour (x2.2)": build(2.2),
    "Fire flow 40 L/s at F": build(1.5, extra={"F": 40.0}),
    "Pipe BC out of service": build(1.5, closed=("BC",)),
    "Break on AD + peak": build(2.2, closed=("AD",)),
}

print(f"{'scenario':<26} " + "".join(f"{n:>7}" for n in base_demand) + "   min [m]  max V [m/s]")
for name, net in scenarios.items():
    res = net.solve()
    heads = {n: res.pressures[n] / RHO_G for n in base_demand}
    worst = min(heads.values())
    vmax = max(res.velocities.values())
    flag = "  <-- below 20 m" if worst < 20 else ""
    print(f"{name:<26} " + "".join(f"{heads[n]:>7.1f}" for n in base_demand) + f"   {worst:>6.1f}  {vmax:>9.2f}{flag}")

print("\nPressures are in metres of water. Typical minimums: 20 m normal service,")
print("~14 m (20 psi) at the hydrant during fire flow.")
