"""Example 15 - Pump operating point: intersecting pump and system curves.

A centrifugal pump lifts water 15 m through 400 m of 200 mm cast-iron pipe.
Optional plot: saves pump_curve.png if matplotlib is installed.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf
from fluidmech.constants import G
from fluidmech.solvers import bisect

water = Fluid.water(20)
static_lift = 15.0  # elevation difference between the water surfaces [m]
D, L, eps = 0.20, 400.0, pf.ROUGHNESS["cast_iron"]  # diameter [m], length [m], roughness [m]
k_total = 0.5 + 4 * 0.3 + 0.15 + 2.0 + 1.0  # entrance, elbows, gate valve, check valve, exit


def pump_head(q: float) -> float:
    """Manufacturer's curve fitted as H = H0 - a Q^2 [m]."""
    return 40.0 - 1500.0 * q**2


def pump_efficiency(q: float) -> float:
    """Parabolic efficiency curve peaking at 80 % at Q = 0.08 m3/s."""
    return max(0.80 * (1.0 - ((q - 0.08) / 0.08) ** 2), 0.05)


def system_head(q: float) -> float:
    if q <= 0.0:
        return static_lift
    return static_lift + pf.head_loss(q, D, L, water, eps, k_total).total_head_loss


print(f"{'Q [L/s]':>8} {'H_pump [m]':>11} {'H_system [m]':>13} {'eff':>6}")
for q_ls in range(0, 161, 20):
    q = q_ls / 1000  # L/s -> m3/s
    print(f"{q_ls:>8} {pump_head(q):>11.2f} {system_head(q):>13.2f} {pump_efficiency(q):>6.1%}")

# upper bracket = pump run-out flow (H = 0)
q_op = bisect(lambda q: pump_head(q) - system_head(q), 1e-6, (40.0 / 1500.0) ** 0.5)
h_op = pump_head(q_op)
eta = pump_efficiency(q_op)
power = water.density * G * q_op * h_op / eta

print(f"\nOperating point: Q = {q_op * 1000:.1f} L/s, H = {h_op:.1f} m, efficiency {eta:.1%}")
print(f"Shaft power = {power / 1e3:.1f} kW")

# Throttling vs. a parallel second pump
print("\nTwo identical pumps in parallel (each carries Q/2):")
# in parallel each pump carries q / 2 at the same head
q_par = bisect(lambda q: pump_head(q / 2) - system_head(q), 1e-6, 2 * (40.0 / 1500.0) ** 0.5)
print(f"  Q = {q_par * 1000:.1f} L/s  (+{(q_par / q_op - 1):.0%}, not +100 %, because losses grow ~Q^2)")

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("\n(matplotlib not installed - skipping plot)")
else:
    qs = [i / 1000 for i in range(0, 171, 2)]  # 0-170 L/s in m3/s; plotted in L/s below
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot([q * 1000 for q in qs], [pump_head(q) for q in qs], label="pump")
    ax.plot([q * 1000 for q in qs], [pump_head(q / 2) for q in qs], "--", label="2 pumps in parallel")
    ax.plot([q * 1000 for q in qs], [system_head(q) for q in qs], label="system")
    ax.plot(q_op * 1000, h_op, "ko")
    ax.annotate(f"  {q_op * 1000:.0f} L/s, {h_op:.1f} m", (q_op * 1000, h_op))
    ax.set_xlabel("Flow rate [L/s]")
    ax.set_ylabel("Head [m]")
    ax.set_ylim(0, 45)
    ax.grid(alpha=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig("pump_curve.png", dpi=150)
    print("\nSaved pump_curve.png")
