"""Compressible flow, checked against the NACA 1135 isentropic and normal-shock tables
and against round trips through the inverse functions."""

import pytest

from fluidmech import compressible as c


@pytest.mark.parametrize(
    "mach, p, t, a",  # standard isentropic tables for k = 1.4
    [
        (0.5, 0.8430, 0.9524, 1.3398),
        (1.0, 0.5283, 0.8333, 1.0),
        (2.0, 0.1278, 0.5556, 1.6875),
        (3.0, 0.02722, 0.3571, 4.2346),
    ],
)
def test_isentropic_tables(mach, p, t, a):
    assert c.pressure_ratio(mach) == pytest.approx(p, rel=1e-3)
    assert c.temperature_ratio(mach) == pytest.approx(t, rel=1e-3)
    assert c.area_ratio(mach) == pytest.approx(a, rel=1e-3)


@pytest.mark.parametrize(
    "m1, m2, p21, t21, p0",  # normal-shock tables for k = 1.4
    [
        (1.5, 0.7011, 2.4583, 1.3202, 0.9298),
        (2.0, 0.5774, 4.5, 1.6875, 0.7209),
        (3.0, 0.4752, 10.333, 2.6790, 0.3283),
    ],
)
def test_normal_shock_tables(m1, m2, p21, t21, p0):
    s = c.normal_shock(m1)
    assert s.mach2 == pytest.approx(m2, rel=1e-3)
    assert s.pressure_ratio == pytest.approx(p21, rel=1e-3)
    assert s.temperature_ratio == pytest.approx(t21, rel=1e-3)
    assert s.stagnation_pressure_ratio == pytest.approx(p0, rel=1e-3)


def test_inverse_functions():
    assert c.mach_from_area_ratio(c.area_ratio(2.5), supersonic=True) == pytest.approx(2.5)
    assert c.mach_from_area_ratio(c.area_ratio(0.3)) == pytest.approx(0.3)
    assert c.mach_from_pressure_ratio(c.pressure_ratio(0.8)) == pytest.approx(0.8)
    s = c.normal_shock(2.2)
    assert c.pitot_mach_supersonic(s.pressure_ratio / c.pressure_ratio(s.mach2)) == pytest.approx(2.2)


def test_speed_of_sound():
    assert c.speed_of_sound(15.0) == pytest.approx(340.3, rel=1e-3)


def test_choked_and_subsonic_nozzle_flow():
    m_choked = c.choked_mass_flow(1e-4, 500e3, 20.0)
    # m = 0.0404 p0 A / sqrt(T0) for air
    assert m_choked == pytest.approx(0.04042 * 500e3 * 1e-4 / (293.15**0.5), rel=2e-3)
    assert c.nozzle_mass_flow(1e-4, 500e3, 101325.0, 20.0) == pytest.approx(m_choked)
    assert c.nozzle_mass_flow(1e-4, 120e3, 101325.0, 20.0) < m_choked
    # continuity at the critical ratio
    pr = c.critical_pressure_ratio()
    assert c.nozzle_mass_flow(1e-4, 200e3, 200e3 * pr * 1.000001) == pytest.approx(
        c.choked_mass_flow(1e-4, 200e3), rel=1e-4
    )


def test_invalid_inputs():
    with pytest.raises(ValueError):
        c.normal_shock(0.8)
    with pytest.raises(ValueError):
        c.mach_from_area_ratio(0.5)
