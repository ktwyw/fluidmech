"""CHME 202 - Week 9 - Example 12: explicit Swamee-Jain formulas for Type 2 and Type 3 problems.

Instead of iterating, Swamee & Jain (1976) give closed-form approximations:
  Q = -0.965 D^2.5 sqrt(g h_f / L) ln[ eps / (3.7 D) + sqrt(3.17 nu^2 L / (g D^3 h_f)) ]
  D = 0.66 [ eps^1.25 (L Q^2 / (g h_f))^4.75 + nu Q^9.4 (L / (g h_f))^5.2 ]^0.04
We compare them with the exact (iterative) solutions of fluidmech.pipe_flow.
"""

import math

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.constants import G

water = Fluid.water(20)
nu = water.kinematic_viscosity
print("Type 2 (flow rate for a given head loss):")
print(f"{'D [m]':>6} {'L [m]':>6} {'h_f [m]':>8} {'eps [mm]':>9} {'Q exact [L/s]':>14} {'Q SJ [L/s]':>11} {'error':>7}")
for D, L, hf, eps in [(0.1, 200, 5, 0.045e-3), (0.3, 1000, 10, 0.26e-3), (0.05, 50, 2, 0.0015e-3)]:
    q_exact = pf.flow_rate_for_head_loss(hf, D, L, water, eps)
    q_sj = (
        -0.965
        * D**2.5
        * math.sqrt(G * hf / L)
        * math.log(eps / (3.7 * D) + math.sqrt(3.17 * nu**2 * L / (G * D**3 * hf)))
    )
    print(
        f"{D:>6} {L:>6} {hf:>8} {eps * 1000:>9.4f} {q_exact * 1000:>14.2f} {q_sj * 1000:>11.2f} {(0.0 if abs(q_sj / q_exact - 1) < 5e-4 else q_sj / q_exact - 1):>+7.1%}"
    )

print("\nType 3 (diameter for a given flow and head loss):")
print(f"{'Q [L/s]':>8} {'L [m]':>6} {'h_f [m]':>8} {'D exact [mm]':>13} {'D SJ [mm]':>10} {'error':>7}")
for Q, L, hf, eps in [(0.02, 200, 5, 0.045e-3), (0.2, 2000, 15, 0.26e-3), (0.002, 30, 1, 0.0015e-3)]:
    d_exact = pf.diameter_for_head_loss(Q, hf, L, water, eps)
    # Swamee-Jain (1976) diameter formula
    d_sj = 0.66 * (eps**1.25 * (L * Q**2 / (G * hf)) ** 4.75 + nu * Q**9.4 * (L / (G * hf)) ** 5.2) ** 0.04
    print(f"{Q * 1000:>8.0f} {L:>6} {hf:>8} {d_exact * 1000:>13.1f} {d_sj * 1000:>10.1f} {d_sj / d_exact - 1:>+7.1%}")
print("\nThe explicit formulas are within a few percent - ideal for spreadsheets and hand checks.")
print("(Minor losses are not included; add them as equivalent length.)")
