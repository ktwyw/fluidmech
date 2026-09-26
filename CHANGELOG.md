# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.5.0] - 2026-09-26

### Added
- `showcase/`: six advanced topics (lid-driven cavity CFD, lattice-Boltzmann vortex shedding,
  Blasius boundary layer, method-of-characteristics water hammer, Rayleigh-Plesset cavitation,
  Taylor dispersion), five GIF animations, four publication-quality multi-panel figures, the
  FluidMech Studio Streamlit web app (six calculators) and two matplotlib slider explorers.
- `viz` (optional, matplotlib): paper/slides/poster styles, Okabe-Ito palette, `savefig` to several
  formats, Moody, pump/system and drag charts, panel labels.
- `cfd` (optional, numpy/scipy): `lid_driven_cavity`, `lbm_cylinder`, `strouhal_from_signal`,
  `taylor_dispersion`, and the Ghia et al. (1982) reference data.
- `cavitation`: Rayleigh-Plesset integration and Rayleigh's collapse time.
- `transients.moc_valve_closure` and `laminar.blasius`.
- Nine new validation checks (64 in total); tests for all new code, including a headless
  Streamlit AppTest; package extras `showcase`, `apps` and `all`.

### Fixed
- Removed 26 stray figure files that earlier checks had left in the repository root.

## [0.4.3] - 2026-09-25

### Changed
- Code-commenting pass over the library, examples and course scripts (about 800 new comments):
  units on every input value, every unit conversion explained (e.g. m3/h -> m3/s), the origin of
  empirical constants cited next to them, and step-by-step notes on the numerical methods
  (Gaussian elimination, Newton network iteration, Colebrook fixed point, direct step, finite
  differences, Crank-Nicolson, Runge-Kutta).
- Module docstrings for every test file stating what is verified and against which reference.
- Readability fixes: `math.pi` instead of truncated literals, a dead assignment removed, repeated
  literals replaced by named variables, and the life-cycle-cost payback now derived from the
  candidate table instead of duplicated numbers.

## [0.4.2] - 2026-09-25

### Added
- 60 further CHME 202 lecture examples (15 per teaching week), including process-gas properties,
  mixture viscosity, shear rates in equipment, membrane bubble point; chimney draft, level
  measurement, decanter jacklegs, hinged gates, rotating U-tubes; rotameters, U-tube oscillation,
  aspirators, spherical-tank draining; circulation, method of images, Rankine ovals, surface
  vortices, particle impaction; radial and squeeze flows, Washburn wicking, Lamb-Oseen decay,
  Crank-Nicolson; slit dies, cone-and-plate rheometry, capillary draining, piston leakage,
  viscosity from velocity profiles; roughness from test data, Swamee-Jain design formulas,
  insertion meters, duct/fan budgets, Reynolds decomposition; pump test rigs, dosing pumps,
  branched filling, pump start-up, life-cycle cost; sedimentation analysis, elutriation,
  extraction-column flooding, aerosols, pneumatic conveying; constant-rate filtration, sand
  filters, concentration polarisation, dam seepage (Laplace), cake washing; weir calibration,
  Reynolds independence, sloshing, bubble size, drain-time scaling; circulation time,
  shear-sensitive mixing, CSTR ideality, RTD from tracer data, segregation and reaction order.

### Fixed
- Audit of all examples: corrected five inaccurate printed claims (friction-formula accuracy,
  Christiansen factor, Pitot compressibility error, Stokes-law validity range) and removed
  negative-zero displays; example 29 now uses the library drag correlation.

## [0.4.1] - 2026-09-25

### Added
- 49 further CHME 202 lecture examples, so that every teaching week (1-6, 9-14) now has 10:
  compressibility, vapour pressure, viscosity units, Newton's law in devices; gauges, hydraulic press,
  tank-shell loads; energy equation with pumps, spray nozzles, Venturi cavitation, diffusers, sluice gates;
  stream function, numerical Laplace solution, elbow meter, Euler turbomachine equation; viscous
  dissipation, Stokes drag, lubrication, the cubic law, grid convergence; Taylor-Couette flow, two-layer
  flow, wire coating, parallel capillaries; valve Kv/Cv sizing, flow regime from data, gas pipelines;
  Hardy Cross by hand, operating-point drift; friction vs. pressure drag, centrifuges and cyclones,
  approach to terminal velocity, settling chambers, bubble-column holdup; Sauter mean diameter,
  filter-cycle optimisation, compressible cakes, well drawdown, filter backwashing; repeating variables
  with SymPy, drag-data collapse, non-dimensional Navier-Stokes, Hinze drop size, correlation fitting;
  solids suspension, oxygen transfer, static mixers and agitator heat load.

