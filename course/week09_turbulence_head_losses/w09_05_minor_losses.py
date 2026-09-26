"""CHME 202 - Week 9 - Example 5: minor losses in fittings, valves and area changes.

h_m = K V^2 / (2g). Equivalent length L_eq = K D / f expresses a fitting as
extra pipe. Sudden expansion: K = (1 - A1/A2)^2 (Borda-Carnot, from momentum).
Reading: White, Section 6.9.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
D, Q = 0.05, 0.004  # pipe diameter [m], flow [m3/s]
V = pf.mean_velocity(Q, D)
f = pf.friction_factor(V * D / water.kinematic_viscosity, pf.ROUGHNESS["commercial_steel"] / D)
print(f"Water, D = {D * 1000:.0f} mm, V = {V:.2f} m/s, f = {f:.4f}\n")
print(f"{'fitting':<22} {'K':>6} {'h_m [m]':>8} {'L_eq [m]':>9} {'L_eq / D':>9}")
for name, k in pf.MINOR_LOSS_K.items():
    print(f"{name:<22} {k:>6.2f} {pf.minor_loss(k, V):>8.3f} {k * D / f:>9.2f} {k / f:>9.0f}")

print("\nSudden expansion (Borda-Carnot) and sudden contraction, based on the SMALL-pipe velocity:")
print(f"{'d/D':>5} {'K expansion':>12} {'K contraction':>14}")
for ratio in [0.2, 0.4, 0.6, 0.8, 0.9]:
    a = ratio**2
    print(f"{ratio:>5} {(1 - a) ** 2:>12.3f} {0.42 * (1 - a):>14.3f}")
print("For large area changes expansions lose far more than contractions; a diffuser (gradual")
print("expansion) avoids most of the Borda-Carnot loss and recovers pressure.\n")

print("Share of minor losses: 10 fittings (sum K = 8) on pipes of different length")
for length in [5, 20, 100, 1000]:
    r = pf.head_loss(Q, D, length, water, pf.ROUGHNESS["commercial_steel"], k_total=8.0)
    print(f"  L = {length:>5} m: minor losses are {r.minor_head_loss / r.total_head_loss:5.0%} of the total")
print("In compact process plant, fittings often dominate; in long pipelines they are negligible.")
