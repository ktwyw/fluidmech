"""Small, dependency-free root-finding helpers used internally."""

from __future__ import annotations

from typing import Callable

Func = Callable[[float], float]


def bisect(
    func: Func,
    lo: float,
    hi: float,
    *,
    xtol: float = 1e-15,
    rtol: float = 1e-12,
    maxiter: int = 300,
) -> float:
    """Find a root of ``func`` in ``[lo, hi]`` by bisection.

    ``func(lo)`` and ``func(hi)`` must have opposite signs.
    """
    f_lo, f_hi = func(lo), func(hi)
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if f_lo * f_hi > 0.0:
        raise ValueError("Root is not bracketed: func(lo) and func(hi) have the same sign.")

    for _ in range(maxiter):  # halve the bracket until it is narrower than the tolerance
        mid = 0.5 * (lo + hi)  # midpoint of the current bracket
        f_mid = func(mid)
        if f_mid == 0.0 or 0.5 * (hi - lo) <= xtol + rtol * abs(mid):
            return mid
        if f_lo * f_mid < 0.0:  # sign change in the lower half -> root lies in [lo, mid]
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    raise RuntimeError("Bisection did not converge.")


def positive_root(func: Func, guess: float = 1.0, *, max_expansions: int = 80) -> float:
    """Find a root of ``func`` on the positive real axis.

    Starting from ``guess``, the bracket ``[lo, hi]`` is widened geometrically
    (``lo /= 2``, ``hi *= 2``) until ``func`` changes sign, then bisection is used.
    Suitable for monotonic engineering relations such as head loss vs. flow rate.
    """
    if guess <= 0.0:
        raise ValueError("guess must be positive.")
    lo = hi = guess
    f_lo = f_hi = func(guess)
    if f_lo == 0.0:
        return guess
    for _ in range(max_expansions):  # widen the bracket geometrically until func changes sign
        lo /= 2.0
        hi *= 2.0
        f_lo, f_hi = func(lo), func(hi)
        if f_lo * f_hi <= 0.0:
            return bisect(func, lo, hi)
    raise RuntimeError("Could not bracket a positive root.")


def solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Solve the square linear system ``A x = b`` by Gaussian elimination.

    Uses partial pivoting. Intended for the small systems that arise in
    engineering calculations (tens to a few hundred unknowns).
    """
    n = len(rhs)
    if any(len(row) != n for row in matrix) or len(matrix) != n:
        raise ValueError("matrix must be square and match the length of rhs.")
    a = [list(map(float, row)) + [float(b)] for row, b in zip(matrix, rhs)]  # augmented matrix [A | b]
    for col in range(n):
        # partial pivoting: use the largest entry in this column
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-300:
            raise ValueError("Matrix is singular (check that every node connects to a fixed head).")
        a[col], a[pivot] = a[pivot], a[col]
        for row in range(col + 1, n):  # forward elimination: zero the column below the pivot
            factor = a[row][col] / a[col][col]
            if factor:
                for k in range(col, n + 1):
                    a[row][k] -= factor * a[col][k]
    x = [0.0] * n  # back substitution, from the last unknown upwards
    for row in range(n - 1, -1, -1):
        s = a[row][n] - sum(a[row][k] * x[k] for k in range(row + 1, n))
        x[row] = s / a[row][row]
    return x


def polyfit(x: list[float], y: list[float], degree: int) -> list[float]:
    """Least-squares polynomial fit. Returns coefficients ``[c0, c1, ..., c_degree]``."""
    if len(x) != len(y) or len(x) <= degree:
        raise ValueError("Need more data points than the polynomial degree.")
    m = degree + 1
    # normal equations (V^T V) c = V^T y, V = Vandermonde matrix
    ata = [[sum(xi ** (i + j) for xi in x) for j in range(m)] for i in range(m)]
    aty = [sum(yi * xi**i for xi, yi in zip(x, y)) for i in range(m)]
    return solve_linear(ata, aty)
