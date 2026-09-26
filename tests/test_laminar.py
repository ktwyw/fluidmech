"""Exact Navier-Stokes solutions: every flow-rate formula is checked by numerically integrating
its own velocity profile, and limiting cases are checked (e.g. power law with n = 1)."""

import math

import pytest

from fluidmech import laminar as lam

MU, G_ = 1e-3, 100.0


def _integrate(f, a, b, n=4000):
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) for i in range(n)) * h


def test_plates_flow_rate_matches_profile_integral():
    h, U = 0.002, 0.05
    q = _integrate(lambda y: lam.plates_velocity(y, h, G_, MU, U), 0, h)
    assert q == pytest.approx(lam.plates_flow_rate(h, G_, MU, U), rel=1e-6)
    lower, upper = lam.plates_wall_shear(h, G=0.0, mu=MU, upper_velocity=U)
    assert lower == pytest.approx(MU * U / h) and upper == pytest.approx(MU * U / h)


def test_hagen_poiseuille_consistency():
    R = 0.01
    q = _integrate(lambda r: 2 * math.pi * r * lam.pipe_velocity(r, R, G_, MU), 0, R)
    assert q == pytest.approx(lam.pipe_flow_rate(G_, R, MU), rel=1e-6)
    assert lam.pipe_pressure_gradient(lam.pipe_flow_rate(G_, R, MU), R, MU) == pytest.approx(G_)


def test_annulus():
    ri, ro = 0.01, 0.03
    q = _integrate(lambda r: 2 * math.pi * r * lam.annulus_velocity(r, ri, ro, G_, MU), ri, ro)
    assert q == pytest.approx(lam.annulus_flow_rate(ri, ro, G_, MU), rel=1e-6)
    assert lam.annulus_velocity(ri, ri, ro, G_, MU) == pytest.approx(0.0, abs=1e-12)
    r_star = lam.annulus_max_velocity_radius(ri, ro)
    eps = 1e-5
    assert lam.annulus_velocity(r_star, ri, ro, G_, MU) >= lam.annulus_velocity(r_star + eps, ri, ro, G_, MU)
    # fRe from the flow-rate solution agrees with the closed form
    k = ri / ro
    v = lam.annulus_flow_rate(ri, ro, G_, MU) / (math.pi * (ro**2 - ri**2))
    dh = 2 * (ro - ri)
    f = G_ * dh / (0.5 * 1000 * v**2)
    assert f * 1000 * v * dh / MU == pytest.approx(lam.annulus_fre(k), rel=1e-9)


def test_film():
    gamma, rho = 0.05, 1000.0
    d = lam.film_thickness(gamma, rho, MU)
    flux = _integrate(lambda y: rho * lam.film_velocity(y, d, rho, MU), 0, d)
    assert flux == pytest.approx(gamma, rel=1e-6)
    assert lam.film_reynolds(gamma, MU) == pytest.approx(200.0)


def test_power_law_reduces_to_newtonian_and_integrates():
    R = 0.01
    assert lam.power_law_pipe_flow_rate(G_, R, MU, 1.0) == pytest.approx(lam.pipe_flow_rate(G_, R, MU))
    k, n = 0.5, 0.4
    q = _integrate(lambda r: 2 * math.pi * r * lam.power_law_pipe_velocity(r, R, 5000.0, k, n), 0, R)
    assert q == pytest.approx(lam.power_law_pipe_flow_rate(5000.0, R, k, n), rel=1e-5)
    assert lam.metzner_reed_reynolds(1000, 1.0, 0.05, MU, 1.0) == pytest.approx(1000 * 0.05 / MU)


def test_bingham():
    R, ty, mp, g = 0.01, 5.0, 0.05, 3000.0
    q = _integrate(lambda r: 2 * math.pi * r * lam.bingham_pipe_velocity(r, R, g, ty, mp), 0, R)
    assert q == pytest.approx(lam.bingham_pipe_flow_rate(g, R, ty, mp), rel=1e-5)
    assert lam.bingham_pipe_flow_rate(g, R, 1e-12, mp) == pytest.approx(lam.pipe_flow_rate(g, R, mp))
    assert lam.bingham_pipe_flow_rate(500.0, R, 5.0, mp) == 0.0  # wall stress below yield


def test_stokes_problems():
    assert lam.stokes_first_problem(0.0, 1.0, 2.0, 1e-6) == pytest.approx(2.0)
    assert lam.stokes_first_problem(0.01, 1.0, 1.0, 1e-6) < 1e-6
    assert lam.stokes_second_problem(0.0, 0.0, 1.0, 10.0, 1e-6) == pytest.approx(1.0)


def test_duct_fre():
    assert lam.rectangular_duct_fre(0.0) == pytest.approx(96.0)
    assert lam.rectangular_duct_fre(1.0) == pytest.approx(56.9, abs=0.05)
    assert lam.annulus_fre(1e-6) < 96 and lam.annulus_fre(0.999) == pytest.approx(96.0, rel=1e-3)
