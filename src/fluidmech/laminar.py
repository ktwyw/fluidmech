"""Exact solutions of the Navier-Stokes equations for laminar flow.

All flows are steady, fully developed and incompressible unless stated. The
driving pressure gradient is written G = -dp/dx > 0 (pressure falling in the
flow direction). Positions are measured as documented in each function.

These are the classical solutions of White, *Fluid Mechanics*, Ch. 4 and 6,
and Bird, Stewart & Lightfoot, *Transport Phenomena*, Ch. 2.

Examples
--------
>>> round(pipe_flow_rate(G=1000.0, radius=0.01, mu=1e-3), 6)  # Hagen-Poiseuille
0.003927
"""

from __future__ import annotations

import math

from .constants import G as GRAVITY


# ---------------------------------------------------------------------------- #
# Flow between parallel plates (gap h, y measured from the lower plate)
# ---------------------------------------------------------------------------- #
def plates_velocity(y: float, h: float, G: float = 0.0, mu: float = 1e-3, upper_velocity: float = 0.0) -> float:
    """Couette-Poiseuille flow between plates a distance h apart.

    u(y) = U y/h + (G / 2 mu) y (h - y); lower plate fixed, upper plate moving at U.
    With U = 0 this is plane Poiseuille flow; with G = 0 plane Couette flow.
    """
    if not 0 <= y <= h:
        raise ValueError("y must lie between 0 and h.")
    return upper_velocity * y / h + G / (2.0 * mu) * y * (h - y)


def plates_flow_rate(h: float, G: float = 0.0, mu: float = 1e-3, upper_velocity: float = 0.0) -> float:
    """Flow rate per unit width [m^2/s]: q = U h / 2 + G h^3 / (12 mu)."""
    return upper_velocity * h / 2.0 + G * h**3 / (12.0 * mu)


def plates_wall_shear(h: float, G: float = 0.0, mu: float = 1e-3, upper_velocity: float = 0.0) -> tuple[float, float]:
    """Shear stress mu du/dy at the lower and upper plates [Pa]."""
    lower = mu * upper_velocity / h + G * h / 2.0
    upper = mu * upper_velocity / h - G * h / 2.0
    return lower, upper


# ---------------------------------------------------------------------------- #
# Circular pipe (Hagen-Poiseuille), r measured from the axis
# ---------------------------------------------------------------------------- #
def pipe_velocity(r: float, radius: float, G: float, mu: float) -> float:
    """u(r) = G (R^2 - r^2) / (4 mu)."""
    if not 0 <= r <= radius:
        raise ValueError("r must lie between 0 and the pipe radius.")
    return G * (radius**2 - r**2) / (4.0 * mu)


def pipe_flow_rate(G: float, radius: float, mu: float) -> float:
    """Hagen-Poiseuille law, Q = pi G R^4 / (8 mu) [m^3/s]."""
    return math.pi * G * radius**4 / (8.0 * mu)


def pipe_pressure_gradient(flow_rate: float, radius: float, mu: float) -> float:
    """Pressure gradient G = 8 mu Q / (pi R^4) needed for a given flow rate [Pa/m]."""
    return 8.0 * mu * flow_rate / (math.pi * radius**4)


# ---------------------------------------------------------------------------- #
# Concentric annulus, inner radius kappa*R, outer radius R
# ---------------------------------------------------------------------------- #
def annulus_velocity(r: float, inner_radius: float, outer_radius: float, G: float, mu: float) -> float:
    """u(r) = (G R^2 / 4 mu) [1 - (r/R)^2 + (1 - k^2) ln(r/R) / ln(1/k)],  k = R_i / R."""
    R, k = outer_radius, inner_radius / outer_radius
    if not inner_radius <= r <= outer_radius or not 0 < k < 1:
        raise ValueError("Need 0 < inner_radius <= r <= outer_radius.")
    return G * R**2 / (4.0 * mu) * (1.0 - (r / R) ** 2 + (1.0 - k**2) * math.log(r / R) / math.log(1.0 / k))


def annulus_flow_rate(inner_radius: float, outer_radius: float, G: float, mu: float) -> float:
    """Q = (pi G R^4 / 8 mu) [1 - k^4 - (1 - k^2)^2 / ln(1/k)] [m^3/s]."""
    R, k = outer_radius, inner_radius / outer_radius
    if not 0 < k < 1:
        raise ValueError("Need 0 < inner_radius < outer_radius.")
    return math.pi * G * R**4 / (8.0 * mu) * (1.0 - k**4 - (1.0 - k**2) ** 2 / math.log(1.0 / k))


