"""Example 49 - Pressure variation along a drip irrigation lateral.

A lateral with many equally spaced emitters loses flow at every outlet, so the
flow (and friction) decreases along its length. Design rule: the pressure
variation along the lateral should stay within about 20 % of the operating pressure.
"""

from fluidmech import Fluid
from fluidmech import pipe_flow as pf

water = Fluid.water(20)
d = 0.0136  # 16 mm polyethylene lateral, inside diameter
eps = pf.ROUGHNESS["pvc"]
spacing = 0.5  # m between emitters
q_emitter = 2.0 / 3600 / 1000  # 2 L/h in m3/s
h_inlet = 10.0  # m of pressure head at the lateral inlet
slope = 0.0  # ground slope (positive = downhill)


def simulate(n_emitters: int, slope: float = 0.0) -> list[float]:
    """March from the inlet, returning the pressure head at each emitter."""
    heads = []
    h = h_inlet
    q = n_emitters * q_emitter
    for _ in range(n_emitters):  # march from the inlet: friction over one spacing, then one emitter's flow leaves
        loss = pf.head_loss(q, d, spacing, water, eps).major_head_loss if q > 0 else 0.0
        h = h - loss + slope * spacing
        heads.append(h)
        q -= q_emitter
    return heads


print(f"16 mm lateral, emitters 2 L/h every {spacing} m, {h_inlet} m inlet head\n")
print(f"{'length [m]':>10} {'emitters':>9} {'inlet Q [L/h]':>14} {'min head':>9} {'variation':>10}  OK?")
for length in [25, 50, 75, 100, 125, 150]:
    n = int(length / spacing)
    heads = simulate(n)
    variation = (h_inlet - min(heads)) / h_inlet
    print(
        f"{length:>10} {n:>9} {n * 2:>14} {min(heads):>9.2f} {variation:>10.1%}  {'yes' if variation <= 0.2 else 'NO'}"
    )

print("\nA gentle downhill slope compensates for friction:")
for s in [0.0, 0.005, 0.01, 0.02]:
    heads = simulate(200, s)
    spread = (max(heads + [h_inlet]) - min(heads)) / h_inlet
    print(
        f"  slope {s:>5.1%}: head along 100 m lateral {min(heads):5.2f} - {max(heads + [h_inlet]):5.2f} m "
        f"(variation {spread:.1%})"
    )

# Christiansen factor check: friction with multiple outlets ~ F x friction with full flow throughout
n = 200
full = pf.head_loss(n * q_emitter, d, n * spacing, water, eps).major_head_loss
actual = h_inlet - simulate(n)[-1]
print(f"\nChristiansen factor F = {actual / full:.3f}")
print("(theory for many outlets: 1/(m+1) = 0.36 for friction exponent m = 1.75, 0.33 for m = 2)")
