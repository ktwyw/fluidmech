"""Public numerical helpers for your own engineering calculations.

Examples
--------
>>> from fluidmech.solvers import bisect, solve_linear
>>> round(bisect(lambda x: x**2 - 2.0, 0.0, 2.0), 6)
1.414214
>>> solve_linear([[2.0, 1.0], [1.0, 3.0]], [3.0, 5.0])
[0.8, 1.4]
"""

from ._solvers import bisect, polyfit, positive_root, solve_linear

__all__ = ["bisect", "polyfit", "positive_root", "solve_linear"]
