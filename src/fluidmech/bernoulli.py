"""Bernoulli equation and flow-measurement devices (ideal, incompressible flow)."""

from __future__ import annotations

import math

from .constants import G


def total_head(pressure: float, velocity: float, elevation: float, density: float = 1000.0, g: float = G) -> float:
    """Total head H = p/(rho g) + V^2/(2 g) + z [m]."""
    return pressure / (density * g) + velocity**2 / (2.0 * g) + elevation


def velocity_head(velocity: float, g: float = G) -> float:
    """Velocity (dynamic) head V^2 / (2 g) [m]."""
    return velocity**2 / (2.0 * g)


def torricelli_velocity(head: float, g: float = G) -> float:
    """Ideal efflux velocity from a tank, V = sqrt(2 g h) [m/s]."""
    if head < 0:
        raise ValueError("head must be non-negative.")
    return math.sqrt(2.0 * g * head)


def pitot_velocity(pressure_difference: float, density: float = 1.225) -> float:
    """Flow velocity from a Pitot-static tube, V = sqrt(2 dp / rho) [m/s].

    ``pressure_difference`` is stagnation minus static pressure [Pa].
    """
    if pressure_difference < 0:
        raise ValueError("pressure_difference must be non-negative.")
    return math.sqrt(2.0 * pressure_difference / density)


def venturi_flow_rate(
    inlet_diameter: float,
    throat_diameter: float,
    pressure_difference: float,
    density: float = 1000.0,
    discharge_coefficient: float = 0.98,
) -> float:
    """Volumetric flow rate through a Venturi meter [m^3/s].

    Q = Cd A2 sqrt( 2 dp / (rho (1 - beta^4)) ),  beta = d2/d1.
    """
    if not 0 < throat_diameter < inlet_diameter:
        raise ValueError("Require 0 < throat_diameter < inlet_diameter.")
    if pressure_difference < 0:
        raise ValueError("pressure_difference must be non-negative.")
    beta = throat_diameter / inlet_diameter
    a2 = math.pi * throat_diameter**2 / 4.0
    return discharge_coefficient * a2 * math.sqrt(2.0 * pressure_difference / (density * (1.0 - beta**4)))


def orifice_flow_rate(orifice_area: float, head: float, discharge_coefficient: float = 0.61, g: float = G) -> float:
    """Flow rate through a small sharp-edged orifice under a head h [m^3/s]."""
    if orifice_area <= 0:
        raise ValueError("orifice_area must be positive.")
    return discharge_coefficient * orifice_area * torricelli_velocity(head, g)


def tank_drain_time(
    tank_area: float,
    orifice_area: float,
    initial_head: float,
    final_head: float = 0.0,
    discharge_coefficient: float = 0.61,
    g: float = G,
) -> float:
    """Time [s] to drain a constant-cross-section tank through a bottom orifice.

    t = (2 A_t / (Cd A_o sqrt(2 g))) (sqrt(h1) - sqrt(h2)).
    """
    if not 0 <= final_head <= initial_head:
        raise ValueError("Require 0 <= final_head <= initial_head.")
    return (
        2.0
        * tank_area
        / (discharge_coefficient * orifice_area * math.sqrt(2.0 * g))
        * (math.sqrt(initial_head) - math.sqrt(final_head))
    )
