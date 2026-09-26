"""CHME 202 - Week 13 - Example 5: the dimensionless groups a chemical engineer meets.

Each group is a ratio of two effects; its size tells you which effect wins.
"""

from fluidmech import Fluid
from fluidmech.drag import eotvos_number, morton_number
from fluidmech.porous import archimedes_number
from fluidmech.properties import water_surface_tension

water = Fluid.water(20)
sigma = water_surface_tension(20)
groups = [
    (
        "Reynolds",
        "rho V L / mu",
        "inertia / viscous",
        water.density * 1.0 * 0.05 / water.dynamic_viscosity,
        "water, 1 m/s in a 50 mm pipe",
    ),
    ("Froude", "V / sqrt(g L)", "inertia / gravity", 1.0 / (9.81 * 0.5) ** 0.5, "open channel, 1 m/s, 0.5 m deep"),
    (
        "Weber",
        "rho V^2 L / sigma",
        "inertia / surface tension",
        water.density * 5.0**2 * 1e-3 / sigma,
        "1 mm drop hitting a wall at 5 m/s",
    ),
    (
        "Capillary",
        "mu V / sigma",
        "viscous / surface tension",
        water.dynamic_viscosity * 0.01 / sigma,
        "meniscus moving at 1 cm/s",
    ),
    (
        "Eotvos (Bond)",
        "g drho d^2 / sigma",
        "gravity / surface tension",
        eotvos_number(3e-3, water.density, sigma),
        "3 mm air bubble in water",
    ),
    (
        "Morton",
        "g mu^4 drho / (rho^2 sigma^3)",
        "fluid-pair property",
        morton_number(water, water.density, sigma),
        "air-water",
    ),
    (
        "Archimedes",
        "rho drho g d^3 / mu^2",
        "buoyancy x inertia / viscous^2",
        archimedes_number(200e-6, 2650, water.density, water.dynamic_viscosity),
        "200 um sand in water",
    ),
    (
        "Euler",
        "dp / (rho V^2)",
        "pressure / inertia",
        50e3 / (water.density * 2.0**2),
        "50 kPa across a valve at 2 m/s",
    ),
    ("Damkohler", "t_flow / t_reaction", "reaction / transport rate", 10.0 / 1.0, "10 s residence, 1 s reaction"),
    ("Mach", "V / c", "flow speed / sound speed", 100 / 343, "air at 100 m/s"),
]
print(f"{'group':<14} {'definition':<30} {'ratio of':<30} {'value':>9}  example")
for name, definition, meaning, value, example in groups:
    print(f"{name:<14} {definition:<30} {meaning:<30} {value:>9.3g}  {example}")
print("\nRules of thumb: Re > ~4000 turbulent pipe flow; Fr > 1 supercritical open-channel flow;")
print("We > ~10 drops break up; Eo < 1 bubbles stay spherical; Da > 1 reaction faster than mixing/flow;")
print("Ma < 0.3 incompressible.")
