"""CHME 202 - Week 1 - Example 1: typical values of fluid properties.

Learning goal: get a feel for the magnitudes of density and viscosity of
fluids met in chemical engineering, and why kinematic viscosity matters.
Reading: White, Fluid Mechanics, Sections 1.4-1.9.
"""

from fluidmech import Fluid

# Values at 20 degC and 1 atm (White, Table A.3/A.4; water and air from fluidmech.properties)
fluids = [
    Fluid.air(20),
    Fluid(680.0, 2.92e-4, "gasoline"),
    Fluid(789.0, 1.20e-3, "ethanol"),
    Fluid.water(20),
    Fluid(891.0, 0.29, "SAE 30 oil"),
    Fluid(1261.0, 1.41, "glycerol"),
    Fluid(13546.0, 1.55e-3, "mercury"),
]

print(f"{'fluid':<20} {'rho [kg/m3]':>12} {'mu [Pa s]':>11} {'nu [m2/s]':>11} {'mu/mu_water':>12}")
mu_w = Fluid.water(20).dynamic_viscosity
for f in fluids:
    print(
        f"{f.name:<20} {f.density:>12.1f} {f.dynamic_viscosity:>11.3e} {f.kinematic_viscosity:>11.3e} "
        f"{f.dynamic_viscosity / mu_w:>12.3g}"
    )

print("\nObservations for discussion:")
print(" * Glycerol is ~1400 times more viscous than water - pumping it is a different problem.")
air, water, mercury = fluids[0], fluids[3], fluids[-1]
print(f" * Air has a LOWER dynamic viscosity than water ({air.dynamic_viscosity / water.dynamic_viscosity:.3f}x)")
print(f"   but a HIGHER kinematic viscosity ({air.kinematic_viscosity / water.kinematic_viscosity:.1f}x):")
print("   momentum diffuses faster in air because it has so little inertia per unit volume.")
print(
    f" * Mercury: dynamic viscosity close to water's, but nu is {water.kinematic_viscosity / mercury.kinematic_viscosity:.0f}x "
    "smaller - flows of mercury are 'less viscous' in the sense that matters (Reynolds number)."
)

# Reynolds number of the same pipe flow for each fluid
V, D = 1.0, 0.05
print(f"\nReynolds number for V = {V} m/s in a {D * 1000:.0f} mm pipe:")
for f in fluids:
    re = V * D / f.kinematic_viscosity
    regime = "laminar" if re < 2300 else ("transitional" if re < 4000 else "turbulent")
    print(f"  {f.name:<20} Re = {re:>10.3g}  ({regime})")
