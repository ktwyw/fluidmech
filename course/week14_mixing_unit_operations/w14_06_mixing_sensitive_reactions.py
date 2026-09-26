"""CHME 202 - Week 14 - Example 6: how micromixing changes product selectivity.

Competitive-consecutive reactions   A + B -> R (k1, fast),   R + B -> S (k2, slow)
with B fed into a large excess of A. With perfect mixing almost no S forms; with
slow micromixing, the fed B meets its own product R before it meets fresh A, and
S rises. Modelled with the engulfment (E) model of Baldyga & Bourne: a feed blob
grows by engulfing surrounding bulk fluid at rate E = 1 / t_micro.
Units: concentrations mol/m3, k in m3/(mol s). Parameters are illustrative.
"""

k1, k2 = 100.0, 1.0  # fast desired, slow undesired reaction
c_a_bulk = 1.0  # bulk concentration of A
c_b_feed = 20.0  # concentrated B in the feed blob


def selectivity_to_s(engulfment_rate: float) -> float:
    """Return X_S = 2 n_S / (n_R + 2 n_S) after all B has reacted (E-model, RK4)."""
    E = engulfment_rate
    v = 1.0  # blob volume (relative)
    n = [0.0, c_b_feed, 0.0, 0.0]  # moles of A, B, R, S in the blob

    def deriv(v, n):
        ca, cb, cr = n[0] / v, n[1] / v, n[2] / v
        r1, r2 = k1 * ca * cb, k2 * cr * cb
        dv = E * v
        return dv, [dv * c_a_bulk - r1 * v, -(r1 + r2) * v, (r1 - r2) * v, r2 * v]

    t = 0.0
    while n[1] > 1e-5 * c_b_feed:  # integrate until the fed B is used up
        cb, ca = n[1] / v, n[0] / v
        # step small compared with the fastest reaction and engulfment times
        dt = min(0.1 / (k1 * (ca + cb) + k2 * cb + E), 0.01 / E)
        dv1, k1n = deriv(v, n)
        dv2, k2n = deriv(v + dt / 2 * dv1, [a + dt / 2 * b for a, b in zip(n, k1n)])
        dv3, k3n = deriv(v + dt / 2 * dv2, [a + dt / 2 * b for a, b in zip(n, k2n)])
        dv4, k4n = deriv(v + dt * dv3, [a + dt * b for a, b in zip(n, k3n)])
        v += dt / 6 * (dv1 + 2 * dv2 + 2 * dv3 + dv4)  # classical 4th-order Runge-Kutta update
        n = [a + dt / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(n, k1n, k2n, k3n, k4n)]
        n = [max(x, 0.0) for x in n]
        t += dt
    return 2 * n[3] / (n[2] + 2 * n[3])  # share of B that ended up in the by-product S


print(f"k1/k2 = {k1 / k2:.0f}, feed B = {c_b_feed} mol/m3 into bulk A = {c_a_bulk} mol/m3\n")
print(f"{'E [1/s]':>8} {'t_micro [ms]':>13} {'Da = k1 c_A / E':>16} {'X_S (by-product)':>17}")
for E in [1000.0, 300.0, 100.0, 30.0, 10.0, 3.0, 1.0]:
    xs = selectivity_to_s(E)
    print(f"{E:>8.0f} {1000 / E:>13.1f} {k1 * c_a_bulk / E:>16.2f} {xs:>17.3f}")
print("\nFaster micromixing (larger E: more power, feed near the impeller) suppresses the by-product.")
print("Selectivity depends on the stirring, not only on the kinetics - scale-up can change product quality.")
