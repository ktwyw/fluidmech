"""Example 25 - Best hydraulic section for a trapezoidal channel.

For a given Q, n and S0, the section with the smallest area (and hence the
cheapest excavation and lining) is half a hexagon: side slope z = 1/sqrt(3)
(60 deg sides) with bottom width b = 2 y (sqrt(1 + z^2) - z).
"""

import math

from fluidmech.open_channel import TrapezoidalChannel
from fluidmech.solvers import positive_root

Q, n, S0 = 20.0, 0.014, 0.0010  # discharge [m3/s], Manning n, bed slope


def best_section_for_slope(z: float) -> tuple[float, float, float]:
    """Optimal depth, bottom width and area for a fixed side slope z."""
    ratio = 2.0 * (math.sqrt(1 + z * z) - z)  # b / y for the best section at this z

    def residual(y: float) -> float:
        return TrapezoidalChannel(ratio * y, z).discharge(y, n, S0) - Q

    y = positive_root(residual)  # depth at which this section carries Q
    ch = TrapezoidalChannel(ratio * y, z)
    return y, ratio * y, ch.area(y)


print(f"Lined canal, Q = {Q} m3/s, n = {n}, S0 = {S0}\n")
print(f"{'z':>6} {'angle':>6} {'y [m]':>7} {'b [m]':>7} {'A [m2]':>8} {'P [m]':>7}  note")
results = []
for z in [0.0, 0.25, 0.5, 1 / math.sqrt(3), 0.75, 1.0, 1.5, 2.0]:
    y, b, a = best_section_for_slope(z)
    p = TrapezoidalChannel(b, z).wetted_perimeter(y)
    results.append((a, z))
    angle = 90.0 if z == 0 else math.degrees(math.atan(1 / z))  # side-wall angle from the horizontal
    note = "rectangle (b = 2y)" if z == 0 else ("half hexagon" if abs(z - 1 / math.sqrt(3)) < 1e-9 else "")
    print(f"{z:>6.3f} {angle:>5.0f}d {y:>7.3f} {b:>7.3f} {a:>8.3f} {p:>7.3f}  {note}")

a_min, z_best = min(results)
print(f"\nSmallest area at z = {z_best:.3f} (theory: 1/sqrt(3) = {1 / math.sqrt(3):.3f})")
print("In practice the side slope is set by soil stability, then b/y is optimised for that z.")

# Compare to an arbitrary wide, shallow design
wide = TrapezoidalChannel(12.0, 1.5)
y_w = wide.normal_depth(Q, n, S0)
print(
    f"\nA wide shallow design (b = 12 m, z = 1.5) needs A = {wide.area(y_w):.2f} m2 "
    f"(+{wide.area(y_w) / a_min - 1:.0%}) and P = {wide.wetted_perimeter(y_w):.2f} m of lining."
)
