"""Rheology: viscosity models for Newtonian and non-Newtonian fluids.

Generalised Newtonian models give the shear stress tau as a function of the
shear rate gamma_dot (both positive, simple shear):

=====================  =========================================================
Newtonian              tau = mu * gamma_dot
Power law (Ostwald)    tau = K * gamma_dot^n     (n < 1 shear-thinning, n > 1 thickening)
Bingham plastic        tau = tau_y + mu_p * gamma_dot          (for tau > tau_y)
Herschel-Bulkley       tau = tau_y + K * gamma_dot^n           (for tau > tau_y)
Carreau                mu = mu_inf + (mu_0 - mu_inf) [1 + (lam gamma_dot)^2]^((n-1)/2)
=====================  =========================================================

The module also fits these models to rheometer data and describes the
temperature dependence of liquid viscosity with the Andrade (Arrhenius) equation.

Examples
--------
>>> fluid = fit_power_law([1.0, 10.0, 100.0], [2.0, 6.32, 20.0])
>>> round(fluid.n, 3), round(fluid.K, 3)
(0.5, 2.0)
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from .constants import KELVIN_OFFSET


def _check_rate(shear_rate: float) -> None:
    if shear_rate < 0:
        raise ValueError("shear_rate must be non-negative.")


@dataclass(frozen=True)
class Newtonian:
    """Newtonian fluid, tau = mu gamma_dot."""

    mu: float

    def stress(self, shear_rate: float) -> float:
        _check_rate(shear_rate)
        return self.mu * shear_rate

    def apparent_viscosity(self, shear_rate: float) -> float:
        return self.mu


@dataclass(frozen=True)
class PowerLaw:
    """Ostwald-de Waele power-law fluid, tau = K gamma_dot^n.

    K is the consistency index [Pa s^n] and n the flow behaviour index.
    """

    K: float
    n: float

    def stress(self, shear_rate: float) -> float:
        _check_rate(shear_rate)
        return self.K * shear_rate**self.n

    def apparent_viscosity(self, shear_rate: float) -> float:
        """mu_app = tau / gamma_dot = K gamma_dot^(n-1) [Pa s]."""
        if shear_rate <= 0:
            raise ValueError("Apparent viscosity requires a positive shear rate.")
        return self.K * shear_rate ** (self.n - 1.0)

    @property
    def behaviour(self) -> str:
        if math.isclose(self.n, 1.0, rel_tol=1e-3):
            return "Newtonian"
        return "shear-thinning (pseudoplastic)" if self.n < 1 else "shear-thickening (dilatant)"


@dataclass(frozen=True)
class Bingham:
    """Bingham plastic: no flow below the yield stress tau_y, then tau = tau_y + mu_p gamma_dot."""

    tau_y: float
    mu_p: float

    def stress(self, shear_rate: float) -> float:
        _check_rate(shear_rate)
        return self.tau_y + self.mu_p * shear_rate

    def apparent_viscosity(self, shear_rate: float) -> float:
        if shear_rate <= 0:
            raise ValueError("Apparent viscosity requires a positive shear rate.")
        return self.tau_y / shear_rate + self.mu_p


@dataclass(frozen=True)
class HerschelBulkley:
    """Herschel-Bulkley fluid: tau = tau_y + K gamma_dot^n (yield stress plus power law)."""

    tau_y: float
    K: float
    n: float

    def stress(self, shear_rate: float) -> float:
        _check_rate(shear_rate)
        return self.tau_y + self.K * shear_rate**self.n

    def apparent_viscosity(self, shear_rate: float) -> float:
        if shear_rate <= 0:
            raise ValueError("Apparent viscosity requires a positive shear rate.")
        return self.stress(shear_rate) / shear_rate


@dataclass(frozen=True)
class Carreau:
    """Carreau model with zero-shear (mu_0) and infinite-shear (mu_inf) plateaus."""

    mu_0: float
    mu_inf: float
    lam: float
    """Time constant [s]; 1/lam is roughly where shear-thinning begins."""
    n: float

    def apparent_viscosity(self, shear_rate: float) -> float:
        _check_rate(shear_rate)
        return self.mu_inf + (self.mu_0 - self.mu_inf) * (1.0 + (self.lam * shear_rate) ** 2) ** ((self.n - 1.0) / 2.0)

    def stress(self, shear_rate: float) -> float:
        return self.apparent_viscosity(shear_rate) * shear_rate


# ---------------------------------------------------------------------------- #
# Fitting rheometer data
# ---------------------------------------------------------------------------- #
def _linear_fit(x: Sequence[float], y: Sequence[float]) -> tuple[float, float, float]:
    """Least-squares line y = a + b x. Returns (a, b, R^2)."""
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Need at least two (x, y) pairs of equal length.")
    xm, ym = sum(x) / n, sum(y) / n
    sxx = sum((xi - xm) ** 2 for xi in x)
    if sxx == 0:
        raise ValueError("x values must not all be equal.")
    b = sum((xi - xm) * (yi - ym) for xi, yi in zip(x, y)) / sxx
    a = ym - b * xm
    ss_tot = sum((yi - ym) ** 2 for yi in y)
    ss_res = sum((yi - a - b * xi) ** 2 for xi, yi in zip(x, y))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0  # coefficient of determination
    return a, b, r2


def fit_newtonian(shear_rates: Sequence[float], stresses: Sequence[float]) -> Newtonian:
    """Best-fit Newtonian viscosity (line through the origin)."""
    num = sum(g * t for g, t in zip(shear_rates, stresses))
    den = sum(g * g for g in shear_rates)
    if den == 0:
        raise ValueError("Need non-zero shear rates.")
    return Newtonian(num / den)


def fit_power_law(shear_rates: Sequence[float], stresses: Sequence[float]) -> PowerLaw:
    """Fit tau = K gamma_dot^n by linear regression of log(tau) on log(gamma_dot)."""
    if any(g <= 0 for g in shear_rates) or any(t <= 0 for t in stresses):
        raise ValueError("Power-law fitting needs positive shear rates and stresses.")
    a, b, _ = _linear_fit([math.log(g) for g in shear_rates], [math.log(t) for t in stresses])
    return PowerLaw(math.exp(a), b)


def fit_bingham(shear_rates: Sequence[float], stresses: Sequence[float]) -> Bingham:
    """Fit tau = tau_y + mu_p gamma_dot by linear regression."""
    a, b, _ = _linear_fit(list(shear_rates), list(stresses))
    return Bingham(max(a, 0.0), b)


def fit_herschel_bulkley(shear_rates: Sequence[float], stresses: Sequence[float], steps: int = 400) -> HerschelBulkley:
    """Fit tau = tau_y + K gamma_dot^n.

    The yield stress is found by a one-dimensional search between zero and the
    smallest measured stress; for each trial tau_y, K and n follow from a
    log-log regression. The combination with the smallest squared error wins.
    """
    tau_min = min(stresses)
    best = None
    for i in range(steps):
        tau_y = tau_min * i / steps  # trial yield stress between 0 and the smallest measured stress
        try:
            pl = fit_power_law(shear_rates, [t - tau_y for t in stresses])  # remaining stress must follow a power law
        except ValueError:
            continue
        err = sum((tau_y + pl.stress(g) - t) ** 2 for g, t in zip(shear_rates, stresses))
        if best is None or err < best[0]:
            best = (err, HerschelBulkley(tau_y, pl.K, pl.n))
    if best is None:
        raise ValueError("Could not fit a Herschel-Bulkley model.")
    return best[1]


def r_squared(model, shear_rates: Sequence[float], stresses: Sequence[float]) -> float:
    """Coefficient of determination of a fitted model on the data."""
    mean = sum(stresses) / len(stresses)
    ss_tot = sum((t - mean) ** 2 for t in stresses)
    ss_res = sum((model.stress(g) - t) ** 2 for g, t in zip(shear_rates, stresses))
    return 1.0 - ss_res / ss_tot


# ---------------------------------------------------------------------------- #
# Temperature dependence of liquid viscosity
# ---------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Andrade:
    """Andrade equation mu = A exp(B / T), T in kelvin (temperatures in degC at the interface)."""

    A: float
    B: float

    def viscosity(self, temperature: float) -> float:
        return self.A * math.exp(self.B / (temperature + KELVIN_OFFSET))

    @property
    def activation_energy(self) -> float:
        """Apparent activation energy for viscous flow, E = B R [J/mol]."""
        return self.B * 8.314462618

    @classmethod
    def from_two_points(cls, t1: float, mu1: float, t2: float, mu2: float) -> Andrade:
        """Fit A and B through two (temperature [degC], viscosity) measurements."""
        k1, k2 = t1 + KELVIN_OFFSET, t2 + KELVIN_OFFSET
        b = math.log(mu1 / mu2) / (1.0 / k1 - 1.0 / k2)
        return cls(mu1 / math.exp(b / k1), b)

    @classmethod
    def fit(cls, temperatures: Sequence[float], viscosities: Sequence[float]) -> Andrade:
        """Least-squares fit of ln(mu) against 1/T."""
        a, b, _ = _linear_fit([1.0 / (t + KELVIN_OFFSET) for t in temperatures], [math.log(m) for m in viscosities])
        return cls(math.exp(a), b)
