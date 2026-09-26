"""Pump curves: fitting, affinity laws, series/parallel combination, operating point and NPSH."""

import pytest

from fluidmech import Fluid, PumpCurve, pumps

WATER = Fluid.water(20)


@pytest.fixture
def pump():
    return PumpCurve.from_points([0.0, 0.05, 0.10], [40.0, 36.25, 25.0], [0.0, 0.75, 0.60])


def test_fit_reproduces_points(pump):
    assert pump.head(0.0) == pytest.approx(40.0)
    assert pump.head(0.10) == pytest.approx(25.0)
    assert pump.efficiency(0.05) == pytest.approx(0.75)


def test_max_flow_and_bep(pump):
    assert pump.head(pump.max_flow()) == pytest.approx(0.0, abs=1e-9)
    q_bep = pump.best_efficiency_point()
    assert pump.efficiency(q_bep) >= pump.efficiency(q_bep * 1.1)
    assert pump.efficiency(q_bep) >= pump.efficiency(q_bep * 0.9)


def test_affinity_laws(pump):
    fast = pump.scaled(speed_ratio=1.2)
    q = 0.06
    assert fast.head(q * 1.2) == pytest.approx(pump.head(q) * 1.44)
    assert fast.efficiency(q * 1.2) == pytest.approx(pump.efficiency(q))


def test_series_and_parallel(pump):
    assert pump.in_series(2).head(0.05) == pytest.approx(2 * pump.head(0.05))
    assert pump.in_parallel(3).head(0.15) == pytest.approx(pump.head(0.05))


def test_operating_point_matches_curves(pump):
    system = pumps.system_curve(15.0, 0.2, 400.0, WATER, 0.26e-3, 4.85)
    op = pumps.operating_point(pump, system, WATER.density)
    assert op.head == pytest.approx(system(op.flow_rate), rel=1e-8)
    assert op.head == pytest.approx(pump.head(op.flow_rate))
    assert op.shaft_power == pytest.approx(WATER.density * 9.80665 * op.flow_rate * op.head / op.efficiency)


def test_operating_point_impossible_static_head(pump):
    with pytest.raises(ValueError):
        pumps.operating_point(pump, lambda q: 50.0 + q)


def test_npsh_available():
    # 20 degC water, surface 2 m below the pump, 0.5 m suction losses:
    # (101325 - 2339)/(998.2*9.80665) - 2 - 0.5 = 7.61 m
    assert pumps.npsh_available(-2.0, 0.5) == pytest.approx(7.61, abs=0.02)


def test_specific_speed_classification():
    assert pumps.pump_type(1450, 0.05, 50) == "radial (centrifugal)"
    assert pumps.pump_type(1450, 2.0, 3.0) == "axial flow"
