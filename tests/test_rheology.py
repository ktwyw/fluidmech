"""Rheology models: fitted parameters must recover those used to generate the data."""

import pytest

from fluidmech import rheology as rh

RATES = [1.0, 5.0, 10.0, 50.0, 100.0, 500.0]


def test_models_basic():
    assert rh.Newtonian(0.01).stress(10) == pytest.approx(0.1)
    pl = rh.PowerLaw(2.0, 0.5)
    assert pl.apparent_viscosity(4.0) == pytest.approx(1.0)
    assert pl.behaviour.startswith("shear-thinning")
    assert rh.Bingham(10.0, 0.1).stress(100.0) == pytest.approx(20.0)
    assert rh.HerschelBulkley(5.0, 2.0, 1.0).stress(3.0) == pytest.approx(11.0)


def test_carreau_limits():
    c = rh.Carreau(mu_0=10.0, mu_inf=0.01, lam=1.0, n=0.4)
    assert c.apparent_viscosity(0.0) == pytest.approx(10.0)
    assert c.apparent_viscosity(1e12) == pytest.approx(0.01, rel=0.01)


@pytest.mark.parametrize(
    "model, fitter",
    [
        (rh.PowerLaw(3.2, 0.45), rh.fit_power_law),
        (rh.Bingham(12.0, 0.08), rh.fit_bingham),
        (rh.HerschelBulkley(4.0, 1.5, 0.7), rh.fit_herschel_bulkley),
    ],
)
def test_fits_recover_parameters(model, fitter):
    stresses = [model.stress(g) for g in RATES]
    fitted = fitter(RATES, stresses)
    for field in model.__dataclass_fields__:
        assert getattr(fitted, field) == pytest.approx(getattr(model, field), rel=0.01)
    assert rh.r_squared(fitted, RATES, stresses) == pytest.approx(1.0, abs=1e-6)


def test_andrade_matches_water_viscosity():
    from fluidmech.properties import water_dynamic_viscosity

    ts = [10, 20, 30, 40, 50]
    a = rh.Andrade.fit(ts, [water_dynamic_viscosity(t) for t in ts])
    # Andrade is only approximate for water (about 1 % error here)
    assert a.viscosity(25) == pytest.approx(water_dynamic_viscosity(25), rel=0.02)
    two = rh.Andrade.from_two_points(20, 1.0e-3, 60, 0.47e-3)
    assert two.viscosity(20) == pytest.approx(1.0e-3)
    assert two.viscosity(60) == pytest.approx(0.47e-3)
