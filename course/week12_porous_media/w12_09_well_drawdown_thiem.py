"""CHME 202 - Week 12 - Example 9: radial Darcy flow to a well (Thiem equation).

Steady flow to a well in a confined aquifer of thickness b and hydraulic conductivity K:
Q = 2 pi K b (h2 - h1) / ln(r2 / r1).
Pumping lowers the water level (drawdown) around the well; this is the drawdown that
the submersible pump of Week 10 (w10_07) has to lift against.
"""

import math

from fluidmech import porous as por

k = 5e-12  # permeability of a silty-sand aquifer [m2]
K = por.hydraulic_conductivity(k)
b = 20.0  # aquifer thickness [m]
r_well, R_influence = 0.15, 300.0
print(f"Aquifer: k = {k:.1e} m2 -> K = {K * 86400:.1f} m/day, thickness {b} m")
print(f"Well radius {r_well} m, radius of influence {R_influence} m\n")
print(f"{'Q [m3/h]':>9} {'drawdown at well [m]':>21} {'at 10 m':>8} {'at 100 m':>9}")
for q_h in [5, 10, 15, 20]:
    q = q_h / 3600  # m3/h -> m3/s

    def s(r, q=q):
        # Thiem: drawdown relative to the radius of influence
        return q / (2 * math.pi * K * b) * math.log(R_influence / r)

    print(f"{q_h:>9} {s(r_well):>21.2f} {s(10):>8.2f} {s(100):>9.2f}")
q = 1 / 3600  # 1 m3/h, to express the specific capacity
print(
    f"\nSpecific capacity Q/s = {q * 3600 / (q / (2 * math.pi * K * b) * math.log(R_influence / r_well)):.1f} m3/h per metre of drawdown"
)
print("Drawdown is proportional to Q (Darcy flow) and falls off logarithmically with distance -")
print("neighbouring wells interfere. Real wells add a well-loss term ~Q^2 from turbulent entry.")
