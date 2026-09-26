"""CHME 202 - Week 5 - Example 15: explicit versus implicit (Crank-Nicolson) time stepping.

Example 2 showed that the explicit scheme for u_t = nu u_yy blows up for nu dt / dy^2 > 1/2.
The Crank-Nicolson scheme averages the explicit and implicit forms; it is stable for ANY
time step and second-order accurate in time - the default in many CFD codes (e.g. COMSOL's
BDF/implicit solvers follow the same idea).
"""

from fluidmech.laminar import stokes_first_problem

nu, U, L, n = 1e-6, 1.0, 0.01, 101  # water, plate speed [m/s], depth [m], grid points
dy = L / (n - 1)
t_end = 5.0


def thomas(a, b, c, d):  # Thomas algorithm: O(n) Gaussian elimination for tridiagonal systems
    """Solve a tridiagonal system (sub-diagonal a, diagonal b, super-diagonal c)."""
    m = len(d)
    cp, dp = [0.0] * m, [0.0] * m
    cp[0], dp[0] = c[0] / b[0], d[0] / b[0]
    for i in range(1, m):
        den = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / den if i < m - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / den
    x = [0.0] * m
    x[-1] = dp[-1]
    for i in range(m - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def crank_nicolson(r):
    dt = r * dy**2 / nu
    steps = max(1, round(t_end / dt))
    rr = nu * (t_end / steps) / dy**2
    u = [U] + [0.0] * (n - 1)
    m = n - 2
    for _ in range(steps):  # each step solves (I - r/2 D2) u_new = (I + r/2 D2) u_old
        d = [u[i] + 0.5 * rr * (u[i + 1] - 2 * u[i] + u[i - 1]) for i in range(1, n - 1)]
        d[0] += 0.5 * rr * U  # boundary value at the new time level
        inner = thomas([-0.5 * rr] * m, [1 + rr] * m, [-0.5 * rr] * m, d)
        u = [U] + inner + [0.0]
    return u, steps


print(f"{'Fourier number':>15} {'steps':>6} {'max error':>10}")
for r in [0.4, 2.0, 10.0, 50.0]:
    u, steps = crank_nicolson(r)
    err = max(abs(u[i] - stokes_first_problem(i * dy, t_end, U, nu)) for i in range(n))
    print(f"{r:>15} {steps:>6} {err:>10.4f}")
print("\nCrank-Nicolson stays stable far beyond the explicit limit of 0.5: at a Fourier number of 10 it")
print("uses 25x fewer steps with the SAME accuracy (the remaining error comes from the grid spacing).")
print("Accuracy still falls with very large steps (and CN can show small oscillations near the sudden")
print("start), so time steps are chosen for accuracy, no longer for stability.")
