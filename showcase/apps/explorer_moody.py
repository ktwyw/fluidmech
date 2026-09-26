"""Desktop explorer: drag the sliders and watch your pipe move on the Moody diagram.

Run:  python showcase/apps/explorer_moody.py   (opens a window; needs a desktop, not a server)
Only matplotlib is required - no web framework.

# requires: matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider

from fluidmech import Fluid, viz
from fluidmech import pipe_flow as pf


def build():
    """Create the figure and widgets; returns (fig, widgets dict, update function)."""
    with viz.style("slides"):
        fig = plt.figure(figsize=(11, 6.5))
        ax = fig.add_axes([0.08, 0.36, 0.58, 0.58])
        viz.moody_chart(ax)
    (marker,) = ax.plot([], [], "*", ms=20, color=viz.COLORS["vermillion"], zorder=10)
    readout = fig.text(0.77, 0.55, "", family="monospace", fontsize=11, va="top")
    s_q = Slider(fig.add_axes([0.1, 0.22, 0.55, 0.03]), "Q [L/s]", 0.05, 200.0, valinit=20.0)
    s_d = Slider(fig.add_axes([0.1, 0.16, 0.55, 0.03]), "D [mm]", 10.0, 500.0, valinit=100.0)
    s_t = Slider(fig.add_axes([0.1, 0.10, 0.55, 0.03]), "T [degC]", 0.0, 100.0, valinit=20.0)
    materials = ["drawn_tubing", "commercial_steel", "cast_iron", "concrete"]
    radio = RadioButtons(fig.add_axes([0.77, 0.62, 0.2, 0.3]), materials, active=1)

    def update(_=None):
        water = Fluid.water(s_t.val)
        r = pf.head_loss(s_q.val / 1000, s_d.val / 1000, 100.0, water, pf.ROUGHNESS[radio.value_selected])
        marker.set_data([r.reynolds], [r.friction_factor])
        readout.set_text(
            f"V   = {r.velocity:7.2f} m/s\nRe  = {r.reynolds:9.3g}\n{r.regime}\n"
            f"f   = {r.friction_factor:7.4f}\nh_f = {r.major_head_loss:7.2f} m per 100 m"
        )
        fig.canvas.draw_idle()

    for s in (s_q, s_d, s_t):
        s.on_changed(update)
    radio.on_clicked(update)
    update()
    return fig, {"Q": s_q, "D": s_d, "T": s_t, "material": radio}, update


if __name__ == "__main__":
    build()
    plt.show()
