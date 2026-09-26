"""CHME 202 - Week 11 - Example 10: gas holdup and interfacial area in a bubble column.

In the homogeneous (bubbly) regime, bubbles rise at their terminal velocity U_b
relative to the liquid, so the gas volume fraction is roughly eps = U_g / (U_g + U_b)
(U_g = superficial gas velocity). The interfacial area a = 6 eps / d_b controls mass transfer.
"""

from fluidmech import Fluid
from fluidmech.drag import mendelson_bubble_velocity
from fluidmech.properties import water_surface_tension

water = Fluid.water(25)
sigma = water_surface_tension(25)
D_col, H_liq = 0.5, 3.0  # column diameter [m], clear liquid height [m]
print(f"Air-water bubble column D = {D_col} m, clear liquid height {H_liq} m\n")
print(f"{'d_b [mm]':>9} {'U_b [m/s]':>10} " + "".join(f"{f'Ug={u} cm/s':>13}" for u in (1, 2, 4)))
for d_mm in [2.0, 4.0, 6.0]:
    ub = mendelson_bubble_velocity(d_mm / 1000, sigma, water)  # mm -> m
    cells = []
    for ug_cm in (1, 2, 4):
        ug = ug_cm / 100
        eps = ug / (ug + ub)  # gas holdup, homogeneous bubbly regime
        a = 6 * eps / (d_mm / 1000)  # interfacial area per volume = 6 eps / d_b
        cells.append(f"{eps:5.1%}/{a:4.0f}")
    print(f"{d_mm:>9} {ub:>10.3f} " + "".join(f"{c:>13}" for c in cells))
print("(entries: gas holdup / interfacial area a [m2/m3])\n")
eps = 0.02 / (0.02 + mendelson_bubble_velocity(4e-3, sigma, water))  # Ug = 2 cm/s, 4 mm bubbles
print(f"At Ug = 2 cm/s with 4 mm bubbles the aerated height rises to {H_liq / (1 - eps):.2f} m.")
print("Interfacial area scales as 1/d_b: halving the bubble size roughly doubles the area for the same")
print("holdup - the reason for fine-bubble diffusers in aeration tanks. (In clean water 1.5-2 mm bubbles")
print("rise fastest; below ~1 mm they slow down sharply, which raises the holdup further.)")
print("Above Ug ~ 5 cm/s the column turns heterogeneous")
print("(large bubbles, churn flow) and this simple model no longer applies.")
