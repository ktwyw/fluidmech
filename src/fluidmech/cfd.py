"""Small computational-fluid-dynamics solvers for teaching (optional; requires numpy, scipy).

* :func:`lid_driven_cavity` - 2D incompressible Navier-Stokes in a square cavity
  (stream function-vorticity formulation), the classic CFD benchmark of Ghia et al. (1982).
* :func:`lbm_cylinder` - lattice-Boltzmann (D2Q9, BGK) flow past a cylinder, which sheds
  a von Karman vortex street; yields vorticity snapshots for animation.
* :func:`taylor_dispersion` - Monte Carlo random walk of tracer particles in laminar pipe
  flow, reproducing Taylor's effective dispersion D_eff = D (1 + Pe^2 / 48).

The codes are deliberately compact and readable rather than fast.
"""

from __future__ import annotations

from collections.abc import Iterator


def _np():
    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover
        raise ImportError("fluidmech.cfd needs numpy (and scipy for the cavity solver)") from exc
    return np


# ---------------------------------------------------------------------------- #
# Lid-driven cavity
# ---------------------------------------------------------------------------- #
def lid_driven_cavity(n: int = 65, reynolds: float = 100.0, t_end: float = 30.0, tol: float = 1e-5) -> dict:
    """Steady flow in a unit square cavity whose lid moves at U = 1 (all quantities dimensionless).

    Equations: vorticity transport  w_t + u w_x + v w_y = (1/Re) lap(w)  and  lap(psi) = -w,
    with u = psi_y, v = -psi_x. Central differences on an n x n grid, explicit time stepping to
    steady state, and a direct sparse solve for psi. Wall vorticity from Thom's formula.

    Returns x, y (1D), psi, w, u, v (2D arrays indexed [j (y), i (x)]), and 'steps'.
    """
    np = _np()
    from scipy.sparse import diags, identity, kron
    from scipy.sparse.linalg import splu

    h = 1.0 / (n - 1)
    x = np.linspace(0, 1, n)
    m = n - 2  # interior nodes per direction
    # Sparse 2D Laplacian for the interior (psi = 0 on all walls) - factorised once, reused every step
    d2 = diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(m, m)) / h**2
    lap = (kron(identity(m), d2) + kron(d2, identity(m))).tocsc()
    solver = splu(lap)

    psi = np.zeros((n, n))
    w = np.zeros((n, n))
    dt = 0.2 * min(h * h * reynolds / 4, h)  # well inside the diffusive and convective (CFL) limits
    steps = int(t_end / dt)
    for step in range(1, steps + 1):
        # 1) stream function from the current vorticity
        psi[1:-1, 1:-1] = solver.solve(-w[1:-1, 1:-1].ravel()).reshape(m, m)
        # 2) wall vorticity (Thom): w_wall = -2 psi_adjacent / h^2, plus the lid term on the top wall
        w[0, :] = -2 * psi[1, :] / h**2  # bottom
        w[-1, :] = -2 * psi[-2, :] / h**2 - 2 / h  # top (lid moving at u = 1)
        w[:, 0] = -2 * psi[:, 1] / h**2  # left
        w[:, -1] = -2 * psi[:, -2] / h**2  # right
        # 3) velocities and one explicit step of the vorticity transport equation
        u = (psi[2:, 1:-1] - psi[:-2, 1:-1]) / (2 * h)  # d psi / dy
        v = -(psi[1:-1, 2:] - psi[1:-1, :-2]) / (2 * h)  # -d psi / dx
        wx = (w[1:-1, 2:] - w[1:-1, :-2]) / (2 * h)
        wy = (w[2:, 1:-1] - w[:-2, 1:-1]) / (2 * h)
        lap_w = (w[1:-1, 2:] + w[1:-1, :-2] + w[2:, 1:-1] + w[:-2, 1:-1] - 4 * w[1:-1, 1:-1]) / h**2
        dw = dt * (-u * wx - v * wy + lap_w / reynolds)
        w[1:-1, 1:-1] += dw
        if step > 100 and np.max(np.abs(dw)) / dt < tol:  # steady state reached
            break
    u_full = np.zeros((n, n))
    v_full = np.zeros((n, n))
    u_full[1:-1, 1:-1] = (psi[2:, 1:-1] - psi[:-2, 1:-1]) / (2 * h)
    v_full[1:-1, 1:-1] = -(psi[1:-1, 2:] - psi[1:-1, :-2]) / (2 * h)
    u_full[-1, :] = 1.0  # the lid
    return {"x": x, "y": x.copy(), "psi": psi, "w": w, "u": u_full, "v": v_full, "steps": step}


