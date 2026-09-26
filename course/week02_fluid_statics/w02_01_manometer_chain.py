"""CHME 202 - Week 2 - Example 1: solving multi-fluid manometers step by step.

Rule: start at a known pressure and walk through the manometer. Going DOWN
by dz in a fluid adds rho g dz; going UP subtracts it; crossing at the same
level in the same fluid changes nothing (Pascal's law).
Reading: White, Sections 2.3-2.4.
"""

from fluidmech.constants import G

WATER, MERCURY, OIL, AIR = 1000.0, 13_600.0, 850.0, 1.2  # densities [kg/m3]


def walk(start_pressure: float, steps: list[tuple[str, float, float]]) -> float:
    """Apply (description, density, dz) steps; dz > 0 means moving downward."""
    p = start_pressure
    print(f"  start: {p / 1e3:9.3f} kPa")
    for label, rho, dz in steps:
        p += rho * G * dz  # hydrostatic step: down (dz > 0) adds pressure, up subtracts
        direction = "down" if dz > 0 else "up"
        print(f"  {direction:>4} {abs(dz):5.3f} m through {label:<8} -> {p / 1e3:9.3f} kPa")
    return p


print("Problem: water pipe A and oil pipe B connected by an inverted-U and a mercury U-tube.")
print("Find pA - pB. Heights in metres (see figure in lecture slides).\n")
p_b = walk(
    0.0,
    [
        ("water", WATER, 0.30),  # from A down to the water-mercury interface
        ("mercury", MERCURY, -0.20),  # up through the mercury
        ("air", AIR, -0.15),  # up through a small air pocket
        ("oil", OIL, 0.45),  # down through oil to pipe B
    ],
)
print(f"\nSetting pA = 0 gives pB = {p_b / 1e3:.3f} kPa, so pA - pB = {-p_b / 1e3:.3f} kPa")
print("The air pocket contributes only a few pascals: gas columns can usually be neglected.\n")

print("Sensitivity: what reading would a single mercury U-tube show for the same dp?")
dp = -p_b
h_hg = dp / ((MERCURY - WATER) * G)
print(f"  dp = {dp / 1e3:.2f} kPa -> {h_hg * 1000:.0f} mm of mercury under water")
print(
    f"  with a water-over-oil differential gauge instead: {dp / ((WATER - OIL) * G):.2f} m (far more sensitive, but impractically tall here)"
)
