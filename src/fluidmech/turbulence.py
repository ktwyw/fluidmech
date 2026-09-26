"""Turbulent wall flows: law of the wall, friction velocity and CFD mesh sizing.

Wall units: u+ = u / u_tau, y+ = y u_tau / nu, with friction velocity
u_tau = sqrt(tau_w / rho). Constants kappa = 0.41, B = 5.0.

Examples
--------
>>> round(law_of_the_wall(1.0), 3)   # viscous sublayer: u+ = y+
1.0
>>> round(law_of_the_wall(1000.0), 2)  # log layer
21.85
"""

from __future__ import annotations

import math

from ._solvers import bisect

KAPPA = 0.41
B_CONST = 5.0


def friction_velocity(wall_shear_stress: float, density: float) -> float:
    """u_tau = sqrt(tau_w / rho) [m/s]."""
    if wall_shear_stress < 0 or density <= 0:
        raise ValueError("Need tau_w >= 0 and rho > 0.")
    return math.sqrt(wall_shear_stress / density)


def pipe_wall_shear_stress(friction_factor: float, density: float, velocity: float) -> float:
    """tau_w = f rho V^2 / 8 for a pipe (Darcy friction factor)."""
    return friction_factor * density * velocity**2 / 8.0


def log_law(y_plus: float) -> float:
    """Logarithmic law u+ = ln(y+)/kappa + B (valid for roughly 30 < y+ < 0.2 Re_tau)."""
    if y_plus <= 0:
        raise ValueError("y_plus must be positive.")
    return math.log(y_plus) / KAPPA + B_CONST


def spalding_y_plus(u_plus: float) -> float:
    """Spalding's single formula for the whole inner layer, y+ as a function of u+."""
    ku = KAPPA * u_plus
    return u_plus + math.exp(-KAPPA * B_CONST) * (math.exp(ku) - 1.0 - ku - ku**2 / 2.0 - ku**3 / 6.0)


def law_of_the_wall(y_plus: float) -> float:
    """u+ from Spalding's law: smooth from the viscous sublayer (u+ = y+) through the log layer."""
    if y_plus < 0:
        raise ValueError("y_plus must be non-negative.")
    if y_plus == 0:
        return 0.0
    return bisect(lambda u: spalding_y_plus(u) - y_plus, 0.0, 100.0)  # Spalding gives y+(u+); invert it numerically


def wall_region(y_plus: float) -> str:
    """Name of the near-wall region: viscous sublayer, buffer layer or log layer."""
    if y_plus < 5:
        return "viscous sublayer"
    if y_plus < 30:
        return "buffer layer"
    return "log layer"


def power_law_profile(r: float, radius: float, centreline_velocity: float, n: float = 7.0) -> float:
    """Empirical 1/n power-law profile u = U_max (1 - r/R)^(1/n)."""
    if not 0 <= r <= radius:
        raise ValueError("r must lie between 0 and the pipe radius.")
    return centreline_velocity * (1.0 - r / radius) ** (1.0 / n)


def power_law_exponent(reynolds: float) -> float:
    """Exponent n of the power-law profile, n ~ -1.7 + 1.8 log10(Re) (n ~ 7 at Re ~ 1e5)."""
    return -1.7 + 1.8 * math.log10(reynolds)


def mean_to_max_velocity_ratio(n: float) -> float:
    """V / U_max = 2 n^2 / ((n + 1)(2n + 1)) for the power-law profile."""
    return 2.0 * n**2 / ((n + 1.0) * (2.0 * n + 1.0))


def viscous_sublayer_thickness(nu: float, u_tau: float, y_plus_edge: float = 5.0) -> float:
    """Thickness of the viscous sublayer, delta_v = 5 nu / u_tau [m]."""
    return y_plus_edge * nu / u_tau


def wall_distance_for_y_plus(y_plus: float, u_tau: float, nu: float) -> float:
    """Physical distance y = y+ nu / u_tau. Use it to size the first CFD cell (e.g. in COMSOL)."""
    return y_plus * nu / u_tau


def pipe_turbulence_intensity(reynolds: float) -> float:
    """Core turbulence intensity in fully developed pipe flow, I ~ 0.16 Re^(-1/8)."""
    return 0.16 * reynolds ** (-0.125)


def entrance_length(reynolds: float, diameter: float) -> float:
    """Hydrodynamic entrance length: 0.06 Re D (laminar), 4.4 Re^(1/6) D (turbulent) [m] (White)."""
    if reynolds < 2300:
        return 0.06 * reynolds * diameter
    return 4.4 * reynolds ** (1.0 / 6.0) * diameter


def kolmogorov_scales(dissipation_rate: float, nu: float) -> tuple[float, float, float]:
    """Kolmogorov length, time and velocity scales (eta, tau_eta, v_eta) for dissipation rate epsilon [W/kg]."""
    if dissipation_rate <= 0:
        raise ValueError("dissipation_rate must be positive.")
    eta = (nu**3 / dissipation_rate) ** 0.25
    tau = (nu / dissipation_rate) ** 0.5
    v = (nu * dissipation_rate) ** 0.25
    return eta, tau, v
