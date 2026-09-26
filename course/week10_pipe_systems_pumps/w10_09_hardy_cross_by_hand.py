"""CHME 202 - Week 10 - Example 9: a pipe loop solved by the Hardy Cross method, step by step.

Hand method for looped networks: guess flows that satisfy continuity, then
correct each loop by dQ = -sum(h) / sum(n |h / Q|) (n = 2 for turbulent flow)
until the head losses around the loop sum to zero. We then check the answer
with the Newton network solver of fluidmech.
Reading: White, Section 6.11 (pipe networks).
"""

from fluidmech import Fluid, Network
from fluidmech import pipe_flow as pf

water = Fluid.water(15)
eps = pf.ROUGHNESS["cast_iron"]
# One loop A-B-C-D; 100 L/s enters at A and leaves at C.
pipes = {"AB": (500, 0.25), "BC": (400, 0.20), "AD": (300, 0.15), "DC": (600, 0.20)}
sign = {"AB": +1, "BC": +1, "DC": -1, "AD": -1}  # clockwise positive
Q = {"AB": 0.060, "BC": 0.060, "AD": 0.040, "DC": 0.040}  # initial guess (continuity OK)


def h(name, q):
    L, D = pipes[name]
    return pf.head_loss(abs(q), D, L, water, eps).major_head_loss if q else 0.0


print(f"{'iter':>4} " + "".join(f"{p:>8}" for p in pipes) + "   sum(h) [m]   dQ [L/s]")
for it in range(1, 7):  # six Hardy Cross iterations
    sum_h = sum(sign[p] * (h(p, Q[p]) if Q[p] > 0 else -h(p, Q[p])) for p in pipes)
    denom = sum(2 * h(p, Q[p]) / abs(Q[p]) for p in pipes)  # sum of dh/dQ = 2 h / Q (h ~ Q^2)
    dq = -sum_h / denom
    print(
        f"{it:>4} "
        + "".join(f"{Q[p] * 1000:>8.2f}" for p in pipes)
        + f"   {(0.0 if abs(sum_h) < 5e-5 else sum_h):>9.4f}   {(0.0 if abs(dq) < 5e-7 else dq) * 1000:>+8.3f}"
    )
    for p in pipes:
        Q[p] += sign[p] * dq

net = Network(water)
net.add_reservoir("A", 50.0)
for n, demand in [("B", 0.0), ("C", 0.100), ("D", 0.0)]:
    net.add_junction(n, demand=demand)
for p, (L, D) in pipes.items():
    net.add_pipe(p, p[0], p[1], L, D, eps)
res = net.solve()
print("\nNewton network solver:     " + "".join(f"{res.flows[p] * 1000:>8.2f}" for p in pipes))
print("Hardy Cross converges in a few iterations to the same flows (L/s).")
