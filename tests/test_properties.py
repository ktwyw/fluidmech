"""Fluid properties against steam tables, NIST data and the standard atmosphere."""

import pytest

from fluidmech.properties import (
    Fluid,
    air_density,
    air_dynamic_viscosity,
    water_density,
    water_dynamic_viscosity,
    water_kinematic_viscosity,
)


@pytest.mark.parametrize(
    "temperature, expected",
    [(4.0, 1000.0), (20.0, 998.2), (50.0, 988.0), (80.0, 971.8)],
)
def test_water_density_matches_tables(temperature, expected):
    assert water_density(temperature) == pytest.approx(expected, rel=2e-3)


@pytest.mark.parametrize(
    "temperature, expected",
    [(10.0, 1.307e-3), (20.0, 1.002e-3), (40.0, 0.653e-3), (80.0, 0.355e-3)],
)
def test_water_viscosity_matches_tables(temperature, expected):
    assert water_dynamic_viscosity(temperature) == pytest.approx(expected, rel=0.03)


def test_water_kinematic_viscosity_20c():
    assert water_kinematic_viscosity(20.0) == pytest.approx(1.004e-6, rel=0.01)


def test_water_out_of_range_raises():
    with pytest.raises(ValueError):
        water_density(150.0)


def test_air_properties_standard_conditions():
    assert air_density(15.0) == pytest.approx(1.225, rel=1e-3)
    assert air_dynamic_viscosity(15.0) == pytest.approx(1.789e-5, rel=0.01)


def test_fluid_factory_and_derived_properties():
    water = Fluid.water(20)
    assert water.kinematic_viscosity == pytest.approx(water_kinematic_viscosity(20))
    assert water.specific_weight == pytest.approx(9790, rel=1e-3)
    assert "water" in water.name


def test_fluid_rejects_nonphysical_values():
    with pytest.raises(ValueError):
        Fluid(density=-1.0, dynamic_viscosity=1e-3)


from fluidmech.properties import water_surface_tension, water_vapor_pressure  # noqa: E402


@pytest.mark.parametrize("t, pv", [(20.0, 2339.0), (50.0, 12352.0), (100.0, 101325.0)])
def test_vapor_pressure_steam_tables(t, pv):
    assert water_vapor_pressure(t) == pytest.approx(pv, rel=0.01)


def test_surface_tension():
    assert water_surface_tension(20.0) == pytest.approx(0.0728, rel=0.01)
