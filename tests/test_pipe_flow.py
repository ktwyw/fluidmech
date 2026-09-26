"""Pipe flow: friction factors against the Moody chart and Colebrook, Hagen-Poiseuille,
and round trips through the Type 1, 2 and 3 problems."""

import math

import pytest

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

WATER = Fluid.water(20)


def test_laminar_friction_factor():
    assert pf.friction_factor(1000) == pytest.approx(0.064)


def test_colebrook_satisfies_its_own_equation():
    re, rr = 1e5, 1e-4
    f = pf.colebrook(re, rr)
    rhs = -2 * math.log10(rr / 3.7 + 2.51 / (re * math.sqrt(f)))
    assert 1 / math.sqrt(f) == pytest.approx(rhs, rel=1e-10)


@pytest.mark.parametrize(
    "re, rr, expected",
    [(1e5, 0.0, 0.0180), (1e5, 1e-4, 0.0185), (1e6, 1e-3, 0.0199), (1e7, 0.01, 0.0380)],
)
def test_colebrook_matches_moody_chart(re, rr, expected):
    assert pf.colebrook(re, rr) == pytest.approx(expected, rel=0.02)


@pytest.mark.parametrize("method", ["swamee_jain", "haaland"])
@pytest.mark.parametrize("re", [5e3, 1e5, 1e7])
@pytest.mark.parametrize("rr", [0.0, 1e-4, 1e-2])
def test_explicit_correlations_close_to_colebrook(method, re, rr):
    f = pf.friction_factor(re, rr, method=method)
    assert f == pytest.approx(pf.colebrook(re, rr), rel=0.03)


def test_unknown_method_raises():
    with pytest.raises(ValueError):
        pf.friction_factor(1e5, method="magic")


def test_laminar_head_loss_matches_hagen_poiseuille():
    oil = Fluid(density=900.0, dynamic_viscosity=0.3)
    q, d, length = 1e-3, 0.05, 10.0
    res = pf.head_loss(q, d, length, oil)
    assert res.regime == "laminar"
    dp_hp = 128 * oil.dynamic_viscosity * length * q / (math.pi * d**4)
    assert res.pressure_drop == pytest.approx(dp_hp, rel=1e-3)


def test_head_loss_textbook_case():
    # 0.1 m commercial steel, 200 m, Q = 0.02 m^3/s water at 20 degC
    res = pf.head_loss(0.02, 0.1, 200.0, WATER, pf.ROUGHNESS["commercial_steel"])
    assert res.velocity == pytest.approx(2.546, rel=1e-3)
    assert res.reynolds == pytest.approx(2.54e5, rel=0.01)
    assert res.friction_factor == pytest.approx(0.0182, rel=0.02)
    assert res.major_head_loss == pytest.approx(12.0, rel=0.02)


def test_minor_losses_add_up():
    base = pf.head_loss(0.02, 0.1, 50.0, WATER, 0.045e-3)
    with_k = pf.head_loss(0.02, 0.1, 50.0, WATER, 0.045e-3, k_total=3.0)
    v = base.velocity
    assert with_k.total_head_loss - base.total_head_loss == pytest.approx(3.0 * v**2 / (2 * 9.80665))


def test_type2_roundtrip():
    q = 0.035
    hl = pf.head_loss(q, 0.15, 500.0, WATER, 0.26e-3, k_total=4.5).total_head_loss
    assert pf.flow_rate_for_head_loss(hl, 0.15, 500.0, WATER, 0.26e-3, 4.5) == pytest.approx(q, rel=1e-8)


def test_type3_roundtrip():
    d = 0.2
    hl = pf.head_loss(0.05, d, 1000.0, WATER, 0.045e-3).total_head_loss
    assert pf.diameter_for_head_loss(0.05, hl, 1000.0, WATER, 0.045e-3) == pytest.approx(d, rel=1e-8)


def test_pumping_power():
    res = pf.head_loss(0.02, 0.1, 200.0, WATER, 0.045e-3)
    assert res.pumping_power(0.8) == pytest.approx(res.pressure_drop * 0.02 / 0.8)


def test_hydraulic_diameter_square_duct():
    assert pf.hydraulic_diameter(0.04, 0.8) == pytest.approx(0.2)
