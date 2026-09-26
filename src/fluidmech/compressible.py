"""One-dimensional compressible flow of a perfect gas.

Isentropic relations, normal shocks, nozzle mass flow and choking.
Defaults are for air (k = 1.4, R = 287.05 J/(kg K)). Temperatures are in degC
at the interface, like the rest of the package.

Examples
--------
>>> round(area_ratio(2.0), 4)
1.6875
>>> round(normal_shock(2.0).mach2, 4)
0.5774
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._solvers import bisect
from .constants import KELVIN_OFFSET, R_AIR

K_AIR = 1.4


def _kelvin(temperature: float) -> float:
    t = temperature + KELVIN_OFFSET
    if t <= 0:
        raise ValueError("Absolute temperature must be positive.")
    return t


def speed_of_sound(temperature: float = 15.0, k: float = K_AIR, gas_constant: float = R_AIR) -> float:
    """Speed of sound c = sqrt(k R T) [m/s] at ``temperature`` [degC]."""
    return math.sqrt(k * gas_constant * _kelvin(temperature))


# ---------------------------------------------------------------------------- #
# Isentropic flow
# ---------------------------------------------------------------------------- #
def temperature_ratio(mach: float, k: float = K_AIR) -> float:
    """Static-to-stagnation temperature ratio T/T0."""
    return 1.0 / (1.0 + 0.5 * (k - 1.0) * mach**2)


def pressure_ratio(mach: float, k: float = K_AIR) -> float:
    """Static-to-stagnation pressure ratio p/p0 (isentropic)."""
    return temperature_ratio(mach, k) ** (k / (k - 1.0))


def density_ratio(mach: float, k: float = K_AIR) -> float:
    """Static-to-stagnation density ratio rho/rho0 (isentropic)."""
    return temperature_ratio(mach, k) ** (1.0 / (k - 1.0))


def area_ratio(mach: float, k: float = K_AIR) -> float:
    """Area ratio A/A* for isentropic flow at Mach number ``mach``."""
    if mach <= 0:
        raise ValueError("mach must be positive.")
    term = (2.0 / (k + 1.0)) * (1.0 + 0.5 * (k - 1.0) * mach**2)  # T*/T0 ratio term of the area-Mach relation
    return term ** ((k + 1.0) / (2.0 * (k - 1.0))) / mach


def critical_pressure_ratio(k: float = K_AIR) -> float:
    """p*/p0: back-pressure ratio below which a converging nozzle chokes (0.528 for air)."""
    return (2.0 / (k + 1.0)) ** (k / (k - 1.0))


def mach_from_area_ratio(ratio: float, supersonic: bool = False, k: float = K_AIR) -> float:
    """Mach number for a given A/A* (choose the subsonic or supersonic branch)."""
    if ratio < 1.0:
        raise ValueError("A/A* cannot be less than 1.")
    if ratio == 1.0:
        return 1.0
    f = lambda m: area_ratio(m, k) - ratio  # noqa: E731
    return bisect(f, 1.0, 100.0) if supersonic else bisect(f, 1e-8, 1.0)  # A/A* has one root on each branch


def mach_from_pressure_ratio(p_over_p0: float, k: float = K_AIR) -> float:
    """Mach number from the isentropic static/stagnation pressure ratio."""
    if not 0 < p_over_p0 <= 1:
        raise ValueError("p/p0 must be in (0, 1].")
    return math.sqrt(2.0 / (k - 1.0) * (p_over_p0 ** (-(k - 1.0) / k) - 1.0))


# ---------------------------------------------------------------------------- #
# Normal shock
# ---------------------------------------------------------------------------- #
@dataclass(frozen=True)
class NormalShock:
    """Property ratios across a stationary normal shock."""

    mach1: float
    mach2: float
    pressure_ratio: float
    """p2/p1"""
    temperature_ratio: float
    """T2/T1"""
    density_ratio: float
    """rho2/rho1"""
    stagnation_pressure_ratio: float
    """p02/p01 (< 1: the loss of stagnation pressure)"""


def normal_shock(mach1: float, k: float = K_AIR) -> NormalShock:
    """Rankine-Hugoniot relations for a normal shock with upstream Mach ``mach1`` > 1."""
    if mach1 < 1.0:
        raise ValueError("A normal shock requires supersonic upstream flow (mach1 >= 1).")
    m1s = mach1**2
    m2 = math.sqrt((1.0 + 0.5 * (k - 1.0) * m1s) / (k * m1s - 0.5 * (k - 1.0)))  # Rankine-Hugoniot relations
    p21 = 1.0 + 2.0 * k / (k + 1.0) * (m1s - 1.0)
    r21 = (k + 1.0) * m1s / ((k - 1.0) * m1s + 2.0)
    t21 = p21 / r21
    p0 = (pressure_ratio(mach1, k) / pressure_ratio(m2, k)) * p21  # p02/p01 = (p2/p1)(p1/p01)(p02/p2)
    return NormalShock(mach1, m2, p21, t21, r21, p0)


def pitot_mach_supersonic(p02_over_p1: float, k: float = K_AIR) -> float:
    """Upstream Mach number from a Pitot reading in supersonic flow (Rayleigh-Pitot formula).

    ``p02_over_p1`` is the Pitot (post-shock stagnation) pressure over the free-stream static pressure.
    """

    def ratio(m: float) -> float:
        s = normal_shock(m, k)
        return s.pressure_ratio / pressure_ratio(s.mach2, k)

    if p02_over_p1 < ratio(1.0):
        raise ValueError("Pressure ratio corresponds to subsonic flow; use mach_from_pressure_ratio.")
    return bisect(lambda m: ratio(m) - p02_over_p1, 1.0, 50.0)


# ---------------------------------------------------------------------------- #
# Nozzle mass flow
# ---------------------------------------------------------------------------- #
def choked_mass_flow(
    throat_area: float,
    stagnation_pressure: float,
    stagnation_temperature: float = 15.0,
    k: float = K_AIR,
    gas_constant: float = R_AIR,
) -> float:
    """Maximum (choked) mass flow through a throat [kg/s]."""
    t0 = _kelvin(stagnation_temperature)
    factor = math.sqrt(k / gas_constant) * (2.0 / (k + 1.0)) ** ((k + 1.0) / (2.0 * (k - 1.0)))
    return throat_area * stagnation_pressure / math.sqrt(t0) * factor


def nozzle_mass_flow(
    exit_area: float,
    stagnation_pressure: float,
    back_pressure: float,
    stagnation_temperature: float = 15.0,
    k: float = K_AIR,
    gas_constant: float = R_AIR,
) -> float:
    """Mass flow [kg/s] through a converging nozzle discharging to ``back_pressure``.

    Accounts for choking when back_pressure / p0 falls below the critical ratio.
    """
    if back_pressure > stagnation_pressure:
        raise ValueError("back_pressure cannot exceed the stagnation pressure.")
    ratio = back_pressure / stagnation_pressure
    if ratio <= critical_pressure_ratio(k):
        return choked_mass_flow(exit_area, stagnation_pressure, stagnation_temperature, k, gas_constant)
    mach = mach_from_pressure_ratio(ratio, k)
    t0 = _kelvin(stagnation_temperature)
    t = t0 * temperature_ratio(mach, k)
    rho = back_pressure / (gas_constant * t)
    return rho * exit_area * mach * math.sqrt(k * gas_constant * t)
