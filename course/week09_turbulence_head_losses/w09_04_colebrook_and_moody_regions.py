"""CHME 202 - Week 9 - Example 4: solving the Colebrook equation and reading the Moody chart.

Shows the fixed-point iteration used by pipe_flow.colebrook step by step, and
identifies the Moody-chart region (laminar, transition, smooth, transitional,
fully rough) from the roughness Reynolds number.
Reading: White, Section 6.7.
"""

import math

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

re, rel = 1.5e5, 0.001  # Reynolds number and relative roughness eps/D
print(f"Colebrook for Re = {re:.3g}, eps/D = {rel}: 1/sqrt(f) = -2 log10(eps/3.7D + 2.51/(Re sqrt(f)))\n")
x = 1 / math.sqrt(0.02)  # initial guess f = 0.02
for i in range(6):
    x_new = -2 * math.log10(rel / 3.7 + 2.51 * x / re)  # one fixed-point step of the Colebrook equation
    print(f"  iteration {i + 1}: f = {1 / x_new**2:.6f}")
    x = x_new
print(f"  library value:   f = {pf.colebrook(re, rel):.6f}  (converges in a few iterations)\n")

print(f"{'Re':>9} {'eps/D':>7} {'f':>8} {'eps+':>7}  Moody region")
for re_i, rel_i in [(1000, 0.001), (3000, 0.001), (1e4, 1e-5), (1e5, 1e-4), (1e6, 1e-3), (1e7, 0.01)]:
    f = pf.friction_factor(re_i, rel_i)
    eps_plus = rel_i * re_i * math.sqrt(f / 8)  # eps+ = eps u_tau / nu = (eps/D) Re sqrt(f/8)
    if re_i < 2300:
        region = "laminar: f = 64/Re, roughness irrelevant"
    elif re_i < 4000:
        region = "transition: f uncertain"
    elif eps_plus < 5:
        region = "smooth turbulent: f depends on Re only"
    elif eps_plus < 70:
        region = "transitional roughness: f depends on both"
    else:
        region = "fully rough: f depends on eps/D only"
    print(f"{re_i:>9.0e} {rel_i:>7g} {f:>8.4f} {eps_plus:>7.1f}  {region}")

print("\nPipes get rougher with age (corrosion, scale). Colebrook-White with an aged roughness:")
for years, eps in [(0, 0.045e-3), (10, 0.3e-3), (25, 1.0e-3)]:
    r = pf.head_loss(0.03, 0.15, 1000.0, Fluid.water(15), eps)
    print(f"  steel main after {years:>2} years (eps ~ {eps * 1000:.2f} mm): head loss {r.major_head_loss:5.2f} m/km")
