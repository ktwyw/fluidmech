"""CHME 202 - Week 12 - Example 8: compressible filter cakes.

Many cakes (flocs, biological solids) compact under pressure, so their specific
resistance rises: alpha = alpha0 dp^s, with compressibility s between 0 (rigid)
and ~1. Then the filtration rate grows only as dp^(1 - s): higher pressure helps little.
"""

import math

# Specific cake resistance measured at four pressures (leaf-filter tests)
dps = [0.5e5, 1e5, 2e5, 4e5]
alphas = [1.8e11, 2.6e11, 3.9e11, 5.7e11]  # measured specific cake resistance [m/kg]
x = [math.log(p) for p in dps]
y = [math.log(a) for a in alphas]
n = len(x)
xm, ym = sum(x) / n, sum(y) / n
# slope of ln(alpha) vs ln(dp) = compressibility s
s = sum((a - xm) * (b - ym) for a, b in zip(x, y)) / sum((a - xm) ** 2 for a in x)
alpha0 = math.exp(ym - s * xm)
print(f"{'dp [bar]':>9} {'alpha [m/kg]':>13}")
for p, a in zip(dps, alphas):
    print(f"{p / 1e5:>9.1f} {a:>13.2e}")
print(f"\nFit: alpha = {alpha0:.3g} dp^{s:.2f}  -> compressibility s = {s:.2f}")

print("\nRelative filtration rate (cake-controlled, rate ~ dp / alpha ~ dp^(1-s)):")
for p in [1, 2, 4, 8]:
    print(f"  {p} bar: {p ** (1 - s):.2f}x the rate at 1 bar  (rigid cake: {p:.0f}x)")
print("\nFor strongly compressible cakes, raising pressure is ineffective; filter aids (diatomaceous")
print("earth) or flocculation to build a more open cake work better.")
