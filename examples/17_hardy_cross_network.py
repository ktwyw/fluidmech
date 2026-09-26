"""Example 17 - Two-loop pipe network solved with the Hardy Cross method.

    A -------- B -------- C          Inflow at A: 120 L/s
    |          |          |          Outflows:    C 30 L/s, D 30 L/s, F 60 L/s
    D -------- E -------- F          Head at A:   50 m

Each loop correction is dQ = -sum(h) / sum(|dh/dQ|), repeated until the head
losses around every loop sum to zero.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
eps = pf.ROUGHNESS["cast_iron"]

# name: (from, to, length [m], diameter [m], initial flow [m3/s] satisfying continuity)
pipes = {
    "AB": ("A", "B", 600.0, 0.25, 0.07),
    "BC": ("B", "C", 600.0, 0.15, 0.04),
    "AD": ("A", "D", 400.0, 0.20, 0.05),
    "BE": ("B", "E", 400.0, 0.15, 0.03),
    "CF": ("C", "F", 400.0, 0.10, 0.01),
    "DE": ("D", "E", 600.0, 0.15, 0.02),
    "EF": ("E", "F", 600.0, 0.20, 0.05),
}
flows = {name: p[4] for name, p in pipes.items()}

# Clockwise loops: +1 if the pipe's positive direction is clockwise
loops = {
    "I": [("AB", +1), ("BE", +1), ("DE", -1), ("AD", -1)],
    "II": [("BC", +1), ("CF", +1), ("EF", -1), ("BE", -1)],
}


def signed_loss(name: str, q: float) -> float:
    """Head loss in the pipe's positive direction (negative if flow reverses)."""
    if abs(q) < 1e-12:
        return 0.0
    _, _, length, d, _ = pipes[name]
    h = pf.head_loss(abs(q), d, length, water, eps).total_head_loss
    return h if q > 0 else -h


print(f"{'iter':>4}  " + "  ".join(f"dQ_{k:<3}" for k in loops) + "   max |sum h| [m]")
for iteration in range(1, 51):  # Hardy Cross: correct each loop in turn until the head losses balance
    max_imbalance = 0.0
    corrections = []
    for members in loops.values():
        sum_h, sum_dh = 0.0, 0.0  # sum of head losses around the loop and of their Q-derivatives
        for name, sign in members:
            q = sign * flows[name]
            h = signed_loss(name, flows[name]) * sign
            dq = max(abs(q) * 1e-6, 1e-9)
            dh = (abs(signed_loss(name, abs(q) + dq)) - abs(signed_loss(name, abs(q)))) / dq
            sum_h += h
            sum_dh += dh
        correction = -sum_h / sum_dh  # Newton step for the loop flow correction
        corrections.append(correction)
        max_imbalance = max(max_imbalance, abs(sum_h))
        for name, sign in members:
            flows[name] += sign * correction
    shown = [0.0 if abs(c) < 5e-7 else c for c in corrections]  # avoid printing -0.000
    print(f"{iteration:>4}  " + "  ".join(f"{c * 1000:>+7.3f}" for c in shown) + f"   {max_imbalance:.2e}")
    if max(abs(c) for c in corrections) < 1e-8:
        break

print(f"\n{'pipe':>4} {'Q [L/s]':>9} {'V [m/s]':>8} {'hf [m]':>7}")
for name, (_, _, _, d, _) in pipes.items():
    q = flows[name]
    print(f"{name:>4} {q * 1000:>9.2f} {pf.mean_velocity(abs(q), d):>8.2f} {signed_loss(name, q):>7.2f}")

# Node heads, walking out from A
heads = {"A": 50.0}
while len(heads) < 6:  # walk outwards from A, adding one node at a time
    for name, (n1, n2, *_rest) in pipes.items():
        if n1 in heads and n2 not in heads:
            heads[n2] = heads[n1] - signed_loss(name, flows[name])
        elif n2 in heads and n1 not in heads:
            heads[n1] = heads[n2] + signed_loss(name, flows[name])
print("\nNode piezometric heads [m]: " + ", ".join(f"{n} {h:.2f}" for n, h in sorted(heads.items())))

# Continuity check
demand = {"A": -0.12, "C": 0.03, "D": 0.03, "F": 0.06}
for node in "ABCDEF":
    net = sum(flows[p] for p, v in pipes.items() if v[1] == node) - sum(
        flows[p] for p, v in pipes.items() if v[0] == node
    )
    assert abs(net - demand.get(node, 0.0)) < 1e-9, node
print("Continuity satisfied at every node.")
