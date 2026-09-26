"""CHME 202 - Week 6 - Example 11: polymer extrusion through a slit die (power-law fluid).

For a slit of half-gap b and pressure gradient G, the flow per unit width is
q = (2n / (2n + 1)) (G / K)^(1/n) b^((2n + 1) / n). With n < 1, doubling the pressure
more than doubles the output - a key property of shear-thinning melts.
"""

K, n = 12000.0, 0.35  # polymer melt [Pa s^n]
b, L, W = 0.6e-3, 0.05, 0.5  # half-gap, die land length, die width [m]


def q_per_width(G, K=K, n=n, b=b):
    return 2 * n / (2 * n + 1) * (G / K) ** (1 / n) * b ** ((2 * n + 1) / n)


def u_profile(y, G):
    return n / (n + 1) * (G / K) ** (1 / n) * (b ** ((n + 1) / n) - abs(y) ** ((n + 1) / n))


G = 100e5 / L  # pressure gradient for 100 bar across the die land [Pa/m]
N = 4000
# numerical check: integrate u(y) across the gap
q_num = sum(u_profile(-b + (i + 0.5) * 2 * b / N, G) * 2 * b / N for i in range(N))
print(f"Slit die: gap {2 * b * 1000} mm, width {W} m, land {L * 1000:.0f} mm; melt K = {K}, n = {n}")
print(f"Check: formula q = {q_per_width(G) * 1e4:.4f} cm2/s, integrated profile {q_num * 1e4:.4f} cm2/s (at 100 bar)\n")
print(f"{'die pressure [bar]':>19} {'output [kg/h]':>14}")
for bar in [50, 75, 100, 150]:
    q = q_per_width(bar * 1e5 / L) * W  # bar -> Pa; times die width
    print(f"{bar:>19} {q * 950 * 3600:>14.1f}")  # m3/s x melt density 950 kg/m3 -> kg/h
print(f"\nOutput ~ dp^(1/n) = dp^{1 / n:.2f}: doubling the pressure multiplies throughput by {2 ** (1 / n):.1f}.")
print(
    f"Newtonian check: n = 1 gives q = 2 G b^3 / (3 mu) = G (2b)^3 / (12 mu): "
    f"{q_per_width(1e6, K=1.0, n=1.0):.4e} vs {1e6 * (2 * b) ** 3 / 12:.4e} m2/s"
)
