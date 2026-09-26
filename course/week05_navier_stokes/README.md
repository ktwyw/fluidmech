# Week 5 - Differential analysis II: Navier-Stokes equations

**Syllabus:** Derivation and application of Navier-Stokes equations of motion for viscous fluids.

**Course learning outcomes:** CLO 3, 4  |  **Assessment:** HW-3

**Reading:** White, Sections 4.3-4.6 and 4.10-4.11.

## Learning objectives

- Reduce the Navier-Stokes equations for fully developed and unsteady unidirectional flows.
- Solve the resulting ODEs/PDEs analytically and with a simple finite-difference scheme.
- Use order-of-magnitude analysis and the Reynolds number to decide which terms matter.
- Explain viscous diffusion time scales and Stokes layers.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w05_01_solving_ns_with_sympy.py`](w05_01_solving_ns_with_sympy.py) | Reducing and solving the Navier-Stokes equations symbolically | sympy |
| [`w05_02_stokes_first_problem_fd.py`](w05_02_stokes_first_problem_fd.py) | Impulsively started plate (Stokes' first problem) by finite differences | fluidmech only |
| [`w05_03_startup_channel_flow.py`](w05_03_startup_channel_flow.py) | Start-up of pressure-driven flow between plates | matplotlib |
| [`w05_04_which_terms_matter.py`](w05_04_which_terms_matter.py) | Order-of-magnitude analysis of the Navier-Stokes equations | fluidmech only |
| [`w05_05_oscillating_plate.py`](w05_05_oscillating_plate.py) | Oscillating flows and the Stokes layer (Stokes' second problem) | fluidmech only |
| [`w05_06_viscous_dissipation.py`](w05_06_viscous_dissipation.py) | Viscous dissipation - friction turns flow work into heat | fluidmech only |
| [`w05_07_creeping_flow_stokes_drag.py`](w05_07_creeping_flow_stokes_drag.py) | Creeping flow around a sphere (Stokes 1851) | fluidmech only |
| [`w05_08_lubrication_slider_bearing.py`](w05_08_lubrication_slider_bearing.py) | Lubrication theory - how a thin wedge of oil carries a load | fluidmech only |
| [`w05_09_cubic_law_thin_gaps.py`](w05_09_cubic_law_thin_gaps.py) | The cubic law - leakage through thin gaps and fractures | fluidmech only |
| [`w05_10_finite_difference_accuracy.py`](w05_10_finite_difference_accuracy.py) | How accurate is a finite-difference solution? Grid convergence | fluidmech only |
| [`w05_11_radial_flow_between_discs.py`](w05_11_radial_flow_between_discs.py) | Radial flow between parallel discs | fluidmech only |
| [`w05_12_squeeze_film.py`](w05_12_squeeze_film.py) | Squeeze films - why it takes time to squeeze liquid out of a gap | fluidmech only |
| [`w05_13_capillary_filling_washburn.py`](w05_13_capillary_filling_washburn.py) | Capillary filling (Washburn equation) | fluidmech only |
| [`w05_14_vortex_decay_lamb_oseen.py`](w05_14_vortex_decay_lamb_oseen.py) | Viscous decay of a vortex (Lamb-Oseen, an exact N-S solution) | fluidmech only |
| [`w05_15_implicit_time_stepping.py`](w05_15_implicit_time_stepping.py) | Explicit versus implicit (Crank-Nicolson) time stepping | fluidmech only |

Run a script from this folder, e.g. `python w05_01_solving_ns_with_sympy.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Change the Fourier number in `w05_02` and find the exact stability limit experimentally.
2. Adapt `w05_03` to the start-up of Couette flow and compare with the series solution.
3. Use SymPy to derive the velocity profile for flow down an inclined plane.
