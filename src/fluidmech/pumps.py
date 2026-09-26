"""Centrifugal pumps: characteristic curves, affinity laws, operating points and NPSH.

A pump curve is represented by a quadratic H(Q) = h0 + h1 Q + h2 Q^2, which is
how manufacturers' curves are usually fitted. An optional efficiency curve
eta(Q) = e0 + e1 Q + e2 Q^2 enables power calculations.

Examples
--------
>>> pump = PumpCurve.from_points([0.0, 0.05, 0.10], [40.0, 36.25, 25.0])
>>> round(pump.head(0.08), 2)
30.4
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from ._solvers import bisect, polyfit
from .constants import P_ATM, G
from .properties import Fluid


@dataclass(frozen=True)
class PumpCurve:
    """Quadratic pump characteristic H = h0 + h1 Q + h2 Q^2 (SI units)."""

    h0: float
    """Shut-off head [m]."""
    h1: float = 0.0
    h2: float = 0.0
    efficiency_coeffs: tuple[float, float, float] | None = None
    """Optional (e0, e1, e2) so that eta = e0 + e1 Q + e2 Q^2 (as a fraction)."""

    # ---- construction ------------------------------------------------------ #
    @classmethod
    def from_points(
        cls,
        flow_rates: Sequence[float],
        heads: Sequence[float],
        efficiencies: Sequence[float] | None = None,
    ) -> PumpCurve:
        """Fit a pump curve (and optionally an efficiency curve) to catalogue points.

        ``efficiencies`` are fractions (0.75, not 75).
        """
        h0, h1, h2 = polyfit(list(flow_rates), list(heads), 2)
        eff = None
        if efficiencies is not None:
            if len(efficiencies) != len(flow_rates):
                raise ValueError("efficiencies must match flow_rates in length.")
            e0, e1, e2 = polyfit(list(flow_rates), list(efficiencies), 2)
            eff = (e0, e1, e2)
        return cls(h0, h1, h2, eff)

    # ---- evaluation -------------------------------------------------------- #
    def head(self, flow_rate: float) -> float:
        """Pump head [m] at ``flow_rate`` [m^3/s]."""
        return self.h0 + self.h1 * flow_rate + self.h2 * flow_rate**2

    def head_slope(self, flow_rate: float) -> float:
        """dH/dQ [s/m^2]."""
        return self.h1 + 2.0 * self.h2 * flow_rate

    def efficiency(self, flow_rate: float) -> float:
        """Pump efficiency (fraction) at ``flow_rate``."""
        if self.efficiency_coeffs is None:
            raise ValueError("This pump curve has no efficiency data.")
        e0, e1, e2 = self.efficiency_coeffs
        return e0 + e1 * flow_rate + e2 * flow_rate**2

    def best_efficiency_point(self) -> float:
        """Flow rate [m^3/s] at the best efficiency point (BEP)."""
        if self.efficiency_coeffs is None:
            raise ValueError("This pump curve has no efficiency data.")
        _, e1, e2 = self.efficiency_coeffs
        if e2 >= 0:
            raise ValueError("Efficiency curve has no maximum.")
        return -e1 / (2.0 * e2)

    def hydraulic_power(self, flow_rate: float, density: float = 1000.0) -> float:
        """Power delivered to the fluid, rho g Q H [W]."""
        return density * G * flow_rate * self.head(flow_rate)

    def shaft_power(self, flow_rate: float, density: float = 1000.0) -> float:
        """Brake (shaft) power rho g Q H / eta [W]."""
        return self.hydraulic_power(flow_rate, density) / self.efficiency(flow_rate)

    def max_flow(self) -> float:
        """Run-out flow rate where the head falls to zero [m^3/s]."""
        if self.h0 <= 0:
            raise ValueError("Shut-off head must be positive.")
        upper = 1.0  # search upwards for a flow where the head has fallen below zero
        while self.head(upper) > 0:
            upper *= 2.0
            if upper > 1e6:
                raise ValueError("Pump curve does not fall to zero head.")
        return bisect(self.head, 0.0, upper)

    # ---- transformations --------------------------------------------------- #
    def scaled(self, speed_ratio: float = 1.0, diameter_ratio: float = 1.0) -> PumpCurve:
        """New curve from the affinity laws.

        Speed change N2/N1: Q ~ N, H ~ N^2. Impeller trim D2/D1 (same pump casing):
        Q ~ D, H ~ D^2 (approximate). Efficiency is assumed unchanged at
        corresponding points.
        """
        if speed_ratio <= 0 or diameter_ratio <= 0:
            raise ValueError("ratios must be positive.")
        rq = speed_ratio * diameter_ratio  # flow scale; head scales with its square
        rh = rq**2
        eff = None
        if self.efficiency_coeffs is not None:
            e0, e1, e2 = self.efficiency_coeffs
            eff = (e0, e1 / rq, e2 / rq**2)
        return PumpCurve(rh * self.h0, rh * self.h1 / rq, rh * self.h2 / rq**2, eff)

    def in_series(self, n: int = 2) -> PumpCurve:
        """Equivalent curve of ``n`` identical pumps in series (heads add)."""
        return PumpCurve(n * self.h0, n * self.h1, n * self.h2, self.efficiency_coeffs)

    def in_parallel(self, n: int = 2) -> PumpCurve:
        """Equivalent curve of ``n`` identical pumps in parallel (flows add)."""
        eff = None
        if self.efficiency_coeffs is not None:
            e0, e1, e2 = self.efficiency_coeffs
            eff = (e0, e1 / n, e2 / n**2)
        return PumpCurve(self.h0, self.h1 / n, self.h2 / n**2, eff)


@dataclass(frozen=True)
class OperatingPoint:
    """Intersection of a pump curve and a system curve."""

    flow_rate: float
    head: float
    efficiency: float | None
    shaft_power: float | None


def system_curve(
    static_head: float,
    diameter: float,
    length: float,
    fluid: Fluid,
    roughness: float = 0.0,
    k_total: float = 0.0,
) -> Callable[[float], float]:
    """Return H_system(Q) = static head + pipe losses (Darcy-Weisbach) as a function."""
    from .pipe_flow import head_loss

    def h_sys(q: float) -> float:
        if q <= 0:
            return static_head
        return static_head + head_loss(q, diameter, length, fluid, roughness, k_total).total_head_loss

    return h_sys


def operating_point(pump: PumpCurve, system: Callable[[float], float], density: float = 1000.0) -> OperatingPoint:
    """Find where the pump curve meets the system curve."""
    if pump.head(0.0) <= system(0.0):
        raise ValueError("Pump shut-off head is below the static head: the pump cannot deliver flow.")
    q_max = pump.max_flow()
    q = bisect(lambda x: pump.head(x) - system(x), 0.0, q_max)  # pump head falls, system head rises: one crossing
    h = pump.head(q)
    if pump.efficiency_coeffs is None:
        return OperatingPoint(q, h, None, None)
    eta = pump.efficiency(q)
    return OperatingPoint(q, h, eta, density * G * q * h / eta if eta > 0 else math.inf)


def npsh_available(
    suction_static_head: float,
    suction_head_loss: float,
    fluid_temperature: float = 20.0,
    surface_pressure: float = P_ATM,
    density: float | None = None,
    vapor_pressure: float | None = None,
) -> float:
    """Net positive suction head available [m].

    NPSHa = (p_surface - p_vapour)/(rho g) + z_s - h_L,s

    ``suction_static_head`` is the height of the free surface ABOVE the pump
    inlet (negative for a suction lift). Water properties are used by default.
    """
    from .properties import water_density, water_vapor_pressure

    rho = density if density is not None else water_density(fluid_temperature)
    pv = vapor_pressure if vapor_pressure is not None else water_vapor_pressure(fluid_temperature)
    return (surface_pressure - pv) / (rho * G) + suction_static_head - suction_head_loss


def specific_speed(speed_rpm: float, flow_rate: float, head: float) -> float:
    """Dimensionless specific speed Omega_s = omega Q^0.5 / (g H)^0.75.

    Roughly: < 1 radial (centrifugal), 1-4 mixed flow, > 4 axial.
    """
    omega = speed_rpm * 2.0 * math.pi / 60.0  # rpm -> rad/s
    return omega * math.sqrt(flow_rate) / (G * head) ** 0.75


def pump_type(speed_rpm: float, flow_rate: float, head: float) -> str:
    """Suggest an impeller type from the specific speed."""
    ns = specific_speed(speed_rpm, flow_rate, head)
    if ns < 1.0:
        return "radial (centrifugal)"
    if ns < 4.0:
        return "mixed flow"
    return "axial flow"
