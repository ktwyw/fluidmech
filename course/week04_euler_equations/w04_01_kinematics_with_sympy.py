"""CHME 202 - Week 4 - Example 1: kinematics of a velocity field, done symbolically.

For a given velocity field we check continuity (div V = 0), and compute the
material acceleration DV/Dt = dV/dt + (V . grad) V, the vorticity and the
stream function. SymPy does the algebra exactly, as you would by hand.
Reading: White, Sections 4.1-4.3 and 4.7.

# requires: sympy
"""

import sympy as sp

x, y, t, a, U, Omega, K = sp.symbols("x y t a U Omega K", real=True)

fields = {
    "stagnation-point flow": (a * x, -a * y),
    "rigid-body rotation": (-Omega * y, Omega * x),
    "free vortex": (-K * y / (x**2 + y**2), K * x / (x**2 + y**2)),
    "unsteady converging flow": (U * (1 + x) * t, -U * y * t),
    "invalid field (check!)": (x**2 * y, x * y**2),
}

for name, (u, v) in fields.items():
    print(f"\n{name}:  u = {u},  v = {v}")
    div = sp.simplify(sp.diff(u, x) + sp.diff(v, y))
    print(
        f"  continuity  du/dx + dv/dy = {div}  ->  {'incompressible' if div == 0 else 'NOT a valid incompressible flow'}"
    )
    ax = sp.simplify(sp.diff(u, t) + u * sp.diff(u, x) + v * sp.diff(u, y))
    ay = sp.simplify(sp.diff(v, t) + u * sp.diff(v, x) + v * sp.diff(v, y))
    print(f"  acceleration  a_x = {ax},  a_y = {ay}")
    omega = sp.simplify(sp.diff(v, x) - sp.diff(u, y))
    print(f"  vorticity  omega_z = {omega}  ->  {'irrotational' if omega == 0 else 'rotational'}")
    if div == 0:
        # stream function: u = dpsi/dy, v = -dpsi/dx
        psi = sp.integrate(u, y)
        psi += sp.integrate(sp.simplify(-v - sp.diff(psi, x)), x)
        print(f"  stream function  psi = {sp.simplify(psi)}")

print("\nNote: a steady flow can still have acceleration (stagnation flow: fluid slows down")
print("approaching the wall). Convective acceleration is what makes the Euler equations nonlinear.")
