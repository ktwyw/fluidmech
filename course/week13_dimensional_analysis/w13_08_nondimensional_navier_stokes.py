"""CHME 202 - Week 13 - Example 8: non-dimensionalising the Navier-Stokes equations.

Scaling x ~ L, u ~ U, t ~ L/U, p - p_inf ~ rho U^2 turns the x-momentum equation into
  du*/dt* + u* du*/dx* + v* du*/dy* = -dp*/dx* + (1/Re) (d2u*/dx*2 + d2u*/dy*2)
The Reynolds number emerges as the only parameter (plus Fr if gravity matters).

# requires: sympy
"""

import sympy as sp

x, y, t = sp.symbols("x y t")
L, U, rho, mu = sp.symbols("L U rho mu", positive=True)
xs, ys, ts = sp.symbols("x_s y_s t_s")  # dimensionless coordinates
us = sp.Function("u_s")(xs, ys, ts)
vs = sp.Function("v_s")(xs, ys, ts)
ps = sp.Function("p_s")(xs, ys, ts)

# dimensional variables written in terms of dimensionless ones
u = U * us
v = U * vs
p = rho * U**2 * ps


# chain rule: d/dx = (1/L) d/dx_s, d/dt = (U/L) d/dt_s
def dx(f):
    return sp.diff(f, xs) / L


def dy(f):
    return sp.diff(f, ys) / L


def dt(f):
    return sp.diff(f, ts) * U / L


lhs = sp.expand(rho * (dt(u) + u * dx(u) + v * dy(u)) / (rho * U**2 / L))
rhs = sp.expand((-dx(p) + mu * (dx(dx(u)) + dy(dy(u)))) / (rho * U**2 / L))
short = {us: sp.Symbol("u"), vs: sp.Symbol("v"), ps: sp.Symbol("p")}
print("Both sides of x-momentum divided by rho U^2 / L (u, v, p, x, y, t now dimensionless):\n")
print("  inertia :", sp.sstr(lhs.subs(short)))
print("  forces  :", sp.sstr(rhs.subs(short)))
coeff = sp.simplify(rhs.coeff(sp.Derivative(us, (xs, 2))))
print(f"\nCoefficient of the viscous term: {coeff}  = 1/Re, with Re = rho U L / mu")
print("\nConsequences: Re -> 0 drops inertia (creeping flow, Week 5); Re -> infinity drops viscosity")
print("(Euler equations, Week 4) except in thin boundary layers. Two flows with the same Re and")
print("geometry have identical dimensionless solutions - the basis of model testing.")
