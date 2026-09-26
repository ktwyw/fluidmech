"""Example 24 - Hydraulic jumps in a stilling basin.

For a rectangular channel:
  sequent depth  y2/y1 = (sqrt(1 + 8 Fr1^2) - 1) / 2
  energy loss    dE    = (y2 - y1)^3 / (4 y1 y2)
"""

from fluidmech.open_channel import RectangularChannel, hydraulic_jump_depth


def jump_type(fr: float) -> str:
    """USBR classification by upstream Froude number."""
    if fr < 1.7:
        return "undular"
    if fr < 2.5:
        return "weak"
    if fr < 4.5:
        return "oscillating"
    if fr < 9.0:
        return "steady"
    return "strong"


width = 10.0  # basin width [m]
y1 = 0.30  # depth entering the jump [m]
ch = RectangularChannel(width)
print(f"Stilling basin, b = {width} m, depth entering the jump y1 = {y1} m\n")
print(f"{'Fr1':>5} {'V1 [m/s]':>9} {'Q [m3/s]':>9} {'y2 [m]':>7} {'dE [m]':>7} {'dE/E1':>6} {'L_j [m]':>8}  type")
for fr1 in [1.5, 2.0, 3.0, 4.5, 6.0, 8.0, 10.0, 12.0]:
    v1 = fr1 * (9.80665 * y1) ** 0.5
    q = v1 * y1 * width
    y2 = hydraulic_jump_depth(y1, fr1)
    e1 = ch.specific_energy(y1, q)
    e2 = ch.specific_energy(y2, q)
    de = (y2 - y1) ** 3 / (4 * y1 * y2)
    assert abs(de - (e1 - e2)) < 1e-9  # the two ways of computing the loss agree
    length = 6.1 * y2  # approximate jump length for steady jumps
    print(f"{fr1:>5.1f} {v1:>9.2f} {q:>9.2f} {y2:>7.2f} {de:>7.3f} {de / e1:>6.1%} {length:>8.1f}  {jump_type(fr1)}")

print("\nDesign practice: aim for a 'steady' jump (4.5 < Fr1 < 9) - efficient energy")
print("dissipation, stable position and a reasonably compact basin.")

# Power dissipated in a design case
fr1 = 6.0
v1 = fr1 * (9.80665 * y1) ** 0.5
q = v1 * y1 * width
y2 = hydraulic_jump_depth(y1, fr1)
de = (y2 - y1) ** 3 / (4 * y1 * y2)
print(f"\nAt Fr1 = {fr1}: the jump dissipates {1000 * 9.80665 * q * de / 1e6:.2f} MW as heat and turbulence.")
