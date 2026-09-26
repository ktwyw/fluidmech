"""CHME 202 - Week 14 - Example 5: residence-time distribution (RTD) and conversion.

How long fluid stays in a vessel depends on the flow pattern: a CSTR, tanks in
series, a plug-flow reactor and a laminar tube (Hagen-Poiseuille profile, Week 6)
give different RTDs and therefore different conversions for the same mean time.
Saves rtd.png.

# requires: matplotlib
"""

import matplotlib.pyplot as plt

from fluidmech import mixing as mx

print("First-order reaction, conversion X for Damkohler number k tau:")
print(f"{'k tau':>6} {'CSTR':>7} {'3 tanks':>8} {'laminar tube':>13} {'PFR':>7}")
for da in [0.1, 0.5, 1.0, 2.0, 5.0]:
    print(
        f"{da:>6} {mx.cstr_conversion(da):>7.3f} {mx.tanks_in_series_conversion(da, 3):>8.3f} "
        f"{mx.laminar_flow_reactor_conversion(da):>13.3f} {mx.pfr_conversion(da):>7.3f}"
    )
print("\nBack-mixing lowers conversion. The laminar tube usually lies between CSTR and PFR: fluid near the")
print("wall stays long, fluid on the axis leaves after only half the mean residence time (u_max = 2 V).")
print("At very low k tau it can even fall slightly BELOW the CSTR - check the first row - because of that")
print("short-circuiting core. Radial diffusion (ignored here) narrows the RTD and helps real tubes.")

ts = [i * 0.01 for i in range(1, 400)]  # t / tau from 0.01 to 4
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(ts, [mx.cstr_rtd(t, 1.0) for t in ts], label="CSTR")
for n in (3, 10):
    ax.plot(ts, [mx.tanks_in_series_rtd(t, 1.0, n) for t in ts], label=f"{n} tanks in series")
ax.plot(ts, [mx.laminar_rtd(t, 1.0) for t in ts], label="laminar tube")
ax.axvline(1.0, color="k", ls=":", label="PFR (all at t = tau)")
ax.set(xlabel="t / tau", ylabel="E(t) tau", title="Residence-time distributions", ylim=(0, 2.5))
ax.legend()
fig.tight_layout()
fig.savefig("rtd.png", dpi=130)
print("Saved rtd.png")