def annulus_max_velocity_radius(inner_radius: float, outer_radius: float) -> float:
    """Radius of maximum velocity, r* = R sqrt((1 - k^2) / (2 ln(1/k)))."""
    R, k = outer_radius, inner_radius / outer_radius
    return R * math.sqrt((1.0 - k**2) / (2.0 * math.log(1.0 / k)))


# ---------------------------------------------------------------------------- #
# Falling film on an inclined plane (y measured from the wall)
# ---------------------------------------------------------------------------- #
def film_thickness(
    mass_flow_per_width: float, density: float, mu: float, angle_deg: float = 90.0, g: float = GRAVITY
) -> float:
    """Nusselt film thickness delta = (3 mu Gamma / (rho^2 g sin beta))^(1/3) [m].

    ``mass_flow_per_width`` Gamma is in kg/(m s); angle is measured from the horizontal.
    """
    s = math.sin(math.radians(angle_deg))
    if mass_flow_per_width <= 0 or s <= 0:
        raise ValueError("Need a positive flow and an inclined plane.")
    return (3.0 * mu * mass_flow_per_width / (density**2 * g * s)) ** (1.0 / 3.0)


def film_velocity(
    y: float, thickness: float, density: float, mu: float, angle_deg: float = 90.0, g: float = GRAVITY
) -> float:
    """u(y) = (rho g sin beta / mu) (delta y - y^2 / 2); maximum at the free surface."""
    if not 0 <= y <= thickness:
        raise ValueError("y must lie within the film.")
    return density * g * math.sin(math.radians(angle_deg)) / mu * (thickness * y - y**2 / 2.0)


def film_reynolds(mass_flow_per_width: float, mu: float) -> float:
    """Film Reynolds number Re = 4 Gamma / mu (laminar and wave-free below about 20-30)."""
    return 4.0 * mass_flow_per_width / mu


# ---------------------------------------------------------------------------- #
# Non-Newtonian fluids in a pipe
# ---------------------------------------------------------------------------- #
def power_law_pipe_velocity(r: float, radius: float, G: float, K: float, n: float) -> float:
    """u(r) = n/(n+1) (G / 2K)^(1/n) [R^((n+1)/n) - r^((n+1)/n)] for a power-law fluid."""
    if not 0 <= r <= radius:
        raise ValueError("r must lie between 0 and the pipe radius.")
    e = (n + 1.0) / n
    return n / (n + 1.0) * (G / (2.0 * K)) ** (1.0 / n) * (radius**e - r**e)


def power_law_pipe_flow_rate(G: float, radius: float, K: float, n: float) -> float:
    """Q = pi n / (3n + 1) (G / 2K)^(1/n) R^((3n+1)/n) [m^3/s]."""
    return math.pi * n / (3.0 * n + 1.0) * (G / (2.0 * K)) ** (1.0 / n) * radius ** ((3.0 * n + 1.0) / n)


def metzner_reed_reynolds(density: float, velocity: float, diameter: float, K: float, n: float) -> float:
    """Metzner-Reed Reynolds number for power-law fluids; laminar f_Darcy = 64 / Re_MR."""
    return density * velocity ** (2.0 - n) * diameter**n / (K * 8.0 ** (n - 1.0) * ((3.0 * n + 1.0) / (4.0 * n)) ** n)


def bingham_plug_radius(G: float, yield_stress: float) -> float:
    """Radius of the unsheared plug, r0 = 2 tau_y / G [m]."""
    return 2.0 * yield_stress / G


def bingham_pipe_velocity(r: float, radius: float, G: float, yield_stress: float, plastic_viscosity: float) -> float:
    """Velocity of a Bingham plastic in a pipe (zero if the wall stress is below tau_y)."""
    r0 = bingham_plug_radius(G, yield_stress)
    if r0 >= radius:
        return 0.0
    rr = max(r, r0)
    return G / (4.0 * plastic_viscosity) * (radius**2 - rr**2) - yield_stress / plastic_viscosity * (radius - rr)


def bingham_pipe_flow_rate(G: float, radius: float, yield_stress: float, plastic_viscosity: float) -> float:
    """Buckingham-Reiner equation, Q = pi R^4 G / (8 mu_p) [1 - 4 phi / 3 + phi^4 / 3], phi = tau_y / tau_w."""
    tau_w = G * radius / 2.0
    phi = yield_stress / tau_w
    if phi >= 1.0:
        return 0.0
    return math.pi * radius**4 * G / (8.0 * plastic_viscosity) * (1.0 - 4.0 * phi / 3.0 + phi**4 / 3.0)


