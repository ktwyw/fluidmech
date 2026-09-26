"""CHME 202 - Week 4 - Example 7: the stream function measures flow rate.

The volume flow (per unit depth) between two streamlines equals psi2 - psi1.
For the stagnation-point flow into a corner, psi = a x y.
Reading: White, Section 4.7.
"""

from fluidmech.potential_flow import Source, Uniform

a = 2.0  # 1/s


def psi(x, y):
    return a * x * y


print("Corner flow psi = a x y (a = 2 1/s): flow between the wall (psi = 0) and a streamline")
for x, y in [(1.0, 0.5), (2.0, 1.0), (0.5, 4.0)]:
    print(f"  through the point ({x}, {y}): q = psi = {psi(x, y):.2f} m2/s per metre depth")

# Check by integrating u across a vertical line x = 1 from y = 0 to y = 0.5
n, x0, y_top = 1000, 1.0, 0.5
q_num = sum(a * x0 * (y_top / n) for _ in range(n))  # u = d(psi)/dy = a x
print(f"  numerical integral of u across x = 1, 0 < y < 0.5: {q_num:.3f} m2/s  (matches psi)\n")

flow = Uniform(3.0) + Source(4.0)
print("Rankine half-body (U = 3 m/s, m = 4 m2/s): the body surface is the streamline psi = m/2")
print(f"  psi on the dividing streamline far downstream: {flow.stream_function(50.0, 4.0 / 6.0):.3f} m2/s ~ m/2 = 2")
print("  All the source's output (m = 4 m2/s) flows inside the body, half above and half below the axis.")
