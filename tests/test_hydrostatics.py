"""Hydrostatics: gate forces and centres of pressure against textbook closed forms,
buoyancy and manometers."""

import pytest

from fluidmech import hydrostatics as hs
from fluidmech.constants import G


def test_pressure_at_depth():
    assert hs.pressure_at_depth(10.0) == pytest.approx(1000 * G * 10)
    assert hs.pressure_at_depth(0.0, surface_pressure=101325) == 101325


def test_vertical_rectangular_gate_from_surface():
    # Classic result: force = rho g (h/2) (b h), centre of pressure at 2h/3.
    res = hs.rectangular_gate(width=1.0, height=2.0, top_depth=0.0)
    assert res.force == pytest.approx(1000 * G * 1.0 * 2.0)
    assert res.center_of_pressure_depth == pytest.approx(4.0 / 3.0)


def test_submerged_gate_center_of_pressure_below_centroid():
    res = hs.rectangular_gate(width=2.0, height=1.0, top_depth=3.0)
    assert res.centroid_depth == pytest.approx(3.5)
    assert res.center_of_pressure_depth > res.centroid_depth
    assert res.center_of_pressure_depth == pytest.approx(3.5 + (2 * 1**3 / 12) / (3.5 * 2))


def test_inclined_gate_force_matches_vertical_projection_depth():
    res = hs.rectangular_gate(width=1.0, height=2.0, top_depth=0.0, angle_deg=30.0)
    # centroid depth = 1.0 * sin(30) = 0.5 m
    assert res.centroid_depth == pytest.approx(0.5)
    assert res.force == pytest.approx(1000 * G * 0.5 * 2.0)
    assert res.center_of_pressure_slant == pytest.approx(4.0 / 3.0)


def test_circular_gate():
    res = hs.circular_gate(diameter=1.0, top_depth=1.0)
    assert res.centroid_depth == pytest.approx(1.5)
    assert res.center_of_pressure_depth == pytest.approx(1.5 + 1.0 / (16 * 1.5))


def test_buoyancy():
    assert hs.buoyant_force(1.0) == pytest.approx(1000 * G)
    assert hs.submerged_fraction(917.0, 1025.0) == pytest.approx(0.8946, rel=1e-3)
    assert hs.submerged_fraction(7850.0) == 1.0


def test_manometer():
    # Mercury (13600) under water, 0.1 m reading
    assert hs.manometer_pressure_difference(0.1, 13600, 1000) == pytest.approx(12600 * G * 0.1)
