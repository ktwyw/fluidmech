"""Dimensionless groups and flow-regime classification (hand-calculated values)."""

import math

import pytest

from fluidmech import dimensionless as dn


def test_reynolds():
    assert dn.reynolds(2.0, 0.1, 1e-6) == pytest.approx(2e5)


def test_froude_is_one_at_wave_speed():
    depth = 2.0
    assert dn.froude(math.sqrt(9.80665 * depth), depth) == pytest.approx(1.0)


def test_mach_weber_euler():
    assert dn.mach(170.0, 340.0) == pytest.approx(0.5)
    assert dn.weber(1000.0, 2.0, 0.01, 0.0728) == pytest.approx(549.45, rel=1e-4)
    assert dn.euler(500.0, 1000.0, 1.0) == pytest.approx(0.5)


@pytest.mark.parametrize("re, regime", [(1000, "laminar"), (3000, "transitional"), (1e5, "turbulent")])
def test_flow_regime(re, regime):
    assert dn.flow_regime(re) == regime


def test_invalid_viscosity_raises():
    with pytest.raises(ValueError):
        dn.reynolds(1.0, 1.0, 0.0)
