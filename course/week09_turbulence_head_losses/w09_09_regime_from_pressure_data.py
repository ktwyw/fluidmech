"""CHME 202 - Week 9 - Example 9: identifying the flow regime from pressure-drop measurements.

Laminar flow: dp ~ Q (slope 1 on log-log axes). Turbulent smooth pipe: dp ~ Q^1.75;
fully rough: dp ~ Q^2. Plotting lab data on log axes reveals transition without a
Reynolds-number calculation - a typical lab analysis (Lab Assignment 2 style).
"""

import math
import random

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

random.seed(7)
fluid = Fluid(870.0, 0.012, "light oil")
D, L = 0.012, 2.0  # tube diameter and length [m]
flows_lpm = [1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20.0, 28.0, 40.0, 56.0, 80.0]  # test flow rates [L/min]
data = []
print(
    f"Oil (nu = {fluid.kinematic_viscosity * 1e6:.1f} cSt) in a {D * 1000:.0f} mm tube, L = {L} m - 'measured' data\n"
)
print(f"{'Q [L/min]':>10} {'dp [kPa]':>9} {'Re (for checking)':>18}")
for q_lpm in flows_lpm:
    q = q_lpm / 60000  # L/min -> m3/s
    r = pf.head_loss(q, D, L, fluid, 0.0)
    dp = r.pressure_drop * (1 + random.gauss(0, 0.02))
    data.append((q, dp))
    print(f"{q_lpm:>10} {dp / 1e3:>9.3f} {r.reynolds:>18.0f}")

print("\nLocal log-log slope d ln(dp) / d ln(Q):")
transition = None
for (q1, p1), (q2, p2) in zip(data, data[1:]):
    slope = math.log(p2 / p1) / math.log(q2 / q1)  # local slope of the log-log plot
    regime = "laminar" if slope < 1.3 else ("transition" if slope < 1.6 or slope > 2.3 else "turbulent")
    if regime == "transition" and transition is None:
        transition = (q1 * 60000, q2 * 60000)  # m3/s -> L/min
    print(f"  {q1 * 60000:5.1f}-{q2 * 60000:5.1f} L/min: slope {slope:5.2f}  -> {regime}")
print(f"\nThe jump in dp between {transition[0]:.0f} and {transition[1]:.0f} L/min marks transition; in turbulent flow")
print("the slope settles near 1.75 (smooth tube). Scatter in the data makes single slopes noisy - fit a")
print("straight line through several points in each regime rather than using neighbouring pairs only.")
