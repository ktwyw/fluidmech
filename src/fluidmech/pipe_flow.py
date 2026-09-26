"""Steady, incompressible flow in circular pipes.

Covers the three classic pipe-flow problem types:

* Type 1 - find the head loss for a given flow rate and diameter
  (:func:`head_loss`).
* Type 2 - find the flow rate for a given head loss and diameter
  (:func:`flow_rate_for_head_loss`).
* Type 3 - find the diameter for a given flow rate and head loss
  (:func:`diameter_for_head_loss`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._solvers import positive_root
from .constants import G
from .properties import Fluid

LAMINAR_LIMIT = 2300.0

ROUGHNESS = {
    "drawn_tubing": 0.0015e-3,
    "pvc": 0.0015e-3,
    "commercial_steel": 0.045e-3,
    "wrought_iron": 0.045e-3,
    "galvanized_iron": 0.15e-3,
    "cast_iron": 0.26e-3,
    "concrete": 1.0e-3,
    "riveted_steel": 3.0e-3,
}
"""Typical absolute roughness values epsilon [m] for new pipes."""

MINOR_LOSS_K = {
    "sharp_entrance": 0.5,
    "rounded_entrance": 0.03,
    "exit": 1.0,
    "elbow_90_regular": 0.3,
    "elbow_90_long_radius": 0.2,
    "elbow_45": 0.2,
    "tee_branch": 1.0,
    "tee_line": 0.2,
    "gate_valve_open": 0.15,
    "globe_valve_open": 10.0,
    "ball_valve_open": 0.05,
}
"""Representative loss coefficients K for common fittings (flanged, turbulent flow)."""


# --------------------------------------------------------------------------- #
# Basic kinematics
# --------------------------------------------------------------------------- #
def area(diameter: float) -> float:
    """Cross-sectional area of a circular pipe [m^2]."""
    if diameter <= 0:
        raise ValueError("diameter must be positive.")
    return math.pi * diameter**2 / 4.0


def mean_velocity(flow_rate: float, diameter: float) -> float:
    """Mean velocity V = Q / A [m/s]."""
    return flow_rate / area(diameter)


# --------------------------------------------------------------------------- #
# Friction factor correlations
# --------------------------------------------------------------------------- #
def _check_turbulent_inputs(reynolds: float, relative_roughness: float) -> None:
    if reynolds <= 0:
        raise ValueError("reynolds must be positive.")
    if relative_roughness < 0:
        raise ValueError("relative_roughness must be non-negative.")


def swamee_jain(reynolds: float, relative_roughness: float = 0.0) -> float:
    """Explicit Swamee-Jain approximation to Colebrook (turbulent flow)."""
    _check_turbulent_inputs(reynolds, relative_roughness)
    return 0.25 / math.log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2


def haaland(reynolds: float, relative_roughness: float = 0.0) -> float:
    """Explicit Haaland approximation to Colebrook (turbulent flow)."""
    _check_turbulent_inputs(reynolds, relative_roughness)
    inv_sqrt_f = -1.8 * math.log10((relative_roughness / 3.7) ** 1.11 + 6.9 / reynolds)
    return 1.0 / inv_sqrt_f**2


def colebrook(reynolds: float, relative_roughness: float = 0.0, tol: float = 1e-12, maxiter: int = 100) -> float:
    """Darcy friction factor from the implicit Colebrook-White equation.

    1/sqrt(f) = -2 log10( (eps/D)/3.7 + 2.51 / (Re sqrt(f)) )

    Solved by fixed-point iteration on x = 1/sqrt(f), seeded with Swamee-Jain.
    """
    _check_turbulent_inputs(reynolds, relative_roughness)
    # x = 1/sqrt(f); explicit estimate as the starting guess
    x = 1.0 / math.sqrt(swamee_jain(reynolds, relative_roughness))
    for _ in range(maxiter):
        # Colebrook rearranged as x = g(x): fixed-point iteration
        x_new = -2.0 * math.log10(relative_roughness / 3.7 + 2.51 * x / reynolds)
        if abs(x_new - x) < tol * abs(x_new):
            return 1.0 / x_new**2
        x = x_new
    raise RuntimeError("Colebrook iteration did not converge.")


_METHODS = {"colebrook": colebrook, "swamee_jain": swamee_jain, "haaland": haaland}


def friction_factor(
    reynolds: float,
    relative_roughness: float = 0.0,
    method: str = "colebrook",
    laminar_limit: float = LAMINAR_LIMIT,
) -> float:
    """Darcy friction factor for laminar or turbulent pipe flow.

    For Re < ``laminar_limit`` the exact laminar result f = 64/Re is used;
    otherwise the chosen turbulent correlation ('colebrook', 'swamee_jain' or
    'haaland'). Results in the transitional range (2300 < Re < 4000) are uncertain.
    """
    if reynolds <= 0:
        raise ValueError("reynolds must be positive.")
    if reynolds < laminar_limit:  # laminar: exact result, independent of roughness
        return 64.0 / reynolds
    try:
        func = _METHODS[method]
    except KeyError:
        raise ValueError(f"Unknown method {method!r}; choose from {sorted(_METHODS)}.") from None
    return func(reynolds, relative_roughness)


# --------------------------------------------------------------------------- #
# Head losses
# --------------------------------------------------------------------------- #
def darcy_weisbach(friction: float, length: float, diameter: float, velocity: float, g: float = G) -> float:
    """Major head loss h_f = f (L/D) V^2/(2g) [m]."""
    return friction * length / diameter * velocity**2 / (2.0 * g)


def minor_loss(k_total: float, velocity: float, g: float = G) -> float:
    """Minor head loss h_m = K V^2/(2g) [m]."""
    return k_total * velocity**2 / (2.0 * g)


@dataclass(frozen=True)
class PipeFlowResult:
    """Summary of a pipe-flow head-loss calculation."""

    flow_rate: float
    diameter: float
    velocity: float
    reynolds: float
    friction_factor: float
    major_head_loss: float
    minor_head_loss: float
    density: float

    @property
    def total_head_loss(self) -> float:
        """Major + minor head loss [m]."""
        return self.major_head_loss + self.minor_head_loss

    @property
    def pressure_drop(self) -> float:
        """Pressure drop for a horizontal pipe, rho g h_L [Pa]."""
        return self.density * G * self.total_head_loss

    @property
    def regime(self) -> str:
        """'laminar', 'transitional' or 'turbulent'."""
        from .dimensionless import flow_regime

        return flow_regime(self.reynolds)

    def pumping_power(self, efficiency: float = 1.0) -> float:
        """Power required to overcome the losses, rho g Q h_L / eta [W]."""
        return self.pressure_drop * self.flow_rate / efficiency


def head_loss(
    flow_rate: float,
    diameter: float,
    length: float,
    fluid: Fluid,
    roughness: float = 0.0,
    k_total: float = 0.0,
    method: str = "colebrook",
) -> PipeFlowResult:
    """Type 1 problem: head loss for a known flow rate and pipe.

    Parameters
    ----------
    flow_rate : Q [m^3/s].
    diameter : Inside diameter D [m].
    length : Pipe length L [m].
    fluid : :class:`~fluidmech.properties.Fluid` instance.
    roughness : Absolute roughness epsilon [m] (see :data:`ROUGHNESS`).
    k_total : Sum of minor-loss coefficients (see :data:`MINOR_LOSS_K`).
    """
    if flow_rate <= 0 or length <= 0:
        raise ValueError("flow_rate and length must be positive.")
    v = mean_velocity(flow_rate, diameter)
    re = v * diameter / fluid.kinematic_viscosity
    f = friction_factor(re, roughness / diameter, method)
    return PipeFlowResult(
        flow_rate=flow_rate,
        diameter=diameter,
        velocity=v,
        reynolds=re,
        friction_factor=f,
        major_head_loss=darcy_weisbach(f, length, diameter, v),
        minor_head_loss=minor_loss(k_total, v),
        density=fluid.density,
    )


def flow_rate_for_head_loss(
    head_loss_available: float,
    diameter: float,
    length: float,
    fluid: Fluid,
    roughness: float = 0.0,
    k_total: float = 0.0,
    method: str = "colebrook",
) -> float:
    """Type 2 problem: flow rate [m^3/s] that produces a given total head loss."""
    if head_loss_available <= 0:
        raise ValueError("head_loss_available must be positive.")

    def residual(q: float) -> float:
        r = head_loss(q, diameter, length, fluid, roughness, k_total, method)
        return r.total_head_loss - head_loss_available

    return positive_root(residual, guess=area(diameter) * 1.0)  # start from Q giving V = 1 m/s


def diameter_for_head_loss(
    flow_rate: float,
    head_loss_allowed: float,
    length: float,
    fluid: Fluid,
    roughness: float = 0.0,
    k_total: float = 0.0,
    method: str = "colebrook",
) -> float:
    """Type 3 problem: diameter [m] giving the allowed total head loss."""
    if head_loss_allowed <= 0:
        raise ValueError("head_loss_allowed must be positive.")

    def residual(d: float) -> float:
        r = head_loss(flow_rate, d, length, fluid, roughness, k_total, method)
        return r.total_head_loss - head_loss_allowed

    guess = math.sqrt(4.0 * flow_rate / math.pi)  # diameter for V = 1 m/s
    return positive_root(residual, guess=guess)


def hydraulic_diameter(area_: float, wetted_perimeter: float) -> float:
    """Hydraulic diameter D_h = 4 A / P for non-circular ducts [m]."""
    if area_ <= 0 or wetted_perimeter <= 0:
        raise ValueError("area and wetted_perimeter must be positive.")
    return 4.0 * area_ / wetted_perimeter
