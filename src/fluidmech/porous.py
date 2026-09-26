"""Flow through porous media: Darcy's law, packed beds, fluidisation, filtration and membranes.

Notation: superficial velocity u = Q / A (based on the empty cross-section),
voidage (porosity) eps, particle diameter d_p and sphericity phi_s.

Examples
--------
>>> DARCY
9.869233e-13
>>> round(ergun_pressure_gradient(0.01, 0.003, 0.4, 1e-3, 1000.0), 1)  # Pa/m
1484.4
"""

from __future__ import annotations

import math

from ._solvers import positive_root
from .constants import G

DARCY = 9.869233e-13
"""One darcy expressed in m^2."""

R_GAS = 8.314462618
"""Universal gas constant [J/(mol K)]."""


# ---------------------------------------------------------------------------- #
# Darcy's law
# ---------------------------------------------------------------------------- #
def darcy_velocity(permeability: float, pressure_drop: float, length: float, mu: float) -> float:
    """Superficial velocity u = k dp / (mu L) [m/s]."""
    if permeability <= 0 or length <= 0 or mu <= 0:
        raise ValueError("permeability, length and mu must be positive.")
    return permeability * pressure_drop / (mu * length)


def permeability_from_test(flow_rate: float, area: float, pressure_drop: float, length: float, mu: float) -> float:
    """Permeability k = Q mu L / (A dp) [m^2] from a permeameter measurement."""
    return flow_rate * mu * length / (area * pressure_drop)


def hydraulic_conductivity(permeability: float, density: float = 1000.0, mu: float = 1e-3, g: float = G) -> float:
    """Hydraulic conductivity K = k rho g / mu [m/s] (groundwater form of Darcy's law)."""
    return permeability * density * g / mu


# ---------------------------------------------------------------------------- #
# Packed beds
# ---------------------------------------------------------------------------- #
def _check_bed(voidage: float, particle_diameter: float) -> None:
    if not 0 < voidage < 1:
        raise ValueError("voidage must be between 0 and 1.")
    if particle_diameter <= 0:
        raise ValueError("particle_diameter must be positive.")


def specific_surface(particle_diameter: float, sphericity: float = 1.0) -> float:
    """Particle surface-to-volume ratio a_v = 6 / (phi_s d_p) [1/m]."""
    return 6.0 / (sphericity * particle_diameter)


def kozeny_carman_permeability(
    particle_diameter: float, voidage: float, sphericity: float = 1.0, kozeny_constant: float = 180.0
) -> float:
    """k = eps^3 (phi_s d_p)^2 / (K (1 - eps)^2) with K = 180 (Carman) [m^2]."""
    _check_bed(voidage, particle_diameter)
    d = sphericity * particle_diameter
    return voidage**3 * d**2 / (kozeny_constant * (1.0 - voidage) ** 2)


def kozeny_carman_pressure_gradient(
    superficial_velocity: float, particle_diameter: float, voidage: float, mu: float, sphericity: float = 1.0
) -> float:
    """Laminar packed-bed pressure gradient dp/L = 180 mu u (1-eps)^2 / (eps^3 (phi_s d_p)^2) [Pa/m]."""
    k = kozeny_carman_permeability(particle_diameter, voidage, sphericity)
    return mu * superficial_velocity / k


def burke_plummer_pressure_gradient(
    superficial_velocity: float, particle_diameter: float, voidage: float, density: float, sphericity: float = 1.0
) -> float:
    """Turbulent limit dp/L = 1.75 rho u^2 (1-eps) / (eps^3 phi_s d_p) [Pa/m]."""
    _check_bed(voidage, particle_diameter)
    return 1.75 * density * superficial_velocity**2 * (1.0 - voidage) / (voidage**3 * sphericity * particle_diameter)


def ergun_pressure_gradient(
    superficial_velocity: float,
    particle_diameter: float,
    voidage: float,
    mu: float,
    density: float,
    sphericity: float = 1.0,
) -> float:
    """Ergun equation (1952): 150 viscous + 1.75 inertial terms [Pa/m]."""
    _check_bed(voidage, particle_diameter)
    d = sphericity * particle_diameter
    u = superficial_velocity
    viscous = 150.0 * mu * u * (1.0 - voidage) ** 2 / (voidage**3 * d**2)  # laminar (Blake-Kozeny) part, ~u
    # inertial (Burke-Plummer) part, ~u^2; abs() keeps the sign of u
    inertial = 1.75 * density * u * abs(u) * (1.0 - voidage) / (voidage**3 * d)
    return viscous + inertial


def bed_reynolds(
    superficial_velocity: float,
    particle_diameter: float,
    voidage: float,
    mu: float,
    density: float,
    sphericity: float = 1.0,
) -> float:
    """Modified particle Reynolds number Re_p = rho u phi_s d_p / (mu (1 - eps)).

    Below ~10 the viscous (Kozeny-Carman) term dominates; above ~1000 the inertial term.
    """
    return density * superficial_velocity * sphericity * particle_diameter / (mu * (1.0 - voidage))


def bed_friction_factor(bed_re: float) -> float:
    """Ergun friction factor f_p = 150 / Re_p + 1.75."""
    return 150.0 / bed_re + 1.75


# ---------------------------------------------------------------------------- #
# Fluidisation
# ---------------------------------------------------------------------------- #
def archimedes_number(
    particle_diameter: float, particle_density: float, density: float, mu: float, g: float = G
) -> float:
    """Ar = rho (rho_p - rho) g d^3 / mu^2."""
    return density * (particle_density - density) * g * particle_diameter**3 / mu**2


