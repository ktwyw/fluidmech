"""Turbulence, porous media, dimensional analysis, mixing, potential flow, rigid-body
hydrostatics, the standard atmosphere and drops/bubbles: limits, round trips and exact results."""

import math

import pytest

from fluidmech import Fluid, drag, hydrostatics, mixing, porous, potential_flow, properties, turbulence
from fluidmech import dimensional as dim

WATER = Fluid.water(20)


# --- turbulence ---------------------------------------------------------------
def test_law_of_the_wall_limits():
    assert turbulence.law_of_the_wall(2.0) == pytest.approx(2.0, rel=0.01)
    assert turbulence.law_of_the_wall(500.0) == pytest.approx(turbulence.log_law(500.0), rel=1e-3)
    assert turbulence.wall_region(15) == "buffer layer"


def test_mesh_sizing_and_entrance_length():
    u_tau = turbulence.friction_velocity(1.0, 1000.0)
    assert turbulence.wall_distance_for_y_plus(1.0, u_tau, 1e-6) == pytest.approx(1e-6 / u_tau)
    assert turbulence.entrance_length(1000, 0.01) == pytest.approx(0.6)
    assert turbulence.mean_to_max_velocity_ratio(7) == pytest.approx(0.8167, rel=1e-3)


# --- porous -------------------------------------------------------------------
def test_ergun_limits():
    args = dict(particle_diameter=0.002, voidage=0.4, sphericity=1.0)
    slow = porous.ergun_pressure_gradient(1e-6, mu=1e-3, density=1000.0, **args)
    kc = porous.kozeny_carman_pressure_gradient(1e-6, mu=1e-3, **args)
    assert slow / kc == pytest.approx(150 / 180, rel=1e-3)
    fast = porous.ergun_pressure_gradient(10.0, mu=1e-3, density=1000.0, **args)
    assert fast == pytest.approx(porous.burke_plummer_pressure_gradient(10.0, density=1000.0, **args), rel=0.01)


def test_min_fluidization_balances_bed_weight():
    u = porous.minimum_fluidization_velocity(500e-6, 2500, 1.2, 1.8e-5, voidage_mf=0.45)
    dp = porous.ergun_pressure_gradient(u, 500e-6, 0.45, 1.8e-5, 1.2)
    assert dp == pytest.approx(porous.fluidized_bed_pressure_drop(1.0, 0.45, 2500, 1.2), rel=1e-6)
    assert 0.1 < porous.minimum_fluidization_velocity(500e-6, 2500, 1.2, 1.8e-5) < 0.4


def test_filtration_round_trip():
    kw = dict(
        area=0.1,
        pressure_drop=2e5,
        mu=1e-3,
        specific_cake_resistance=1e11,
        solids_per_filtrate=20.0,
        medium_resistance=1e10,
    )
    times = [porous.filtration_time(v, **kw) for v in (0.002, 0.004, 0.006, 0.008)]
    assert porous.filtration_volume(times[2], **kw) == pytest.approx(0.006)
    alpha, rm, *_ = porous.filtration_constants_from_data(times, [0.002, 0.004, 0.006, 0.008], 0.1, 2e5, 1e-3, 20.0)
    assert alpha == pytest.approx(1e11) and rm == pytest.approx(1e10)


def test_membranes_and_units():
    pi = porous.vant_hoff_osmotic_pressure(600.0, 25.0, 2)  # ~0.6 M NaCl ~ seawater
    assert pi / 1e5 == pytest.approx(29.7, rel=0.01)
    assert porous.membrane_flux(10e5, 1e-3, 1e13) == pytest.approx(1e-4)  # 10 bar
    assert porous.membrane_flux(10e5, 1e-3, 1e13, osmotic_pressure_difference=10e5) == 0.0
    assert porous.lmh(1e-5) == pytest.approx(36.0)
    assert porous.DARCY == pytest.approx(9.869233e-13)


# --- dimensional analysis -----------------------------------------------------
def test_pipe_pi_groups():
    v = {
        "dp": "pressure",
        "rho": "density",
        "V": "velocity",
        "D": "diameter",
        "mu": "dynamic_viscosity",
        "L": "length",
        "eps": "roughness",
    }
    groups = dim.pi_groups(v)
    assert len(groups) == 4 == len(v) - dim.dimension_matrix_rank(v)
    assert all(dim.is_dimensionless(g, v) for g in groups)
    assert dim.format_group(groups[0]) == "dp rho^-1 V^-2"


def test_explicit_repeating_and_errors():
    v = {"F": "force", "rho": "density", "V": "velocity", "D": "length"}
    with pytest.raises(ValueError):
        dim.pi_groups(v, repeating=["rho", "V"])
    with pytest.raises(ValueError):
        dim.parse_dimension("M L^x")
    g = dim.pi_groups(v)[0]
    assert dim.evaluate_group(g, {"F": 10.0, "rho": 1.0, "V": 1.0, "D": 1.0}) == pytest.approx(10.0)


