"""Dimensional analysis: the Buckingham Pi theorem, done automatically.

Describe each variable by its dimensions in terms of mass M, length L, time T
and temperature Theta, and :func:`pi_groups` returns a complete set of
independent dimensionless groups, computed exactly with rational arithmetic.

Examples
--------
>>> groups = pi_groups(
...     {"dp": "M L^-1 T^-2", "rho": "M L^-3", "V": "L T^-1", "D": "L", "mu": "M L^-1 T^-1"},
...     repeating=["rho", "V", "D"],
... )
>>> [format_group(g) for g in groups]
['dp rho^-1 V^-2', 'mu rho^-1 V^-1 D^-1']
"""

from __future__ import annotations

import re
from fractions import Fraction

BASE = ("M", "L", "T", "Theta")

COMMON = {
    "length": "L",
    "diameter": "L",
    "area": "L^2",
    "volume": "L^3",
    "velocity": "L T^-1",
    "acceleration": "L T^-2",
    "gravity": "L T^-2",
    "flow_rate": "L^3 T^-1",
    "mass_flow": "M T^-1",
    "density": "M L^-3",
    "pressure": "M L^-1 T^-2",
    "stress": "M L^-1 T^-2",
    "dynamic_viscosity": "M L^-1 T^-1",
    "kinematic_viscosity": "L^2 T^-1",
    "surface_tension": "M T^-2",
    "force": "M L T^-2",
    "power": "M L^2 T^-3",
    "energy": "M L^2 T^-2",
    "torque": "M L^2 T^-2",
    "frequency": "T^-1",
    "angular_velocity": "T^-1",
    "specific_energy": "L^2 T^-2",
    "bulk_modulus": "M L^-1 T^-2",
    "temperature": "Theta",
    "time": "T",
    "dissipation_rate": "L^2 T^-3",
    "roughness": "L",
}
"""Dimensions of common fluid-mechanics quantities."""

_TOKEN = re.compile(r"^(M|L|T|Theta)(?:\^?(-?\d+(?:/\d+)?))?$")


def parse_dimension(text: str) -> tuple[Fraction, ...]:
    """Parse a dimension string such as 'M L^-1 T^-2' (or '1' for dimensionless)."""
    exps = dict.fromkeys(BASE, Fraction(0))
    text = text.strip()
    if text in ("", "1", "-"):
        return tuple(exps.values())
    for token in text.replace("*", " ").split():
        m = _TOKEN.match(token)
        if not m:
            raise ValueError(f"Cannot parse dimension token {token!r} (use M, L, T, Theta with ^ exponents).")
        exps[m.group(1)] += Fraction(m.group(2) or 1)
    return tuple(exps.values())


def _as_vector(dim) -> tuple[Fraction, ...]:
    if isinstance(dim, str):
        return parse_dimension(COMMON.get(dim, dim))
    vec = tuple(Fraction(x) for x in dim)
    if len(vec) != len(BASE):
        raise ValueError("Dimension tuples must have four entries (M, L, T, Theta).")
    return vec


def _rank(rows: list[list[Fraction]]) -> int:
    m = [list(r) for r in rows]
    rank, ncols = 0, len(m[0]) if m else 0  # Gaussian elimination in exact fractions; rank = number of pivots
    for col in range(ncols):
        # any non-zero entry can be the pivot (exact arithmetic)
        pivot = next((r for r in range(rank, len(m)) if m[r][col] != 0), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        for r in range(len(m)):
            if r != rank and m[r][col] != 0:
                f = m[r][col] / m[rank][col]
                m[r] = [a - f * b for a, b in zip(m[r], m[rank])]
        rank += 1
    return rank


def _solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve a (possibly over-determined but consistent) rational system by elimination."""
    rows = [list(r) + [b] for r, b in zip(matrix, rhs)]  # augmented matrix; reduced to row-echelon form below
    n = len(matrix[0])
    rank = 0
    pivots = []
    for col in range(n):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        rows[rank] = [x / rows[rank][col] for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rank])]
        pivots.append(col)
        rank += 1
    if any(all(x == 0 for x in r[:-1]) and r[-1] != 0 for r in rows):  # a row 0 = c (c != 0) means no solution exists
        raise ValueError("Inconsistent system: the repeating variables cannot cancel this variable's dimensions.")
    sol = [Fraction(0)] * n
    for i, col in enumerate(pivots):
        sol[col] = rows[i][-1]
    return sol


def dimension_matrix_rank(variables: dict[str, object]) -> int:
    """Rank r of the dimensional matrix; the number of Pi groups is n - r."""
    vecs = [_as_vector(d) for d in variables.values()]
    return _rank([[v[i] for v in vecs] for i in range(len(BASE))])


def pi_groups(variables: dict[str, object], repeating: list[str] | None = None) -> list[dict[str, Fraction]]:
    """Find a complete set of dimensionless Pi groups (Buckingham Pi theorem).

    Parameters
    ----------
    variables : mapping name -> dimension, given as a string ('M L^-3'), a name from
        :data:`COMMON` ('density'), or a tuple of exponents (M, L, T, Theta).
        Put the dependent variable first.
    repeating : the r repeating variables. If omitted, they are chosen automatically as the
        first dimensionally independent variables AFTER the dependent one, so list the
        variables as: dependent variable, then your preferred repeating set (e.g. rho, V, D).

    Returns
    -------
    One dict per group mapping variable name -> exponent (non-repeating variable to the power 1).
    """
    names = list(variables)
    vecs = {n: _as_vector(variables[n]) for n in names}
    r = dimension_matrix_rank(variables)
    if repeating is None:
        repeating = []
        for name in names[1:]:  # greedy choice: keep a variable if it is independent of those already chosen
            trial = repeating + [name]
            if _rank([[vecs[v][i] for v in trial] for i in range(len(BASE))]) == len(trial):
                repeating = trial
            if len(repeating) == r:
                break
    if len(repeating) != r:
        raise ValueError(f"Need exactly {r} repeating variables (the rank of the dimensional matrix).")
    # columns = dimensions of the repeating variables
    rep_matrix = [[vecs[v][i] for v in repeating] for i in range(len(BASE))]
    if _rank(rep_matrix) != r:
        raise ValueError("The repeating variables are not dimensionally independent.")
    groups = []
    for name in names:
        if name in repeating:
            continue
        # exponents that cancel this variable's M, L, T, Theta
        exps = _solve(rep_matrix, [-vecs[name][i] for i in range(len(BASE))])
        group = {name: Fraction(1)}
        group.update({v: e for v, e in zip(repeating, exps) if e != 0})
        groups.append(group)
    return groups


def group_dimensions(group: dict[str, Fraction], variables: dict[str, object]) -> tuple[Fraction, ...]:
    """Net dimensions of a product of powers (all zeros for a valid Pi group)."""
    total = [Fraction(0)] * len(BASE)
    for name, e in group.items():
        for i, x in enumerate(_as_vector(variables[name])):
            total[i] += e * x
    return tuple(total)


def is_dimensionless(group: dict[str, Fraction], variables: dict[str, object]) -> bool:
    return all(x == 0 for x in group_dimensions(group, variables))


def format_group(group: dict[str, Fraction]) -> str:
    """Human-readable form, e.g. 'dp rho^-1 V^-2'."""
    parts = []
    for name, e in group.items():
        parts.append(name if e == 1 else f"{name}^{e}")
    return " ".join(parts)


def evaluate_group(group: dict[str, Fraction], values: dict[str, float]) -> float:
    """Numerical value of a group for given variable values (SI units)."""
    result = 1.0
    for name, e in group.items():
        result *= values[name] ** float(e)
    return result
