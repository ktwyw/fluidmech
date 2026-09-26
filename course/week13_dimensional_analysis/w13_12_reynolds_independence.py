"""CHME 202 - Week 13 - Example 12: Reynolds-number independence in wind-tunnel testing.

A 1:100 model of a process structure in a wind tunnel cannot reach the full-scale Reynolds
number. For SHARP-EDGED bodies this hardly matters: separation is fixed at the edges and Cd
is constant above Re ~ 1e4. For ROUNDED bodies (stacks, spheres, tanks) the drag crisis
makes Cd depend on Re, and model results can mislead.
"""

from fluidmech import Fluid
from fluidmech.dimensionless import reynolds
from fluidmech.drag import sphere_drag_coefficient

air = Fluid.air(15)
scale = 1 / 100  # model : full-scale length ratio
L_full, V_full = 30.0, 25.0  # full-scale size and design wind speed
re_full = reynolds(V_full, L_full, air.kinematic_viscosity)
for v_tunnel in [10.0, 30.0]:
    re_model = reynolds(v_tunnel, L_full * scale, air.kinematic_viscosity)
    print(
        f"Model at {v_tunnel:.0f} m/s: Re_model = {re_model:.1e} vs Re_full = {re_full:.1e} ({re_full / re_model:.0f}x larger)"
    )
print("\nSharp-edged building (Cd ~ 1.05-1.2): Cd essentially the same at both Re -> model is fine.")
print("Rounded body, sphere as an example:")
for re in [1e4, 5e4, 1e5, 2e5]:
    print(f"  Re = {re:.0e}: Cd = {sphere_drag_coefficient(re):.3f}")
print("  above ~3e5 the drag crisis cuts Cd to ~0.1-0.2 - a model at Re ~ 1e5 overestimates full-scale drag.")
print("\nRemedies: roughen rounded models (trip wires) to trigger turbulent boundary layers early, test in")
print("pressurised tunnels, or rely on full-scale data for curved structures.")
