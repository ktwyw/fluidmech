"""CHME 202 - Week 14 - Example 9: laminar mixing - stretching and folding in a static mixer.

Without turbulence, mixing relies on molecular diffusion over a distance s, taking
t ~ s^2 / D_m. A helical-element static mixer splits and folds the stream, doubling
the number of layers per element: after n elements the striation thickness is d / 2^n.
"""

d = 0.025  # pipe diameter [m]
D_m = 1e-9  # molecular diffusivity in a liquid [m2/s]
V = 0.1  # velocity [m/s]
element_length = 1.5 * d
print(f"Two viscous streams side by side in a {d * 1000:.0f} mm pipe at {V} m/s, D_m = {D_m} m2/s\n")
print(f"{'elements':>9} {'layers':>8} {'striation [um]':>15} {'diffusion time':>15} {'pipe length':>12}")
for n in [0, 4, 8, 12, 16, 20]:
    s = d / 2 ** (n + 1)  # each element doubles the layers; two initial streams
    t_diff = s**2 / D_m  # diffusion time across one striation
    if t_diff > 3600:
        t_txt = f"{t_diff / 3600:.1f} h"
    elif t_diff > 0.1:
        t_txt = f"{t_diff:.1f} s"
    elif t_diff > 1e-4:
        t_txt = f"{t_diff * 1000:.1f} ms"
    else:
        t_txt = f"{t_diff * 1e6:.2f} us"
    length = n * element_length + V * t_diff
    print(f"{n:>9} {2**n:>8} {s * 1e6:>15.2f} {t_txt:>15} {length:>10.2f} m")
print("\nWithout a mixer, diffusion across the pipe would take days; 12-16 elements reduce the")
print("striations to micrometres and diffusion finishes in a fraction of a second.")
print("Static mixers have no moving parts but cost pressure drop (several times that of the empty pipe).")
