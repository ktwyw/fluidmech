"""CHME 202 - Week 9 - Example 10: pressure drop in a long gas pipeline (isothermal compressible flow).

When the pressure drop is a large fraction of the inlet pressure, gas density changes
along the pipe. For isothermal ideal-gas flow with mass flux G = m_dot / A:
    p1^2 - p2^2 = G^2 R T [ f L / D + 2 ln(p1 / p2) ]
Compare with the incompressible formula using inlet density.
Reading: White, Section 9.8 (isothermal flow with friction).
"""

import math

from fluidmech import pipe_flow as pf
from fluidmech.solvers import bisect

R, T, mu = 518.3, 288.0, 1.1e-5  # methane gas constant, temperature, viscosity
D, L = 0.30, 50e3
p1 = 60e5  # inlet pressure [Pa]
eps = pf.ROUGHNESS["commercial_steel"]
A = math.pi * D**2 / 4
print(f"Natural-gas pipeline D = {D} m, L = {L / 1000:.0f} km, inlet {p1 / 1e5:.0f} bar, {T - 273.15:.0f} degC\n")
print(f"{'m_dot [kg/s]':>13} {'Re':>9} {'f':>7} {'p2 isothermal':>14} {'p2 incompressible':>18} {'V1 -> V2 [m/s]':>16}")
for mdot in [10.0, 20.0, 30.0, 40.0]:
    G = mdot / A  # mass flux [kg/(m2 s)], constant along the pipe
    re = G * D / mu
    f = pf.friction_factor(re, eps / D)

    def residual(p2, G=G, f=f):
        return p1**2 - p2**2 - G**2 * R * T * (f * L / D + 2 * math.log(p1 / p2))

    try:
        p2 = bisect(residual, 1e4, p1 * 0.999999)  # outlet pressure satisfying the isothermal-flow equation
        p2_txt = f"{p2 / 1e5:>11.1f} bar"
    except ValueError:
        p2, p2_txt = None, f"{'impossible':>14}"
    rho1 = p1 / (R * T)
    dp_inc = f * L / D * G**2 / (2 * rho1)  # incompressible Darcy-Weisbach with inlet density
    p2_inc = p1 - dp_inc
    v_txt = f"{G / rho1:.1f} -> {G / (p2 / (R * T)):.1f}" if p2 else "-"
    inc_txt = f"{p2_inc / 1e5:>15.1f} bar" if p2_inc > 0 else f"{'negative!':>18}"
    print(f"{mdot:>13} {re:>9.2e} {f:>7.4f} {p2_txt} {inc_txt} {v_txt:>16}")
print("\nAs the gas expands it accelerates, so friction losses grow towards the outlet. The incompressible")
print("formula with inlet density underestimates the pressure drop once dp exceeds ~10-20 % of p1.")
print("'impossible': no positive outlet pressure satisfies the equation - this pipe cannot carry that flow")
print("from 60 bar (it would need compression stations along the route).")
print("(Using the AVERAGE density in the incompressible formula is a common, better approximation.)")
