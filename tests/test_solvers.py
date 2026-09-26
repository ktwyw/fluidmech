"""Numerical helpers: bisection, bracket expansion, linear systems with pivoting, polynomial fits."""

import math

import pytest

from fluidmech.solvers import bisect, positive_root


def test_bisect_sqrt2():
    assert bisect(lambda x: x * x - 2.0, 0.0, 2.0) == pytest.approx(math.sqrt(2.0), rel=1e-10)


def test_bisect_requires_bracket():
    with pytest.raises(ValueError):
        bisect(lambda x: x * x + 1.0, -1.0, 1.0)


def test_positive_root_expands_bracket():
    assert positive_root(lambda x: x - 1234.5, guess=1.0) == pytest.approx(1234.5, rel=1e-10)
    assert positive_root(lambda x: x - 1e-4, guess=1.0) == pytest.approx(1e-4, rel=1e-10)


from fluidmech.solvers import polyfit, solve_linear  # noqa: E402


def test_solve_linear_needs_pivoting():
    x = solve_linear([[0.0, 2.0, 1.0], [1.0, 1.0, 1.0], [2.0, 1.0, 0.0]], [5.0, 4.0, 4.0])
    assert x == pytest.approx([1.0, 2.0, 1.0])


def test_solve_linear_singular():
    with pytest.raises(ValueError):
        solve_linear([[1.0, 2.0], [2.0, 4.0]], [1.0, 2.0])


def test_polyfit_exact_quadratic():
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    assert polyfit(xs, [3 - 2 * x + 0.5 * x * x for x in xs], 2) == pytest.approx([3.0, -2.0, 0.5])
