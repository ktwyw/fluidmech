"""CHME 202 - Week 9 - Example 1: laminar-turbulent transition and entrance length.

Reynolds' experiment: dye stays as a thread below Re ~ 2300 and disperses
above ~4000. Flow needs an entrance length to become fully developed:
L_e / D ~ 0.06 Re (laminar), 4.4 Re^(1/6) (turbulent).
Reading: White, Sections 6.1-6.3.
"""

from fluidmech import Fluid
from fluidmech.dimensionless import flow_regime
from fluidmech.turbulence import entrance_length

water = Fluid.water(20)
oil = Fluid(880.0, 0.08, "light oil")
D = 0.05  # pipe diameter [m]
print(f"{'fluid':<16} {'V [m/s]':>8} {'Re':>9} {'regime':>13} {'L_e [m]':>8} {'L_e/D':>6}")
for fluid, vs in [(oil, [0.1, 0.5, 2.0]), (water, [0.02, 0.05, 0.1, 1.0, 3.0])]:
    for v in vs:
        re = v * D / fluid.kinematic_viscosity
        le = entrance_length(re, D)
        print(f"{fluid.name:<16} {v:>8.2f} {re:>9.0f} {flow_regime(re):>13} {le:>8.2f} {le / D:>6.0f}")
print("\nLaminar entrance lengths grow with Re, up to ~140 D near Re = 2300; turbulent ones are only 20-40 D.")
print("Practical consequence: flow meters need 10-30 D of straight pipe upstream, and friction is")
print("higher in the entrance region than the fully developed formulas predict.\n")

print("Critical velocity for transition (Re = 2300) in a 50 mm pipe:")
for f in [water, oil, Fluid(1261.0, 1.41, "glycerol")]:
    print(f"  {f.name:<16} V_crit = {2300 * f.kinematic_viscosity / D:.3f} m/s")
