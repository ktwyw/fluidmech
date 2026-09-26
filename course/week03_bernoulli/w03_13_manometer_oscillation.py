"""CHME 202 - Week 3 - Example 13: unsteady Bernoulli - oscillation of liquid in a U-tube.

When a U-tube manometer is disturbed, the liquid column of length L oscillates.
The unsteady Bernoulli equation gives L d2z/dt2 + 2 g z = 0 (inviscid), a simple
harmonic motion with omega = sqrt(2 g / L). It sets how fast a manometer can respond.
Reading: White, Section 3.5 (unsteady Bernoulli).
"""

import math

from fluidmech.constants import G

print(f"{'column length L [m]':>20} {'period [s]':>11} {'frequency [Hz]':>15}")
for L in [0.2, 0.5, 1.0, 2.0, 5.0]:
    w = math.sqrt(2 * G / L)
    print(f"{L:>20} {2 * math.pi / w:>11.2f} {w / (2 * math.pi):>15.3f}")
print("\nThe period does not depend on the liquid density or the tube diameter (inviscid).")
print("Viscosity damps the motion; narrow tubes and viscous gauge liquids give overdamped, sluggish")
print("manometers, wide tubes give oscillating readings. The same physics describes surge tanks and")
print("sloshing in long pipes connecting two tanks (with L the pipe length).")

# Two tanks connected by a long pipe: level oscillation (U-tube with area ratio)
A_tank, A_pipe, L_pipe = 20.0, 0.05, 200.0
w = math.sqrt(2 * G * A_pipe / (L_pipe * A_tank))
print(f"\nTwo {A_tank} m2 tanks joined by {L_pipe:.0f} m of pipe ({A_pipe} m2): period {2 * math.pi / w / 60:.1f} min")
