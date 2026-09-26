"""Desktop explorer: build potential flows by superposition and watch the streamlines change.

Sliders control a uniform stream, a source (Rankine half-body), a doublet (cylinder) and a vortex
(circulation -> lift). Run:  python showcase/apps/explorer_potential_flow.py

# requires: matplotlib, numpy
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from fluidmech import viz
from fluidmech.potential_flow import Doublet, Flow, Source, Uniform, Vortex

X, Y = np.meshgrid(np.linspace(-3, 3, 120), np.linspace(-2, 2, 80))  # grid for the velocity field


def superposed(U, m, kappa, gamma):
    parts = [Uniform(U)]
    if abs(m) > 1e-9:
        parts.append(Source(m))
    if abs(kappa) > 1e-9:
        parts.append(Doublet(kappa))
    if abs(gamma) > 1e-9:
        parts.append(Vortex(gamma))
    return Flow(parts)


def velocity_field(flow):
    """Velocity on the grid. Streamlines are drawn from (u, v) rather than by contouring psi:
    a source's stream function m*theta/(2 pi) jumps by m across the negative x axis (a branch cut),
    which would draw a false dense line there; the velocity field has no such cut."""
    uv = np.array(
        [
            [flow.velocity(x, y) if x * x + y * y > 0.02 else (np.nan, np.nan) for x, y in zip(rx, ry)]
            for rx, ry in zip(X, Y)
        ]
    )
    return uv[..., 0], uv[..., 1]


def build():
    with viz.style("slides"):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_axes([0.08, 0.34, 0.86, 0.6])
    sliders = {
        "U": Slider(fig.add_axes([0.15, 0.22, 0.7, 0.03]), "U", 0.0, 3.0, valinit=1.0),
        "m": Slider(fig.add_axes([0.15, 0.17, 0.7, 0.03]), "source m", -6.0, 6.0, valinit=0.0),
        "kappa": Slider(fig.add_axes([0.15, 0.12, 0.7, 0.03]), "doublet", 0.0, 10.0, valinit=3.0),
        "gamma": Slider(fig.add_axes([0.15, 0.07, 0.7, 0.03]), "circulation", -15.0, 15.0, valinit=0.0),
    }

    def update(_=None):
        ax.clear()
        v = {k: s.val for k, s in sliders.items()}
        u, w = velocity_field(superposed(v["U"], v["m"], v["kappa"], v["gamma"]))
        speed = np.hypot(u, w)
        speed = np.minimum(speed, np.nanpercentile(speed, 95))  # clip: the singular centre would swamp the colours
        ax.streamplot(X, Y, u, w, density=1.6, color=speed, cmap="viridis", linewidth=0.8, arrowsize=0.8)
        ax.set(
            aspect="equal",
            xlim=(-3, 3),
            ylim=(-2, 2),
            title="uniform + source + doublet + vortex  (doublet = 2 pi U R^2 gives a cylinder)",
        )
        fig.canvas.draw_idle()

    for s in sliders.values():
        s.on_changed(update)
    update()
    return fig, sliders, update


if __name__ == "__main__":
    build()
    plt.show()
