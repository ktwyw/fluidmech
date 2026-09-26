"""Steady-state pipe network solver (reservoirs, junctions, pipes and pumps).

The network is solved with Newton's method applied simultaneously to the
energy equation in every link and the continuity equation at every junction
(the "global gradient" formulation used by EPANET, Todini & Pilati 1988).
Unlike the Hardy Cross method, no loops need to be identified and any number
of fixed-head nodes (reservoirs, tanks) is allowed.

Friction is computed with Darcy-Weisbach and the Colebrook equation, so the
solver handles laminar, transitional and turbulent pipes consistently.

Example
-------
>>> from fluidmech.networks import Network
>>> net = Network()
>>> net.add_reservoir("R", head=50.0)
>>> net.add_junction("J", elevation=10.0, demand=0.02)
>>> net.add_pipe("P1", "R", "J", length=500.0, diameter=0.15, roughness=0.045e-3)
>>> result = net.solve()
>>> round(result.flows["P1"], 4)
0.02
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ._solvers import solve_linear
from .constants import G
from .pipe_flow import area, head_loss
from .properties import Fluid
from .pumps import PumpCurve


@dataclass
class _Junction:
    name: str
    elevation: float
    demand: float


@dataclass
class _Reservoir:
    name: str
    head: float


@dataclass
class _Pipe:
    name: str
    start: str
    end: str
    length: float
    diameter: float
    roughness: float
    k_minor: float


@dataclass
class _Pump:
    name: str
    start: str
    end: str
    curve: PumpCurve


@dataclass
class NetworkResult:
    """Solution of a pipe network. Flows are positive from ``start`` to ``end``."""

    flows: dict[str, float]
    """Link flow rates [m^3/s]."""
    heads: dict[str, float]
    """Piezometric head at every node [m]."""
    pressures: dict[str, float]
    """Gauge pressure at junctions [Pa] (reservoirs are omitted)."""
    velocities: dict[str, float]
    """Mean velocity in pipes [m/s] (absolute value)."""
    head_losses: dict[str, float]
    """Head loss along each pipe in the direction of flow [m]; pumps give negative values."""
    iterations: int
    max_continuity_error: float
    reservoir_outflows: dict[str, float] = field(default_factory=dict)
    """Net flow leaving each reservoir into the network [m^3/s]."""

    def summary(self) -> str:
        """Return a formatted text report."""
        lines = [
            f"Converged in {self.iterations} iterations (max continuity error {self.max_continuity_error:.1e} m3/s)",
            "",
        ]
        lines.append(f"{'Link':<10} {'Q [L/s]':>10} {'V [m/s]':>9} {'h_L [m]':>9}")
        for name, q in self.flows.items():
            v = self.velocities.get(name)
            v_txt = f"{v:>9.3f}" if v is not None else f"{'pump':>9}"
            lines.append(f"{name:<10} {q * 1000:>10.3f} {v_txt} {self.head_losses[name]:>9.3f}")
        lines.append("")
        lines.append(f"{'Node':<10} {'Head [m]':>10} {'p [kPa]':>9}")
        for name, h in self.heads.items():
            p = self.pressures.get(name)
            p_txt = f"{p / 1e3:>9.2f}" if p is not None else f"{'(fixed)':>9}"
            lines.append(f"{name:<10} {h:>10.3f} {p_txt}")
        return "\n".join(lines)


class Network:
    """A steady-state pipe network.

    Build it with :meth:`add_reservoir`, :meth:`add_junction`, :meth:`add_pipe`
    and :meth:`add_pump`, then call :meth:`solve`.
    """

    def __init__(self, fluid: Fluid | None = None) -> None:
        self.fluid = fluid if fluid is not None else Fluid.water(20.0)
        self._junctions: dict[str, _Junction] = {}
        self._reservoirs: dict[str, _Reservoir] = {}
        self._links: dict[str, _Pipe | _Pump] = {}

    # ---- building ---------------------------------------------------------- #
    def _check_new_node(self, name: str) -> None:
        if name in self._junctions or name in self._reservoirs:
            raise ValueError(f"Node {name!r} already exists.")

    def add_junction(self, name: str, elevation: float = 0.0, demand: float = 0.0) -> None:
        """Add a junction. ``demand`` [m^3/s] is withdrawn from the network (negative = inflow)."""
        self._check_new_node(name)
        self._junctions[name] = _Junction(name, elevation, demand)

    def add_reservoir(self, name: str, head: float) -> None:
        """Add a fixed-head node (reservoir or tank water level) [m]."""
        self._check_new_node(name)
        self._reservoirs[name] = _Reservoir(name, head)

    def _check_link(self, name: str, start: str, end: str) -> None:
        if name in self._links:
            raise ValueError(f"Link {name!r} already exists.")
        for node in (start, end):
            if node not in self._junctions and node not in self._reservoirs:
                raise ValueError(f"Unknown node {node!r}; add it before connecting links.")
        if start == end:
            raise ValueError("A link must connect two different nodes.")

    def add_pipe(
        self,
        name: str,
        start: str,
        end: str,
        length: float,
        diameter: float,
        roughness: float = 0.0,
        k_minor: float = 0.0,
    ) -> None:
        """Add a pipe. The positive flow direction is from ``start`` to ``end``."""
        self._check_link(name, start, end)
        if length <= 0 or diameter <= 0 or roughness < 0 or k_minor < 0:
            raise ValueError("Invalid pipe properties.")
        self._links[name] = _Pipe(name, start, end, length, diameter, roughness, k_minor)

    def add_pump(self, name: str, start: str, end: str, curve: PumpCurve) -> None:
        """Add a pump lifting water from ``start`` (suction) to ``end`` (discharge)."""
        self._check_link(name, start, end)
        self._links[name] = _Pump(name, start, end, curve)

    # ---- hydraulics of a single link --------------------------------------- #
    def _pipe_loss(self, pipe: _Pipe, q: float) -> tuple[float, float]:
        """Signed head loss and its derivative dh/dQ for a pipe."""
        nu = self.fluid.kinematic_viscosity
        # Laminar (Hagen-Poiseuille) resistance for vanishing flows
        # laminar resistance h = r_lam Q (Hagen-Poiseuille)
        r_lam = 128.0 * nu * pipe.length / (G * math.pi * pipe.diameter**4)
        q_abs = abs(q)
        if q_abs < 1e-9:  # near-zero flow: use the linear laminar law (avoids 0/0 in Darcy-Weisbach)
            return r_lam * q, r_lam

        def h(qq: float) -> float:
            return head_loss(qq, pipe.diameter, pipe.length, self.fluid, pipe.roughness, pipe.k_minor).total_head_loss

        eps = 1e-6  # relative step for the numerical derivative dh/dQ
        loss = h(q_abs)
        dh = (h(q_abs * (1 + eps)) - h(q_abs * (1 - eps))) / (2 * eps * q_abs)  # central difference
        return math.copysign(loss, q), max(dh, r_lam)

    @staticmethod
    def _pump_loss(pump: _Pump, q: float) -> tuple[float, float]:
        """A pump is a link with a negative head loss equal to its head."""
        # a pump 'loses' negative head; dh/dQ kept positive for stability
        return -pump.curve.head(q), max(-pump.curve.head_slope(q), 1e-6)

    def _link_loss(self, link: _Pipe | _Pump, q: float) -> tuple[float, float]:
        if isinstance(link, _Pipe):
            return self._pipe_loss(link, q)
        return self._pump_loss(link, q)

    # ---- solver ------------------------------------------------------------ #
    def solve(self, tol: float = 1e-10, max_iterations: int = 100) -> NetworkResult:
        """Solve for all link flows and junction heads."""
        if not self._reservoirs:
            raise ValueError("The network needs at least one reservoir (fixed-head node).")
        if not self._links:
            raise ValueError("The network has no links.")

        junctions = list(self._junctions)
        index = {name: i for i, name in enumerate(junctions)}
        links = list(self._links.values())
        nj = len(junctions)

        # initial guess: 1 m/s in pipes, mid-range flow in pumps
        flows = []
        for link in links:
            if isinstance(link, _Pipe):
                flows.append(area(link.diameter) * 1.0)
            else:
                flows.append(0.5 * link.curve.max_flow())
        heads = [0.0] * nj  # starting heads are arbitrary: they enter the equations linearly

        def node_head(name: str) -> float:
            if name in self._reservoirs:
                return self._reservoirs[name].head
            return heads[index[name]]

        for iteration in range(1, max_iterations + 1):  # Newton iteration on all link flows and junction heads together
            losses, derivs, energy = [], [], []
            for link, q in zip(links, flows):
                h, d = self._link_loss(link, q)
                losses.append(h)
                derivs.append(d)
                # energy residual E = h_loss - (H_start - H_end)
                energy.append(h - (node_head(link.start) - node_head(link.end)))

            # continuity residual at junctions: inflow - outflow - demand
            # continuity residual C = inflow - outflow - demand at each junction
            cont = [-self._junctions[j].demand for j in junctions]
            for link, q in zip(links, flows):
                if link.end in index:
                    cont[index[link.end]] += q
                if link.start in index:
                    cont[index[link.start]] -= q

            # Newton step: (A21 D^-1 A12) dH = C - A21 D^-1 E
            # assemble A21 D^-1 A12 (a weighted graph Laplacian) and the right-hand side
            mat = [[0.0] * nj for _ in range(nj)]
            rhs = list(cont)
            for link, d, e in zip(links, derivs, energy):
                ends = []
                if link.start in index:
                    ends.append((index[link.start], -1.0))
                if link.end in index:
                    ends.append((index[link.end], 1.0))
                for i, si in ends:
                    rhs[i] -= si * e / d
                    for k, sk in ends:
                        mat[i][k] += si * sk / d
            d_heads = solve_linear(mat, rhs) if nj else []  # head corrections from one linear solve
            for i in range(nj):
                heads[i] += d_heads[i]

            max_dq = 0.0
            for n, (link, d, e) in enumerate(zip(links, derivs, energy)):
                a12_dh = 0.0
                if link.start in index:
                    a12_dh -= d_heads[index[link.start]]
                if link.end in index:
                    a12_dh += d_heads[index[link.end]]
                dq = -(e + a12_dh) / d  # flow correction dQ = -D^-1 (E + A12 dH) for this link
                flows[n] += dq
                max_dq = max(max_dq, abs(dq))

            scale = max(abs(q) for q in flows) or 1.0
            # converged when the largest flow correction is negligible
            if max_dq < tol * max(scale, 1e-3) and iteration > 1:
                break
        else:
            raise RuntimeError("Network solver did not converge; check the network data.")

        return self._build_result(links, flows, heads, index, iteration)

    def _build_result(self, links, flows, heads, index, iterations) -> NetworkResult:
        def node_head(name: str) -> float:
            if name in self._reservoirs:
                return self._reservoirs[name].head
            return heads[index[name]]

        rho_g = self.fluid.density * G
        result_flows, velocities, losses = {}, {}, {}
        for link, q in zip(links, flows):
            result_flows[link.name] = q
            losses[link.name] = (
                abs(self._link_loss(link, q)[0]) if isinstance(link, _Pipe) else self._link_loss(link, q)[0]
            )
            if isinstance(link, _Pipe):
                velocities[link.name] = abs(q) / area(link.diameter)

        node_heads = {name: heads[i] for name, i in index.items()}
        node_heads.update({name: r.head for name, r in self._reservoirs.items()})
        pressures = {name: (heads[i] - self._junctions[name].elevation) * rho_g for name, i in index.items()}

        max_err = 0.0  # report the worst continuity error as a check on the solution
        for name in index:
            net = -self._junctions[name].demand
            for link, q in zip(links, flows):
                net += q if link.end == name else (-q if link.start == name else 0.0)
            max_err = max(max_err, abs(net))

        outflows = {}  # net flow leaving each reservoir (negative = the reservoir is filling)
        for name in self._reservoirs:
            out = 0.0
            for link, q in zip(links, flows):
                out += q if link.start == name else (-q if link.end == name else 0.0)
            outflows[name] = out

        return NetworkResult(result_flows, node_heads, pressures, velocities, losses, iterations, max_err, outflows)
