"""CHME 202 - Week 12 - Example 6: which particle diameter goes into the Ergun equation?

Real packings have a size distribution. Pressure drop depends on surface area per
volume, so the right average is the Sauter (surface-volume) mean
d32 = 1 / sum(x_i / d_i) for mass fractions x_i (particles of equal density).
"""

from fluidmech import Fluid
from fluidmech import porous as por

# Sieve analysis: size range [mm] and mass fraction retained
sieves = [((2.8, 3.35), 0.10), ((2.36, 2.8), 0.25), ((2.0, 2.36), 0.30), ((1.7, 2.0), 0.20), ((1.4, 1.7), 0.15)]
d_i = [((lo * hi) ** 0.5) / 1000 for (lo, hi), _ in sieves]  # geometric mean of each sieve interval
x_i = [x for _, x in sieves]
d_mass_mean = sum(x * d for x, d in zip(x_i, d_i))
d32 = 1 / sum(x / d for x, d in zip(x_i, d_i))  # Sauter mean from mass fractions
print(f"{'sieve [mm]':>12} {'mass frac':>10} {'d_i [mm]':>9}")
for ((lo, hi), x), d in zip(sieves, d_i):
    print(f"{f'{lo}-{hi}':>12} {x:>10.2f} {d * 1000:>9.2f}")
print(f"\nmass-mean diameter {d_mass_mean * 1000:.2f} mm, Sauter mean d32 = {d32 * 1000:.2f} mm")

water = Fluid.water(20)
u, eps, L = 0.01, 0.40, 1.0  # superficial velocity [m/s], voidage, bed depth [m]
for label, d in [("mass mean", d_mass_mean), ("Sauter mean", d32), ("largest sieve", d_i[0]), ("smallest", d_i[-1])]:
    dp = por.ergun_pressure_gradient(u, d, eps, water.dynamic_viscosity, water.density) * L
    print(f"  Ergun with {label:<14} d = {d * 1000:.2f} mm: dp = {dp / 1e3:.2f} kPa/m")
print("\nThe fines control the surface area: using the mass mean underestimates the pressure drop.")
print("Mixed sizes also pack more densely (lower voidage), raising dp further - measure eps when possible.")
