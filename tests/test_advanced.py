"""Advanced topics: MOC water hammer, Blasius, Rayleigh-Plesset, CFD solvers and publication plots.

Each result is checked against a classical reference: Joukowsky's surge, Blasius' constants,
Rayleigh's collapse time, Ghia et al. (1982), Taylor-Aris dispersion and physical plausibility.
"""

import math

import pytest

from fluidmech import cavitation, laminar, transients


def test_blasius_constants():
    b = laminar.blasius()
    assert b["fpp0"] == pytest.approx(0.332057, rel=1e-4)
    assert b["delta99"] == pytest.approx(4.91, abs=0.01)
    assert b["delta_star"] == pytest.approx(1.7208, rel=1e-3)
    assert b["theta"] == pytest.approx(0.6641, rel=1e-3)
    assert b["fp"][-1] == pytest.approx(1.0, abs=1e-6)


def test_moc_fast_closure_matches_joukowsky():
    r = transients.moc_valve_closure(600, 0.5, 1200, 0.0, 1.5, 100, closure_time=0.1, t_end=1.0)
    rise = max(r["head_valve"]) - r["head_valve"][0]
    assert rise == pytest.approx(1200 * 1.5 / 9.80665, rel=0.01)  # frictionless: exact Joukowsky


def test_moc_slow_closure_is_gentler_and_flow_stops():
    fast = transients.moc_valve_closure(600, 0.5, 1200, 0.018, 1.5, 100, 0.5, t_end=6)
    slow = transients.moc_valve_closure(600, 0.5, 1200, 0.018, 1.5, 100, 5.0, t_end=10)
    assert max(slow["head_valve"]) < max(fast["head_valve"])
    assert slow["flow_valve"][-1] == 0.0
    assert all(hmax >= hmin for hmax, hmin in zip(fast["head_max"], fast["head_min"]))


def test_rayleigh_collapse_time():
    dp = 1e5
    res = cavitation.rayleigh_plesset(1e-3, dp + 2.34e3, 2e-4, viscosity=0.0, surface_tension=0.0)
    assert res["t"][-1] == pytest.approx(cavitation.rayleigh_collapse_time(1e-3, 998.0, dp), rel=1e-3)


def test_gas_bubble_rebounds():
    res = cavitation.rayleigh_plesset(1e-3, 1e5, 3e-4, gas_pressure=5e3)
    r_min = min(res["R"])
    assert r_min > 0 and res["R"][-1] > 2 * r_min  # it collapses, then grows again


np = pytest.importorskip("numpy")
pytest.importorskip("scipy")
from fluidmech import cfd  # noqa: E402


def test_cavity_against_ghia_coarse():
    r = cfd.lid_driven_cavity(33, 100.0, t_end=20.0)
    uc = r["u"][:, 16]
    err = max(abs(np.interp(y, r["y"], uc) - u) for y, u in zip(cfd.GHIA_RE100_Y, cfd.GHIA_RE100_U))
    assert err < 0.02  # coarse 33x33 grid; the 65x65 showcase run agrees to 0.003
    assert r["psi"].min() == pytest.approx(-0.1034, rel=0.05)


def test_lbm_runs_and_stays_finite():
    snaps = list(cfd.lbm_cylinder(nx=120, ny=50, radius=5, steps=400, snapshot_every=200))
    assert len(snaps) == 2
    assert np.isfinite(snaps[-1]["u"]).all()
    assert 0.5 < snaps[-1]["tau"] < 1.0


def test_strouhal_from_synthetic_signal():
    period = 400
    sig = [math.sin(2 * math.pi * k / period) for k in range(20000)]
    assert cfd.strouhal_from_signal(sig, diameter=20, u_in=0.05) == pytest.approx(20 / period / 0.05, rel=1e-2)


def test_taylor_dispersion_matches_theory():
    ks = []
    for seed in (1, 2, 3):
        r = cfd.taylor_dispersion(peclet=10, particles=3000, t_end=5, snapshot_times=(), seed=seed)
        late = r["time"] > 2
        ks.append(np.polyfit(r["time"][late], r["variance"][late], 1)[0] / 2)
    assert np.mean(ks) == pytest.approx(r["theory_K"], rel=0.08)


def test_viz_helpers(tmp_path):
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    from fluidmech import Fluid, PumpCurve, pumps, viz

    with viz.style("paper"):
        fig, axes = viz.figure("double", ncols=3)
        viz.moody_chart(axes[0])
        pump = PumpCurve.from_points([0, 0.04, 0.08, 0.12], [42, 40, 33.5, 22.5])
        viz.pump_system_chart(
            axes[1], pump, pumps.system_curve(12, 0.25, 800, Fluid.water(20), 0.26e-3), 0.14, speeds=(1.0, 0.8, 0.5)
        )
        viz.drag_curve_chart(axes[2], [(1, 27), (100, 1.1)])
        viz.label_panels(axes)
        files = viz.savefig(fig, tmp_path / "fig", ("pdf", "png", "svg"))
    assert all(f.exists() and f.stat().st_size > 1000 for f in files)
    with pytest.raises(ValueError):
        with viz.style("magazine"):
            pass
