"""Fluid properties of water and air.

Correlations
------------
* Water density: Tanaka et al. (2001) fit, valid 0-40 degC and
  accurate to about 0.1 % up to 100 degC.
* Water viscosity: Vogel equation, accurate to a few percent for 0-100 degC.
* Air density: ideal-gas law with the specific gas constant of dry air.
* Air viscosity: Sutherland's law.
* Water vapour pressure: Antoine equation.
* Water surface tension: IAPWS (1994) correlation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import KELVIN_OFFSET, P_ATM, R_AIR


def _check_water_range(temperature: float) -> None:
    if not 0.0 <= temperature <= 100.0:
        raise ValueError("Water correlations are valid for 0-100 degC only.")


def water_density(temperature: float = 20.0) -> float:
    """Density of liquid water [kg/m^3] at ``temperature`` [degC]."""
    _check_water_range(temperature)
    t = temperature
    return 1000.0 * (1.0 - (t + 288.9414) / (508929.2 * (t + 68.12963)) * (t - 3.9863) ** 2)


def water_dynamic_viscosity(temperature: float = 20.0) -> float:
    """Dynamic viscosity of liquid water [Pa s] at ``temperature`` [degC]."""
    _check_water_range(temperature)
    t_k = temperature + KELVIN_OFFSET
    return 2.414e-5 * 10.0 ** (247.8 / (t_k - 140.0))  # Vogel equation constants for water


def water_kinematic_viscosity(temperature: float = 20.0) -> float:
    """Kinematic viscosity of liquid water [m^2/s] at ``temperature`` [degC]."""
    return water_dynamic_viscosity(temperature) / water_density(temperature)


def water_vapor_pressure(temperature: float = 20.0) -> float:
    """Saturation vapour pressure of water [Pa] (Antoine equation, 1-100 degC).

    Needed for cavitation checks: liquid boils where the absolute pressure
    falls to this value.
    """
    _check_water_range(temperature)
    # Antoine constants for water (1-100 degC), result in mmHg
    mmhg = 10.0 ** (8.07131 - 1730.63 / (233.426 + temperature))
    return mmhg * 133.322  # mmHg -> Pa


def water_surface_tension(temperature: float = 20.0) -> float:
    """Surface tension of water against air [N/m] (IAPWS correlation)."""
    _check_water_range(temperature)
    tau = 1.0 - (temperature + KELVIN_OFFSET) / 647.096  # 647.096 K = critical temperature of water
    return 0.2358 * tau**1.256 * (1.0 - 0.625 * tau)


def air_density(temperature: float = 20.0, pressure: float = P_ATM) -> float:
    """Density of dry air [kg/m^3] from the ideal-gas law."""
    t_k = temperature + KELVIN_OFFSET
    if t_k <= 0.0:
        raise ValueError("Absolute temperature must be positive.")
    return pressure / (R_AIR * t_k)


def air_dynamic_viscosity(temperature: float = 20.0) -> float:
    """Dynamic viscosity of air [Pa s] from Sutherland's law."""
    mu0, t0, s = 1.716e-5, 273.15, 110.4  # Sutherland constants for air: reference viscosity, T0, S [K]
    t_k = temperature + KELVIN_OFFSET
    if t_k <= 0.0:
        raise ValueError("Absolute temperature must be positive.")
    return mu0 * (t_k / t0) ** 1.5 * (t0 + s) / (t_k + s)


def air_kinematic_viscosity(temperature: float = 20.0, pressure: float = P_ATM) -> float:
    """Kinematic viscosity of air [m^2/s]."""
    return air_dynamic_viscosity(temperature) / air_density(temperature, pressure)


@dataclass(frozen=True)
class Fluid:
    """A Newtonian fluid described by its density and dynamic viscosity.

    Examples
    --------
    >>> water = Fluid.water(20)
    >>> round(water.density, 1)
    998.2
    """

    density: float
    """Density [kg/m^3]."""
    dynamic_viscosity: float
    """Dynamic viscosity [Pa s]."""
    name: str = "fluid"

    def __post_init__(self) -> None:
        if self.density <= 0 or self.dynamic_viscosity <= 0:
            raise ValueError("Density and viscosity must be positive.")

    @property
    def kinematic_viscosity(self) -> float:
        """Kinematic viscosity [m^2/s]."""
        return self.dynamic_viscosity / self.density

    @property
    def specific_weight(self) -> float:
        """Specific weight rho*g [N/m^3]."""
        from .constants import G

        return self.density * G

    @classmethod
    def water(cls, temperature: float = 20.0) -> Fluid:
        """Liquid water at ``temperature`` [degC]."""
        return cls(
            water_density(temperature),
            water_dynamic_viscosity(temperature),
            f"water @ {temperature:g} degC",
        )

    @classmethod
    def air(cls, temperature: float = 20.0, pressure: float = P_ATM) -> Fluid:
        """Dry air at ``temperature`` [degC] and ``pressure`` [Pa]."""
        return cls(
            air_density(temperature, pressure),
            air_dynamic_viscosity(temperature),
            f"air @ {temperature:g} degC",
        )


def standard_atmosphere(altitude: float) -> tuple[float, float, float]:
    """International Standard Atmosphere (troposphere, 0-11 km).

    Returns (temperature [degC], pressure [Pa], density [kg/m^3]) at ``altitude`` [m].
    T = 288.15 - 0.0065 z,  p = 101325 (T / 288.15)^5.2559.
    """
    if not 0.0 <= altitude <= 11000.0:
        raise ValueError("This model covers the troposphere only (0-11 000 m).")
    t_k = 288.15 - 0.0065 * altitude  # ISA lapse rate 6.5 K/km from 15 degC at sea level
    p = P_ATM * (t_k / 288.15) ** 5.2559  # exponent g / (R L) = 5.2559
    return t_k - KELVIN_OFFSET, p, p / (R_AIR * t_k)
