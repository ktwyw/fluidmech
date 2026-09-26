"""Publication-quality figures for fluid mechanics (optional; requires matplotlib).

The rest of fluidmech has no dependencies; this module imports matplotlib only when used.

Features
--------
* :func:`style` - a context manager with journal-ready settings (font sizes, inward ticks,
  thin lines, tight layout, 300 dpi) in ``"paper"``, ``"slides"`` or ``"poster"`` flavours.
* :data:`COLORS` - the Okabe-Ito palette, distinguishable by readers with colour-vision deficiency
  and still readable when printed in greyscale.
* :func:`savefig` - save one figure as vector (PDF/SVG) and raster (PNG) in one call.
* Ready-made charts: :func:`moody_chart`, :func:`pump_system_chart`, :func:`drag_curve_chart`.
* :func:`label_panels` - add (a), (b), (c) labels to multi-panel figures.

Example
-------
>>> import matplotlib
>>> matplotlib.use("Agg")
>>> from fluidmech import viz
>>> with viz.style("paper"):
...     fig, ax = viz.figure(width="single")
...     _ = viz.moody_chart(ax)
"""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path

COLORS = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
}
"""Okabe-Ito colour-blind-safe palette."""

CYCLE = [COLORS[c] for c in ("blue", "vermillion", "green", "orange", "purple", "sky", "black")]

# Figure widths in inches for typical journal layouts (single column, 1.5 column, full page)
WIDTHS = {"single": 3.5, "onehalf": 5.5, "double": 7.2}

_PRESETS = {
    "paper": {
        "font.size": 8,
        "axes.labelsize": 8,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "lines.linewidth": 1.1,
        "axes.linewidth": 0.6,
    },
    "slides": {
        "font.size": 14,
        "axes.labelsize": 14,
        "legend.fontsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "lines.linewidth": 2.2,
        "axes.linewidth": 1.0,
    },
    "poster": {
        "font.size": 20,
        "axes.labelsize": 20,
        "legend.fontsize": 16,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "lines.linewidth": 3.0,
        "axes.linewidth": 1.4,
    },
}


def _mpl():
    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise ImportError("fluidmech.viz needs matplotlib: pip install matplotlib") from exc
    return matplotlib, plt


@contextlib.contextmanager
def style(kind: str = "paper") -> Iterator[None]:
    """Temporarily apply publication settings: ``with viz.style("paper"): ...``."""
    if kind not in _PRESETS:
        raise ValueError(f"kind must be one of {sorted(_PRESETS)}")
    matplotlib, _ = _mpl()
    from cycler import cycler

    params = {
        "axes.prop_cycle": cycler(color=CYCLE),
        "axes.spines.top": True,
        "axes.spines.right": True,
        "xtick.direction": "in",  # inward ticks, as most journals prefer
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,  # embed TrueType fonts so text stays editable in Illustrator/Inkscape
        "svg.fonttype": "none",
        "font.family": "sans-serif",
        "mathtext.fontset": "dejavusans",
    }
    params.update(_PRESETS[kind])
    logging.getLogger("fontTools").setLevel(logging.ERROR)  # silence font-subsetting chatter when saving PDFs
    with matplotlib.rc_context(params):
        yield


def figure(width: str | float = "single", aspect: float = 0.75, nrows: int = 1, ncols: int = 1, **kwargs):
    """Create a figure sized for a journal column. ``width`` is 'single', 'onehalf', 'double' or inches."""
    _, plt = _mpl()
    w = WIDTHS.get(width, width) if isinstance(width, str) else width
    return plt.subplots(nrows, ncols, figsize=(w, w * aspect), constrained_layout=True, **kwargs)


def savefig(fig, path: str | Path, formats: Iterable[str] = ("pdf", "png")) -> list[Path]:
    """Save ``fig`` in several formats (``path`` without extension). Returns the files written."""
    base = Path(path)
    base.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for fmt in formats:
        target = base.with_suffix("." + fmt)
        fig.savefig(target)
        written.append(target)
    return written


