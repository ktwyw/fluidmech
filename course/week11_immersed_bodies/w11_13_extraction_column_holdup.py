"""CHME 202 - Week 11 - Example 13: drops in a liquid-liquid extraction column - holdup and flooding.

Light organic drops rise against a downflowing aqueous phase. The slip velocity between
the phases, U_d/phi + U_c/(1 - phi) = U_t (1 - phi)^(n - 1) (Richardson-Zaki form), fixes
the dispersed-phase holdup phi. If no holdup satisfies it, the column FLOODS.
"""

from fluidmech import Fluid
from fluidmech.drag import richardson_zaki_exponent, terminal_velocity

water = Fluid.water(25)
d, rho_d = 2.5e-3, 870.0  # toluene-like drops
ut = abs(terminal_velocity(d, rho_d, water))
re = water.density * ut * d / water.dynamic_viscosity
n = richardson_zaki_exponent(re)
print(f"Drops d = {d * 1000} mm (rho = {rho_d}): rigid-sphere rise velocity {ut * 1000:.0f} mm/s, n = {n:.2f}\n")
U_c = 0.004  # continuous (aqueous) phase superficial velocity, downward [m/s]
print(f"Continuous phase U_c = {U_c * 1000:.0f} mm/s")
print(f"{'U_d [mm/s]':>11} {'holdup phi':>11}")
for ud_mm in [1, 3, 5, 8, 12, 16]:
    U_d = ud_mm / 1000  # mm/s -> m/s
    # scan phi from small to large; take the first (stable, low-holdup) root
    phi_found = None
    prev = None
    for i in range(1, 900):  # scan phi = 0.001 ... 0.899 for the first sign change
        phi = i / 1000
        # slip-velocity balance: zero at the operating holdup
        f = U_d / phi + U_c / (1 - phi) - ut * (1 - phi) ** (n - 1)
        if prev is not None and prev > 0 >= f:
            phi_found = phi
            break
        prev = f
    txt = f"{phi_found:>11.3f}" if phi_found else f"{'FLOODED':>11}"
    print(f"{ud_mm:>11} {txt}")
print("\nHoldup rises steeply as the flows increase until the drops can no longer rise against the")
print("counter-current: flooding. Columns are designed at ~50-70 % of the flooding throughput.")
