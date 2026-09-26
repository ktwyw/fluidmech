"""Example 41 - Measuring Mach number in a supersonic wind tunnel.

A Pitot tube in supersonic flow sits behind its own normal shock, so the
subsonic Bernoulli/isentropic formula gives the wrong answer. The
Rayleigh-Pitot formula accounts for the shock.
"""

from fluidmech import compressible as c

print("Normal shock table (k = 1.4)")
print(f"{'M1':>5} {'M2':>7} {'p2/p1':>7} {'T2/T1':>7} {'rho2/rho1':>10} {'p02/p01':>8}")
for m1 in [1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]:
    s = c.normal_shock(m1)
    print(
        f"{m1:>5.1f} {s.mach2:>7.4f} {s.pressure_ratio:>7.3f} {s.temperature_ratio:>7.3f} "
        f"{s.density_ratio:>10.3f} {s.stagnation_pressure_ratio:>8.4f}"
    )
print("Note rho2/rho1 approaches 6 for strong shocks, while p02/p01 collapses.\n")

# Wind tunnel readings: static pressure at the wall and Pitot pressure on the centreline
readings = [(32.0, 120.0), (18.0, 125.0), (9.5, 118.0)]  # (p1 static, p02 pitot) in kPa
print("Tunnel readings")
print(f"{'p1 [kPa]':>9} {'Pitot [kPa]':>12} {'naive M':>8} {'Rayleigh-Pitot M':>17}")
for p1, p02 in readings:
    naive = c.mach_from_pressure_ratio(p1 / p02)
    true_m = c.pitot_mach_supersonic(p02 / p1)
    print(f"{p1:>9.1f} {p02:>12.1f} {naive:>8.3f} {true_m:>17.3f}")
print("Ignoring the bow shock overestimates the Mach number badly.")

m = c.pitot_mach_supersonic(125.0 / 18.0)
p0_reservoir = 18.0 / c.pressure_ratio(m)  # static pressure 18 kPa -> stagnation pressure [kPa]
print(
    f"\nFor the second reading the tunnel reservoir pressure must be {p0_reservoir:.0f} kPa "
    f"and the test-section/throat area ratio {c.area_ratio(m):.3f}."
)
