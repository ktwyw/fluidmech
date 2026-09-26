"""Example 10 - Draft and stability of a rectangular floating barge.

Metacentric height GM = KB + BM - KG. The barge is stable if GM > 0.
"""

from fluidmech.constants import G
from fluidmech.hydrostatics import buoyant_force, submerged_fraction

L, B, H = 20.0, 6.0, 3.0  # length, beam, depth [m]
rho_sea = 1025.0
mass_empty = 90_000.0  # kg
kg_empty = 1.2  # centre of gravity above keel [m]

print(f"Barge {L} m x {B} m x {H} m in sea water (rho = {rho_sea} kg/m3)\n")
print(f"{'cargo [t]':>9} {'draft':>7} {'freeboard':>10} {'KB':>6} {'BM':>6} {'KG':>6} {'GM':>6}  status")

for cargo_t, cargo_kg_height in [(0, 0), (50, 2.0), (100, 2.5), (150, 3.0), (200, 4.0), (250, 5.0)]:
    mass = mass_empty + cargo_t * 1000.0  # tonnes -> kg
    draft = mass / (rho_sea * L * B)  # Archimedes: displaced volume L B T = mass / rho
    if draft >= H:
        print(f"{cargo_t:>9} sinks: draft {draft:.2f} m exceeds the hull depth")
        continue
    # Combined centre of gravity (cargo CG measured above the keel)
    kg = (mass_empty * kg_empty + cargo_t * 1000.0 * cargo_kg_height) / mass
    kb = draft / 2.0
    bm = B**2 / (12.0 * draft)  # I / V for a rectangular waterplane
    gm = kb + bm - kg
    status = "stable" if gm > 0.3 else ("marginal" if gm > 0 else "UNSTABLE")
    print(f"{cargo_t:>9} {draft:>7.2f} {H - draft:>10.2f} {kb:>6.2f} {bm:>6.2f} {kg:>6.2f} {gm:>6.2f}  {status}")

# Check equilibrium with Archimedes for the empty barge
draft0 = mass_empty / (rho_sea * L * B)
fb = buoyant_force(L * B * draft0, rho_sea)
print(f"\nEmpty barge: buoyancy {fb / 1e3:.1f} kN vs weight {mass_empty * G / 1e3:.1f} kN")
effective_density = mass_empty / (L * B * H)
print(f"Submerged fraction of hull volume: {submerged_fraction(effective_density, rho_sea):.1%}")
print("\nTip: stacking cargo high raises KG faster than it lowers BM -> watch deck loads.")
