"""CHME 202 - Week 1 - Example 13: what shear rate does a non-Newtonian fluid 'see' in equipment?

The apparent viscosity of a shear-thinning fluid depends on the shear rate, so we need
typical shear rates: pipe wall 8V/D x (3n+1)/(4n); stirred tank ~k_s N (Metzner-Otto,
k_s ~ 11 for turbines); coating and spraying far higher.
"""

from fluidmech.rheology import PowerLaw

fluid = PowerLaw(K=4.0, n=0.40)  # e.g. a xanthan-gum solution
print(f"Power-law fluid K = {fluid.K} Pa s^n, n = {fluid.n}\n")
n = fluid.n
situations = [
    ("settling of a fine particle", 0.01),
    ("slow draining from a tank", 1.0),
    ("stirred tank, 60 rpm (k_s = 11)", 11 * 1.0),
    ("stirred tank, 300 rpm", 11 * 5.0),
    ("pipe wall, V = 1 m/s, D = 50 mm", 8 * 1.0 / 0.05 * (3 * n + 1) / (4 * n)),
    ("pipe wall, V = 2 m/s, D = 25 mm", 8 * 2.0 / 0.025 * (3 * n + 1) / (4 * n)),
    ("brushing / coating", 1e4),
]
print(f"{'situation':<34} {'shear rate [1/s]':>17} {'apparent mu [Pa s]':>19}")
for name, rate in situations:
    print(f"{name:<34} {rate:>17.3g} {fluid.apparent_viscosity(rate):>19.3g}")
print("\nThe same liquid behaves like a thick gel at rest (suspends particles) and flows easily in a pipe.")
print("Always quote the shear rate with an apparent viscosity - and measure the rheology over the")
print("range of shear rates that the process actually applies.")