# Ghia, Ghia & Shin (1982), Re = 100: u along the vertical centreline (x = 0.5)
GHIA_RE100_Y = [
    0.0,
    0.0547,
    0.0625,
    0.0703,
    0.1016,
    0.1719,
    0.2813,
    0.4531,
    0.5,
    0.6172,
    0.7344,
    0.8516,
    0.9531,
    0.9609,
    0.9688,
    0.9766,
    1.0,
]
GHIA_RE100_U = [
    0.0,
    -0.03717,
    -0.04192,
    -0.04775,
    -0.06434,
    -0.10150,
    -0.15662,
    -0.21090,
    -0.20581,
    -0.13641,
    0.00332,
    0.23151,
    0.68717,
    0.73722,
    0.78871,
    0.84123,
    1.0,
]


# ---------------------------------------------------------------------------- #
# Lattice Boltzmann: flow past a cylinder
# ---------------------------------------------------------------------------- #
def lbm_cylinder(
    nx: int = 300,
    ny: int = 100,
    radius: int = 10,
    u_in: float = 0.06,
    reynolds: float = 100.0,
    steps: int = 25000,
    snapshot_every: int = 200,
    probe_offset: float = 3.0,
) -> Iterator[dict]:
    """D2Q9 BGK lattice-Boltzmann simulation of flow past a circular cylinder (lattice units).

    Yields a dict every ``snapshot_every`` steps with 'step', 'vorticity' (ny x nx), 'u', 'v',
    and the transverse velocity 'probe_v' history at a point ``probe_offset`` diameters behind the
    cylinder (used to measure the shedding frequency). Inflow: equilibrium at u_in on the left;
    outflow: zero-gradient on the right; top and bottom periodic; bounce-back on the cylinder.
    """
    np = _np()
    # D2Q9 lattice: velocity vectors c_k and weights w_k
    c = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]])
    wts = np.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4)
    opposite = [0, 3, 4, 1, 2, 7, 8, 5, 6]
    nu = u_in * 2 * radius / reynolds  # lattice viscosity from Re = U D / nu
    tau = 3 * nu + 0.5  # BGK relaxation time
    cx, cy = nx // 4, ny // 2
    yy, xx = np.mgrid[0:ny, 0:nx]
    solid = (xx - cx) ** 2 + (yy - cy) ** 2 <= radius**2

    def equilibrium(rho, ux, uy):
        cu = 3 * (c[:, 0, None, None] * ux + c[:, 1, None, None] * uy)
        usq = 1.5 * (ux**2 + uy**2)
        return wts[:, None, None] * rho * (1 + cu + 0.5 * cu**2 - usq)

    # start from uniform flow with a small transverse perturbation to trigger shedding sooner
    ux = u_in * (1 + 1e-4 * np.sin(2 * np.pi * yy / ny))
    uy = np.zeros((ny, nx))
    uy[:, : cx + radius] += 0.01 * u_in * np.sin(np.pi * yy[:, : cx + radius] / ny)
    f = equilibrium(np.ones((ny, nx)), ux, uy)
    probe = (cy, int(cx + probe_offset * 2 * radius))
    probe_hist = []
    for step in range(1, steps + 1):
        rho = f.sum(axis=0)
        ux = (f * c[:, 0, None, None]).sum(axis=0) / rho
        uy = (f * c[:, 1, None, None]).sum(axis=0) / rho
        ux[:, 0], uy[:, 0], rho[:, 0] = u_in, 0.0, 1.0  # inflow boundary (equilibrium)
        ux[solid], uy[solid] = 0.0, 0.0
        feq = equilibrium(rho, ux, uy)
        f_post = f - (f - feq) / tau  # BGK collision
        f_post[:, solid] = f[opposite][:, solid]  # bounce-back inside the cylinder (no-slip wall)
        f_post[:, :, 0] = feq[:, :, 0]
        for k in range(9):  # streaming: move each population one cell along c_k
            f[k] = np.roll(np.roll(f_post[k], c[k, 0], axis=1), c[k, 1], axis=0)
        f[:, :, -1] = f[:, :, -2]  # zero-gradient outflow
        probe_hist.append(float(uy[probe]))
        if snapshot_every and step % snapshot_every == 0:
            dv_dx = (np.roll(uy, -1, axis=1) - np.roll(uy, 1, axis=1)) / 2  # central differences, lattice units
            du_dy = (np.roll(ux, -1, axis=0) - np.roll(ux, 1, axis=0)) / 2
            vort = dv_dx - du_dy
            vort[solid] = np.nan
            yield {
                "step": step,
                "vorticity": vort,
                "u": ux.copy(),
                "v": uy.copy(),
                "probe_v": list(probe_hist),
                "solid": solid,
                "tau": tau,
                "diameter": 2 * radius,
                "u_in": u_in,
            }


