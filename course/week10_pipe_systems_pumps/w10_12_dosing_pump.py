"""CHME 202 - Week 10 - Example 12: positive-displacement (dosing) pumps versus centrifugal pumps.

A PD pump delivers a fixed volume per stroke: its flow hardly depends on the discharge
pressure, whereas a centrifugal pump's flow falls steeply as the head rises. That makes
PD pumps ideal for accurate chemical dosing - but it also means they must NEVER run against
a closed valve without a relief valve. Pulsation: a single-piston pump's peak flow is
about pi times its mean (sinusoidal discharge stroke). Pump data are ILLUSTRATIVE.
"""

import math

from fluidmech import PumpCurve

stroke_volume, spm = 12e-6, 90  # m3 per stroke, strokes per minute
slip_per_bar = 0.003  # fractional slip per bar of back-pressure
centrifugal = PumpCurve(h0=60.0, h1=0.0, h2=-60.0 / (1.5e-3) ** 2)  # shut-off 60 m, runout 1.5 L/s
print(f"Dosing pump: {stroke_volume * 1e6:.0f} mL/stroke at {spm} strokes/min\n")
print(f"{'back-pressure [bar]':>20} {'dosing pump [L/h]':>18} {'centrifugal [L/h]':>18}")
for bar in [0.5, 2, 4, 5, 5.8]:
    q_pd = stroke_volume * spm / 60 * (1 - slip_per_bar * bar)  # displacement per second minus slip
    head = bar * 1e5 / (1000 * 9.80665)  # bar -> m of water
    q_c = math.sqrt(max(0.0, (centrifugal.h0 - head) / -centrifugal.h2))
    print(f"{bar:>20} {q_pd * 3.6e6:>18.2f} {q_c * 3.6e6:>18.0f}")
mean = stroke_volume * spm / 60  # mean flow [m3/s] (strokes per minute -> per second)
print(f"\nSingle-piston pulsation: mean {mean * 3.6e6:.1f} L/h, peak ~{math.pi * mean * 3.6e6:.1f} L/h (pi x mean).")
print("Friction losses in the dosing line must be checked at the PEAK flow; pulsation dampeners or")
print("multi-head pumps smooth it. Flow is set by stroke rate and length, not by throttling.")
print("(The course covers the line-loss fundamentals; selection of dosing pumps, chemical compatibility")
print(" and metering control need specific product training.)")
