"""Two-dimensional potential (inviscid, irrotational) flow by superposition.

Elementary flows (uniform stream, source/sink, vortex, doublet) can be added
with ``+`` to build flows past half-bodies, cylinders and more. Each provides
the velocity, stream function psi and velocity potential phi at a point.

Examples
--------
>>> flow = cylinder(U=10.0, radius=1.0)
>>> u, v = flow.velocity(0.0, 1.0)      # top of the cylinder: 2U
>>> round(u, 6), round(v, 6)
(20.0, 0.0)
>>> round(flow.pressure_coefficient(0.0, 1.0, 10.0), 6)
-3.0
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


class _Element:
    def velocity(self, x: float, y: float) -> tuple[float, float]:
        raise NotImplementedError

    def stream_function(self, x: float, y: float) -> float:
        raise NotImplementedError

    def potential(self, x: float, y: float) -> float:
        raise NotImplementedError

    def __add__(self, other: _Element) -> Flow:
        return Flow([self]) + other


@dataclass(frozen=True)
class Uniform(_Element):
    """Uniform stream of speed U at angle ``angle_deg`` to the x axis."""

    U: float
    angle_deg: float = 0.0

    def _components(self) -> tuple[float, float]:
        a = math.radians(self.angle_deg)
        return self.U * math.cos(a), self.U * math.sin(a)

    def velocity(self, x, y):
        return self._components()

    def stream_function(self, x, y):
        u, v = self._components()
        return u * y - v * x

    def potential(self, x, y):
        u, v = self._components()
        return u * x + v * y


@dataclass(frozen=True)
class Source(_Element):
    """Line source of strength m [m^2/s] (volume flow per unit depth); negative m is a sink."""

    m: float
    x0: float = 0.0
    y0: float = 0.0

    def velocity(self, x, y):
        dx, dy = x - self.x0, y - self.y0
        r2 = dx * dx + dy * dy
        if r2 == 0:
            raise ValueError("Velocity is singular at the source.")
        k = self.m / (2.0 * math.pi * r2)
        return k * dx, k * dy

    def stream_function(self, x, y):
        return self.m / (2.0 * math.pi) * math.atan2(y - self.y0, x - self.x0)

    def potential(self, x, y):
        return self.m / (2.0 * math.pi) * math.log(math.hypot(x - self.x0, y - self.y0))


@dataclass(frozen=True)
class Vortex(_Element):
    """Free (irrotational) vortex with circulation Gamma [m^2/s], positive counter-clockwise."""

    gamma: float
    x0: float = 0.0
    y0: float = 0.0

    def velocity(self, x, y):
        dx, dy = x - self.x0, y - self.y0
        r2 = dx * dx + dy * dy
        if r2 == 0:
            raise ValueError("Velocity is singular at the vortex centre.")
        k = self.gamma / (2.0 * math.pi * r2)
        return -k * dy, k * dx

    def stream_function(self, x, y):
        return -self.gamma / (2.0 * math.pi) * math.log(math.hypot(x - self.x0, y - self.y0))

    def potential(self, x, y):
        return self.gamma / (2.0 * math.pi) * math.atan2(y - self.y0, x - self.x0)


@dataclass(frozen=True)
class Doublet(_Element):
    """Doublet of strength kappa [m^3/s] pointing in -x (source-sink pair limit)."""

    kappa: float
    x0: float = 0.0
    y0: float = 0.0

    def velocity(self, x, y):
        dx, dy = x - self.x0, y - self.y0
        r2 = dx * dx + dy * dy
        if r2 == 0:
            raise ValueError("Velocity is singular at the doublet.")
        k = self.kappa / (2.0 * math.pi * r2 * r2)
        return -k * (dx * dx - dy * dy), -k * 2.0 * dx * dy

    def stream_function(self, x, y):
        dx, dy = x - self.x0, y - self.y0
        return -self.kappa / (2.0 * math.pi) * dy / (dx * dx + dy * dy)

    def potential(self, x, y):
        dx, dy = x - self.x0, y - self.y0
        return self.kappa / (2.0 * math.pi) * dx / (dx * dx + dy * dy)


@dataclass
class Flow(_Element):
    """Superposition of elementary flows."""

    elements: list = field(default_factory=list)

    def __add__(self, other: _Element) -> Flow:
        extra = other.elements if isinstance(other, Flow) else [other]
        return Flow(self.elements + list(extra))

    def velocity(self, x, y):
        u = v = 0.0
        for e in self.elements:
            du, dv = e.velocity(x, y)
            u += du
            v += dv
        return u, v

    def speed(self, x, y) -> float:
        return math.hypot(*self.velocity(x, y))

    def stream_function(self, x, y):
        return sum(e.stream_function(x, y) for e in self.elements)

    def potential(self, x, y):
        return sum(e.potential(x, y) for e in self.elements)

    def pressure_coefficient(self, x, y, free_stream_speed: float) -> float:
        """Cp = (p - p_inf) / (rho U^2 / 2) = 1 - (V / U)^2 from Bernoulli."""
        return 1.0 - (self.speed(x, y) / free_stream_speed) ** 2


def cylinder(U: float, radius: float, circulation: float = 0.0) -> Flow:
    """Flow past a circular cylinder (uniform stream + doublet [+ vortex for lift])."""
    flow = Flow([Uniform(U), Doublet(2.0 * math.pi * U * radius**2)])
    if circulation:
        flow = flow + Vortex(circulation)
    return flow


def rankine_half_body(U: float, m: float) -> Flow:
    """Uniform stream plus a source at the origin; stagnation point at x = -m / (2 pi U)."""
    return Flow([Uniform(U), Source(m)])


def rankine_oval(U: float, m: float, a: float) -> Flow:
    """Uniform stream with a source at x = -a and an equal sink at x = +a."""
    return Flow([Uniform(U), Source(m, -a, 0.0), Source(-m, a, 0.0)])


def kutta_joukowski_lift(density: float, U: float, circulation: float) -> float:
    """Lift per unit span L' = rho U Gamma [N/m] (drag is zero: d'Alembert's paradox)."""
    return density * U * circulation
