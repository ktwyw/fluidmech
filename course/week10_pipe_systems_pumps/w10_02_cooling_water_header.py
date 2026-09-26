"""CHME 202 - Week 10 - Example 2: flow distribution in a cooling-water header (parallel branches).

A header feeds three heat exchangers in parallel. Without balancing, the branch
closest to the pump and with the lowest resistance takes most of the water.
Solved with the fluidmech.Network solver.
"""

from fluidmech import Fluid, Network, PumpCurve
from fluidmech import pipe_flow as pf

water = Fluid.water(30)
eps = pf.ROUGHNESS["commercial_steel"]
pump = PumpCurve.from_points([0, 0.01, 0.02, 0.03], [35, 33.5, 29, 21.5])
targets = {"HX1": 6.0, "HX2": 6.0, "HX3": 6.0}  # required flows, L/s


def build(balancing: dict[str, float]) -> Network:
    net = Network(water)
    net.add_reservoir("Basin", 0.0)  # cooling-tower basin (supply and return)
    net.add_reservoir("Return", 2.0)  # return to the tower distribution deck, 2 m up
    net.add_junction("PD", 0.0)
    for n in ("H1", "H2", "H3"):
        net.add_junction(n, 1.0)
    net.add_pump("Pump", "Basin", "PD", pump)
    net.add_pipe("main1", "PD", "H1", 20, 0.10, eps, 1.0)
    net.add_pipe("main2", "H1", "H2", 30, 0.08, eps)
    net.add_pipe("main3", "H2", "H3", 30, 0.065, eps)
    # each exchanger branch: 15 m of 50 mm pipe, exchanger K = 12, plus a balancing valve
    for hx, node in zip(targets, ("H1", "H2", "H3")):
        net.add_pipe(hx, node, "Return", 15, 0.05, eps, 12.0 + balancing.get(hx, 0.0))
    return net


print(f"{'':<22}" + "".join(f"{hx:>9}" for hx in targets) + "   total [L/s]")
res = build({}).solve()
print(
    f"{'unbalanced':<22}"
    + "".join(f"{res.flows[hx] * 1000:>9.2f}" for hx in targets)
    + f"   {res.flows['Pump'] * 1000:.2f}"
)

# Balance by adding valve resistance to the favoured branches (simple iteration)
kv = {hx: 0.0 for hx in targets}
for _ in range(40):  # iterative balancing: throttle branches that get more than the weakest one
    res = build(kv).solve()
    low = min(res.flows[hx] for hx in targets)
    for hx in targets:
        # add valve resistance in proportion to the excess flow
        kv[hx] = max(0.0, kv[hx] + 20.0 * (res.flows[hx] / low - 1.0))
print(
    f"{'balanced':<22}"
    + "".join(f"{res.flows[hx] * 1000:>9.2f}" for hx in targets)
    + f"   {res.flows['Pump'] * 1000:.2f}"
)
print(f"{'balancing valve K':<22}" + "".join(f"{kv[hx]:>9.1f}" for hx in targets))
print("\nThe far exchanger needs no valve; the near ones are throttled until all flows match.")
print("Balancing costs pump head - the price of good distribution.")
