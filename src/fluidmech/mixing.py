"""Mixing in stirred tanks and the effect of mixing on chemical reactions.

Impeller power: P = Np rho N^3 D^5, with the power number Np a function of the
impeller Reynolds number Re = rho N D^2 / mu. Blend time, turbulence scales,
micromixing, scale-up rules, and ideal-reactor residence-time behaviour
(CSTR, PFR, tanks-in-series, laminar-flow reactor).

The impeller data in :data:`IMPELLERS` are representative values from published
power curves for standard baffled tanks; use manufacturer data for design.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

IMPELLERS = {
    # name: (turbulent power number, laminar constant Kp in Np = Kp / Re)
    "rushton_turbine": (5.0, 70.0),
    "pitched_blade_45": (1.3, 50.0),
    "hydrofoil": (0.3, 40.0),
    "marine_propeller": (0.35, 40.0),
}
"""Representative (Np_turbulent, Kp) for baffled tanks."""


def impeller_reynolds(speed_rps: float, diameter: float, density: float, mu: float) -> float:
    """Re = rho N D^2 / mu, N in revolutions per SECOND. Laminar < ~10, turbulent > ~1e4."""
    return density * speed_rps * diameter**2 / mu


def mixing_regime(reynolds: float) -> str:
    if reynolds < 10:
        return "laminar"
    if reynolds < 1e4:
        return "transitional"
    return "turbulent"


def power_number(reynolds: float, impeller: str = "rushton_turbine") -> float:
    """Approximate power number Np = Kp / Re + Np_turbulent (exact in the laminar and turbulent limits)."""
    np_t, kp = IMPELLERS[impeller]
    return kp / reynolds + np_t


def impeller_power(power_number_: float, density: float, speed_rps: float, diameter: float) -> float:
    """P = Np rho N^3 D^5 [W]."""
    return power_number_ * density * speed_rps**3 * diameter**5


def tip_speed(speed_rps: float, diameter: float) -> float:
    """Impeller tip speed pi N D [m/s]."""
    return math.pi * speed_rps * diameter


def blend_time_turbulent(
    power_number_: float, speed_rps: float, impeller_diameter: float, tank_diameter: float
) -> float:
    """95 % blend time, N theta_95 = 5.20 Np^(-1/3) (T/D)^2 (Grenville; turbulent, H = T) [s]."""
    # Grenville (1992)
    return 5.20 * power_number_ ** (-1.0 / 3.0) * (tank_diameter / impeller_diameter) ** 2 / speed_rps


def mean_dissipation_rate(power: float, density: float, volume: float) -> float:
    """Mean energy dissipation rate epsilon = P / (rho V) [W/kg]."""
    return power / (density * volume)


def engulfment_rate(dissipation_rate: float, nu: float) -> float:
    """Engulfment (micromixing) rate E = 0.058 (epsilon / nu)^(1/2) [1/s] (Baldyga & Bourne)."""
    return 0.058 * math.sqrt(dissipation_rate / nu)  # Baldyga & Bourne engulfment-model constant


def micromixing_time(dissipation_rate: float, nu: float) -> float:
    """Micromixing time t_E = 1/E ~ 17.2 (nu / epsilon)^(1/2) [s]."""
    return 1.0 / engulfment_rate(dissipation_rate, nu)


def damkohler(mixing_time: float, reaction_time: float) -> float:
    """Da = t_mix / t_reaction. Da << 1: kinetics control; Da >> 1: mixing controls selectivity."""
    return mixing_time / reaction_time


def scale_up_speed(
    speed_rps: float, diameter_small: float, diameter_large: float, rule: str = "power_per_volume"
) -> float:
    """Impeller speed on scale-up with geometric similarity.

    rule: 'power_per_volume' (N ~ D^-2/3, turbulent), 'tip_speed' (N ~ D^-1),
    'reynolds' (N ~ D^-2) or 'blend_time' (N constant).
    """
    ratio = diameter_small / diameter_large
    exponents = {"power_per_volume": 2.0 / 3.0, "tip_speed": 1.0, "reynolds": 2.0, "blend_time": 0.0}
    if rule not in exponents:
        raise ValueError(f"rule must be one of {sorted(exponents)}.")
    return speed_rps * ratio ** exponents[rule]


@dataclass(frozen=True)
class StirredTank:
    """A standard baffled tank with liquid height equal to its diameter."""

    tank_diameter: float
    impeller_diameter: float
    impeller: str = "rushton_turbine"

    @property
    def volume(self) -> float:
        return math.pi * self.tank_diameter**3 / 4.0

    def analyse(self, speed_rps: float, density: float, mu: float) -> dict[str, float]:
        """Reynolds number, power, P/V, blend time, Kolmogorov scale and micromixing time."""
        re = impeller_reynolds(speed_rps, self.impeller_diameter, density, mu)
        np_ = power_number(re, self.impeller)
        p = impeller_power(np_, density, speed_rps, self.impeller_diameter)
        eps = mean_dissipation_rate(p, density, self.volume)
        nu = mu / density
        out = {
            "reynolds": re,
            "power_number": np_,
            "power_W": p,
            "power_per_volume_W_m3": p / self.volume,
            "tip_speed_m_s": tip_speed(speed_rps, self.impeller_diameter),
            "dissipation_W_kg": eps,
            "kolmogorov_length_m": (nu**3 / eps) ** 0.25,
            "micromixing_time_s": micromixing_time(eps, nu),
        }
        if re > 1e4:
            out["blend_time_s"] = blend_time_turbulent(np_, speed_rps, self.impeller_diameter, self.tank_diameter)
        return out


# ---------------------------------------------------------------------------- #
# Residence time and ideal reactors (first-order reaction, rate constant k)
# ---------------------------------------------------------------------------- #
def cstr_conversion(damkohler_number: float) -> float:
    """First-order conversion in a CSTR, X = k tau / (1 + k tau)."""
    return damkohler_number / (1.0 + damkohler_number)


def pfr_conversion(damkohler_number: float) -> float:
    """First-order conversion in a plug-flow reactor, X = 1 - exp(-k tau)."""
    return 1.0 - math.exp(-damkohler_number)


def tanks_in_series_conversion(damkohler_number: float, n_tanks: int) -> float:
    """First-order conversion in N equal CSTRs in series, X = 1 - (1 + k tau / N)^-N."""
    return 1.0 - (1.0 + damkohler_number / n_tanks) ** (-n_tanks)


def laminar_flow_reactor_conversion(damkohler_number: float, steps: int = 4000) -> float:
    """First-order conversion in a laminar (Hagen-Poiseuille) tubular reactor without diffusion.

    Segregated flow with E(t) = tau^2 / (2 t^3) for t >= tau/2, which follows from the
    parabolic velocity profile. The integral is evaluated numerically in s = tau / (2t).
    """
    x = damkohler_number
    # 1 - X = integral_0^1 2 s exp(-x / (2 s)) ds  after substituting s = tau / (2 t)
    total = 0.0
    for i in range(steps):  # midpoint rule for the integral of 2 s exp(-x / 2s) ds over 0 < s < 1
        s = (i + 0.5) / steps
        total += 2.0 * s * math.exp(-x / (2.0 * s))
    return 1.0 - total / steps


def cstr_rtd(t: float, tau: float) -> float:
    """Residence-time distribution of a CSTR, E(t) = exp(-t/tau) / tau."""
    return math.exp(-t / tau) / tau


def tanks_in_series_rtd(t: float, tau: float, n_tanks: int) -> float:
    """RTD of N equal tanks in series with total mean residence time tau."""
    n = n_tanks
    return (n / tau) ** n * t ** (n - 1) * math.exp(-n * t / tau) / math.factorial(n - 1)


def laminar_rtd(t: float, tau: float) -> float:
    """RTD of laminar pipe flow, E(t) = tau^2 / (2 t^3) for t >= tau/2."""
    return 0.0 if t < tau / 2.0 else tau**2 / (2.0 * t**3)
