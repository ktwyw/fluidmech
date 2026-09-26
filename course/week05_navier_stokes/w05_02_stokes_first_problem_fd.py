"""CHME 202 - Week 5 - Example 2: impulsively started plate (Stokes' first problem) by finite differences.

u_t = nu u_yy with u(0, t) = U. The exact solution is u = U erfc(y / 2 sqrt(nu t)).
We solve it with the explicit (FTCS) scheme and show its stability limit
nu dt / dy^2 <= 1/2 - a first taste of computational fluid dynamics.
"""

from fluidmech.laminar import penetration_depth, stokes_first_problem

nu, U = 1e-6, 1.0  # water, plate speed
L, n = 0.01, 101  # domain depth 10 mm, grid points
dy = L / (n - 1)
t_end = 5.0  # simulated time [s]


def solve(r: float) -> list[float]:
    """March the FTCS scheme with Fourier number r = nu dt / dy^2."""
    dt = r * dy**2 / nu
    u = [0.0] * n  # fluid at rest ...
    u[0] = U  # ... except the wall, which moves from t = 0
    t = 0.0
    while t < t_end - 1e-12:  # explicit (FTCS) time marching
        step = min(dt, t_end - t)
        rr = nu * step / dy**2
        # u_new = u + r (u_E - 2u + u_W); boundaries fixed
        u = [U] + [u[i] + rr * (u[i + 1] - 2 * u[i] + u[i - 1]) for i in range(1, n - 1)] + [0.0]
        t += step
        if max(abs(v) for v in u) > 1e3:  # stop early once the unstable solution has blown up
            return u
    return u


print(f"Water (nu = {nu} m2/s), plate started at {U} m/s; profile after {t_end} s")
print(f"Momentum penetration depth ~ 4 sqrt(nu t) = {penetration_depth(nu, t_end) * 1000:.1f} mm\n")
for r in [0.25, 0.5, 0.52]:
    u = solve(r)
    max_err = max(abs(u[i] - stokes_first_problem(i * dy, t_end, U, nu)) for i in range(n))
    status = "stable" if max_err < 0.05 else "UNSTABLE - oscillations grow without bound"
    print(f"Fourier number {r:4.2f}: max error vs exact = {max_err:10.3g}  ({status})")

u = solve(0.4)
print(f"\n{'y [mm]':>7} {'FD':>7} {'exact':>7}")
for i in range(0, 60, 6):
    print(f"{i * dy * 1000:>7.1f} {u[i]:>7.4f} {stokes_first_problem(i * dy, t_end, U, nu):>7.4f}")
print("\nAfter 5 s the plate has only dragged a ~9 mm layer of water with it: viscous diffusion is slow.")
