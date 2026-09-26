"""Example 16 - Pipes in series and in parallel."""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.solvers import bisect

water = Fluid.water(15)
steel = pf.ROUGHNESS["commercial_steel"]

# --- Series: same flow, losses add ------------------------------------------ #
series = [(300.0, 0.20), (150.0, 0.15), (80.0, 0.10)]  # (length, diameter)
q = 0.030
print(f"Series pipeline carrying Q = {q * 1000:.0f} L/s")
print(f"{'L [m]':>6} {'D [mm]':>7} {'V [m/s]':>8} {'Re':>9} {'f':>7} {'hf [m]':>7}")
total = 0.0
for length, d in series:
    r = pf.head_loss(q, d, length, water, steel)
    total += r.major_head_loss
    print(
        f"{length:>6.0f} {d * 1000:>7.0f} {r.velocity:>8.2f} {r.reynolds:>9.3g} {r.friction_factor:>7.4f} "
        f"{r.major_head_loss:>7.2f}"
    )
# sudden contractions between sections: K ~ 0.42 (1 - (d2/d1)^2) based on downstream velocity
for (_, d1), (_, d2) in zip(series, series[1:]):
    k = 0.42 * (1 - (d2 / d1) ** 2)  # sudden-contraction loss coefficient (downstream velocity)
    total += pf.minor_loss(k, pf.mean_velocity(q, d2))
print(f"Total head loss (incl. contractions): {total:.2f} m")
print("The smallest pipe dominates: hf scales roughly as 1/D^5.\n")

# --- Parallel: same head loss, flows add ------------------------------------ #
branches = [(500.0, 0.15), (350.0, 0.10), (800.0, 0.20)]
q_total = 0.080  # total flow shared by the branches [m3/s]


def branch_flow(h: float, length: float, d: float) -> float:
    return pf.flow_rate_for_head_loss(h, d, length, water, steel)


# common head loss whose branch flows add up to Q
h = bisect(lambda h: sum(branch_flow(h, L, d) for L, d in branches) - q_total, 1e-3, 200.0)
print(f"Three parallel branches sharing Q = {q_total * 1000:.0f} L/s")
print(f"Common head loss across the branches: {h:.2f} m")
print(f"{'L [m]':>6} {'D [mm]':>7} {'Q [L/s]':>8} {'share':>6}")
for length, d in branches:
    qb = branch_flow(h, length, d)
    print(f"{length:>6.0f} {d * 1000:>7.0f} {qb * 1000:>8.2f} {qb / q_total:>6.1%}")
print("The large, long pipe still takes most of the flow.")
