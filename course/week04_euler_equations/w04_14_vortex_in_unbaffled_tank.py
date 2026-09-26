"""CHME 202 - Week 4 - Example 14: the free-surface vortex in an unbaffled stirred tank.

Swirl in an unbaffled tank is close to a Rankine vortex: forced (rigid) rotation inside
a core of radius r_c, free vortex outside. The radial Euler equation dp/dr = rho v^2 / r
at the free surface gives the surface shape z(r). Deep vortices draw air to the impeller.
"""

from fluidmech.constants import G

R_tank, r_c = 0.5, 0.12  # tank radius, vortex-core radius (~impeller radius)
print(f"Tank radius {R_tank} m, vortex core radius {r_c} m\n")
print(f"{'core speed [m/s]':>17} {'depth of vortex below the wall level [cm]':>44}")
for v_c in [0.5, 1.0, 1.5, 2.0]:
    # core: z rises as v^2/(2g) (r/r_c)^2 up to r_c; outside: free vortex adds v_c^2/(2g) (1 - (r_c/r)^2)
    rise_core = v_c**2 / (2 * G)  # forced-vortex core: paraboloid rise
    rise_outer = v_c**2 / (2 * G) * (1 - (r_c / R_tank) ** 2)  # free-vortex region from r_c to the wall
    print(f"{v_c:>17} {(rise_core + rise_outer) * 100:>44.1f}")
print("\nSurface profile for a 1.5 m/s core:")
v_c = 1.5  # peak swirl velocity at the core edge [m/s]
for r in [0.0, 0.06, 0.12, 0.2, 0.3, 0.5]:
    if r <= r_c:
        z = v_c**2 / (2 * G) * (r / r_c) ** 2
    else:
        z = v_c**2 / (2 * G) * (2 - (r_c / r) ** 2)
    print(f"  r = {r:4.2f} m: surface {z * 100:5.1f} cm above the centre")
print("Total depth ~ v_c^2 / g: at 1.5 m/s the vortex is ~22 cm deep. Four wall baffles (1/10 of T")
print("wide) stop the swirl - which is why practically all process tanks are baffled (Week 14).")
