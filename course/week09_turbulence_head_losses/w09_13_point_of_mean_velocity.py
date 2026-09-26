"""CHME 202 - Week 9 - Example 13: where in the pipe does the local velocity equal the mean?

Single-point (insertion) flow meters and Pitot tubes measure one local velocity. With the
turbulent power-law profile u = U_max (1 - r/R)^(1/n) the local velocity equals the mean
V at a fixed fraction of the radius, nearly independent of Re: about 0.76 R from the axis
(~1/8 of the diameter in from the wall).
"""

from fluidmech import turbulence as tb

print(f"{'Re':>9} {'n':>6} {'V/U_max':>8} {'r/R where u = V':>16} {'depth from wall / D':>20}")
for re in [1e4, 1e5, 1e6, 1e7]:
    n = tb.power_law_exponent(re)
    ratio = tb.mean_to_max_velocity_ratio(n)
    r_over_R = 1 - ratio**n  # (1 - r/R)^(1/n) = V/U_max
    print(f"{re:>9.0e} {n:>6.2f} {ratio:>8.3f} {r_over_R:>16.3f} {(1 - r_over_R) / 2:>20.3f}")
print("\nThe point of mean velocity stays at r/R ~ 0.76 over three decades of Re - so an insertion")
print("probe placed there reads the mean velocity without a traverse. It needs a fully developed")
print("profile: install it 20-30 D downstream of bends and valves (Example 1, entrance length).")
print("For laminar flow (parabola) the point would instead be r/R = 0.707.")
