"""CHME 202 - Week 13 - Example 10: finding a dimensionless correlation from experiments.

Packed-bed tests with several particle sizes and flow rates are reduced to the bed
friction factor f_p = (dp/L) d eps^3 / (rho u^2 (1 - eps)) and Re_p = rho u d / (mu (1 - eps)).
Fitting f_p Re_p = a + b Re_p recovers the constants of the Ergun equation (150, 1.75).
The data are generated with 4 % scatter to mimic a laboratory.
"""

import random

from fluidmech import Fluid
from fluidmech import porous as por

random.seed(5)
eps = 0.40  # bed voidage
fluids = [Fluid.water(20), Fluid(1150.0, 0.012, "glycol solution"), Fluid.air(20)]
rows = []
for fl in fluids:
    for d in (1e-3, 3e-3, 6e-3):
        for u in (0.002, 0.01, 0.05, 0.2, 1.0):
            re = por.bed_reynolds(u, d, eps, fl.dynamic_viscosity, fl.density)
            if not 0.5 < re < 3000:
                continue
            grad = por.ergun_pressure_gradient(u, d, eps, fl.dynamic_viscosity, fl.density) * (
                1 + random.gauss(0, 0.04)
            )
            fp = grad * d * eps**3 / (fl.density * u**2 * (1 - eps))  # bed friction factor from the 'measured' gradient
            rows.append((re, fp))
x = [r for r, _ in rows]
y = [r * f for r, f in rows]
n = len(x)
xm, ym = sum(x) / n, sum(y) / n
b = sum((xi - xm) * (yi - ym) for xi, yi in zip(x, y)) / sum((xi - xm) ** 2 for xi in x)
a = ym - b * xm
print(f"{n} tests covering Re_p = {min(x):.1f} to {max(x):.0f}")
print(f"Least-squares fit of f_p Re_p = a + b Re_p:  a = {a:.0f} (Ergun 150), b = {b:.2f} (Ergun 1.75)")
print("\nSelected points:")
for re, fp in sorted(rows)[:: max(1, n // 8)]:
    print(f"  Re_p = {re:8.1f}  f_p = {fp:8.3f}  fit {a / re + b:8.3f}")
print("\nRegressing f_p Re_p against Re_p (a straight line) is better conditioned than fitting f_p directly.")
print("Report the Re range of the data: extrapolating a correlation outside it is a common mistake.")
