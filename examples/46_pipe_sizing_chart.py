"""Example 46 - Pipe sizing chart: head-loss gradient vs. flow for standard sizes.

The classic design chart on every hydraulic engineer's wall, generated for
any roughness and fluid. Saves pipe_sizing_chart.png.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(15)
eps = 0.1e-3  # lined ductile iron
sizes_mm = [50, 80, 100, 150, 200, 250, 300, 400, 500, 600]

fig, ax = plt.subplots(figsize=(9, 7))
for d_mm in sizes_mm:
    d = d_mm / 1000  # mm -> m
    # velocities 0.2-4 m/s in 8 % steps -> flows
    qs = [pf.area(d) * v for v in [0.2 * 1.08**i for i in range(60) if 0.2 * 1.08**i <= 4.0]]
    grad = [pf.head_loss(q, d, 1000.0, water, eps).major_head_loss for q in qs]  # head loss per km
    ax.loglog([q * 1000 for q in qs], grad, lw=1.4)
    ax.text(qs[-1] * 1000, grad[-1], f" {d_mm}", fontsize=8, va="center")

# Lines of constant velocity
for v in [0.5, 1.0, 2.0, 3.0]:
    pts = [
        (
            pf.area(d / 1000) * v * 1000,
            pf.head_loss(pf.area(d / 1000) * v, d / 1000, 1000, water, eps).major_head_loss,
        )
        for d in sizes_mm
    ]
    ax.loglog(*zip(*pts), "k--", lw=0.7)
    ax.text(pts[-1][0], pts[-1][1] * 0.8, f"{v} m/s", fontsize=8, rotation=-25)

ax.set_xlabel("Flow rate [L/s]")
ax.set_ylabel("Head loss [m per km]")
ax.set_title("Pipe sizing chart - water 15 degC, roughness 0.1 mm\n(labels: nominal ID in mm; dashed: velocity)")
ax.grid(True, which="both", alpha=0.3)
ax.set_ylim(0.1, 200)
fig.tight_layout()
fig.savefig("pipe_sizing_chart.png", dpi=150)
print("Saved pipe_sizing_chart.png")

# Also print a quick selection table
print("\nSmallest size keeping V <= 1.5 m/s and h_f <= 5 m/km:")
for q_ls in [2, 5, 10, 20, 50, 100, 200]:
    q = q_ls / 1000  # L/s -> m3/s
    for d_mm in sizes_mm:
        r = pf.head_loss(q, d_mm / 1000, 1000.0, water, eps)
        if r.velocity <= 1.5 and r.major_head_loss <= 5.0:
            print(f"  {q_ls:>4} L/s -> DN{d_mm:<4} (V = {r.velocity:.2f} m/s, {r.major_head_loss:.2f} m/km)")
            break
