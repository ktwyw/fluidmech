"""Example 36 - A small town water distribution network.

A treatment works (reservoir) feeds a pumping station, which supplies eight
demand nodes and an elevated storage tank. We check service pressures
against a typical minimum of 20 m (about 200 kPa) and maximum velocity 2 m/s.

       Works --pump--> J1 ---- J2 ---- J3
                       |       |       |
                       J4 ---- J5 ---- J6 ---- Tank
                       |       |
                       J7 ---- J8
"""

from fluidmech import Fluid, Network, PumpCurve
from fluidmech import pipe_flow as pf

water = Fluid.water(15)
net = Network(water)
di = pf.ROUGHNESS["cast_iron"]

net.add_reservoir("Works", head=102.0)
net.add_reservoir("Tank", head=148.0)  # water level in the elevated tank
junctions = {  # name: (elevation [m], demand [L/s])
    "PS": (100.0, 0.0),
    "J1": (104.0, 8.0),
    "J2": (108.0, 12.0),
    "J3": (112.0, 10.0),
    "J4": (103.0, 15.0),
    "J5": (106.0, 20.0),
    "J6": (115.0, 9.0),
    "J7": (101.0, 14.0),
    "J8": (105.0, 11.0),
}
for name, (z, q) in junctions.items():
    net.add_junction(name, elevation=z, demand=q / 1000)  # demand L/s -> m3/s

pump = PumpCurve.from_points([0.0, 0.05, 0.10, 0.15], [68.0, 65.0, 56.0, 40.0])
net.add_pump("Pump", "Works", "PS", pump)

pipes = [  # name, from, to, length [m], diameter [m]
    ("P0", "PS", "J1", 200, 0.35),
    ("P1", "J1", "J2", 500, 0.25),
    ("P2", "J2", "J3", 450, 0.20),
    ("P3", "J1", "J4", 400, 0.30),
    ("P4", "J2", "J5", 400, 0.20),
    ("P5", "J3", "J6", 400, 0.15),
    ("P6", "J4", "J5", 500, 0.25),
    ("P7", "J5", "J6", 450, 0.20),
    ("P8", "J4", "J7", 350, 0.20),
    ("P9", "J5", "J8", 350, 0.15),
    ("P10", "J7", "J8", 500, 0.15),
    ("P11", "J6", "Tank", 300, 0.20),
]
for name, a, b, length, d in pipes:
    net.add_pipe(name, a, b, length, d, di)

res = net.solve()
print(res.summary())

total_demand = sum(q for _, q in junctions.values())
tank_flow = -res.reservoir_outflows["Tank"]
print(
    f"\nTotal demand {total_demand:.0f} L/s; pump delivers {res.flows['Pump'] * 1000:.1f} L/s "
    f"at {-res.head_losses['Pump']:.1f} m head"
)
print(f"The tank is {'FILLING' if tank_flow > 0 else 'DRAINING'} at {abs(tank_flow) * 1000:.1f} L/s")

print("\nDesign checks:")
for name in junctions:
    p_head = res.pressures[name] / (water.density * 9.80665)
    if name != "PS" and p_head < 20:
        print(f"  LOW PRESSURE at {name}: {p_head:.1f} m")
for name, v in res.velocities.items():
    if v > 2.0:
        print(f"  HIGH VELOCITY in {name}: {v:.2f} m/s")
low = min((res.pressures[n] / (water.density * 9.80665), n) for n in junctions if n != "PS")
print(f"  minimum service pressure: {low[0]:.1f} m at {low[1]}")
