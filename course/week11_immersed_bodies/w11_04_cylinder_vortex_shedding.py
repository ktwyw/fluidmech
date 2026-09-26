"""CHME 202 - Week 11 - Example 4: flow past cylinders - drag and vortex shedding.

A cylinder in cross-flow sheds a Karman vortex street at f = St U / D (St ~ 0.2).
If f approaches a natural frequency of the structure it can resonate: a classic
failure of thermowells in process pipes and of tall stacks in wind.
Reading: White, Section 7.6.
"""

from fluidmech import Fluid
from fluidmech.drag import cylinder_drag_coefficient, drag_force, vortex_shedding_frequency

# Thermowell in a steam/gas line
gas = Fluid(8.0, 2.0e-5, "process gas at 10 bar")  # density [kg/m3], viscosity [Pa s]
d_tw, L_tw = 0.02, 0.15  # thermowell diameter and immersion length [m]
f_natural = 900.0  # natural frequency of the thermowell [Hz] (from a structural calculation)
print(f"Thermowell d = {d_tw * 1000:.0f} mm, natural frequency {f_natural:.0f} Hz, in {gas.name}")
print(f"{'V [m/s]':>8} {'Re':>9} {'Cd':>6} {'drag [N]':>9} {'f_shed [Hz]':>12} {'f_shed/f_n':>11}")
for v in [5, 10, 20, 40, 60, 80]:
    re = v * d_tw / gas.kinematic_viscosity
    cd = cylinder_drag_coefficient(min(re, 2e5))  # correlation valid up to Re = 2e5
    f_s = vortex_shedding_frequency(v, d_tw)
    flag = "  <- RESONANCE RISK" if 0.8 < f_s / f_natural < 1.2 else ""
    print(
        f"{v:>8} {re:>9.3g} {cd:>6.2f} {drag_force(cd, gas.density, v, d_tw * L_tw):>9.2f} "
        f"{f_s:>12.0f} {f_s / f_natural:>11.2f}{flag}"
    )
print("(Cd is capped at the Re = 2e5 value; above ~3e5 the drag crisis may lower it.)")
print("Design codes (e.g. ASME PTC 19.3 TW) require the shedding frequency to stay well below f_n.\n")

# Tall process column in wind
air = Fluid.air(15)
D, H, v = 3.0, 40.0, 30.0  # column diameter [m], height [m], wind speed [m/s]
re = v * D / air.kinematic_viscosity
cd = 0.7  # supercritical cylinder with some roughness
F = drag_force(cd, air.density, v, D * H)
print(f"Distillation column D = {D} m, H = {H} m in a {v} m/s wind: Re = {re:.1e} (beyond the drag crisis)")
print(f"  wind force {F / 1e3:.0f} kN, overturning moment {F * H / 2 / 1e3:.0f} kN m")
print(f"  shedding frequency {vortex_shedding_frequency(v, D):.2f} Hz - compare with the column's sway frequency;")
print("  helical strakes on chimneys break up the vortex street.")
