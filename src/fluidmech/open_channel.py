"""Uniform and critical flow in prismatic open channels (SI units, Manning's equation)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._solvers import positive_root
from .constants import G

MANNING_N = {
    "glass": 0.010,
    "finished_concrete": 0.012,
    "unfinished_concrete": 0.014,
    "brickwork": 0.015,
    "earth_clean": 0.022,
    "earth_gravel": 0.025,
    "natural_stream_clean": 0.030,
    "natural_stream_weedy": 0.050,
}
"""Typical Manning roughness coefficients n [s/m^(1/3)]."""


@dataclass(frozen=True)
class TrapezoidalChannel:
    """Prismatic trapezoidal channel.

    Parameters
    ----------
    bottom_width : Bottom width b [m]. Use 0 for a triangular channel.
    side_slope : Side slope z (horizontal : vertical = z : 1). Use 0 for a
        rectangular channel.
    """

    bottom_width: float
    side_slope: float = 0.0

    def __post_init__(self) -> None:
        if self.bottom_width < 0 or self.side_slope < 0:
            raise ValueError("bottom_width and side_slope must be non-negative.")
        if self.bottom_width == 0 and self.side_slope == 0:
            raise ValueError("Channel must have a non-zero width.")

    # ---- geometry --------------------------------------------------------- #
    def area(self, depth: float) -> float:
        """Flow area A [m^2]."""
        return (self.bottom_width + self.side_slope * depth) * depth

    def wetted_perimeter(self, depth: float) -> float:
        """Wetted perimeter P [m]."""
        return self.bottom_width + 2.0 * depth * math.sqrt(1.0 + self.side_slope**2)

    def top_width(self, depth: float) -> float:
        """Free-surface width T [m]."""
        return self.bottom_width + 2.0 * self.side_slope * depth

    def hydraulic_radius(self, depth: float) -> float:
        """Hydraulic radius R = A / P [m]."""
        return self.area(depth) / self.wetted_perimeter(depth)

    def hydraulic_depth(self, depth: float) -> float:
        """Hydraulic depth D = A / T [m]."""
        return self.area(depth) / self.top_width(depth)

    # ---- flow ------------------------------------------------------------- #
    def discharge(self, depth: float, manning_n: float, slope: float) -> float:
        """Uniform-flow discharge from Manning's equation [m^3/s].

        Q = (1/n) A R^(2/3) S^(1/2)
        """
        _check_positive(depth=depth, manning_n=manning_n, slope=slope)
        return self.area(depth) * self.hydraulic_radius(depth) ** (2.0 / 3.0) * math.sqrt(slope) / manning_n

    def normal_depth(self, flow_rate: float, manning_n: float, slope: float) -> float:
        """Normal (uniform-flow) depth y_n [m] for a given discharge."""
        _check_positive(flow_rate=flow_rate, manning_n=manning_n, slope=slope)
        # Manning discharge rises with depth: unique root
        return positive_root(lambda y: self.discharge(y, manning_n, slope) - flow_rate)

    def froude(self, depth: float, flow_rate: float, g: float = G) -> float:
        """Froude number Fr = V / sqrt(g D), D = hydraulic depth."""
        _check_positive(depth=depth)
        velocity = flow_rate / self.area(depth)
        return velocity / math.sqrt(g * self.hydraulic_depth(depth))

    def critical_depth(self, flow_rate: float, g: float = G) -> float:
        """Critical depth y_c [m], where Q^2 T / (g A^3) = 1."""
        _check_positive(flow_rate=flow_rate)
        return positive_root(lambda y: self.froude(y, flow_rate, g) - 1.0)  # critical flow: Froude number equal to one

    def specific_energy(self, depth: float, flow_rate: float, g: float = G) -> float:
        """Specific energy E = y + V^2/(2g) [m]."""
        _check_positive(depth=depth)
        velocity = flow_rate / self.area(depth)
        return depth + velocity**2 / (2.0 * g)

    def flow_type(self, depth: float, flow_rate: float, g: float = G) -> str:
        """'subcritical', 'critical' or 'supercritical'."""
        fr = self.froude(depth, flow_rate, g)
        if math.isclose(fr, 1.0, rel_tol=1e-3):
            return "critical"
        return "subcritical" if fr < 1.0 else "supercritical"


class RectangularChannel(TrapezoidalChannel):
    """Rectangular channel of width ``width`` [m]."""

    def __init__(self, width: float) -> None:
        super().__init__(bottom_width=width, side_slope=0.0)

    def __repr__(self) -> str:
        return f"RectangularChannel(width={self.bottom_width!r})"


def hydraulic_jump_depth(upstream_depth: float, upstream_froude: float) -> float:
    """Sequent depth after a hydraulic jump in a rectangular channel [m].

    y2 / y1 = 0.5 (sqrt(1 + 8 Fr1^2) - 1)
    """
    _check_positive(upstream_depth=upstream_depth)
    if upstream_froude <= 1.0:
        raise ValueError("A hydraulic jump requires supercritical upstream flow (Fr1 > 1).")
    return 0.5 * upstream_depth * (math.sqrt(1.0 + 8.0 * upstream_froude**2) - 1.0)


def _check_positive(**values: float) -> None:
    for name, value in values.items():
        if value <= 0:
            raise ValueError(f"{name} must be positive.")


def hydraulic_jump_energy_loss(upstream_depth: float, downstream_depth: float) -> float:
    """Head lost in a hydraulic jump in a rectangular channel, (y2 - y1)^3 / (4 y1 y2) [m]."""
    _check_positive(upstream_depth=upstream_depth, downstream_depth=downstream_depth)
    y1, y2 = upstream_depth, downstream_depth
    return (y2 - y1) ** 3 / (4.0 * y1 * y2)


# ---------------------------------------------------------------------------- #
# Flow-measurement and control structures
# ---------------------------------------------------------------------------- #
def rectangular_weir_flow(head: float, crest_length: float, discharge_coefficient: float = 0.62, g: float = G) -> float:
    """Sharp-crested rectangular weir, Q = Cd (2/3) sqrt(2g) L H^1.5 [m^3/s]."""
    _check_positive(head=head, crest_length=crest_length)
    return discharge_coefficient * (2.0 / 3.0) * math.sqrt(2.0 * g) * crest_length * head**1.5


def v_notch_weir_flow(
    head: float, notch_angle_deg: float = 90.0, discharge_coefficient: float = 0.58, g: float = G
) -> float:
    """Sharp-crested triangular (V-notch) weir, Q = Cd (8/15) sqrt(2g) tan(theta/2) H^2.5 [m^3/s]."""
    _check_positive(head=head)
    tan_half = math.tan(math.radians(notch_angle_deg / 2.0))
    return discharge_coefficient * (8.0 / 15.0) * math.sqrt(2.0 * g) * tan_half * head**2.5


def broad_crested_weir_flow(head: float, width: float, discharge_coefficient: float = 0.95, g: float = G) -> float:
    """Broad-crested weir (critical depth on the crest), Q = Cd b sqrt(g) (2H/3)^1.5 [m^3/s]."""
    _check_positive(head=head, width=width)
    return discharge_coefficient * width * math.sqrt(g) * (2.0 * head / 3.0) ** 1.5


def sluice_gate_flow(
    gate_opening: float,
    upstream_depth: float,
    width: float,
    discharge_coefficient: float = 0.61,
    g: float = G,
) -> float:
    """Free flow under a vertical sluice gate, Q = Cd b a sqrt(2 g y1) [m^3/s]."""
    _check_positive(gate_opening=gate_opening, upstream_depth=upstream_depth, width=width)
    if gate_opening >= upstream_depth:
        raise ValueError("gate_opening must be smaller than the upstream depth.")
    return discharge_coefficient * width * gate_opening * math.sqrt(2.0 * g * upstream_depth)


# ---------------------------------------------------------------------------- #
# Gradually varied flow
# ---------------------------------------------------------------------------- #
def friction_slope(channel: TrapezoidalChannel, depth: float, flow_rate: float, manning_n: float) -> float:
    """Energy slope S_f from Manning's equation at the given depth."""
    velocity = flow_rate / channel.area(depth)
    return (manning_n * velocity) ** 2 / channel.hydraulic_radius(depth) ** (4.0 / 3.0)


