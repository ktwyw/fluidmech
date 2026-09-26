"""CHME 202 - Week 5 - Example 12: squeeze films - why it takes time to squeeze liquid out of a gap.

Two discs of radius R approaching each other push liquid out radially. Lubrication theory
(Stefan 1874) gives the force F = 3 pi mu R^4 (-dh/dt) / (2 h^3); under a constant force the
time to go from gap h0 to h1 is  t = (3 pi mu R^4 / (4 F)) (1/h1^2 - 1/h0^2).
Behind squeeze-film dampers, pressing of pastes, and why wet glass plates are hard to separate.
"""

import math

R, F = 0.05, 100.0  # disc radius [m], pressing force [N]
print(f"Disc R = {R * 1000:.0f} mm pressed with {F:.0f} N from a 1 mm gap\n")
print(f"{'liquid':<12} {'mu [Pa s]':>10} " + "".join(f"{f'to {h} um':>12}" for h in (100, 20, 5)))
for name, mu in [("water", 0.001), ("oil", 0.1), ("honey", 10.0)]:
    # t from h0 = 1 mm to h (um -> m)
    times = [3 * math.pi * mu * R**4 / (4 * F) * (1 / (h * 1e-6) ** 2 - 1 / 1e-3**2) for h in (100, 20, 5)]
    print(f"{name:<12} {mu:>10} " + "".join(f"{t:>10.3g} s" for t in times))
print("\nThe time grows as 1/h^2: the last few micrometres take almost all of it. The gap never")
print("reaches zero in finite time for a Newtonian film - surface roughness or elasticity end it.")
print("Separating two plates at speed dh/dt requires the same force in reverse (suction), which is")
print("why wet glass slides seem 'stuck' together.")
