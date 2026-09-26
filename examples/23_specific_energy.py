"""Example 23 - Specific energy, alternate depths and flow over a hump.

In a rectangular channel carrying q per unit width, the same specific energy E
can occur at two 'alternate' depths - one subcritical, one supercritical.
Optional plot: saves specific_energy.png if matplotlib is installed.
"""

from fluidmech.open_channel import RectangularChannel
from fluidmech.solvers import bisect

width = 3.0  # channel width [m]
Q = 6.0  # discharge [m3/s]
ch = RectangularChannel(width)
yc = ch.critical_depth(Q)
e_min = ch.specific_energy(yc, Q)
print(f"Rectangular channel b = {width} m, Q = {Q} m3/s (q = {Q / width:.2f} m2/s)")
print(f"Critical depth y_c = {yc:.3f} m, minimum specific energy E_min = {e_min:.3f} m\n")


def alternate_depths(E: float) -> tuple[float, float]:
    """Supercritical and subcritical depths having specific energy E."""
    f = lambda y: ch.specific_energy(y, Q) - E  # noqa: E731
    y_super = bisect(f, 1e-4, yc)  # supercritical root lies below y_c
    y_sub = bisect(f, yc, E)  # subcritical root between y_c and E
    return y_super, y_sub


print(f"{'E [m]':>6} {'y_super [m]':>12} {'Fr':>6} {'y_sub [m]':>10} {'Fr':>6}")
for E in [e_min * k for k in (1.01, 1.1, 1.25, 1.5, 2.0, 3.0)]:
    y1, y2 = alternate_depths(E)
    print(f"{E:>6.3f} {y1:>12.3f} {ch.froude(y1, Q):>6.2f} {y2:>10.3f} {ch.froude(y2, Q):>6.2f}")

# Hump in the channel bed
y_up = 1.8
e_up = ch.specific_energy(y_up, Q)
print(f"\nUpstream depth {y_up} m (subcritical, E = {e_up:.3f} m). Water flows over a raised hump:")
print(f"{'hump [m]':>9} {'depth on hump [m]':>18} {'surface change [m]':>19}")
for dz in [0.0, 0.1, 0.2, 0.3, e_up - e_min]:
    e_hump = e_up - dz
    if e_hump < e_min - 1e-9:
        break
    y_h = alternate_depths(max(e_hump, e_min * (1 + 1e-9)))[1] if e_hump > e_min else yc
    print(f"{dz:>9.3f} {y_h:>18.3f} {(y_h + dz) - y_up:>+19.3f}")
print(f"\nMaximum hump height before the flow chokes: {e_up - e_min:.3f} m")
print("The water surface DROPS over a hump in subcritical flow.")

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("(matplotlib not installed - skipping plot)")
else:
    ys = [yc * (0.3 + 0.01 * i) for i in range(1, 400)]  # depths from 0.3 y_c upwards for the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    for q_i in (3.0, 6.0, 9.0):
        ax.plot([ch.specific_energy(y, q_i) for y in ys], ys, label=f"Q = {q_i:g} m3/s")
    ax.plot([0, 4], [0, 4], "k:", lw=0.8, label="E = y")
    ax.axhline(yc, color="grey", lw=0.6)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3.5)
    ax.set_xlabel("Specific energy E [m]")
    ax.set_ylabel("Depth y [m]")
    ax.set_title("Specific energy diagram")
    ax.legend()
    ax.grid(alpha=0.4)
    fig.tight_layout()
    fig.savefig("specific_energy.png", dpi=150)
    print("Saved specific_energy.png")
