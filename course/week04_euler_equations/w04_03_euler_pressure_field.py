"""CHME 202 - Week 4 - Example 3: pressure field from the Euler equations.

For the stagnation-point flow u = a x, v = -a y, integrate Euler's equations
  dp/dx = -rho (u du/dx + v du/dy),  dp/dy = -rho (u dv/dx + v dv/dy) - rho g
and compare with Bernoulli. Because the flow is irrotational, Bernoulli holds
between ANY two points, not only along a streamline.
Reading: White, Sections 4.3 and 4.9.
"""

from fluidmech.constants import G

rho, a, p0 = 1000.0, 2.0, 200e3  # p0 = pressure at the stagnation point (0, 0)


def euler_gradient(x: float, y: float) -> tuple[float, float]:
    u, v = a * x, -a * y
    dudx, dudy, dvdx, dvdy = a, 0.0, 0.0, -a
    return -rho * (u * dudx + v * dudy), -rho * (u * dvdx + v * dvdy) - rho * G


def integrate_path(x1: float, y1: float, n: int = 2000) -> float:
    """Line-integrate grad p from (0,0) to (x1,y1) along a straight path."""
    p = p0
    for i in range(n):  # line integral of grad p along a straight path (midpoint rule)
        s = (i + 0.5) / n
        gx, gy = euler_gradient(s * x1, s * y1)
        p += gx * x1 / n + gy * y1 / n
    return p


print(f"Stagnation-point flow, a = {a} 1/s, p = {p0 / 1e3:.0f} kPa at the origin (y is vertical)\n")
print(f"{'point':>12} {'p (Euler) [kPa]':>16} {'p (Bernoulli) [kPa]':>20}")
for x1, y1 in [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, 0.5)]:
    p_euler = integrate_path(x1, y1)
    speed2 = (a * x1) ** 2 + (a * y1) ** 2
    # Bernoulli between the origin and the point (valid: irrotational flow)
    p_bern = p0 - 0.5 * rho * speed2 - rho * G * y1
    print(f"{f'({x1}, {y1})':>12} {p_euler / 1e3:>16.3f} {p_bern / 1e3:>20.3f}")
print("\nThe results agree to the integration accuracy. Pressure falls away from the stagnation point")
print("as the fluid accelerates: p = p0 - rho a^2 (x^2 + y^2) / 2 - rho g y.")
