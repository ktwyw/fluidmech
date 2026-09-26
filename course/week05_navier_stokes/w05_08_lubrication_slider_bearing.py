"""CHME 202 - Week 5 - Example 8: lubrication theory - how a thin wedge of oil carries a load.

In a thin, slowly varying gap h(x) Navier-Stokes reduces to the Reynolds equation
d/dx (h^3 dp/dx) = 6 mu U dh/dx. For a plane slider tilted from h1 to h2 we integrate
numerically and compare the load with the classical closed form.
"""

import math

from fluidmech.solvers import bisect

mu, U, L = 0.04, 5.0, 0.05  # oil viscosity, sliding speed, pad length
h2 = 20e-6  # outlet (minimum) film thickness


def pressure_profile(h1: float, n: int = 2000):
    """Integrate dp/dx = 6 mu U (h - hm) / h^3 with p(0) = p(L) = 0 (hm chosen by shooting)."""

    def h_at(x):
        return h1 + (h2 - h1) * x / L

    def p_end(hm):
        p = 0.0
        for i in range(n):
            x = (i + 0.5) * L / n
            h = h_at(x)
            # Reynolds equation integrated once: dp/dx = 6 mu U (h - h_m) / h^3
            p += 6 * mu * U * (h - hm) / h**3 * L / n
        return p

    hm = bisect(p_end, h2, h1)  # shooting: choose h_m (gap at peak pressure) so that p(L) = 0
    xs, ps, p = [0.0], [0.0], 0.0
    for i in range(n):
        x = (i + 0.5) * L / n
        h = h_at(x)
        p += 6 * mu * U * (h - hm) / h**3 * L / n
        xs.append((i + 1) * L / n)
        ps.append(p)
    return xs, ps


print(f"Slider pad L = {L * 1000:.0f} mm, U = {U} m/s, oil mu = {mu} Pa s, minimum film {h2 * 1e6:.0f} um\n")
print(f"{'h1/h2':>6} {'p_max [MPa]':>12} {'load numeric [kN/m]':>20} {'closed form':>12}")
for ratio in [1.5, 2.0, 2.2, 3.0, 4.0]:
    xs, ps = pressure_profile(ratio * h2)
    # trapezoidal integral of p dx
    load = sum((ps[i] + ps[i + 1]) / 2 * (xs[i + 1] - xs[i]) for i in range(len(xs) - 1))
    K = ratio - 1
    # classical plane-slider load per width
    exact = 6 * mu * U * L**2 / (h2**2 * K**2) * (math.log(1 + K) - 2 * K / (2 + K))
    print(f"{ratio:>6} {max(ps) / 1e6:>12.2f} {load / 1e3:>20.1f} {exact / 1e3:>12.1f}")
print("\nThe load capacity peaks near h1/h2 ~ 2.2. A parallel gap (h1 = h2) carries no load at all:")
print("the converging wedge is essential. Pressures of MPa from a film thinner than a hair!")
