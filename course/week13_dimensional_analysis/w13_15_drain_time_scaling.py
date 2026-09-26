"""CHME 202 - Week 13 - Example 15: scaling the draining time of a tank.

The time to empty depends on the tank area A, the outlet area a, the initial depth H and g:
t = f(A, a, H, g). Two Pi groups: t sqrt(g / H) = phi(A / a). Torricelli (Week 3) gives
phi = sqrt(2) (A/a) / Cd. One lab test on a small tank therefore predicts any similar tank.
"""

import math

from fluidmech import dimensional as dim
from fluidmech.bernoulli import tank_drain_time

groups = dim.pi_groups({"t": "time", "g": "gravity", "H": "length", "A": "area", "a": "area"})
print("Pi groups:", ", ".join(dim.format_group(g) for g in groups), "\n")

# Lab test: 0.3 m diameter tank, 8 mm hole, 0.5 m deep
A_lab, a_lab, H_lab = math.pi * 0.15**2, math.pi * 0.004**2, 0.5
t_lab = tank_drain_time(A_lab, a_lab, H_lab, 0.0, 0.61)
pi_lab = t_lab * math.sqrt(9.80665 / H_lab)
print(f"Lab tank: t = {t_lab:.0f} s -> t sqrt(g/H) = {pi_lab:.0f} at A/a = {A_lab / a_lab:.0f}")
# Full scale, geometrically similar: 3 m tank, 80 mm hole, 5 m deep (same A/a)
A_f, a_f, H_f = math.pi * 1.5**2, math.pi * 0.04**2, 5.0
t_pred = pi_lab * math.sqrt(H_f / 9.80665)  # same Pi group value at the same A/a
print(f"Full-scale tank (10x larger): predicted t = {t_pred / 60:.1f} min from the lab result alone")
print(f"Torricelli check: {tank_drain_time(A_f, a_f, H_f, 0.0, 0.61) / 60:.1f} min")
print(f"\nThe draining time scales as sqrt(length): a 10x larger tank takes sqrt(10) = {math.sqrt(10):.2f}x longer.")
print("(If the outlet were not scaled with the tank, A/a would change and the full curve phi(A/a) is needed.)")
