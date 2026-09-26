"""Regenerate the figures used in the README gallery.

Usage:  python docs/make_figures.py   (requires matplotlib)
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import cm, colors  # noqa: E402

from fluidmech import (  # noqa: E402
    Fluid,
    Network,
    PumpCurve,
    pumps,  # noqa: E402
)
from fluidmech import pipe_flow as pf  # noqa: E402
from fluidmech.open_channel import TrapezoidalChannel, gvf_profile  # noqa: E402

OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def network_map() -> None:
    water = Fluid.water(15)
    net = Network(water)
    pos = {
        "Works": (-1.4, 2),
        "PS": (-0.6, 2),
        "J1": (0, 2),
        "J2": (2, 2),
        "J3": (4, 2),
        "J4": (0, 1),
        "J5": (2, 1),
        "J6": (4, 1),
        "J7": (0, 0),
        "J8": (2, 0),
        "Tank": (5.2, 1),
    }
    net.add_reservoir("Works", 102.0)
    net.add_reservoir("Tank", 148.0)
    nodes = {
        "PS": (100, 0),
        "J1": (104, 8),
        "J2": (108, 12),
        "J3": (112, 10),
        "J4": (103, 15),
        "J5": (106, 20),
        "J6": (115, 9),
        "J7": (101, 14),
        "J8": (105, 11),
    }
    for n, (z, q) in nodes.items():
        net.add_junction(n, elevation=z, demand=q / 1000)
    net.add_pump("Pump", "Works", "PS", PumpCurve.from_points([0, 0.05, 0.10, 0.15], [68, 65, 56, 40]))
    pipes = [
        ("P0", "PS", "J1", 200, 0.35),
        ("P1", "J1", "J2", 500, 0.25),
        ("P2", "J2", "J3", 450, 0.20),
        ("P3", "J1", "J4", 400, 0.30),
        ("P4", "J2", "J5", 400, 0.20),
        ("P5", "J3", "J6", 400, 0.15),
        ("P6", "J4", "J5", 500, 0.25),
        ("P7", "J5", "J6", 450, 0.20),
        ("P8", "J4", "J7", 350, 0.20),
        ("P9", "J5", "J8", 350, 0.15),
        ("P10", "J7", "J8", 500, 0.15),
        ("P11", "J6", "Tank", 300, 0.20),
    ]
    for name, a, b, length, d in pipes:
        net.add_pipe(name, a, b, length, d, pf.ROUGHNESS["cast_iron"])
    res = net.solve()

    fig, ax = plt.subplots(figsize=(9, 5.4))
    vnorm = colors.Normalize(0, max(res.velocities.values()))
    for name, a, b, _, d in pipes:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        q = res.flows[name]
        ax.plot(
            [x1, x2],
            [y1, y2],
            color=cm.viridis(vnorm(res.velocities[name])),
            lw=2 + 18 * d,
            zorder=1,
            solid_capstyle="round",
        )
        if q < 0:
            x1, y1, x2, y2 = x2, y2, x1, y1
        ax.annotate(
            "",
            xy=(x1 + 0.58 * (x2 - x1), y1 + 0.58 * (y2 - y1)),
            xytext=(x1 + 0.42 * (x2 - x1), y1 + 0.42 * (y2 - y1)),
            arrowprops={"arrowstyle": "-|>", "color": "white", "lw": 1.5},
            zorder=2,
        )
        if abs(x2 - x1) > abs(y2 - y1):
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.1, f"{abs(q) * 1000:.0f} L/s", ha="center", fontsize=7.5)
        else:
            ax.text(x1 + 0.1, (y1 + y2) / 2, f"{abs(q) * 1000:.0f} L/s", ha="left", va="center", fontsize=7.5)
    (x1, y1), (x2, y2) = pos["Works"], pos["PS"]
    ax.plot([x1, x2], [y1, y2], "k", lw=2)
    ax.text((x1 + x2) / 2, y1 + 0.13, "pump", ha="center", fontsize=8)
    pnorm = colors.Normalize(30, 55)
    for n in nodes:
        head = res.pressures[n] / (water.density * 9.80665)
        ax.scatter(*pos[n], s=260, color=cm.plasma(pnorm(head)), edgecolor="k", zorder=3)
        ax.text(pos[n][0] - 0.12, pos[n][1] - 0.1, f"{n}\n{head:.0f} m", ha="right", va="top", fontsize=8)
    for n, marker in [("Works", "s"), ("Tank", "s")]:
        ax.scatter(*pos[n], s=380, marker=marker, color="tab:blue", edgecolor="k", zorder=3)
        ax.text(pos[n][0], pos[n][1] - 0.28, n, ha="center", va="top", fontsize=8)
    ax.set_position([0.02, 0.2, 0.96, 0.7])
    cax_v = fig.add_axes([0.1, 0.1, 0.35, 0.03])
    cax_p = fig.add_axes([0.55, 0.1, 0.35, 0.03])
    horizontal = {"orientation": "horizontal"}
    fig.colorbar(cm.ScalarMappable(vnorm, cm.viridis), cax=cax_v, label="pipe velocity [m/s]", **horizontal)
    fig.colorbar(cm.ScalarMappable(pnorm, cm.plasma), cax=cax_p, label="node pressure head [m]", **horizontal)
    ax.set_title("Pipe network solved with fluidmech.Network (pump, tank, 9 nodes, 12 pipes)")
    ax.set_xlim(-1.8, 5.6)
    ax.set_ylim(-0.6, 2.4)
    ax.axis("off")
    fig.savefig(OUT / "network.png", dpi=130)


def moody() -> None:
    fig, ax = plt.subplots(figsize=(7, 4.6))
    re_lam = [600 * (2300 / 600) ** (i / 40) for i in range(41)]
    ax.loglog(re_lam, [64 / r for r in re_lam], "k", lw=2)
    re_t = [4000 * (1e8 / 4000) ** (i / 200) for i in range(201)]
    for rr in [0, 1e-5, 1e-4, 5e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]:
        f = [pf.colebrook(r, rr) for r in re_t]
        ax.loglog(re_t, f, lw=1.2)
        ax.text(1.1e8, f[-1], "smooth" if rr == 0 else f"{rr:g}", fontsize=7, va="center")
    ax.axvspan(2300, 4000, color="grey", alpha=0.15)
    ax.set(
        xlim=(600, 1e8),
        ylim=(0.007, 0.1),
        xlabel="Reynolds number",
        ylabel="Darcy friction factor",
        title="Moody diagram from pipe_flow.colebrook",
    )
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "moody.png", dpi=130)


def pump_curves() -> None:
    water = Fluid.water(20)
    pump = PumpCurve.from_points([0.0, 0.04, 0.08, 0.12], [42.0, 40.0, 33.5, 22.5], [0.0, 0.62, 0.80, 0.68])
    system = pumps.system_curve(12.0, 0.25, 800.0, water, 0.26e-3, 8.0)
    qs = [i / 1000 for i in range(0, 141, 2)]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    for r in (1.0, 0.9, 0.8, 0.7):
        curve = pump.scaled(speed_ratio=r)
        ax.plot([q * 1000 for q in qs], [curve.head(q) for q in qs], color="tab:blue", alpha=0.35 + 0.65 * (r == 1))
        op = pumps.operating_point(curve, system)
        ax.plot(op.flow_rate * 1000, op.head, "o", color="tab:red")
        ax.text(op.flow_rate * 1000 + 2, op.head + 1, f"{r:.0%} speed, eta {op.efficiency:.0%}", fontsize=8)
    ax.plot([q * 1000 for q in qs], [system(q) for q in qs], color="tab:green", lw=2, label="system curve")
    ax.set(
        ylim=(0, 48),
        xlabel="Flow rate [L/s]",
        ylabel="Head [m]",
        title="Variable-speed pump operating points (pumps module)",
    )
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "pump_curves.png", dpi=130)


def backwater() -> None:
    canal = TrapezoidalChannel(4.0, 1.5)
    q, n, s0 = 25.0, 0.012, 0.0008
    yn, yc = canal.normal_depth(q, n, s0), canal.critical_depth(q)
    prof = gvf_profile(canal, q, n, s0, 2.8, 1.01 * yn, steps=60)
    x = [-p[0] for p in prof]
    bed = [s0 * xi for xi in x]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.fill_between(x, bed, [b + p[1] for b, p in zip(bed, prof)], color="tab:blue", alpha=0.25)
    ax.plot(x, [b + p[1] for b, p in zip(bed, prof)], color="tab:blue", lw=2, label="water surface (M1)")
    ax.plot(x, [b + yn for b in bed], "--", color="tab:orange", label="normal depth")
    ax.plot(x, [b + yc for b in bed], ":", color="tab:red", label="critical depth")
    ax.fill_between(x, [b - 0.4 for b in bed], bed, color="saddlebrown", alpha=0.6)
    ax.invert_xaxis()
    ax.set(
        xlabel="Distance upstream of weir [m]",
        ylabel="Elevation [m]",
        title="Backwater curve behind a weir (open_channel.gvf_profile)",
    )
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "backwater.png", dpi=130)


if __name__ == "__main__":
    for func in (network_map, moody, pump_curves, backwater):
        func()
        print("made", func.__name__)
