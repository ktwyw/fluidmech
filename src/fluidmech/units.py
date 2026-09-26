"""Unit conversion to and from SI for common fluid mechanics quantities.

Examples
--------
>>> round(convert(100, "gpm", "L/s"), 3)
6.309
>>> round(convert(30, "psi", "kPa"), 2)
206.84
>>> convert(68, "degF", "degC")
20.0
"""

from __future__ import annotations

_FT = 0.3048  # exact international definitions
_IN = 0.0254
_GAL = 3.785411784e-3  # US gallon [m3]
_G = 9.80665

UNITS: dict[str, dict[str, float]] = {
    "length": {
        "m": 1.0,
        "mm": 1e-3,
        "cm": 1e-2,
        "km": 1e3,
        "in": _IN,
        "ft": _FT,
        "yd": 0.9144,
        "mi": 1609.344,
    },
    "area": {
        "m2": 1.0,
        "cm2": 1e-4,
        "mm2": 1e-6,
        "ft2": _FT**2,
        "in2": _IN**2,
        "ha": 1e4,
        "acre": 4046.8564224,
    },
    "volume": {
        "m3": 1.0,
        "L": 1e-3,
        "mL": 1e-6,
        "gal": _GAL,
        "ft3": _FT**3,
        "in3": _IN**3,
        "bbl": 0.158987294928,
    },
    "flow_rate": {
        "m3/s": 1.0,
        "m3/h": 1 / 3600,
        "m3/day": 1 / 86400,
        "L/s": 1e-3,
        "L/min": 1e-3 / 60,
        "gpm": _GAL / 60,
        "cfs": _FT**3,
        "cfm": _FT**3 / 60,
        "mgd": 1e6 * _GAL / 86400,
    },
    "velocity": {"m/s": 1.0, "km/h": 1 / 3.6, "ft/s": _FT, "mph": 0.44704, "knot": 1852 / 3600},
    "pressure": {
        "Pa": 1.0,
        "kPa": 1e3,
        "MPa": 1e6,
        "bar": 1e5,
        "mbar": 100.0,
        "atm": 101325.0,
        "psi": 6894.757293168,
        "mH2O": 1000 * _G,
        "ftH2O": 1000 * _G * _FT,
        "inH2O": 1000 * _G * _IN,
        "mmHg": 133.322387415,
        "inHg": 3386.388640341,
    },
    "force": {"N": 1.0, "kN": 1e3, "MN": 1e6, "lbf": 4.4482216152605, "kgf": _G},
    "power": {"W": 1.0, "kW": 1e3, "MW": 1e6, "hp": 745.69987158227, "ft*lbf/s": 1.3558179483314},
    "density": {"kg/m3": 1.0, "g/cm3": 1e3, "lb/ft3": 16.018463373960, "slug/ft3": 515.378818},
    "dynamic_viscosity": {"Pa*s": 1.0, "cP": 1e-3, "P": 0.1, "lbf*s/ft2": 47.880258888889},
    "kinematic_viscosity": {"m2/s": 1.0, "cSt": 1e-6, "St": 1e-4, "ft2/s": _FT**2},
    "mass": {"kg": 1.0, "g": 1e-3, "t": 1e3, "lb": 0.45359237, "slug": 14.593902937},
}

_TEMPERATURE = {"degC", "degF", "K", "degR"}


def _dimension_of(unit: str) -> str:
    for dim, table in UNITS.items():
        if unit in table:
            return dim
    raise ValueError(f"Unknown unit {unit!r}. Known units: {', '.join(sorted(available_units()))}")


def available_units() -> list[str]:
    """All unit symbols understood by :func:`convert`."""
    names = [u for table in UNITS.values() for u in table]
    return names + sorted(_TEMPERATURE)


def _to_kelvin(value: float, unit: str) -> float:
    return {"K": value, "degC": value + 273.15, "degF": (value - 32) * 5 / 9 + 273.15, "degR": value * 5 / 9}[unit]


def _from_kelvin(value: float, unit: str) -> float:
    return {"K": value, "degC": value - 273.15, "degF": (value - 273.15) * 9 / 5 + 32, "degR": value * 9 / 5}[unit]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` between two units of the same kind (see :data:`UNITS`)."""
    if from_unit in _TEMPERATURE or to_unit in _TEMPERATURE:
        if not (from_unit in _TEMPERATURE and to_unit in _TEMPERATURE):
            raise ValueError("Cannot convert between temperature and a non-temperature unit.")
        return round(_from_kelvin(_to_kelvin(value, from_unit), to_unit), 12)
    dim_from, dim_to = _dimension_of(from_unit), _dimension_of(to_unit)
    if dim_from != dim_to:
        raise ValueError(f"Cannot convert {dim_from} ({from_unit}) to {dim_to} ({to_unit}).")
    return value * UNITS[dim_from][from_unit] / UNITS[dim_to][to_unit]


def to_si(value: float, unit: str) -> float:
    """Convert ``value`` in ``unit`` to the SI base unit of that quantity."""
    if unit in _TEMPERATURE:
        return convert(value, unit, "degC")
    return value * UNITS[_dimension_of(unit)][unit]
