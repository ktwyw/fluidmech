"""CHME 202 - Week 11 - Example 1: the drag curve of a sphere.

Creeping flow (Stokes, Cd = 24/Re), intermediate regime, Newton's regime
(Cd ~ 0.44) and the drag crisis near Re ~ 3e5 when the boundary layer turns
turbulent and separation moves rearwards. Saves sphere_drag.png.
Reading: White, Sections 7.5-7.6.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech.drag import sphere_drag_coefficient

print(f"{'Re':>9} {'Cd (correlation)':>17} {'Cd Stokes':>10}  regime")
for re in [0.01, 0.1, 1, 10, 100, 1e3, 1e4, 1e5, 2e5]:
    cd = sphere_drag_coefficient(re)
    regime = "Stokes (creeping)" if re < 0.3 else ("intermediate" if re < 1000 else "Newton (Cd ~ const)")
    print(f"{re:>9g} {cd:>17.3f} {24 / re:>10.3f}  {regime}")
print("\nIn creeping flow drag is purely viscous: F = 3 pi mu d U (proportional to U).")
print("In Newton's regime drag is mostly pressure (form) drag behind the separated wake: F ~ U^2.")
print("Above Re ~ 3e5 the drag crisis cuts Cd to ~0.1-0.2 (not covered by the correlation).")

res = [10 ** (i / 20) for i in range(-40, 107)]  # Re from 0.01 to ~2e5, 20 points per decade
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.loglog(res, [sphere_drag_coefficient(r) for r in res], "k", lw=2, label="Brown & Lawler (2003)")
ax.loglog([r for r in res if r < 10], [24 / r for r in res if r < 10], "--", label="Stokes 24/Re")
ax.axhline(0.44, ls=":", color="grey", label="Newton ~0.44")
ax.annotate("drag crisis", xy=(3e5, 0.3), xytext=(2e4, 0.08), arrowprops={"arrowstyle": "->"})
ax.set(xlabel="Re = rho U d / mu", ylabel="Cd", title="Drag coefficient of a sphere", ylim=(0.05, 3000))
ax.grid(alpha=0.3, which="both")
ax.legend()
fig.tight_layout()
fig.savefig("sphere_drag.png", dpi=130)
print("Saved sphere_drag.png")
