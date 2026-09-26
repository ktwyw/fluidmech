"""CHME 202 - Week 5 - Example 1: reducing and solving the Navier-Stokes equations symbolically.

For fully developed flow the x-momentum equation collapses to an ODE. SymPy
solves it with the boundary conditions, exactly as in the lecture derivation.
Reading: White, Sections 4.3, 4.6 and 4.10.

# requires: sympy
"""

import sympy as sp

y, r, h, R, mu, U = sp.symbols("y r h R mu U", positive=True)
G = sp.symbols("G", real=True)  # G = -dp/dx
u = sp.Function("u")

# 1. Couette-Poiseuille flow: mu u'' = -G, u(0) = 0, u(h) = U
sol = sp.dsolve(sp.Eq(mu * u(y).diff(y, 2), -G), u(y), ics={u(0): 0, u(h): U})
u_cp = sp.simplify(sol.rhs)
print("1) Flow between plates (lower fixed, upper moving at U), G = -dp/dx")
print("   u(y) =", sp.factor(u_cp))
q = sp.simplify(sp.integrate(u_cp, (y, 0, h)))
print("   flow per unit width q =", q)
y_rev = sp.solve(sp.Eq(sp.diff(u_cp, y).subs(y, 0), 0), G)
print("   the wall shear at y = 0 vanishes when G =", y_rev[0], "(onset of back-flow for more adverse G)\n")

# 2. Hagen-Poiseuille: (mu / r) d/dr (r du/dr) = -G, u(R) = 0, u finite at r = 0
C1, C2 = sp.symbols("C1 C2")
general = -G * r**2 / (4 * mu) + C1 * sp.log(r) + C2
print("2) Pipe flow: general solution u(r) =", general)
print("   finiteness at r = 0 forces C1 = 0; u(R) = 0 gives C2:")
c2 = sp.solve(general.subs({C1: 0, r: R}), C2)[0]
u_hp = sp.factor(general.subs({C1: 0, C2: c2}))
print("   u(r) =", u_hp)
check = sp.simplify(mu / r * sp.diff(r * sp.diff(u_hp, r), r) + G)
print("   substituting back into the ODE gives residual", check)
Q = sp.simplify(sp.integrate(2 * sp.pi * r * u_hp, (r, 0, R)))
print("   Q =", Q, "  (Hagen-Poiseuille)")
V = sp.simplify(Q / (sp.pi * R**2))
tau_w = sp.simplify(-mu * sp.diff(u_hp, r).subs(r, R))
rho = sp.symbols("rho", positive=True)
f = sp.simplify(8 * tau_w / (rho * V**2))
print(
    "   Darcy friction factor f = 8 tau_w / (rho V^2) =",
    f,
    "= 64 / Re with Re = rho V (2R) / mu:",
    sp.simplify(f - 64 * mu / (rho * V * 2 * R)) == 0,
)
