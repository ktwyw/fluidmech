"""CHME 202 - Week 11 - Example 5: settling of concentrated suspensions (hindered settling).

In a suspension, particles settle slower than a single particle because the
displaced liquid flows upward between them: U = U_t eps^n (Richardson-Zaki).
Used to size clarifiers and thickeners.
"""

from fluidmech import Fluid
from fluidmech.drag import hindered_settling_velocity, richardson_zaki_exponent, terminal_velocity

water = Fluid.water(20)
d, rho_p = 150e-6, 2650.0  # sand diameter [m], density [kg/m3]
ut = terminal_velocity(d, rho_p, water)
re_t = water.density * ut * d / water.dynamic_viscosity
n = richardson_zaki_exponent(re_t)
print(f"Sand d = {d * 1e6:.0f} um: single-particle U_t = {ut * 1000:.2f} mm/s, Re_t = {re_t:.1f}, n = {n:.2f}\n")
print(f"{'solids vol. fraction':>21} {'voidage':>8} {'U [mm/s]':>9} {'U/U_t':>6} {'solids flux [kg/m2 h]':>22}")
for c in [0.01, 0.05, 0.10, 0.20, 0.30, 0.40]:
    eps = 1 - c  # voidage = liquid volume fraction
    u = hindered_settling_velocity(ut, eps, re_t)
    flux = u * c * rho_p * 3600  # solids flux [kg/(m2 h)]
    print(f"{c:>21.2f} {eps:>8.2f} {u * 1000:>9.3f} {u / ut:>6.2f} {flux:>22.0f}")
print("\nThe solids flux passes through a maximum: this limiting flux sizes a continuous thickener.")
q_feed, c_feed = 50.0 / 3600, 0.05  # m3/s of slurry at 5 vol % solids
u_feed = hindered_settling_velocity(ut, 1 - c_feed, re_t)
print(f"Clarification area for {q_feed * 3600:.0f} m3/h at 5 % solids: A > Q / U = {q_feed / u_feed:.1f} m2")
