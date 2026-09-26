"""CHME 202 - Week 12 - Example 11: constant-rate filtration - the pressure rises as the cake grows.

With a positive-displacement feed pump the filtrate rate Q is fixed, so
dp(t) = mu alpha c Q^2 t / A^2 + mu R_m Q / A rises linearly in time. When dp reaches the
pump's limit, operation switches to constant pressure (Examples 4 and 7).
"""

mu, A, c = 1e-3, 10.0, 30.0  # water, filter area [m2], kg solids per m3 filtrate
alpha, r_m = 5e11, 1e11  # specific cake resistance [m/kg], medium resistance [1/m]
Q = 1.5e-3  # m3/s filtrate
dp_max = 5e5
print(
    f"Filter {A} m2, filtrate rate {Q * 3600:.1f} m3/h, alpha = {alpha:.1e} m/kg, pump limit {dp_max / 1e5:.0f} bar\n"
)
print(f"{'t [min]':>8} {'V [m3]':>7} {'cake [kg]':>10} {'dp [bar]':>9}")
for t_min in range(0, 61, 5):  # table every 5 minutes
    t = t_min * 60  # min -> s
    dp = mu * alpha * c * Q**2 * t / A**2 + mu * r_m * Q / A
    if dp > dp_max:
        print(f"{t_min:>8}  (would need {dp / 1e5:.1f} bar - beyond the pump; constant-pressure phase from here)")
        break
    print(f"{t_min:>8} {Q * t:>7.2f} {c * Q * t:>10.0f} {dp / 1e5:>9.2f}")
t_lim = (dp_max - mu * r_m * Q / A) / (mu * alpha * c * Q**2 / A**2)
print(f"\nThe pressure limit is reached after {t_lim / 60:.0f} min ({Q * t_lim:.1f} m3 of filtrate); after that the")
print("filter runs at constant pressure and the rate falls. The initial pressure (clean cloth) is only")
print(f"{mu * r_m * Q / A / 1e5:.3f} bar - almost all resistance comes from the growing cake.")
