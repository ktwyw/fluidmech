"""Example 43 - Where does the hydraulic jump form downstream of a sluice gate?

Supercritical flow leaves the gate at the vena contracta depth and gradually
deepens (M3 profile). The jump forms where the sequent depth of this
supercritical flow equals the normal (tailwater) depth downstream.
"""

from fluidmech.open_channel import (
    RectangularChannel,
    classify_profile,
    gvf_profile,
    hydraulic_jump_depth,
    hydraulic_jump_energy_loss,
    sluice_gate_flow,
)

b, n, S0 = 5.0, 0.014, 0.0004  # width [m], Manning n, bed slope
y_upstream, opening = 4.0, 0.5  # upstream depth and gate opening [m]
ch = RectangularChannel(b)

Q = sluice_gate_flow(opening, y_upstream, b)
y_vc = 0.61 * opening  # vena contracta depth
yn = ch.normal_depth(Q, n, S0)
yc = ch.critical_depth(Q)
print(f"Gate opening {opening} m under {y_upstream} m head: Q = {Q:.2f} m3/s")
print(f"Vena contracta y1 = {y_vc:.3f} m, critical y_c = {yc:.3f} m, normal (tailwater) y_n = {yn:.3f} m")
print(
    f"Channel is {'mild' if yn > yc else 'steep'}; flow leaving the gate follows an "
    f"{classify_profile(ch, Q, n, S0, y_vc)} profile\n"
)

profile = gvf_profile(ch, Q, n, S0, y_vc, 0.99 * yc, steps=200)
print(f"{'x [m]':>7} {'y [m]':>7} {'Fr':>6} {'sequent y2 [m]':>15}")
jump_at = None
for i, (x, y) in enumerate(profile):
    fr = ch.froude(y, Q)
    y2 = hydraulic_jump_depth(y, fr)
    if i % 20 == 0 or i == len(profile) - 1:
        print(f"{x:>7.1f} {y:>7.3f} {fr:>6.2f} {y2:>15.3f}")
    if jump_at is None and y2 <= yn:  # jump forms where the sequent depth has fallen to the tailwater depth
        jump_at = (x, y, fr)

if jump_at:
    x, y, fr = jump_at
    print(f"\nThe jump forms about {x:.1f} m downstream of the gate:")
    print(f"  y1 = {y:.3f} m (Fr1 = {fr:.2f}) jumps to y2 = {yn:.3f} m")
    print(
        f"  energy dissipated = {hydraulic_jump_energy_loss(y, yn):.3f} m of head, "
        f"{1000 * 9.80665 * Q * hydraulic_jump_energy_loss(y, yn) / 1e3:.0f} kW"
    )
else:
    print("\nThe tailwater is too low for a jump before the flow reaches critical depth;")
    print("the jump is swept downstream. A stilling basin or end sill is required.")
