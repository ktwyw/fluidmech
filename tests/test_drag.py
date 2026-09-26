"""External flow: drag correlations against the standard drag curve, Blasius skin friction and
Stokes' law limits."""

import pytest

from fluidmech import Fluid, drag

WATER = Fluid.water(20)


def test_drag_force():
    assert drag.drag_force(1.0, 1.2, 10.0, 2.0) == pytest.approx(120.0)


def test_sphere_cd_limits():
    assert drag.sphere_drag_coefficient(0.01) == pytest.approx(24 / 0.01, rel=0.01)  # Stokes
    # standard drag curve (Clift, Grace & Weber 1978)
    assert drag.sphere_drag_coefficient(100) == pytest.approx(1.09, rel=0.03)
    assert drag.sphere_drag_coefficient(1e4) == pytest.approx(0.41, rel=0.03)


def test_cylinder_cd():
    assert drag.cylinder_drag_coefficient(1e4) == pytest.approx(1.0, abs=0.1)


def test_flat_plate_friction():
    assert drag.flat_plate_friction_coefficient(1e5) == pytest.approx(1.328 / 1e5**0.5)
    assert drag.flat_plate_friction_coefficient(1e7, "turbulent") == pytest.approx(0.074 / 1e7**0.2)
    mixed = drag.flat_plate_friction_coefficient(1e6)
    assert mixed < drag.flat_plate_friction_coefficient(1e6, "schlichting")


def test_boundary_layer_thickness():
    d = drag.boundary_layer_thickness(0.5, 1.0, 1e-5)  # Re_x = 5e4, laminar
    assert d == pytest.approx(4.91 * 0.5 / 5e4**0.5)


def test_terminal_velocity_stokes_regime_and_rising_bubble():
    u = drag.terminal_velocity(10e-6, 2650, WATER)
    assert u == pytest.approx(drag.stokes_velocity(10e-6, 2650, WATER), rel=0.02)
    assert drag.terminal_velocity(1e-3, 50, WATER) < 0  # buoyant sphere rises
    assert drag.terminal_velocity(1e-3, WATER.density, WATER) == 0.0
