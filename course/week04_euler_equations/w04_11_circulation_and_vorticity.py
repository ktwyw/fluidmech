"""CHME 202 - Week 4 - Example 11: circulation, vorticity and Stokes' theorem.

Circulation Gamma = closed-loop integral of V . ds equals the total vorticity enclosed.
A forced vortex (rigid rotation) has vorticity 2 omega everywhere; a free vortex is
irrotational everywhere except at its centre. We integrate numerically around loops.
"""

import math


def forced(x, y, omega=2.0):
    return -omega * y, omega * x


def free(x, y, K=1.0):
    r2 = x * x + y * y
    return -K * y / r2, K * x / r2


def circulation(field, cx, cy, radius, n=2000):
    total = 0.0
    for i in range(n):  # sum V . ds around a circle (midpoint rule)
        th = 2 * math.pi * (i + 0.5) / n
        x, y = cx + radius * math.cos(th), cy + radius * math.sin(th)
        u, v = field(x, y)
        total += (u * -math.sin(th) + v * math.cos(th)) * radius * 2 * math.pi / n  # tangential component x arc length
    return total


print(f"{'loop':<38} {'forced vortex':>14} {'free vortex':>12}")
for label, cx, cy, r in [
    ("circle r = 1 around the centre", 0, 0, 1.0),
    ("circle r = 2 around the centre", 0, 0, 2.0),
    ("circle r = 0.5 NOT enclosing centre", 2, 0, 0.5),
]:
    g_free = circulation(free, cx, cy, r)
    g_free = 0.0 if abs(g_free) < 1e-9 else g_free
    print(f"{label:<38} {circulation(forced, cx, cy, r):>14.4f} {g_free:>12.4f}")
print("\nForced vortex: Gamma = 2 omega x area (vorticity 2 omega = 4 1/s everywhere).")
print("Free vortex: Gamma = 2 pi K for ANY loop around the centre, zero for loops that miss it -")
print("the flow is irrotational except at the singular centre. Potential flow allows circulation")
print("(and hence lift) even though every fluid element is irrotational.")