## [0.4.0] - 2026-09-25

### Added
- `course/`: weekly Python teaching materials for CHME 202 Fluid Mechanics - 77 scripts covering every
  teaching week, Python versions of Lab Assignments 1-3, midterm and final review problems with
  solutions, an integrated design problem and a pump-selection bridge project; per-week READMEs with
  learning objectives, CLO mapping, readings and student exercises; `course/run_all.py`.
- `rheology`: Newtonian, power-law, Bingham, Herschel-Bulkley and Carreau models, data fitting, Andrade fits.
- `laminar`: exact Navier-Stokes solutions (plates, pipes, annuli, films, power-law and Bingham fluids,
  Stokes' problems) and laminar f*Re for rectangular ducts and annuli.
- `potential_flow`: 2D elementary flows and superposition.
- `turbulence`: law of the wall (Spalding), y+ and first-cell height, entrance length, Kolmogorov scales.
- `porous`: Darcy's law, Kozeny-Carman, Burke-Plummer, Ergun, fluidisation, cake filtration, membranes.
- `dimensional`: automatic Buckingham Pi groups.
- `mixing`: impeller power, blend time, micromixing, scale-up, residence-time distributions and conversions.
- `hydrostatics`: rigid-body acceleration and rotation, curved-surface forces.
- `drag`: drops and bubbles (Hadamard-Rybczynski, Mendelson), Eotvos and Morton numbers,
  Richardson-Zaki hindered settling, vortex shedding.
- `properties`: International Standard Atmosphere.
- 13 new validation checks (55 in total); smoke tests now run every course script.

## [0.3.0] - 2026-09-25

### Added
- `networks`: steady-state pipe-network solver (Newton / global gradient algorithm) with
  reservoirs, junctions, pipes and pumps.
- `pumps`: pump-curve fitting, affinity laws, series/parallel combination, operating point,
  NPSH available and specific speed.
- `compressible`: isentropic relations, normal shocks, Rayleigh-Pitot formula, choked and
  subsonic nozzle flow.
- `drag`: sphere and cylinder drag, flat-plate skin friction, boundary-layer thickness,
  terminal settling velocity.
- `transients`: water-hammer wave speed and surge pressures.
- `units`: conversion between SI and US customary units.
- `open_channel`: gradually varied flow profiles (direct step), profile classification,
  weirs, sluice gates and jump energy loss.
- `properties`: water vapour pressure and surface tension.
- `solvers`: linear-system solver and polynomial least-squares fit.
- Command-line calculator (`fluidmech pipe | channel | props | convert`).
- 18 new examples (33-50), four executed Jupyter tutorials, a README gallery,
  `docs/THEORY.md`, and `docs/VALIDATION.md` with 42 checks against reference data.
- CI on Linux, Windows and macOS; notebook execution; PyPI publishing workflow;
  issue templates, pre-commit configuration and `CITATION.cff`.

## [0.2.0] - 2026-09-25

### Added
- 28 new worked examples (05-32) covering properties, hydrostatics, Bernoulli and momentum,
  pipe flow (pumps, networks, water hammer, grade lines), open channels and external flow.
- `examples/README.md` index and `examples/run_all.py` runner.
- Public `solvers` module exposing `bisect` and `positive_root`.
- Smoke test that runs every example in CI.

## [0.1.0] - 2026-09-25

### Added
- `properties`: water and air property correlations and the `Fluid` class.
- `dimensionless`: Reynolds, Froude, Mach, Weber and Euler numbers.
- `hydrostatics`: pressure at depth, manometers, forces on plane gates, buoyancy.
- `bernoulli`: total head, Torricelli, Pitot tube, Venturi, orifice, tank draining.
- `pipe_flow`: Colebrook, Swamee-Jain and Haaland friction factors; Type 1, 2 and 3 pipe problems.
- `open_channel`: Manning's equation, normal and critical depth, Froude number, hydraulic jump.
- Test suite, worked examples and GitHub Actions CI.
