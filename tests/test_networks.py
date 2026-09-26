"""Pipe-network solver: agreement with single-pipe Type-2 solutions, the Hardy Cross example,
pump operating points, continuity at every node and energy balance around loops."""

import math

import pytest

from fluidmech import Fluid, Network, PumpCurve, pumps
from fluidmech import pipe_flow as pf

WATER = Fluid.water(20)


def test_single_pipe_between_reservoirs_matches_type2():
    net = Network(WATER)
    net.add_reservoir("R1", 100.0)
    net.add_reservoir("R2", 80.0)
    net.add_pipe("P", "R1", "R2", 1000.0, 0.2, 0.045e-3, k_minor=1.5)
    res = net.solve()
    expected = pf.flow_rate_for_head_loss(20.0, 0.2, 1000.0, WATER, 0.045e-3, 1.5)
    assert res.flows["P"] == pytest.approx(expected, rel=1e-8)


def test_reversed_pipe_definition_gives_negative_flow():
    net = Network(WATER)
    net.add_reservoir("R1", 100.0)
    net.add_reservoir("R2", 80.0)
    net.add_pipe("P", "R2", "R1", 1000.0, 0.2, 0.045e-3)
    assert net.solve().flows["P"] < 0


def test_two_loop_network_matches_hardy_cross_and_continuity():
    net = Network(WATER)
    net.add_reservoir("A", 50.0)
    for n, d in [("B", 0), ("C", 0.03), ("D", 0.03), ("E", 0), ("F", 0.06)]:
        net.add_junction(n, demand=d)
    eps = 0.26e-3
    for name, a, b, length, dia in [
        ("AB", "A", "B", 600, 0.25),
        ("BC", "B", "C", 600, 0.15),
        ("AD", "A", "D", 400, 0.20),
        ("BE", "B", "E", 400, 0.15),
        ("CF", "C", "F", 400, 0.10),
        ("DE", "D", "E", 600, 0.15),
        ("EF", "E", "F", 600, 0.20),
    ]:
        net.add_pipe(name, a, b, length, dia, eps)
    res = net.solve()
    assert res.flows["AB"] == pytest.approx(0.06653, abs=2e-5)  # Hardy Cross, example 17
    assert res.flows["CF"] == pytest.approx(0.00479, abs=2e-5)
    assert res.max_continuity_error < 1e-12
    assert res.reservoir_outflows["A"] == pytest.approx(0.12)
    # energy around loop I sums to zero
    loop = res.head_losses["AB"] + res.head_losses["BE"] - res.head_losses["DE"] - res.head_losses["AD"]
    assert loop == pytest.approx(0.0, abs=1e-8)


def test_three_reservoir_problem_balances():
    net = Network(WATER)
    net.add_reservoir("R1", 120.0)
    net.add_reservoir("R2", 100.0)
    net.add_reservoir("R3", 70.0)
    net.add_junction("J", elevation=60.0)
    net.add_pipe("P1", "R1", "J", 1500, 0.30, 0.26e-3)
    net.add_pipe("P2", "J", "R2", 1000, 0.20, 0.26e-3)
    net.add_pipe("P3", "J", "R3", 1200, 0.25, 0.26e-3)
    res = net.solve()
    assert res.flows["P1"] == pytest.approx(res.flows["P2"] + res.flows["P3"], rel=1e-9)
    assert 70.0 < res.heads["J"] < 120.0


def test_pump_in_network_matches_operating_point():
    curve = PumpCurve(40.0, 0.0, -1500.0)
    net = Network(WATER)
    net.add_reservoir("Sump", 0.0)
    net.add_reservoir("Tank", 15.0)
    net.add_junction("Out", elevation=0.0)
    net.add_pump("Pump", "Sump", "Out", curve)
    net.add_pipe("Main", "Out", "Tank", 400.0, 0.2, 0.26e-3, k_minor=4.85)
    res = net.solve()
    op = pumps.operating_point(curve, pumps.system_curve(15.0, 0.2, 400.0, WATER, 0.26e-3, 4.85))
    assert res.flows["Pump"] == pytest.approx(op.flow_rate, rel=1e-6)
    assert res.head_losses["Pump"] == pytest.approx(-op.head, rel=1e-6)


def test_dead_end_zero_flow_branch():
    net = Network(WATER)
    net.add_reservoir("R", 30.0)
    net.add_junction("J1", demand=0.01)
    net.add_junction("J2", demand=0.0)
    net.add_pipe("P1", "R", "J1", 300, 0.1, 0.0)
    net.add_pipe("P2", "J1", "J2", 100, 0.05, 0.0)
    res = net.solve()
    assert res.flows["P2"] == pytest.approx(0.0, abs=1e-12)
    assert res.heads["J2"] == pytest.approx(res.heads["J1"], abs=1e-6)


def test_invalid_networks():
    net = Network(WATER)
    with pytest.raises(ValueError):
        net.solve()
    net.add_junction("J")
    with pytest.raises(ValueError):
        net.add_pipe("P", "J", "missing", 10, 0.1)
    with pytest.raises(ValueError):
        net.add_junction("J")


def test_summary_is_text():
    net = Network(WATER)
    net.add_reservoir("R", 10.0)
    net.add_junction("J", demand=0.001)
    net.add_pipe("P", "R", "J", 50, 0.05)
    text = net.solve().summary()
    assert "Converged" in text and "P" in text
    assert not math.isnan(net.solve().pressures["J"])
