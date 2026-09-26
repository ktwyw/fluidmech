"""CHME 202 - Week 5 - Example 10: how accurate is a finite-difference solution? Grid convergence.

We solve fully developed flow in an annulus, (1/r) d/dr (r du/dr) = -G/mu, with
central differences and compare with the exact solution. The error falls as h^2:
halving the grid spacing cuts the error by 4 - the basis of grid-independence
studies in CFD (and in your COMSOL labs).
"""

import math

from fluidmech.laminar import annulus_velocity
from fluidmech.solvers import solve_linear

ri, ro, G, mu = 0.01, 0.03, 100.0, 1e-3  # annulus radii [m], -dp/dx [Pa/m], water


def solve(n: int) -> float:
    """Return the maximum error of the FD solution on n intervals."""
    h = (ro - ri) / n
    r = [ri + i * h for i in range(n + 1)]
    m = n - 1
    A = [[0.0] * m for _ in range(m)]  # tridiagonal system for the interior nodes
    b = [-G / mu] * m
    for k in range(m):
        i = k + 1
        rp, rm = r[i] + h / 2, r[i] - h / 2  # radii at the cell faces (conservative form of (1/r)(r u')')
        A[k][k] = -(rp + rm) / (r[i] * h**2)
        if k > 0:
            A[k][k - 1] = rm / (r[i] * h**2)
        if k < m - 1:
            A[k][k + 1] = rp / (r[i] * h**2)
    u = solve_linear(A, b)  # u = 0 on both walls is built into the matrix
    return max(abs(u[k] - annulus_velocity(r[k + 1], ri, ro, G, mu)) for k in range(m))


print(f"{'intervals':>10} {'h [mm]':>8} {'max error [mm/s]':>17} {'error ratio':>12} {'observed order':>15}")
prev = None
for n in [5, 10, 20, 40, 80]:
    err = solve(n)
    if prev:
        ratio = prev / err
        print(f"{n:>10} {(ro - ri) / n * 1000:>8.3f} {err * 1000:>17.5f} {ratio:>12.2f} {math.log2(ratio):>15.2f}")
    else:
        print(f"{n:>10} {(ro - ri) / n * 1000:>8.3f} {err * 1000:>17.5f}")
    prev = err
print("\nObserved order ~2: the central-difference scheme is second-order accurate.")
print("Report CFD results only after refining the mesh until the quantity of interest stops changing.")
