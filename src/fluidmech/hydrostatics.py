"""Hydrostatics: pressure at depth, forces on submerged surfaces and buoyancy."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import G


def pressure_at_depth(depth: float, density: float = 1000.0, surface_pressure: float = 0.0, g: float = G) -> float:
    """Hydrostatic pressure p = p0 + rho g h [Pa].

    Use ``surface_pressure=0`` for gauge pressure or the atmospheric pressure
    for absolute pressure.
    """
    if depth < 0:
        raise ValueError("depth must be non-negative.")
    return surface_pressure + density * g * depth


def manometer_pressure_difference(
    height_difference: float, gauge_density: float, flowing_density: float = 0.0, g: float = G
) -> float:
    """Pressure difference measured by a differential U-tube manometer [Pa].

    dp = (rho_gauge - rho_fluid) g h, where ``flowing_density`` is the density of the
    fluid above the gauge liquid (zero if it is a gas, to good approximation).
    """
    return (gauge_density - flowing_density) * g * height_difference


@dataclass(frozen=True)
class SurfaceForce:
    """Result of a hydrostatic force calculation on a plane surface."""

    force: float
    """Resultant hydrostatic force [N]."""
    centroid_depth: float
    """Vertical depth of the centroid below the free surface [m]."""
    center_of_pressure_depth: float
    """Vertical depth of the center of pressure below the free surface [m]."""
    center_of_pressure_slant: float
    """Distance of the center of pressure from the free surface, measured along the plate [m]."""


def plane_surface_force(
    area: float,
    centroid_depth: float,
    second_moment_centroid: float,
    angle_deg: float = 90.0,
    density: float = 1000.0,
    g: float = G,
) -> SurfaceForce:
    """Hydrostatic force on a submerged plane surface (gauge pressure).

    Parameters
    ----------
    area : Surface area A [m^2].
    centroid_depth : Vertical depth h_c of the centroid [m].
    second_moment_centroid : Second moment of area I_xc about the horizontal
        centroidal axis in the plane of the surface [m^4].
    angle_deg : Angle between the surface and the free surface (90 = vertical).
    density : Fluid density [kg/m^3].

    Notes
    -----
    F = rho g h_c A and y_cp = y_c + I_xc / (y_c A), with y measured along the plate.
    """
    if area <= 0 or centroid_depth <= 0:
        raise ValueError("area and centroid_depth must be positive.")
    if not 0.0 < angle_deg <= 90.0:
        raise ValueError("angle_deg must be in (0, 90].")
    sin_t = math.sin(math.radians(angle_deg))
    force = density * g * centroid_depth * area
    y_c = centroid_depth / sin_t
    y_cp = y_c + second_moment_centroid / (y_c * area)
    return SurfaceForce(force, centroid_depth, y_cp * sin_t, y_cp)


def rectangular_gate(
    width: float,
    height: float,
    top_depth: float = 0.0,
    angle_deg: float = 90.0,
    density: float = 1000.0,
    g: float = G,
) -> SurfaceForce:
    """Hydrostatic force on a rectangular gate.

    ``height`` is measured along the gate, ``top_depth`` is the vertical depth of
    the gate's top edge below the free surface.
    """
    if width <= 0 or height <= 0 or top_depth < 0:
        raise ValueError("width and height must be positive and top_depth non-negative.")
    sin_t = math.sin(math.radians(angle_deg))
    area = width * height
    centroid_depth = top_depth + 0.5 * height * sin_t
    i_xc = width * height**3 / 12.0
    return plane_surface_force(area, centroid_depth, i_xc, angle_deg, density, g)


def circular_gate(
    diameter: float,
    top_depth: float = 0.0,
    angle_deg: float = 90.0,
    density: float = 1000.0,
    g: float = G,
) -> SurfaceForce:
    """Hydrostatic force on a circular gate (see :func:`rectangular_gate`)."""
    if diameter <= 0 or top_depth < 0:
        raise ValueError("diameter must be positive and top_depth non-negative.")
    sin_t = math.sin(math.radians(angle_deg))
    area = math.pi * diameter**2 / 4.0
    centroid_depth = top_depth + 0.5 * diameter * sin_t
    i_xc = math.pi * diameter**4 / 64.0
    return plane_surface_force(area, centroid_depth, i_xc, angle_deg, density, g)


def buoyant_force(displaced_volume: float, density: float = 1000.0, g: float = G) -> float:
    """Archimedes' buoyant force F_B = rho g V [N]."""
    if displaced_volume < 0:
        raise ValueError("displaced_volume must be non-negative.")
    return density * g * displaced_volume


