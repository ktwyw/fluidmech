"""CHME 202 - Week 10 - Example 1: total dynamic head for a process transfer line.

A pump moves water from an atmospheric storage tank to a reactor held at
3 bar(g). The required pump head (TDH) is the sum of static head, pressure
head and friction; the SYSTEM CURVE shows how it changes with flow.
Reading: White, Sections 6.9-6.11.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.constants import G

water = Fluid.water(25)
dz = 12.0  # reactor inlet above the tank liquid level [m]
p_reactor = 3e5  # Pa gauge
suction = dict(diameter=0.1023, length=6.0, k=0.5 + 0.3 + 0.15)  # 4" Sch 40: entrance, elbow, valve
discharge = dict(diameter=0.0779, length=85.0, k=6 * 0.3 + 2 * 0.15 + 10.0 + 1.0)  # 3" Sch 40, check valve ~10
eps = pf.ROUGHNESS["commercial_steel"]


def tdh(q: float) -> tuple[float, float, float, float]:
    """Return (static, pressure, friction, total) head [m] at flow q."""
    static = dz
    pressure = p_reactor / (water.density * G)
    friction = (
        sum(
            pf.head_loss(q, s["diameter"], s["length"], water, eps, s["k"]).total_head_loss
            for s in (suction, discharge)
        )
        if q > 0
        else 0.0
    )
    return static, pressure, friction, static + pressure + friction


q_design = 30 / 3600  # 30 m3/h -> m3/s
st, pr, fr, total = tdh(q_design)
print(f"Design flow {q_design * 3600:.0f} m3/h")
print(f"  static head   {st:6.2f} m")
print(f"  pressure head {pr:6.2f} m  (3 bar(g) in the reactor)")
print(f"  friction head {fr:6.2f} m  (suction + discharge, pipes + fittings)")
print(f"  TDH           {total:6.2f} m -> hydraulic power {water.density * G * q_design * total / 1e3:.2f} kW\n")

print("System curve (what any pump must supply):")
print(f"{'Q [m3/h]':>9} {'static+pressure':>16} {'friction':>9} {'TDH [m]':>8}")
for qh in [0, 10, 20, 30, 40, 50]:
    st, pr, fr, total = tdh(qh / 3600)  # m3/h -> m3/s
    print(f"{qh:>9} {st + pr:>16.2f} {fr:>9.2f} {total:>8.2f}")
print("\nThe static + pressure part is fixed; friction grows ~Q^2. Here most of the head is 'static',")
print("so the system curve is flat - important when choosing and controlling the pump (Example 3).")
