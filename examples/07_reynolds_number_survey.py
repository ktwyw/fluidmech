"""Example 7 - Reynolds numbers of everyday and engineering flows.

Shows how the same formula, Re = V L / nu, spans many orders of magnitude and
decides whether a flow is laminar or turbulent.
"""

from fluidmech import Fluid
from fluidmech.dimensionless import flow_regime, reynolds

water = Fluid.water(20)
air = Fluid.air(20)
blood = Fluid(density=1060.0, dynamic_viscosity=3.5e-3, name="blood")
engine_oil = Fluid(density=891.0, dynamic_viscosity=0.29, name="SAE 30 oil")
honey = Fluid(density=1420.0, dynamic_viscosity=10.0, name="honey")

# (description, fluid, velocity [m/s], length [m], internal pipe flow?)
cases = [
    ("Honey poured through a 10 mm nozzle", honey, 0.05, 0.010, True),
    ("Oil in a 50 mm lubrication line", engine_oil, 1.0, 0.050, True),
    ("Blood in the aorta (25 mm)", blood, 0.30, 0.025, True),
    ("Water from a kitchen tap (15 mm)", water, 1.0, 0.015, True),
    ("Water main (300 mm)", water, 1.5, 0.300, True),
    ("Air in an HVAC duct (400 mm)", air, 5.0, 0.400, True),
    ("Swimmer (length 1.8 m)", water, 1.5, 1.8, False),
    ("Car on a motorway (4.5 m)", air, 30.0, 4.5, False),
    ("Airliner wing chord (5 m)", air, 250.0, 5.0, False),
    ("Container ship (300 m)", water, 12.0, 300.0, False),
]

print(f"{'Flow':<38} {'Re':>12}  Regime")
print("-" * 68)
for name, fluid, v, length, internal in cases:
    re = reynolds(v, length, fluid.kinematic_viscosity)
    if internal:
        regime = flow_regime(re)
    else:
        # External flat-plate boundary layers transition near Re_x ~ 5e5
        regime = "laminar BL" if re < 5e5 else "turbulent BL"
    print(f"{name:<38} {re:>12.3g}  {regime}")

print("\nInternal flows use Re_crit ~ 2300 (pipe diameter);")
print("external boundary layers use Re_x,crit ~ 5e5 (length along the surface).")
