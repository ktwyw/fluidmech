"""Bernoulli-equation devices: Torricelli, Pitot, Venturi and tank draining, checked against
closed-form results derived from Bernoulli plus continuity."""

import math

import pytest

from fluidmech import bernoulli as b
from fluidmech.constants import G


def test_torricelli():
    assert b.torricelli_velocity(5.0) == pytest.approx(math.sqrt(2 * G * 5))


def test_total_head_conserved_between_two_points():
    # Tank free surface (p=0, V=0, z=10) -> jet at z=0 (p=0)
    h1 = b.total_head(0.0, 0.0, 10.0)
    v2 = b.torricelli_velocity(10.0)
    h2 = b.total_head(0.0, v2, 0.0)
    assert h1 == pytest.approx(h2)


def test_pitot():
    assert b.pitot_velocity(0.5 * 1.225 * 30**2) == pytest.approx(30.0)


def test_venturi_ideal_matches_continuity_and_bernoulli():
    d1, d2, q = 0.1, 0.05, 0.01
    v1 = q / (math.pi * d1**2 / 4)
    v2 = q / (math.pi * d2**2 / 4)
    dp = 0.5 * 1000 * (v2**2 - v1**2)
    assert b.venturi_flow_rate(d1, d2, dp, discharge_coefficient=1.0) == pytest.approx(q)


def test_venturi_invalid_geometry():
    with pytest.raises(ValueError):
        b.venturi_flow_rate(0.05, 0.1, 1000.0)


def test_tank_drain_time_full_and_partial():
    full = b.tank_drain_time(1.0, 0.001, 4.0, discharge_coefficient=1.0)
    assert full == pytest.approx(2 * 1.0 / (0.001 * math.sqrt(2 * G)) * 2.0)
    half = b.tank_drain_time(1.0, 0.001, 4.0, 1.0, discharge_coefficient=1.0)
    assert half == pytest.approx(full / 2)
