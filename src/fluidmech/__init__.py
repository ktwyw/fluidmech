"""fluidmech: a dependency-free toolkit for engineering fluid mechanics.

All quantities are in SI units (m, kg, s, Pa, N) unless stated otherwise.
Temperatures are in degrees Celsius. See :mod:`fluidmech.units` for conversions.

Modules
-------
properties     water and air properties, the Fluid class
dimensionless  Reynolds, Froude, Mach, Weber and Euler numbers
hydrostatics   pressure, manometers, forces on gates, buoyancy
bernoulli      flow meters, orifices, tank draining
pipe_flow      friction factors and the three classic pipe problems
networks       steady-state pipe network solver with reservoirs and pumps
pumps          pump curves, affinity laws, operating point, NPSH
open_channel   Manning flow, critical flow, jumps, weirs, water-surface profiles
compressible   isentropic flow, normal shocks, choked nozzles
drag           drag coefficients, boundary layers, terminal velocity
transients     water hammer
rheology       non-Newtonian viscosity models and fitting
laminar        exact Navier-Stokes solutions (Poiseuille, Couette, annulus, films, ...)
potential_flow 2D inviscid flow by superposition
turbulence     law of the wall, y+ and Kolmogorov scales
porous         Darcy's law, packed beds, fluidisation, filtration, membranes
dimensional    automatic Buckingham Pi groups
mixing         stirred tanks, micromixing and ideal reactors
cavitation     Rayleigh-Plesset bubble dynamics
cfd            (optional, numpy/scipy) lid-driven cavity, lattice Boltzmann, Taylor dispersion
viz            (optional, matplotlib) publication-quality figures
units          unit conversion
solvers        root finding, linear systems, curve fitting
"""

__version__ = "0.5.0"

from . import (  # noqa: E402
    bernoulli,
    cavitation,
    compressible,
    dimensional,
    dimensionless,
    drag,
    hydrostatics,
    laminar,
    mixing,
    networks,
    open_channel,
    pipe_flow,
    porous,
    potential_flow,
    properties,
    pumps,
    rheology,
    solvers,
    transients,
    turbulence,
    units,
)
from .constants import G  # noqa: E402
from .networks import Network  # noqa: E402
from .properties import Fluid  # noqa: E402
from .pumps import PumpCurve  # noqa: E402

__all__ = [
    "G",
    "Fluid",
    "Network",
    "PumpCurve",
    "bernoulli",
    "cavitation",
    "compressible",
    "dimensional",
    "dimensionless",
    "drag",
    "hydrostatics",
    "laminar",
    "mixing",
    "networks",
    "open_channel",
    "pipe_flow",
    "porous",
    "potential_flow",
    "properties",
    "pumps",
    "rheology",
    "solvers",
    "transients",
    "turbulence",
    "units",
    "__version__",
]