# ---------------------------------------------------------------------------- #
# Unsteady flows (Stokes' problems)
# ---------------------------------------------------------------------------- #
def stokes_first_problem(y: float, t: float, plate_velocity: float, nu: float) -> float:
    """Impulsively started plate: u = U erfc(y / (2 sqrt(nu t)))."""
    if t <= 0:
        return plate_velocity if y == 0 else 0.0
    return plate_velocity * math.erfc(y / (2.0 * math.sqrt(nu * t)))


def stokes_second_problem(y: float, t: float, amplitude: float, omega: float, nu: float) -> float:
    """Oscillating plate: u = U exp(-k y) cos(omega t - k y), k = sqrt(omega / 2 nu)."""
    k = math.sqrt(omega / (2.0 * nu))
    return amplitude * math.exp(-k * y) * math.cos(omega * t - k * y)


def penetration_depth(nu: float, t: float) -> float:
    """Momentum diffusion distance, delta ~ 4 sqrt(nu t) (where u/U falls to about 0.5 %)."""
    return 4.0 * math.sqrt(nu * t)


# ---------------------------------------------------------------------------- #
# Laminar friction in non-circular ducts
# ---------------------------------------------------------------------------- #
def rectangular_duct_fre(aspect_ratio: float) -> float:
    """Darcy f * Re (based on hydraulic diameter) for laminar flow in a rectangular duct.

    Shah & London (1978) fit, aspect ratio = short side / long side (0 to 1):
    f Re = 96 (1 - 1.3553 a + 1.9467 a^2 - 1.7012 a^3 + 0.9564 a^4 - 0.2537 a^5).
    Gives 96 for parallel plates (a = 0) and 56.9 for a square duct (a = 1).
    """
    a = aspect_ratio if aspect_ratio <= 1 else 1.0 / aspect_ratio
    if a < 0:
        raise ValueError("aspect_ratio must be positive.")
    return 96.0 * (1 - 1.3553 * a + 1.9467 * a**2 - 1.7012 * a**3 + 0.9564 * a**4 - 0.2537 * a**5)


def annulus_fre(radius_ratio: float) -> float:
    """Darcy f * Re (based on D_h = 2(R - R_i)) for laminar flow in a concentric annulus."""
    k = radius_ratio
    if not 0 < k < 1:
        raise ValueError("radius_ratio must be between 0 and 1.")
    return 64.0 * (1.0 - k) ** 2 / (1.0 + k**2 + (1.0 - k**2) / math.log(k))


# ---------------------------------------------------------------------------- #
# Blasius boundary layer (similarity solution)
# ---------------------------------------------------------------------------- #
def blasius(eta_max: float = 10.0, steps: int = 2000) -> dict:
    """Solve the Blasius equation f''' + (1/2) f f'' = 0, f(0) = f'(0) = 0, f'(inf) = 1.

    Shooting method: RK4 integration for a trial wall curvature s = f''(0), with bisection on s
    until f'(eta_max) = 1. Here u/U = f'(eta) with eta = y sqrt(U / (nu x)).
    Returns eta, f, fp (= u/U), fpp and the wall value fpp0 (0.33206; skin friction
    C_f = 0.664 / sqrt(Re_x)), plus the thickness coefficients delta_99, delta* and theta.
    """
    h = eta_max / steps

    def integrate(s, keep=False):
        y = [0.0, 0.0, s]  # f, f', f''
        rows = [(0.0, *y)] if keep else None

        def rhs(v):
            return [v[1], v[2], -0.5 * v[0] * v[2]]

        for i in range(steps):
            k1 = rhs(y)
            k2 = rhs([a + 0.5 * h * b for a, b in zip(y, k1)])
            k3 = rhs([a + 0.5 * h * b for a, b in zip(y, k2)])
            k4 = rhs([a + h * b for a, b in zip(y, k3)])
            y = [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
            if keep:
                rows.append(((i + 1) * h, *y))
        return (y, rows) if keep else y

    from ._solvers import bisect

    s0 = bisect(lambda s: integrate(s)[1] - 1.0, 0.1, 1.0, rtol=1e-12)
    _, rows = integrate(s0, keep=True)
    eta = [r[0] for r in rows]
    fp = [r[2] for r in rows]
    delta99 = next(e for e, u in zip(eta, fp) if u >= 0.99)
    delta_star = sum((1 - (fp[i] + fp[i + 1]) / 2) * h for i in range(steps))  # integral of (1 - u/U)
    theta = sum(((fp[i] + fp[i + 1]) / 2) * (1 - (fp[i] + fp[i + 1]) / 2) * h for i in range(steps))
    return {
        "eta": eta,
        "f": [r[1] for r in rows],
        "fp": fp,
        "fpp": [r[3] for r in rows],
        "fpp0": s0,
        "delta99": delta99,
        "delta_star": delta_star,
        "theta": theta,
    }