def classify_profile(
    channel: TrapezoidalChannel, flow_rate: float, manning_n: float, slope: float, depth: float
) -> str:
    """Classify a gradually varied flow profile: M1-M3, S1-S3, C1/C3, H2/H3 or A2/A3."""
    yc = channel.critical_depth(flow_rate)  # critical depth decides between zones 1-2-3 together with y_n
    if slope <= 0:
        letter = "H" if slope == 0 else "A"
        return f"{letter}2" if depth > yc else f"{letter}3"
    yn = channel.normal_depth(flow_rate, manning_n, slope)
    if math.isclose(yn, yc, rel_tol=1e-3):
        return "C1" if depth > yc else "C3"
    letter = "M" if yn > yc else "S"
    upper, lower = max(yn, yc), min(yn, yc)
    zone = 1 if depth > upper else (2 if depth > lower else 3)  # zone 1 above both y_n and y_c, 3 below both
    return f"{letter}{zone}"


def gvf_profile(
    channel: TrapezoidalChannel,
    flow_rate: float,
    manning_n: float,
    slope: float,
    start_depth: float,
    end_depth: float,
    steps: int = 50,
) -> list[tuple[float, float]]:
    """Water-surface profile by the direct step method.

    Starts at a control section with depth ``start_depth`` (x = 0) and steps in
    depth towards ``end_depth``. Returns (x, y) pairs where x is the distance
    along the channel measured in the flow direction: negative values lie
    upstream of the control (subcritical profiles are computed upstream from a
    downstream control, supercritical ones downstream from an upstream control).

    ``end_depth`` must not equal the normal depth exactly (it is approached
    asymptotically); stop about 1 % short of it.
    """
    _check_positive(flow_rate=flow_rate, manning_n=manning_n, start_depth=start_depth, end_depth=end_depth)
    if steps < 1:
        raise ValueError("steps must be at least 1.")
    dy = (end_depth - start_depth) / steps  # direct step: fix the depth increment, compute the distance
    x, y = 0.0, start_depth
    profile = [(x, y)]
    for _ in range(steps):
        y_next = y + dy
        # change of specific energy
        de = channel.specific_energy(y_next, flow_rate) - channel.specific_energy(y, flow_rate)
        # mean friction slope over the step
        sf = 0.5 * (
            friction_slope(channel, y, flow_rate, manning_n) + friction_slope(channel, y_next, flow_rate, manning_n)
        )
        denominator = slope - sf
        if denominator == 0:
            raise ValueError("Reached normal depth; choose an end_depth short of it.")
        x += de / denominator  # dx = dE / (S0 - Sf)
        y = y_next
        profile.append((x, y))
    return profile
