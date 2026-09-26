"""CHME 202 - Week 5 - Example 14: viscous decay of a vortex (Lamb-Oseen, an exact N-S solution).

A line vortex of circulation Gamma released at t = 0 spreads by viscous diffusion:
v(r, t) = Gamma / (2 pi r) [1 - exp(-r^2 / (4 nu t))]. The core radius (maximum velocity)
grows as r_max = 2.24 sqrt(nu t) and the peak velocity falls as 1 / sqrt(t).
Relevant to the swirl left in a tank after the agitator stops and to aircraft wake vortices.
"""

import math

gamma = 0.5  # m2/s
for name, nu in [("water", 1.0e-6), ("oil", 1.0e-4)]:
    print(f"{name} (nu = {nu} m2/s):")
    print(f"  {'t [s]':>6} {'core radius [mm]':>17} {'peak v [m/s]':>13}")
    for t in [1, 10, 100, 1000]:
        r_max = 2.2418 * math.sqrt(nu * t)  # radius of peak velocity for the Lamb-Oseen vortex
        v_max = gamma / (2 * math.pi * r_max) * (1 - math.exp(-(r_max**2) / (4 * nu * t)))
        print(f"  {t:>6} {r_max * 1000:>17.1f} {v_max:>13.3f}")
print("\nOutside the core the flow is still the free vortex Gamma/(2 pi r): viscosity only spreads the core.")
print("In water a pure viscous decay is slow (minutes to hours); in practice turbulence and wall")
print("friction stop swirl in a tank much faster.")