def strouhal_from_signal(signal: list[float], diameter: float, u_in: float, discard: float = 0.5) -> float:
    """Shedding Strouhal number St = f D / U from a probe signal (one sample per time step).

    Counts upward zero crossings of the (mean-removed) second half of the record.
    """
    np = _np()
    s = np.asarray(signal[int(len(signal) * discard) :])
    s = s - s.mean()
    ups = np.where((s[:-1] < 0) & (s[1:] >= 0))[0]
    if len(ups) < 3:
        raise ValueError("Not enough shedding cycles in the signal; run longer.")
    period = (ups[-1] - ups[0]) / (len(ups) - 1)
    return diameter / period / u_in


# ---------------------------------------------------------------------------- #
# Taylor dispersion (Monte Carlo)
# ---------------------------------------------------------------------------- #
def taylor_dispersion(
    peclet: float = 20.0,
    particles: int = 4000,
    t_end: float = 6.0,
    dt: float = 1e-3,
    snapshot_times=(0.05, 0.3, 1.0, 3.0, 6.0),
    seed: int = 1,
) -> dict:
    """Tracer particles in Poiseuille flow u = 2 U (1 - r^2) with molecular diffusion (dimensionless).

    Lengths are scaled by the tube radius a, time by a^2 / D, so the mean velocity equals the
    Peclet number Pe = U a / D. Each step particles are advected axially and take a random
    Brownian step in the cross-section (reflected at the wall). Returns times, the axial
    variance of the cloud, the theoretical Taylor-Aris coefficient 1 + Pe^2/48 and snapshots.
    """
    np = _np()
    rng = np.random.default_rng(seed)
    # start uniformly over the cross-section at x = 0
    r0 = np.sqrt(rng.random(particles))
    th = 2 * np.pi * rng.random(particles)
    y, z = r0 * np.cos(th), r0 * np.sin(th)
    x = np.zeros(particles)
    step_sd = np.sqrt(2 * dt)  # Brownian step with D = 1
    times, variances, snaps = [], [], []
    snap_steps = {int(round(t / dt)): t for t in snapshot_times}
    n_steps = int(round(t_end / dt))
    for k in range(1, n_steps + 1):
        r2 = y * y + z * z
        x += 2 * peclet * (1 - r2) * dt + step_sd * rng.standard_normal(particles)  # advection + axial diffusion
        y += step_sd * rng.standard_normal(particles)
        z += step_sd * rng.standard_normal(particles)
        r = np.sqrt(y * y + z * z)
        out = r > 1
        scale = np.where(out, (2 - r) / np.maximum(r, 1e-12), 1.0)  # reflect back inside the wall
        y *= scale
        z *= scale
        if k % 10 == 0:
            times.append(k * dt)
            variances.append(float(np.var(x)))
        if k in snap_steps:
            snaps.append((snap_steps[k], x.copy(), y.copy()))
    return {
        "time": np.array(times),
        "variance": np.array(variances),
        "theory_K": 1 + peclet**2 / 48,
        "peclet": peclet,
        "snapshots": snaps,
    }
