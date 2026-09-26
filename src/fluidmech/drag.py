"""External flow: drag coefficients, boundary layers and terminal velocity.

Correlations
------------
* Sphere: Brown & Lawler (2003), Cd = 24/Re (1 + 0.150 Re^0.681) + 0.407 / (1 + 8710/Re),
  for Re < 2e5 (within a few percent of the standard drag curve).
* Cylinder (cross-flow): White, Cd = 1 + 10 Re^(-2/3), for 1 < Re < 2e5.
* Flat plate skin friction: Blasius (laminar), 1/7-power law (turbulent),
  Prandtl-Schlichting (high Re) and the mixed laminar-turbulent formula.
"""

from __future__ import annotations

import math

from ._solvers import positive_root
from .constants import G
from .properties import Fluid

TRANSITION_RE = 5e5
"""Typical transition Reynolds number for a flat-plate boundary layer."""

TYPICAL_CD = {
    "sphere_subcritical": 0.47,
    "sphere_supercritical": 0.2,
    "cylinder_subcritical": 1.2,
    "flat_plate_normal_3d": 1.17,
    "flat_plate_normal_2d": 2.0,
    "cube": 1.05,
    "hemisphere_open_to_flow": 1.42,
    "hemisphere_facing_away": 0.38,
    "streamlined_body": 0.04,
    "modern_car": 0.30,
    "bus_or_truck": 0.65,
    "upright_cyclist": 0.9,
}
"""Representative drag coefficients based on frontal area (high Re)."""


def drag_force(drag_coefficient: float, density: float, velocity: float, area: float) -> float:
    """Drag force F = Cd (1/2) rho V^2 A [N]."""
    return drag_coefficient * 0.5 * density * velocity**2 * area


def sphere_drag_coefficient(reynolds: float) -> float:
    """Drag coefficient of a smooth sphere (Brown & Lawler 2003, Re < 2e5)."""
    if reynolds <= 0:
        raise ValueError("reynolds must be positive.")
    re = reynolds
    return 24.0 / re * (1.0 + 0.150 * re**0.681) + 0.407 / (1.0 + 8710.0 / re)  # Brown & Lawler (2003)


def cylinder_drag_coefficient(reynolds: float) -> float:
    """Drag coefficient of a long circular cylinder in cross-flow (1 < Re < 2e5)."""
    if reynolds <= 0:
        raise ValueError("reynolds must be positive.")
    return 1.0 + 10.0 * reynolds ** (-2.0 / 3.0)  # White's cylinder correlation


def flat_plate_friction_coefficient(reynolds_length: float, method: str = "auto") -> float:
    """Average skin-friction coefficient C_f of a flat plate (one side).

    method: 'laminar' (Blasius 1.328/sqrt(Re)), 'turbulent' (0.074/Re^0.2),
    'schlichting' (0.455/(log10 Re)^2.58), 'mixed' (Schlichting minus 1700/Re,
    laminar leading edge), or 'auto' (laminar below 5e5, mixed above).
    """
    re = reynolds_length
    if re <= 0:
        raise ValueError("reynolds_length must be positive.")
    if method == "auto":
        method = "laminar" if re < TRANSITION_RE else "mixed"
    if method == "laminar":
        return 1.328 / math.sqrt(re)
    if method == "turbulent":
        return 0.074 / re**0.2
    if method == "schlichting":
        return 0.455 / math.log10(re) ** 2.58
    if method == "mixed":
        return 0.455 / math.log10(re) ** 2.58 - 1700.0 / re
    raise ValueError(f"Unknown method {method!r}.")


def boundary_layer_thickness(x: float, velocity: float, kinematic_viscosity: float) -> float:
    """99 % boundary-layer thickness at distance ``x`` from the leading edge [m].

    Laminar (Blasius) 4.91 x / sqrt(Re_x) below Re_x = 5e5, turbulent 0.37 x / Re_x^0.2 above.
    """
    if x <= 0 or velocity <= 0:
        raise ValueError("x and velocity must be positive.")
    re_x = velocity * x / kinematic_viscosity
    if re_x < TRANSITION_RE:
        return 4.91 * x / math.sqrt(re_x)
    return 0.37 * x / re_x**0.2


