"""Open-channel flow: geometry, critical depth (closed form), normal-depth round trips,
jumps, weirs, gates and gradually-varied-flow profiles."""

import pytest

from fluidmech.constants import G
from fluidmech.open_channel import (
    RectangularChannel,
    TrapezoidalChannel,
    hydraulic_jump_depth,
)


def test_trapezoid_geometry():
    ch = TrapezoidalChannel(bottom_width=3.0, side_slope=2.0)
    y = 1.5
    assert ch.area(y) == pytest.approx((3 + 2 * 1.5) * 1.5)
    assert ch.top_width(y) == pytest.approx(3 + 2 * 2 * 1.5)
    assert ch.wetted_perimeter(y) == pytest.approx(3 + 2 * 1.5 * 5**0.5)


def test_rectangular_critical_depth_closed_form():
    ch = RectangularChannel(width=4.0)
    q = 10.0
    yc = (q / 4.0) ** (2 / 3) / G ** (1 / 3)
    assert ch.critical_depth(q) == pytest.approx(yc, rel=1e-9)
    assert ch.froude(yc, q) == pytest.approx(1.0)
    # Minimum specific energy in a rectangular channel is 1.5 yc
    assert ch.specific_energy(yc, q) == pytest.approx(1.5 * yc)


def test_normal_depth_roundtrip():
    ch = TrapezoidalChannel(bottom_width=5.0, side_slope=1.5)
    q = ch.discharge(1.2, 0.015, 0.001)
    assert ch.normal_depth(q, 0.015, 0.001) == pytest.approx(1.2, rel=1e-9)


def test_flow_type_classification():
    ch = RectangularChannel(width=2.0)
    q = 5.0
    yc = ch.critical_depth(q)
    assert ch.flow_type(2 * yc, q) == "subcritical"
    assert ch.flow_type(0.5 * yc, q) == "supercritical"
    assert ch.flow_type(yc, q) == "critical"


def test_hydraulic_jump():
    y2 = hydraulic_jump_depth(0.5, 3.0)
    assert y2 == pytest.approx(0.5 * 0.5 * ((1 + 8 * 9) ** 0.5 - 1))
    with pytest.raises(ValueError):
        hydraulic_jump_depth(0.5, 0.8)


def test_invalid_channel():
    with pytest.raises(ValueError):
        TrapezoidalChannel(bottom_width=0.0, side_slope=0.0)


from fluidmech.open_channel import (  # noqa: E402
    broad_crested_weir_flow,
    classify_profile,
    gvf_profile,
    hydraulic_jump_energy_loss,
    rectangular_weir_flow,
    sluice_gate_flow,
    v_notch_weir_flow,
)


def test_jump_energy_loss_equals_specific_energy_difference():
    ch = RectangularChannel(1.0)
    y1, fr1 = 0.4, 5.0
    q = fr1 * (G * y1) ** 0.5 * y1
    y2 = hydraulic_jump_depth(y1, fr1)
    assert hydraulic_jump_energy_loss(y1, y2) == pytest.approx(ch.specific_energy(y1, q) - ch.specific_energy(y2, q))


def test_weirs_and_gate():
    assert rectangular_weir_flow(0.2, 1.0) == pytest.approx(0.62 * 2 / 3 * (2 * G) ** 0.5 * 0.2**1.5)
    assert v_notch_weir_flow(0.1) == pytest.approx(0.58 * 8 / 15 * (2 * G) ** 0.5 * 0.1**2.5)
    # broad-crested weir with Cd = 1 passes critical flow over the crest
    q = broad_crested_weir_flow(0.6, 2.0, discharge_coefficient=1.0)
    assert RectangularChannel(2.0).critical_depth(q) == pytest.approx(0.4)
    assert sluice_gate_flow(0.5, 3.0, 4.0) == pytest.approx(0.61 * 4 * 0.5 * (2 * G * 3) ** 0.5)
    with pytest.raises(ValueError):
        sluice_gate_flow(3.0, 2.0, 1.0)


def test_profile_classification():
    ch = TrapezoidalChannel(4.0, 1.5)
    q, n = 25.0, 0.012
    assert classify_profile(ch, q, n, 0.0008, 2.8) == "M1"
    assert classify_profile(ch, q, n, 0.0008, 1.4) == "M2"
    assert classify_profile(ch, q, n, 0.0008, 1.0) == "M3"
    assert classify_profile(ch, q, n, 0.02, 1.0) == "S2"
    assert classify_profile(ch, q, n, 0.0, 2.0) == "H2"
    assert classify_profile(ch, q, n, -0.001, 1.0) == "A3"


def test_m1_backwater_profile():
    ch = TrapezoidalChannel(4.0, 1.5)
    q, n, s0 = 25.0, 0.012, 0.0008
    yn = ch.normal_depth(q, n, s0)
    prof = gvf_profile(ch, q, n, s0, 2.8, 1.01 * yn, steps=40)
    xs = [x for x, _ in prof]
    assert all(b < a for a, b in zip(xs, xs[1:]))  # computed upstream: x decreasing
    assert prof[-1][0] == pytest.approx(-2316, rel=0.01)
    # finer steps converge to the same length
    fine = gvf_profile(ch, q, n, s0, 2.8, 1.01 * yn, steps=400)
    assert fine[-1][0] == pytest.approx(prof[-1][0], rel=0.01)
