"""CHME 202 - Week 13 - Example 6: the method of repeating variables, step by step.

Drag on a sphere, F = f(rho, V, D, mu). Form Pi = F rho^a V^b D^c and require
zero net powers of M, L and T. SymPy solves the three linear equations exactly as
you would on paper; the second group follows the same way with mu.

# requires: sympy
"""

import sympy as sp

a, b, c = sp.symbols("a b c")
dims = {"F": (1, 1, -2), "rho": (1, -3, 0), "V": (0, 1, -1), "D": (0, 1, 0), "mu": (1, -1, -1)}
print("Dimensions (M, L, T):", ", ".join(f"{k} = {v}" for k, v in dims.items()))
print("n = 5 variables, r = 3 dimensions -> 2 Pi groups\n")
for target in ("F", "mu"):
    t = dims[target]
    eqs = [
        sp.Eq(t[0] + dims["rho"][0] * a + dims["V"][0] * b + dims["D"][0] * c, 0),
        sp.Eq(t[1] + dims["rho"][1] * a + dims["V"][1] * b + dims["D"][1] * c, 0),
        sp.Eq(t[2] + dims["rho"][2] * a + dims["V"][2] * b + dims["D"][2] * c, 0),
    ]
    print(f"Pi = {target} rho^a V^b D^c:")
    for name, eq in zip("MLT", eqs):
        print(f"   {name}: {eq.lhs} = 0")
    sol = sp.solve(eqs, (a, b, c))
    print(f"   -> a = {sol[a]}, b = {sol[b]}, c = {sol[c]}:  Pi = {target} / (rho^{-sol[a]} V^{-sol[b]} D^{-sol[c]})\n")
print("So F / (rho V^2 D^2) = phi(mu / (rho V D)), i.e. Cd = phi(Re).")
print("Check with fluidmech.dimensional.pi_groups - it solves the same equations automatically.")
