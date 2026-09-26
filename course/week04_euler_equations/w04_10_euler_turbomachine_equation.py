"""CHME 202 - Week 4 - Example 10: Euler's turbomachine equation - ideal head of a centrifugal pump.

Angular momentum applied to an impeller gives H = (u2 V_t2 - u1 V_t1) / g.
With no inlet swirl and backward-curved blades at angle beta2 (from the tangent):
V_t2 = u2 - V_r2 / tan(beta2), V_r2 = Q / (pi D2 b2). The ideal head falls linearly with Q.
Reading: White, Section 11.2.
"""

import math

from fluidmech.constants import G

D2, b2, rpm = 0.25, 0.02, 1450  # impeller exit diameter [m], exit width [m], speed
u2 = math.pi * D2 * rpm / 60  # blade tip speed [m/s]
print(f"Impeller D2 = {D2} m, exit width {b2 * 1000:.0f} mm, {rpm} rpm: tip speed u2 = {u2:.2f} m/s")
print(f"Shut-off (Q = 0) ideal head u2^2 / g = {u2**2 / G:.1f} m\n")
print(f"{'Q [L/s]':>8} " + "".join(f"{f'beta2 = {b} deg':>16}" for b in (20, 30, 90, 120)))
for q_ls in [0, 20, 40, 60, 80]:
    q = q_ls / 1000  # L/s -> m3/s
    vr = q / (math.pi * D2 * b2)  # radial velocity at the impeller exit
    heads = [(u2 - vr / math.tan(math.radians(b))) * u2 / G for b in (20, 30, 90, 120)]
    print(f"{q_ls:>8} " + "".join(f"{h:>16.1f}" for h in heads))
print("\nBackward-curved blades (beta2 < 90 deg) give a falling head curve, which is stable in")
print("parallel operation - almost all process pumps use them. Real pumps deliver ~60-75 % of the")
print("ideal head because of slip, friction and shock losses (compare the pump curves in Week 10).")
print("Scaling: H ~ u2^2 ~ N^2 D^2 and Q ~ N D^3 - the affinity laws of Week 13 follow directly.")