def label_panels(axes, labels: str = "abcdefgh", x: float = 0.0, y: float = 1.02) -> None:
    """Write (a), (b), ... just above the top-left corner of each axis."""
    for ax, letter in zip(list(getattr(axes, "flat", axes)), labels):
        ax.text(x, y, f"({letter})", transform=ax.transAxes, fontweight="bold", va="bottom", ha="left")


# ---------------------------------------------------------------------------- #
# Ready-made fluid-mechanics charts
# ---------------------------------------------------------------------------- #
def moody_chart(ax=None, relative_roughness=(0, 1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05), label: bool = True):
    """Draw a Moody diagram (Colebrook) on ``ax``; returns the axis."""
    from .pipe_flow import colebrook

    _, plt = _mpl()
    ax = ax or plt.gca()
    lam = [600 * (2300 / 600) ** (i / 30) for i in range(31)]  # laminar branch, Re 600-2300
    ax.loglog(lam, [64 / r for r in lam], color=COLORS["black"], lw=1.4)
    re = [4000 * (1e8 / 4000) ** (i / 150) for i in range(151)]  # turbulent branch, Re 4e3-1e8
    cmap = plt.get_cmap("viridis")  # sequential colours: roughness is an ORDERED parameter
    n = max(len(relative_roughness) - 1, 1)
    for k, rr in enumerate(relative_roughness):
        f = [colebrook(r, rr) for r in re]
        ax.loglog(re, f, lw=0.9, color=cmap(0.9 * k / n))
        if label:
            ax.text(1.15e8, f[-1], "smooth" if rr == 0 else f"{rr:g}", fontsize="x-small", va="center")
    ax.axvspan(2300, 4000, color="0.85", lw=0)  # uncertain transition region
    ax.set(xlim=(600, 1e8), ylim=(0.006, 0.1), xlabel=r"Reynolds number $Re$", ylabel=r"Darcy friction factor $f$")
    ax.text(650, 0.024, r"$64/Re$", fontsize="small")  # below-left of the laminar line
    ax.grid(True, which="both", lw=0.3, alpha=0.5)
    return ax


def pump_system_chart(
    ax,
    pump,
    system: Callable[[float], float],
    q_max: float,
    speeds=(1.0,),
    q_unit: float = 1000.0,
    q_label: str = "Flow rate [L/s]",
):
    """Pump curves at several speed ratios, the system curve and the operating points."""
    from .pumps import operating_point

    qs = [q_max * i / 100 for i in range(101)]
    for s in speeds:
        curve = pump.scaled(speed_ratio=s)
        alpha = 1.0 if s == 1 else 0.35  # rated speed drawn solid, other speeds faded
        ax.plot([q * q_unit for q in qs], [curve.head(q) for q in qs], color=COLORS["blue"], alpha=alpha)
        try:
            op = operating_point(curve, system)
            ax.plot(op.flow_rate * q_unit, op.head, "o", color=COLORS["vermillion"], ms=4, zorder=5)
        except ValueError:
            pass  # this speed cannot overcome the static head
    ax.plot([q * q_unit for q in qs], [system(q) for q in qs], color=COLORS["green"], lw=1.6, label="system")
    ax.set(xlabel=q_label, ylabel="Head [m]", ylim=(0, None))
    return ax


def drag_curve_chart(ax, data: Iterable[tuple[float, float]] | None = None):
    """Sphere drag coefficient versus Re with Stokes and Newton regimes; optional (Re, Cd) data points."""
    from .drag import sphere_drag_coefficient

    res = [10 ** (i / 20) for i in range(-40, 107)]
    ax.loglog(res, [sphere_drag_coefficient(r) for r in res], color=COLORS["black"], label="Brown & Lawler (2003)")
    creeping = [r for r in res if r < 5]
    ax.loglog(creeping, [24 / r for r in creeping], "--", color=COLORS["blue"], label="Stokes, 24/Re")
    ax.axhline(0.44, ls=":", color=COLORS["vermillion"], label="Newton, 0.44")
    if data:
        re_d, cd_d = zip(*data)
        ax.loglog(re_d, cd_d, "o", mfc="none", color=COLORS["vermillion"], ms=4, label="experiment")
    ax.set(xlabel=r"$Re$", ylabel=r"$C_D$", ylim=(0.1, 3000))
    ax.legend(loc="upper right")
    return ax
