"""CHME 202 - Week 5 - Example 4: order-of-magnitude analysis of the Navier-Stokes equations.

Inertia rho V^2 / L versus viscous forces mu V / L^2 -> Reynolds number.
Re << 1: creeping (Stokes) flow, inertia negligible.  Re >> 1: viscosity matters
only in thin boundary layers; elsewhere the Euler equations apply.
"""

from fluidmech import Fluid

water, air = Fluid.water(20), Fluid.air(20)
glycerol = Fluid(1261.0, 1.41, "glycerol")
cases = [
    ("bacterium swimming", water, 30e-6, 2e-6),
    ("microfluidic channel", water, 1e-3, 100e-6),
    ("glycerol in a 10 mm tube", glycerol, 0.05, 0.01),
    ("blood in a capillary", Fluid(1060.0, 3.5e-3, "blood"), 1e-3, 8e-6),
    ("water in a 50 mm pipe", water, 1.5, 0.05),
    ("air over a car", air, 30.0, 4.0),
    ("river", water, 1.0, 5.0),
]
print(f"{'flow':<26} {'Re':>10} {'viscous time L^2/nu':>20} {'flow time L/V':>14}  regime")
for name, f, v, length in cases:
    re = v * length / f.kinematic_viscosity
    t_visc = length**2 / f.kinematic_viscosity
    t_flow = length / v
    if re < 1:
        regime = "creeping: drop inertia (Stokes eqs.)"
    elif re < 1e3:
        regime = "both terms matter (full N-S)"
    else:
        regime = "inertia dominates; boundary layers"
    print(f"{name:<26} {re:>10.3g} {t_visc:>18.3g} s {t_flow:>12.3g} s  {regime}")
print("\nRe is also the ratio of the viscous diffusion time to the flow (convection) time.")
print("Microfluidic mixers struggle because at low Re there is no turbulence to mix streams (Week 14).")