def skin_friction_drag(length: float, wetted_area: float, velocity: float, fluid: Fluid, method: str = "auto") -> float:
    """Friction drag on a flat surface of given length and wetted area [N]."""
    re = velocity * length / fluid.kinematic_viscosity
    cf = flat_plate_friction_coefficient(re, method)
    return drag_force(cf, fluid.density, velocity, wetted_area)


def terminal_velocity(diameter: float, particle_density: float, fluid: Fluid, g: float = G) -> float:
    """Terminal settling (or rise) velocity of a smooth sphere [m/s].

    Balances net weight against drag using :func:`sphere_drag_coefficient`.
    Returns a negative value for a sphere lighter than the fluid (it rises).
    """
    if diameter <= 0:
        raise ValueError("diameter must be positive.")
    delta = particle_density - fluid.density
    if delta == 0:
        return 0.0
    volume = math.pi * diameter**3 / 6.0
    frontal = math.pi * diameter**2 / 4.0
    net_weight = abs(delta) * g * volume

    def residual(u: float) -> float:
        re = u * diameter / fluid.kinematic_viscosity
        return drag_force(sphere_drag_coefficient(re), fluid.density, u, frontal) - net_weight

    u = positive_root(residual, guess=0.01)  # drag rises monotonically with U, so the root is unique
    return math.copysign(u, delta)


def stokes_velocity(diameter: float, particle_density: float, fluid: Fluid, g: float = G) -> float:
    """Stokes' law settling velocity (valid for Re < ~1) [m/s]."""
    return (particle_density - fluid.density) * g * diameter**2 / (18.0 * fluid.dynamic_viscosity)


# ---------------------------------------------------------------------------- #
# Drops, bubbles and suspensions
# ---------------------------------------------------------------------------- #
def hadamard_rybczynski_velocity(
    diameter: float, drop_density: float, drop_viscosity: float, fluid: Fluid, g: float = G
) -> float:
    """Creeping-flow terminal velocity of a fluid sphere (drop or bubble) with a mobile interface.

    U = U_Stokes * 3 (1 + k) / (2 + 3k), k = mu_drop / mu_fluid. For a clean gas bubble
    (k -> 0) this is 1.5 times the rigid-sphere Stokes velocity. Negative values rise.
    """
    k = drop_viscosity / fluid.dynamic_viscosity
    return stokes_velocity(diameter, drop_density, fluid, g) * 3.0 * (1.0 + k) / (2.0 + 3.0 * k)


def mendelson_bubble_velocity(diameter: float, surface_tension: float, fluid: Fluid, g: float = G) -> float:
    """Rise velocity of larger bubbles (d > ~1.5 mm) from Mendelson's wave analogy.

    U = sqrt(2 sigma / (rho d) + g d / 2) [m/s]; the minimum is about 0.23 m/s for air in water.
    """
    return math.sqrt(2.0 * surface_tension / (fluid.density * diameter) + g * diameter / 2.0)


def eotvos_number(diameter: float, density_difference: float, surface_tension: float, g: float = G) -> float:
    """Eotvos (Bond) number Eo = g d_rho d^2 / sigma: gravity versus surface tension (shape of drops/bubbles)."""
    return g * density_difference * diameter**2 / surface_tension


def morton_number(fluid: Fluid, density_difference: float, surface_tension: float, g: float = G) -> float:
    """Morton number Mo = g mu^4 d_rho / (rho^2 sigma^3): a property group of the fluid pair."""
    return g * fluid.dynamic_viscosity**4 * density_difference / (fluid.density**2 * surface_tension**3)


def richardson_zaki_exponent(terminal_reynolds: float) -> float:
    """Exponent n in U = U_t eps^n (Rowe 1987): 4.7 in creeping flow, 2.35 at high Re."""
    a = terminal_reynolds**0.75
    return (4.7 + 0.41 * a) / (1.0 + 0.175 * a)


def hindered_settling_velocity(terminal_velocity_: float, voidage: float, terminal_reynolds: float) -> float:
    """Settling velocity of a suspension, U = U_t eps^n (Richardson-Zaki)."""
    if not 0 < voidage <= 1:
        raise ValueError("voidage must be in (0, 1].")
    return terminal_velocity_ * voidage ** richardson_zaki_exponent(terminal_reynolds)


def vortex_shedding_frequency(velocity: float, diameter: float, strouhal: float = 0.2) -> float:
    """Karman vortex-shedding frequency f = St V / D [Hz] (St ~ 0.2 for cylinders, 300 < Re < 2e5)."""
    return strouhal * velocity / diameter
