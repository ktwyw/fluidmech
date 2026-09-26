"""Water hammer: wave speeds, Joukowsky and slow-closure surge pressures."""

import pytest

from fluidmech import transients as t


def test_rigid_pipe_wave_speed():
    assert t.wave_speed(1000.0) == pytest.approx((2.2e9 / 1000) ** 0.5)


def test_elastic_pipe_slower():
    c = t.wave_speed(1000.0, diameter=0.3, wall_thickness=0.008, youngs_modulus=200e9)
    assert 1100 < c < t.wave_speed(1000.0)
    c_pvc = t.wave_speed(1000.0, diameter=0.3, wall_thickness=0.015, youngs_modulus=3e9)
    assert c_pvc < 500


def test_joukowsky_and_michaud():
    assert t.joukowsky_surge(1000, 1200, 2.0) == pytest.approx(2.4e6)
    tc = t.critical_closure_time(1200, 1200)
    assert tc == pytest.approx(2.0)
    assert t.surge_pressure(1000, 1200, 2.0, 1200, 1.0) == pytest.approx(2.4e6)
    assert t.surge_pressure(1000, 1200, 2.0, 1200, 10.0) == pytest.approx(2 * 1000 * 1200 * 2 / 10)
