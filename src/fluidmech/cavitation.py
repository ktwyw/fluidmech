"""Cavitation bubble dynamics: the Rayleigh-Plesset equation.

    R R'' + (3/2) R'^2 = (1/rho) [ p_B - p_inf - 2 sigma / R - 4 mu R' / R ]

where p_B = p_v + p_g0 (R0/R)^(3 kappa) is the pressure inside the bubble (vapour + gas).
A bubble that grows in a low-pressure zone (a pump inlet, a propeller, a valve throat) and is
then carried into higher pressure collapses violently - the cause of cavitation erosion.

Examples
--------
>>> round(rayleigh_collapse_time(1e-3, 1000.0, 1e5), 6)   # 1 mm cavity, 1 bar driving pressure
9.1e-05
"""

from __future__ import annotations

import math


def rayleigh_collapse_time(radius: float, density: float, pressure_difference: float) -> float:
    """Rayleigh (1917) collapse time of an empty spherical cavity, t = 0.9147 R0 sqrt(rho / dp) [s]."""
    return 0.914681 * radius * math.sqrt(density / pressure_difference)


def rayleigh_plesset(
    radius: float,
    p_inf,
    t_end: float,
    density: float = 998.0,
    viscosity: float = 1.0e-3,
    surface_tension: float = 0.072,
    vapour_pressure: float = 2.34e3,
    gas_pressure: float = 0.0,
    kappa: float = 1.4,
    min_radius_fraction: float = 1e-3,
    max_step: float | None = None,
) -> dict:
    """Integrate the Rayleigh-Plesset equation with an adaptive RK4 step.

    ``p_inf`` is the far-field pressure [Pa]: a number or a function of time.
    ``gas_pressure`` is the initial partial pressure of non-condensable gas in the bubble
    (0 gives a pure vapour cavity that collapses to a point). Integration stops at ``t_end``
    or when R falls below ``min_radius_fraction`` x R0. Returns dict with t, R, Rdot.
    """
    p_far = p_inf if callable(p_inf) else (lambda t, p=p_inf: p)
    R0 = radius

    def accel(t, R, U):
        p_bubble = vapour_pressure + gas_pressure * (R0 / R) ** (3 * kappa)
        p_wall = p_bubble - 2 * surface_tension / R - 4 * viscosity * U / R  # liquid pressure at the wall
        return ((p_wall - p_far(t)) / density - 1.5 * U * U) / R

    t, R, U = 0.0, radius, 0.0
    ts, Rs, Us = [t], [R], [U]
    h_max = max_step or t_end / 2000
    while t < t_end and R > min_radius_fraction * R0:
        # step small compared with the time scale R / |U| on which the radius changes
        h = min(h_max, 0.02 * R / (abs(U) + 1e-12), t_end - t)
        k1r, k1u = U, accel(t, R, U)
        k2r, k2u = U + 0.5 * h * k1u, accel(t + 0.5 * h, R + 0.5 * h * k1r, U + 0.5 * h * k1u)
        k3r, k3u = U + 0.5 * h * k2u, accel(t + 0.5 * h, R + 0.5 * h * k2r, U + 0.5 * h * k2u)
        k4r, k4u = U + h * k3u, accel(t + h, R + h * k3r, U + h * k3u)
        R += h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        U += h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        t += h
        ts.append(t)
        Rs.append(R)
        Us.append(U)
    return {"t": ts, "R": Rs, "Rdot": Us}
