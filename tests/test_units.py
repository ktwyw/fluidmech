"""Unit conversions against exact definitions, round trips and error handling."""

import pytest

from fluidmech.units import available_units, convert, to_si


@pytest.mark.parametrize(
    "value, a, b, expected",
    [
        (1, "ft", "m", 0.3048),
        (1, "psi", "Pa", 6894.757),
        (1, "cfs", "L/s", 28.3168),
        (1, "hp", "kW", 0.7457),
        (10, "mH2O", "kPa", 98.0665),
        (1, "atm", "bar", 1.01325),
        (1, "mgd", "L/s", 43.8126),
        (100, "degC", "degF", 212.0),
        (0, "degC", "K", 273.15),
        (1, "cP", "Pa*s", 0.001),
    ],
)
def test_conversions(value, a, b, expected):
    assert convert(value, a, b) == pytest.approx(expected, rel=1e-5)


def test_round_trip():
    assert convert(convert(123.4, "gpm", "m3/h"), "m3/h", "gpm") == pytest.approx(123.4)


def test_to_si():
    assert to_si(1.0, "in") == pytest.approx(0.0254)


def test_incompatible_units():
    with pytest.raises(ValueError):
        convert(1, "m", "psi")
    with pytest.raises(ValueError):
        convert(1, "degC", "m")
    with pytest.raises(ValueError):
        convert(1, "furlong", "m")
    assert "gpm" in available_units()