# --- mixing -------------------------------------------------------------------
def test_mixing_power_and_scale_up():
    assert mixing.power_number(1e6) == pytest.approx(5.0, rel=1e-3)
    assert mixing.power_number(0.1) == pytest.approx(705.0)
    n2 = mixing.scale_up_speed(5.0, 0.1, 1.0, "power_per_volume")
    p1 = mixing.impeller_power(5.0, 1000, 5.0, 0.1) / 0.1**3
    p2 = mixing.impeller_power(5.0, 1000, n2, 1.0) / 1.0**3
    assert p1 == pytest.approx(p2)
    assert mixing.micromixing_time(1.0, 1e-6) == pytest.approx(17.24e-3, rel=1e-3)


def test_reactor_conversions_order():
    da = 2.0
    cstr, lfr, pfr = mixing.cstr_conversion(da), mixing.laminar_flow_reactor_conversion(da), mixing.pfr_conversion(da)
    assert cstr < lfr < pfr
    assert mixing.tanks_in_series_conversion(da, 1) == pytest.approx(cstr)
    assert mixing.tanks_in_series_conversion(da, 2000) == pytest.approx(pfr, rel=1e-3)
    area = sum(mixing.laminar_rtd((i + 0.5) * 0.001, 1.0) * 0.001 for i in range(100000))
    assert area == pytest.approx(1.0, rel=1e-3)


# --- potential flow -----------------------------------------------------------
def test_cylinder_surface():
    f = potential_flow.cylinder(5.0, 0.5)
    for theta in (0.3, 1.0, 2.5):
        x, y = 0.5 * math.cos(theta), 0.5 * math.sin(theta)
        assert f.speed(x, y) == pytest.approx(2 * 5.0 * math.sin(theta))  # |u| = 2 U sin(theta)
        assert f.stream_function(x, y) == pytest.approx(0.0, abs=1e-12)  # surface is a streamline


def test_half_body_and_lift():
    hb = potential_flow.rankine_half_body(2.0, 3.0)
    x_s = -3.0 / (2 * math.pi * 2.0)
    u, v = hb.velocity(x_s, 0.0)
    assert u == pytest.approx(0.0, abs=1e-12) and v == 0
    assert potential_flow.kutta_joukowski_lift(1.2, 10.0, 5.0) == pytest.approx(60.0)
    # velocity equals the gradient of the potential
    flow = potential_flow.Uniform(1.0, 30) + potential_flow.Vortex(2.0, 1, 1) + potential_flow.Source(1.5)
    h = 1e-6
    dphidx = (flow.potential(0.7 + h, -0.4) - flow.potential(0.7 - h, -0.4)) / (2 * h)
    assert flow.velocity(0.7, -0.4)[0] == pytest.approx(dphidx, rel=1e-6)


# --- hydrostatics, properties, drag ------------------------------------------
def test_rigid_body_motion():
    assert hydrostatics.accelerating_surface_slope(9.80665) == pytest.approx(-1.0)
    tank = hydrostatics.RotatingTank(radius=0.3, initial_depth=0.4, omega=5.0)
    # volume conservation: mean surface height of the paraboloid equals the initial depth
    mean = sum(tank.surface_height(0.3 * math.sqrt((i + 0.5) / 1000)) for i in range(1000)) / 1000
    assert mean == pytest.approx(0.4, rel=1e-4)
    fast = hydrostatics.RotatingTank(0.3, 0.4, tank.speed_to_expose_bottom())
    assert fast.centre_depth == pytest.approx(0.0, abs=1e-12)


def test_standard_atmosphere():
    t, p, rho = properties.standard_atmosphere(11000.0)
    assert t == pytest.approx(-56.5, abs=0.01)
    assert p == pytest.approx(22632, rel=1e-3)


def test_bubbles_and_hindered_settling():
    stokes = drag.stokes_velocity(1e-4, 1.2, WATER)
    assert drag.hadamard_rybczynski_velocity(1e-4, 1.2, 0.0, WATER) == pytest.approx(1.5 * stokes)  # inviscid gas limit
    assert drag.mendelson_bubble_velocity(3e-3, 0.072, WATER) == pytest.approx(0.25, abs=0.01)
    assert drag.richardson_zaki_exponent(1e-3) == pytest.approx(4.7, rel=0.01)
    assert drag.hindered_settling_velocity(1.0, 1.0, 1.0) == 1.0
    assert drag.vortex_shedding_frequency(10.0, 0.5) == pytest.approx(4.0)