def submerged_fraction(body_density: float, fluid_density: float = 1000.0) -> float:
    """Fraction of a floating body's volume below the free surface.

    Returns 1.0 if the body is denser than the fluid (it sinks).
    """
    if body_density <= 0 or fluid_density <= 0:
        raise ValueError("densities must be positive.")
    return min(body_density / fluid_density, 1.0)


# ---------------------------------------------------------------------------- #
# Rigid-body motion
# ---------------------------------------------------------------------------- #
def accelerating_surface_slope(
    horizontal_acceleration: float, vertical_acceleration: float = 0.0, g: float = G
) -> float:
    """Free-surface slope dz/dx = -a_x / (g + a_z) for a liquid in uniform linear acceleration.

    Returns the tangent of the surface angle (negative: the surface drops towards the front).
    """
    if g + vertical_acceleration <= 0:
        raise ValueError("Vertical acceleration must be greater than -g (free fall).")
    return -horizontal_acceleration / (g + vertical_acceleration)


def accelerating_pressure(
    x: float,
    z: float,
    horizontal_acceleration: float,
    vertical_acceleration: float = 0.0,
    density: float = 1000.0,
    reference_pressure: float = 0.0,
    g: float = G,
) -> float:
    """Pressure p = p0 - rho a_x x - rho (g + a_z) z relative to the point (0, 0) [Pa]."""
    return reference_pressure - density * horizontal_acceleration * x - density * (g + vertical_acceleration) * z


@dataclass(frozen=True)
class RotatingTank:
    """Open cylindrical tank of liquid in rigid-body rotation (a forced vortex).

    The free surface is a paraboloid z(r) = z_centre + omega^2 r^2 / (2g). The
    liquid volume is conserved, so the surface falls at the centre by half the
    total rise and climbs at the wall by the other half.
    """

    radius: float
    initial_depth: float
    omega: float
    """Angular velocity [rad/s]."""

    @property
    def rise(self) -> float:
        """Height difference between wall and centre, omega^2 R^2 / (2g) [m]."""
        return self.omega**2 * self.radius**2 / (2.0 * G)

    @property
    def centre_depth(self) -> float:
        """Liquid depth on the axis [m] (negative: the bottom is exposed)."""
        return self.initial_depth - self.rise / 2.0

    @property
    def wall_depth(self) -> float:
        return self.initial_depth + self.rise / 2.0

    def surface_height(self, r: float) -> float:
        """Free-surface elevation above the tank bottom at radius r [m]."""
        return self.centre_depth + self.omega**2 * r**2 / (2.0 * G)

    def pressure(self, r: float, z: float, density: float = 1000.0) -> float:
        """Gauge pressure at (r, z), p = rho omega^2 r^2 / 2 - rho g (z - z_centre) [Pa]."""
        return density * self.omega**2 * r**2 / 2.0 - density * G * (z - self.centre_depth)

    def speed_to_expose_bottom(self) -> float:
        """Angular velocity at which the free surface first touches the bottom centre [rad/s]."""
        return math.sqrt(4.0 * G * self.initial_depth) / self.radius


def curved_surface_force(horizontal_projection_force: float, weight_of_fluid_above: float) -> tuple[float, float]:
    """Resultant magnitude and angle (deg from horizontal) of the force on a curved surface.

    F_H = force on the vertical projection; F_V = weight of fluid above the surface.
    """
    return math.hypot(horizontal_projection_force, weight_of_fluid_above), math.degrees(
        math.atan2(weight_of_fluid_above, horizontal_projection_force)
    )
