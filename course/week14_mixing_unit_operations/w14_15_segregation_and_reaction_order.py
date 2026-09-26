"""CHME 202 - Week 14 - Example 15: does micromixing change conversion? It depends on reaction order.

In a CSTR with a given RTD, two extremes of micromixing are possible: complete segregation
(fluid parcels never mix, each behaves as a batch reactor for its residence time) and
maximum mixedness (ideal CSTR). For first-order reactions both give the same conversion;
for second order, segregation gives MORE conversion, for half order LESS.
"""

import math

from fluidmech.solvers import bisect


def x_batch(t, k_c0, order):
    if order == 1:
        return 1 - math.exp(-k_c0 * t)
    if order == 2:
        return k_c0 * t / (1 + k_c0 * t)
    # order 0.5: dC/dt = -k C^0.5 (C0 = 1) -> sqrt(C) = 1 - k t / 2
    return 1 - max(0.0, 1 - k_c0 * t / 2) ** 2


def x_segregated(da, order, n=20000):
    # CSTR RTD with tau = 1: E(t) = exp(-t); integrate X_batch(t) E(t) dt
    dt = 30.0 / n  # integrate to t = 30 tau (E(t) is negligible beyond)
    return sum(x_batch((i + 0.5) * dt, da, order) * math.exp(-(i + 0.5) * dt) * dt for i in range(n))


def x_ideal_cstr(da, order):
    # design equation: X = Da (1 - X)^order  (tau = 1, C0 = 1)
    return bisect(lambda x: x - da * (1 - x) ** order, 0.0, 1.0 - 1e-12)


print(f"{'order':>6} {'Da = k tau C0^(n-1)':>20} {'maximum mixedness':>18} {'segregated':>11}")
for order in (0.5, 1, 2):
    for da in (0.5, 2.0):
        print(f"{order:>6} {da:>20} {x_ideal_cstr(da, order):>18.3f} {x_segregated(da, order):>11.3f}")
print("\nFor order > 1 keeping reactants concentrated (segregated) speeds the reaction; for order < 1 it")
print("slows it. Only first-order reactions are insensitive to micromixing - which is why mixing matters")
print("most for fast, non-linear and competing reactions (Example 6).")
