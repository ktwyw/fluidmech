"""Water hammer: pressure surges in pipelines caused by rapid flow changes."""

from __future__ import annotations

import math

WATER_BULK_MODULUS = 2.2e9
"""Bulk modulus of water near 20 degC [Pa]."""

PIPE_YOUNGS_MODULUS = {
    "steel": 200e9,
    "ductile_iron": 170e9,
    "cast_iron": 100e9,
    "copper": 117e9,
    "concrete": 30e9,
    "pvc": 3.0e9,
    "hdpe": 0.9e9,
}
"""Young's modulus of common pipe materials [Pa]."""


def wave_speed(
    density: float = 1000.0,
    bulk_modulus: float = WATER_BULK_MODULUS,
    diameter: float | None = None,
    wall_thickness: float | None = None,
    youngs_modulus: float | None = None,
    restraint_factor: float = 1.0,
) -> float:
    """Pressure-wave speed [m/s] (Korteweg formula).

    c = sqrt( (K/rho) / (1 + c1 K D / (E e)) )

    Omit the pipe properties for a rigid pipe (c = sqrt(K/rho)).
    """
    base = bulk_modulus / density
    if diameter is None or wall_thickness is None or youngs_modulus is None:
        return math.sqrt(base)
    return math.sqrt(base / (1.0 + restraint_factor * bulk_modulus * diameter / (youngs_modulus * wall_thickness)))


def joukowsky_surge(density: float, wave_speed_: float, velocity_change: float) -> float:
    """Joukowsky pressure rise dp = rho c dV [Pa] for closure faster than 2L/c."""
    return density * wave_speed_ * abs(velocity_change)


def critical_closure_time(length: float, wave_speed_: float) -> float:
    """Pipe period 2L/c [s]: closures faster than this give the full Joukowsky surge."""
    return 2.0 * length / wave_speed_


def surge_pressure(density: float, wave_speed_: float, velocity: float, length: float, closure_time: float) -> float:
    """Peak surge [Pa] for a valve closed linearly in ``closure_time``.

    Uses Joukowsky for rapid closure and Michaud's formula 2 rho L V / t_c for slow closure.
    """
    if closure_time <= critical_closure_time(length, wave_speed_):
        return joukowsky_surge(density, wave_speed_, velocity)
    return 2.0 * density * length * abs(velocity) / closure_time


# ---------------------------------------------------------------------------- #
# Method of characteristics (MOC): reservoir - pipe - closing valve
# ---------------------------------------------------------------------------- #
def moc_valve_closure(
    length: float,
    diameter: float,
    wave_speed_: float,
    friction_factor: float,
    initial_velocity: float,
    reservoir_head: float,
    closure_time: float,
    sections: int = 20,
    t_end: float | None = None,
    snapshot_every: int = 0,
    g: float = 9.80665,
) -> dict:
    """Transient flow after a downstream valve closes linearly in ``closure_time`` [s].

    Classical MOC (Wylie & Streeter; Chaudhry): the pipe is split into ``sections`` reaches,
    dt = dx / c, and along the characteristics C+ and C-
        C+:  H_P = C_P - B Q_P,   C_P = H_A + B Q_A - R Q_A |Q_A|
        C-:  H_P = C_M + B Q_P,   C_M = H_B - B Q_B + R Q_B |Q_B|
    with B = c / (g A) and R = f dx / (2 g D A^2). The upstream reservoir fixes H; at the valve
    Q_P = -B Cv + sqrt((B Cv)^2 + 2 Cv C_P) with Cv = (tau Q0)^2 / (2 H0_valve).

    Returns a dict with 'time', 'head_valve', 'flow_valve', 'head_max'/'head_min' envelopes
    along the pipe, 'x', and (if ``snapshot_every`` > 0) 'snapshots' of the head profile.
    """
    area = math.pi * diameter**2 / 4
    q0 = initial_velocity * area
    n = sections
    dx = length / n
    dt = dx / wave_speed_  # Courant number 1: characteristics pass exactly through grid nodes
    B = wave_speed_ / (g * area)
    R = friction_factor * dx / (2 * g * diameter * area**2)
    # steady initial state: head falls linearly by the friction loss
    heads = [reservoir_head - R * q0 * q0 * i for i in range(n + 1)]
    flows = [q0] * (n + 1)
    h0_valve = heads[-1]
    t_end = t_end if t_end is not None else 10 * length / wave_speed_
    steps = int(round(t_end / dt))
    out = {
        "x": [i * dx for i in range(n + 1)],
        "time": [0.0],
        "head_valve": [h0_valve],
        "flow_valve": [q0],
        "head_max": list(heads),
        "head_min": list(heads),
        "snapshots": [],
        "dt": dt,
    }
    if snapshot_every:
        out["snapshots"].append((0.0, list(heads)))
    for step in range(1, steps + 1):
        t = step * dt
        new_h, new_q = [0.0] * (n + 1), [0.0] * (n + 1)
        for i in range(1, n):  # interior nodes: intersect C+ from i-1 and C- from i+1
            cp = heads[i - 1] + B * flows[i - 1] - R * flows[i - 1] * abs(flows[i - 1])
            cm = heads[i + 1] - B * flows[i + 1] + R * flows[i + 1] * abs(flows[i + 1])
            new_h[i] = 0.5 * (cp + cm)
            new_q[i] = (cp - cm) / (2 * B)
        # upstream reservoir: head fixed, flow from the C- characteristic
        cm = heads[1] - B * flows[1] + R * flows[1] * abs(flows[1])
        new_h[0] = reservoir_head
        new_q[0] = (reservoir_head - cm) / B
        # downstream valve: relative opening tau falls linearly to zero
        tau = max(0.0, 1.0 - t / closure_time)
        cp = heads[n - 1] + B * flows[n - 1] - R * flows[n - 1] * abs(flows[n - 1])
        cv = (tau * q0) ** 2 / (2 * h0_valve)
        new_q[n] = -B * cv + math.sqrt((B * cv) ** 2 + 2 * cv * cp) if cv > 0 else 0.0
        new_h[n] = cp - B * new_q[n]
        heads, flows = new_h, new_q
        out["time"].append(t)
        out["head_valve"].append(heads[-1])
        out["flow_valve"].append(flows[-1])
        out["head_max"] = [max(a, b) for a, b in zip(out["head_max"], heads)]
        out["head_min"] = [min(a, b) for a, b in zip(out["head_min"], heads)]
        if snapshot_every and step % snapshot_every == 0:
            out["snapshots"].append((t, list(heads)))
    return out
