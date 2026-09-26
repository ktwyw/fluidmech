"""CHME 202 - Week 14 - Example 3: scaling up a stirred tank - you cannot keep everything constant.

A 20 L pilot vessel is scaled up 1000x in volume (10x in diameter) with geometric
similarity. Each scale-up rule preserves one quantity and changes all the others.
"""

from fluidmech import mixing as mx

rho, mu = 1000.0, 1e-3  # water
T1, N1 = 0.294, 5.0  # 20 L pilot, 300 rpm
T2 = 10 * T1
d1, d2 = T1 / 3, T2 / 3
base = mx.StirredTank(T1, d1).analyse(N1, rho, mu)
print(
    f"Pilot: T = {T1} m, {N1 * 60:.0f} rpm, P/V = {base['power_per_volume_W_m3']:.0f} W/m3, "
    f"blend time {base['blend_time_s']:.1f} s\n"
)
print(f"{'rule':<18} {'rpm':>6} {'P [kW]':>8} {'P/V':>7} {'tip speed':>9} {'Re':>9} {'blend t [s]':>11}")
for rule in ["power_per_volume", "tip_speed", "reynolds", "blend_time"]:
    n2 = mx.scale_up_speed(N1, d1, d2, rule)
    r = mx.StirredTank(T2, d2).analyse(n2, rho, mu)
    print(
        f"{rule:<18} {n2 * 60:>6.1f} {r['power_W'] / 1e3:>8.2f} {r['power_per_volume_W_m3'] / base['power_per_volume_W_m3']:>6.2f}x "
        f"{r['tip_speed_m_s'] / base['tip_speed_m_s']:>8.2f}x {r['reynolds']:>9.2e} {r.get('blend_time_s', float('nan')):>11.1f}"
    )
print("\nConstant P/V (common for mass transfer and suspension) makes blending ~4.6x slower at full scale.")
print("Keeping the blend time needs 100x the power per volume - usually impossible.")
print("Constant Re gives a large tank turning at 3 rpm with almost no power - essentially unstirred.")
print("Real scale-up is a compromise chosen by what controls the process (blending, suspension, gas-liquid, heat).")