def fluidized_bed_pressure_drop(
    bed_height: float, voidage: float, particle_density: float, density: float, g: float = G
) -> float:
    """Pressure drop across a fluidised bed = buoyant weight per area, (1-eps)(rho_p - rho) g L [Pa]."""
    return (1.0 - voidage) * (particle_density - density) * g * bed_height


def minimum_fluidization_velocity(
    particle_diameter: float,
    particle_density: float,
    density: float,
    mu: float,
    voidage_mf: float | None = None,
    sphericity: float = 1.0,
    g: float = G,
) -> float:
    """Minimum fluidisation velocity u_mf [m/s].

    With ``voidage_mf`` given, the Ergun equation is equated to the bed's buoyant
    weight and solved exactly. Otherwise the Wen & Yu (1966) correlation
    Re_mf = sqrt(33.7^2 + 0.0408 Ar) - 33.7 is used.
    """
    if voidage_mf is None:
        ar = archimedes_number(particle_diameter, particle_density, density, mu, g)
        re_mf = math.sqrt(33.7**2 + 0.0408 * ar) - 33.7  # Wen & Yu (1966)
        return re_mf * mu / (density * particle_diameter)
    target = (1.0 - voidage_mf) * (particle_density - density) * g  # buoyant weight of the bed per unit height

    def residual(u: float) -> float:
        return ergun_pressure_gradient(u, particle_diameter, voidage_mf, mu, density, sphericity) - target

    return positive_root(residual, guess=1e-3)


# ---------------------------------------------------------------------------- #
# Cake filtration
# ---------------------------------------------------------------------------- #
def filtration_time(
    volume: float,
    area: float,
    pressure_drop: float,
    mu: float,
    specific_cake_resistance: float,
    solids_per_filtrate: float,
    medium_resistance: float,
) -> float:
    """Constant-pressure filtration time for filtrate volume V (Ruth equation) [s].

    t = (mu alpha c / (2 A^2 dp)) V^2 + (mu R_m / (A dp)) V
    with alpha [m/kg], c = kg of dry cake per m^3 of filtrate, R_m [1/m].
    """
    kp = mu * specific_cake_resistance * solids_per_filtrate / (area**2 * pressure_drop)
    b = mu * medium_resistance / (area * pressure_drop)
    return 0.5 * kp * volume**2 + b * volume


def filtration_volume(
    time: float,
    area: float,
    pressure_drop: float,
    mu: float,
    specific_cake_resistance: float,
    solids_per_filtrate: float,
    medium_resistance: float,
) -> float:
    """Filtrate volume collected after ``time`` at constant pressure [m^3] (inverse of :func:`filtration_time`)."""
    kp = mu * specific_cake_resistance * solids_per_filtrate / (area**2 * pressure_drop)
    b = mu * medium_resistance / (area * pressure_drop)
    return (-b + math.sqrt(b * b + 2.0 * kp * time)) / kp  # positive root of (Kp/2) V^2 + B V - t = 0


def filtration_constants_from_data(
    times: list[float], volumes: list[float], area: float, pressure_drop: float, mu: float, solids_per_filtrate: float
) -> tuple[float, float, float, float]:
    """Analyse constant-pressure test data with the t/V versus V plot.

    Fits t/V = (Kp/2) V + B and returns (alpha, R_m, Kp, B):
    specific cake resistance alpha = Kp A^2 dp / (mu c), medium resistance R_m = B A dp / mu.
    """
    x = volumes
    y = [t / v for t, v in zip(times, volumes)]
    n = len(x)
    xm, ym = sum(x) / n, sum(y) / n
    slope = sum((xi - xm) * (yi - ym) for xi, yi in zip(x, y)) / sum((xi - xm) ** 2 for xi in x)
    intercept = ym - slope * xm
    kp = 2.0 * slope  # slope of t/V vs V equals Kp / 2
    alpha = kp * area**2 * pressure_drop / (mu * solids_per_filtrate)  # from Kp = mu alpha c / (A^2 dp)
    r_m = intercept * area * pressure_drop / mu  # from intercept B = mu R_m / (A dp)
    return alpha, r_m, kp, intercept


# ---------------------------------------------------------------------------- #
# Membranes
# ---------------------------------------------------------------------------- #
def vant_hoff_osmotic_pressure(
    molar_concentration: float, temperature: float = 25.0, ions_per_formula: int = 1
) -> float:
    """Osmotic pressure pi = i C R T [Pa] for ``molar_concentration`` in mol/m^3 (= mmol/L)."""
    return ions_per_formula * molar_concentration * R_GAS * (temperature + 273.15)


def membrane_flux(
    transmembrane_pressure: float,
    mu: float,
    membrane_resistance: float,
    fouling_resistance: float = 0.0,
    osmotic_pressure_difference: float = 0.0,
) -> float:
    """Resistance-in-series model J = (dp - d_pi) / (mu (R_m + R_f)) [m^3/(m^2 s)]."""
    driving = transmembrane_pressure - osmotic_pressure_difference
    return max(driving, 0.0) / (mu * (membrane_resistance + fouling_resistance))


def lmh(flux_si: float) -> float:
    """Convert a flux from m^3/(m^2 s) to the membrane-industry unit L/(m^2 h) ('LMH')."""
    return flux_si * 1000.0 * 3600.0
