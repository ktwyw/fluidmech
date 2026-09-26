"""Example 22 - Stage-discharge rating curve for a trapezoidal channel.

Builds the depth-discharge table used by hydrologists to turn a water-level
reading into a flow rate, and fits the classic power law Q = a y^b.
"""

import math

from fluidmech.open_channel import MANNING_N, TrapezoidalChannel

channel = TrapezoidalChannel(bottom_width=6.0, side_slope=2.0)
n = MANNING_N["earth_clean"]
S0 = 0.0005  # bed slope [m/m]

print(f"Earth channel: b = 6 m, z = 2, n = {n}, S0 = {S0}\n")
print(f"{'y [m]':>6} {'A [m2]':>8} {'R [m]':>7} {'V [m/s]':>8} {'Q [m3/s]':>9} {'Fr':>6}")
depths = [0.25 * i for i in range(1, 13)]  # 0.25 to 3.0 m
discharges = []
for y in depths:
    q = channel.discharge(y, n, S0)
    discharges.append(q)
    print(
        f"{y:>6.2f} {channel.area(y):>8.2f} {channel.hydraulic_radius(y):>7.3f} "
        f"{q / channel.area(y):>8.3f} {q:>9.2f} {channel.froude(y, q):>6.3f}"
    )

# Least-squares fit of log Q = log a + b log y
xs = [math.log(y) for y in depths]
ys = [math.log(q) for q in discharges]
m = len(xs)
x_bar, y_bar = sum(xs) / m, sum(ys) / m
# least-squares slope of ln Q vs ln y = exponent b
b = sum((x - x_bar) * (yv - y_bar) for x, yv in zip(xs, ys)) / sum((x - x_bar) ** 2 for x in xs)
a = math.exp(y_bar - b * x_bar)
print(f"\nPower-law rating curve: Q = {a:.2f} y^{b:.3f}")
worst = max(abs(a * y**b - q) / q for y, q in zip(depths, discharges))
print(f"Maximum fit error over the table: {worst:.1%}")

print("\nInverse use - gauge reads 1.80 m:")
q = channel.discharge(1.80, n, S0)
print(f"  Manning: Q = {q:.2f} m3/s, rating curve: Q = {a * 1.8**b:.2f} m3/s")
print(f"  and a flow of 40 m3/s would give a stage of {channel.normal_depth(40.0, n, S0):.3f} m")
