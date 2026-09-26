"""Example 3 - Hydrostatic force on a sluice gate and a floating body."""

from fluidmech import hydrostatics as hs

# A 3 m wide, 2 m tall vertical gate whose top edge is 4 m below the reservoir level.
gate = hs.rectangular_gate(width=3.0, height=2.0, top_depth=4.0)
print("Vertical rectangular gate (3 m x 2 m, top 4 m deep)")
print(f"  resultant force         = {gate.force / 1e3:.1f} kN")
print(f"  centroid depth          = {gate.centroid_depth:.3f} m")
print(f"  centre of pressure depth = {gate.center_of_pressure_depth:.3f} m\n")

# Same gate inclined at 60 degrees to the horizontal
inclined = hs.rectangular_gate(width=3.0, height=2.0, top_depth=4.0, angle_deg=60.0)
print("Same gate inclined at 60 deg")
print(f"  resultant force = {inclined.force / 1e3:.1f} kN")
print(f"  centre of pressure {inclined.center_of_pressure_slant:.3f} m along the gate from the free-surface line\n")

# Iceberg in sea water
frac = hs.submerged_fraction(body_density=917.0, fluid_density=1025.0)
print(f"An iceberg floats with {frac:.1%} of its volume below the sea surface.")
