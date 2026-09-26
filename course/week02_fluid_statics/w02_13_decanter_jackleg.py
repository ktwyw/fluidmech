"""CHME 202 - Week 2 - Example 13: the continuous gravity decanter and its jackleg.

Light liquid A overflows at the top (height z_A1); heavy liquid B leaves through a
'jackleg' whose overflow is at z_B2. A hydrostatic balance gives the interface height
z_B1 = (z_B2 - z_A1 rho_A / rho_B) / (1 - rho_A / rho_B)
(McCabe, Smith & Harriott - gravity decanters).
"""

rho_A, rho_B = 870.0, 1000.0  # light (organic) and heavy (aqueous) phases
z_A1 = 1.20  # light-liquid overflow height [m]
print(f"Decanter: light phase {rho_A} kg/m3 overflows at {z_A1} m, heavy phase {rho_B} kg/m3\n")
print(f"{'jackleg overflow z_B2 [m]':>26} {'interface z_B1 [m]':>19}")
for z_B2 in [1.05, 1.07, 1.10, 1.13, 1.15]:
    z_B1 = (z_B2 - z_A1 * rho_A / rho_B) / (1 - rho_A / rho_B)
    note = (
        "  <- heavy phase would leave with the light overflow"
        if z_B1 >= z_A1
        else ("  <- light phase escapes through the jackleg" if z_B1 <= 0 else "")
    )
    print(f"{z_B2:>26.2f} {z_B1:>19.2f}{note}")
amp = 1 / (1 - rho_A / rho_B)  # d(z_B1)/d(z_B2): interface moves this much per unit of jackleg
print(f"\nThe interface moves {amp:.1f}x as much as the jackleg: 1 cm on the jackleg shifts the interface")
print(f"{amp:.1f} cm. With close densities the amplification grows - adjustable jacklegs are standard.")
