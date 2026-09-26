"""Example 26 - Backwater (M1) profile behind a weir: the direct step method.

A weir raises the depth to 2.8 m in the canal of example 4 (mild slope).
The water surface returns to normal depth far upstream. Between two depths
the distance is dx = (E2 - E1) / (S0 - Sf_mean), with Sf from Manning.
Optional plot: saves backwater_profile.png if matplotlib is installed.
"""

from fluidmech.open_channel import TrapezoidalChannel

canal = TrapezoidalChannel(bottom_width=4.0, side_slope=1.5)
n, S0, Q = 0.012, 0.0008, 25.0  # Manning n, bed slope, discharge [m3/s]
yn = canal.normal_depth(Q, n, S0)
yc = canal.critical_depth(Q)
y_weir = 2.8  # depth imposed by the weir [m]
print(f"Normal depth y_n = {yn:.3f} m, critical depth y_c = {yc:.3f} m -> mild slope")
print(f"Depth at the weir: {y_weir} m (> y_n) -> M1 backwater curve\n")


def friction_slope(y: float) -> float:
    v = Q / canal.area(y)
    return (n * v) ** 2 / canal.hydraulic_radius(y) ** (4 / 3)


steps = 40  # number of depth increments
y_end = 1.01 * yn  # stop at 1 % above normal depth (normal depth is reached asymptotically)
dy = (y_weir - y_end) / steps
x = 0.0  # distance upstream of the weir
profile = [(x, y_weir)]
y = y_weir
for _ in range(steps):  # direct step method, marching upstream from the weir
    y_next = y - dy
    de = canal.specific_energy(y_next, Q) - canal.specific_energy(y, Q)
    sf = 0.5 * (friction_slope(y) + friction_slope(y_next))  # average friction slope over the step
    x += de / (S0 - sf)  # negative -> upstream
    y = y_next
    profile.append((x, y))

print(f"{'distance upstream [m]':>22} {'depth [m]':>10} {'rise above y_n [m]':>19}")
for i, (xi, yi) in enumerate(profile):
    if i % 5 == 0 or i == steps:
        print(f"{abs(xi):>22.0f} {yi:>10.3f} {yi - yn:>19.3f}")
print(f"\nThe weir's influence extends about {-profile[-1][0] / 1000:.1f} km upstream.")
print(f"(A crude estimate, (y_weir - y_n)/S0 = {(y_weir - yn) / S0 / 1000:.1f} km, underestimates it.)")

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("(matplotlib not installed - skipping plot)")
else:
    xs = [-xi for xi, _ in profile]
    bed = [S0 * xi for xi in xs]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(xs, [b + yi for b, (_, yi) in zip(bed, profile)], label="water surface (M1)")
    ax.plot(xs, [b + yn for b in bed], "--", label="normal depth line")
    ax.plot(xs, [b + yc for b in bed], ":", label="critical depth line")
    ax.plot(xs, bed, "k", lw=2, label="channel bed")
    ax.invert_xaxis()
    ax.set_xlabel("Distance upstream of weir [m]")
    ax.set_ylabel("Elevation [m]")
    ax.legend()
    ax.grid(alpha=0.4)
    fig.tight_layout()
    fig.savefig("backwater_profile.png", dpi=150)
    print("Saved backwater_profile.png")
