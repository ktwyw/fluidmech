"""Common dimensionless groups of fluid mechanics."""

from __future__ import annotations

import math

from .constants import G


def reynolds(velocity: float, length: float, kinematic_viscosity: float) -> float:
    """Reynolds number Re = V L / nu (inertia / viscous forces)."""
    if kinematic_viscosity <= 0:
        raise ValueError("kinematic_viscosity must be positive.")
    return velocity * length / kinematic_viscosity


def froude(velocity: float, length: float, g: float = G) -> float:
    """Froude number Fr = V / sqrt(g L) (inertia / gravity forces)."""
    if length <= 0:
        raise ValueError("length must be positive.")
    return velocity / math.sqrt(g * length)


def mach(velocity: float, speed_of_sound: float) -> float:
    """Mach number Ma = V / c."""
    if speed_of_sound <= 0:
        raise ValueError("speed_of_sound must be positive.")
    return velocity / speed_of_sound


def weber(density: float, velocity: float, length: float, surface_tension: float) -> float:
    """Weber number We = rho V^2 L / sigma (inertia / surface tension)."""
    if surface_tension <= 0:
        raise ValueError("surface_tension must be positive.")
    return density * velocity**2 * length / surface_tension


def euler(pressure_difference: float, density: float, velocity: float) -> float:
    """Euler number Eu = dp / (rho V^2) (pressure / inertia forces)."""
    if density <= 0 or velocity == 0:
        raise ValueError("density must be positive and velocity non-zero.")
    return pressure_difference / (density * velocity**2)


def flow_regime(re: float, laminar_limit: float = 2300.0, turbulent_limit: float = 4000.0) -> str:
    """Classify internal pipe flow as 'laminar', 'transitional' or 'turbulent'."""
    if re < laminar_limit:
        return "laminar"
    if re < turbulent_limit:
        return "transitional"
    return "turbulent"
