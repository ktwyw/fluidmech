"""CHME 202 - Week 3 - Example 15: draining a tank whose cross-section varies with height.

Quasi-steady Bernoulli: A(h) dh/dt = -Cd a sqrt(2 g h). For a spherical tank A(h)
changes with h, so we integrate numerically and compare with a vertical cylinder
of the same volume and height.
"""

import math

from fluidmech.constants import G

R = 2.0  # sphere radius [m]
cd, d_hole = 0.8, 0.05
a = cd * math.pi * d_hole**2 / 4


def area_sphere(h: float) -> float:
    return math.pi * (2 * R * h - h * h)  # cross-section at height h above the bottom


def drain_time(area_func, h0: float, n: int = 20000) -> float:
    """t = integral of A(h) dh / (Cd a sqrt(2 g h)) from 0 to h0 (midpoint rule in h).

    Integrating over height rather than stepping in time avoids huge steps where A(h) is small.
    """
    dh = h0 / n
    return sum(area_func((i + 0.5) * dh) / (a * math.sqrt(2 * G * (i + 0.5) * dh)) * dh for i in range(n))


V_sphere = 4 / 3 * math.pi * R**3  # tank volume [m3]
t_sphere = drain_time(area_sphere, 2 * R)
exact_sphere = math.pi * (2 * R) ** 1.5 * (8 * R / 15) / (a * math.sqrt(2 * G))
A_cyl = V_sphere / (2 * R)  # cylinder of equal volume and height
t_cyl = drain_time(lambda h: A_cyl, 2 * R)
exact_cyl = A_cyl / a * math.sqrt(2 * 2 * R / G)
print(f"Spherical tank R = {R} m ({V_sphere:.1f} m3), outlet {d_hole * 1000:.0f} mm, Cd = {cd}")
print(f"  time to empty: {t_sphere / 60:.1f} min (exact {exact_sphere / 60:.1f} min)")
print(f"Vertical cylinder of equal volume and height: {t_cyl / 60:.1f} min (exact {exact_cyl / 60:.1f} min)")
print(f"Ratio {t_sphere / t_cyl:.3f} (theory: exactly 0.8)")
print("\nThe sphere empties faster: most of its liquid sits high up, where the head (and outflow) is large;")
print("only a little liquid remains in the narrow bottom, where the flow is slow.")
