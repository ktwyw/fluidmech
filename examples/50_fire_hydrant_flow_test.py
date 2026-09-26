"""Example 50 - Interpreting a fire hydrant flow test.

A flow test records the static pressure, then the residual pressure while a
hydrant flows. Assuming head loss ~ Q^1.85 (Hazen-Williams exponent), the flow
available at any residual pressure is

    Q_r = Q_f * ((p_s - p_r) / (p_s - p_f))^0.54

This is the standard NFPA 291 method, done here in both psi/gpm and SI.
"""

from fluidmech.units import convert

static_psi = 72.0  # pressure with no hydrant flowing [psi]
residual_psi = 55.0  # pressure while the test hydrant flows [psi]
flow_gpm = 1150.0  # measured hydrant flow [gpm]

print(f"Test: static {static_psi} psi, residual {residual_psi} psi while flowing {flow_gpm:.0f} gpm\n")


def available_flow(target_residual_psi: float) -> float:
    # 0.54 = 1/1.85 (Hazen-Williams exponent)
    return flow_gpm * ((static_psi - target_residual_psi) / (static_psi - residual_psi)) ** 0.54


print(f"{'residual [psi]':>15} {'[kPa]':>7} {'available [gpm]':>16} {'[L/s]':>7}")
for p in [60, 50, 40, 30, 20, 10]:
    q = available_flow(p)
    print(f"{p:>15} {convert(p, 'psi', 'kPa'):>7.0f} {q:>16.0f} {convert(q, 'gpm', 'L/s'):>7.1f}")

q20 = available_flow(20.0)
print(f"\nRated fire flow at 20 psi residual: {q20:,.0f} gpm ({convert(q20, 'gpm', 'L/s'):.0f} L/s)")
for required in [1000, 1500, 2500, 3500]:
    ok = "meets" if q20 >= required else "DOES NOT meet"
    print(f"  {ok} a {required} gpm fire-flow requirement")

# Water supply curve points for plotting on N^1.85 graph paper
print("\nSupply curve (for a sprinkler hydraulic calculation):")
for q in [0, 500, 1000, 1500, 2000, 2500]:
    p = static_psi - (static_psi - residual_psi) * (q / flow_gpm) ** 1.85
    print(f"  {q:>5} gpm -> {max(p, 0):5.1f} psi")
