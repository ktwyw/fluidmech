"""CHME 202 - Week 4 - Example 6: free, forced and Rankine vortices.

Radial Euler equation for circular streamlines: dp/dr = rho v_theta^2 / r.
Forced vortex (rigid rotation, v = omega r) inside a core; free vortex
(v = Gamma / 2 pi r) outside: the Rankine vortex models tornadoes, drain
vortices and the surface vortex in an unbaffled stirred tank.
Reading: White, Section 4.9 and 8.2.
"""

import math

rho_air = 1.2  # [kg/m3]
r_core, v_max = 50.0, 60.0  # tornado core radius [m] and peak wind speed [m/s]
omega = v_max / r_core  # core rotates as a rigid body
gamma = 2 * math.pi * r_core * v_max  # circulation of the outer free vortex (matches at r_core)


def v_theta(r: float) -> float:
    return omega * r if r <= r_core else gamma / (2 * math.pi * r)


def pressure_deficit(r: float, n: int = 20000, r_far: float = 50_000.0) -> float:
    """p(r) - p_infinity from integrating dp/dr = rho v^2 / r inwards from far away."""
    total = 0.0
    lo = r
    for i in range(n):  # integrate dp/dr = rho v^2 / r from far away inwards (midpoint rule)
        a = lo + (r_far - lo) * i / n
        b = lo + (r_far - lo) * (i + 1) / n
        mid = 0.5 * (a + b)
        total += rho_air * v_theta(mid) ** 2 / mid * (b - a)
    return -total


print(f"Rankine vortex: core radius {r_core} m, peak wind {v_max} m/s\n")
print(f"{'r [m]':>7} {'v [m/s]':>8} {'p - p_inf [hPa]':>16}")
for r in [1, 10, 25, 50, 100, 200, 500]:
    print(f"{r:>7} {v_theta(r):>8.1f} {pressure_deficit(r) / 100:>16.2f}")
exact_centre = -rho_air * v_max**2
print(f"\nExact centre deficit -rho v_max^2 = {exact_centre / 100:.2f} hPa: half from the free vortex outside,")
print("half from the forced vortex core. Bernoulli does NOT hold across circular streamlines of the")
print("forced vortex (it is rotational), but it does hold everywhere in the free (irrotational) vortex.")

# Stirred-tank surface vortex depth (unbaffled): depth ~ v_max^2 / g for a Rankine vortex
tip = 1.5  # m/s, approximate peak tangential velocity
print(
    f"\nUnbaffled stirred tank with peak swirl {tip} m/s: surface vortex depth ~ v^2/g = {tip**2 / 9.81 * 100:.0f} cm"
)
print("-> baffles are installed to stop solid-body swirl and vortexing (Week 14).")
