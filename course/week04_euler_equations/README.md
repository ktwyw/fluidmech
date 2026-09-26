# Week 4 - Differential analysis I: Euler equations for inviscid flow

**Syllabus:** Derivation and application of Euler's equations of motion for inviscid fluids.

**Course learning outcomes:** CLO 3, 4  |  **Assessment:** HW-2

**Reading:** White, Sections 4.1-4.3, 4.7-4.9 and Ch. 8.1-8.4 (potential flow).

## Learning objectives

- Test velocity fields for continuity; compute acceleration, vorticity and stream functions.
- Distinguish streamlines, pathlines and streaklines.
- Integrate the Euler equations for a pressure field and relate the result to Bernoulli.
- Build flows by superposition and explain d'Alembert's paradox and Kutta-Joukowski lift.

## Scripts

| Script | Content | Needs |
|---|---|---|
| [`w04_01_kinematics_with_sympy.py`](w04_01_kinematics_with_sympy.py) | Kinematics of a velocity field, done symbolically | sympy |
| [`w04_02_streamlines_pathlines.py`](w04_02_streamlines_pathlines.py) | Streamlines, pathlines and streaklines | matplotlib |
| [`w04_03_euler_pressure_field.py`](w04_03_euler_pressure_field.py) | Pressure field from the Euler equations | fluidmech only |
| [`w04_04_cylinder_potential_flow.py`](w04_04_cylinder_potential_flow.py) | Potential flow past a cylinder, d'Alembert's paradox and lift | matplotlib, numpy |
| [`w04_05_rankine_half_body.py`](w04_05_rankine_half_body.py) | The Rankine half-body (flow around a blunt nose) | fluidmech only |
| [`w04_06_vortices.py`](w04_06_vortices.py) | Free, forced and Rankine vortices | fluidmech only |
| [`w04_07_stream_function_flow_rate.py`](w04_07_stream_function_flow_rate.py) | The stream function measures flow rate | fluidmech only |
| [`w04_08_laplace_numerical_channel.py`](w04_08_laplace_numerical_channel.py) | Solving potential flow numerically (Laplace equation) | numpy, matplotlib |
| [`w04_09_curved_streamlines_elbow_meter.py`](w04_09_curved_streamlines_elbow_meter.py) | Pressure across curved streamlines - the elbow flow meter | fluidmech only |
| [`w04_10_euler_turbomachine_equation.py`](w04_10_euler_turbomachine_equation.py) | Euler's turbomachine equation - ideal head of a centrifugal pump | fluidmech only |
| [`w04_11_circulation_and_vorticity.py`](w04_11_circulation_and_vorticity.py) | Circulation, vorticity and Stokes' theorem | fluidmech only |
| [`w04_12_method_of_images.py`](w04_12_method_of_images.py) | A sink near a wall - the method of images | fluidmech only |
| [`w04_13_rankine_oval.py`](w04_13_rankine_oval.py) | The Rankine oval - a closed body from a source-sink pair | fluidmech only |
| [`w04_14_vortex_in_unbaffled_tank.py`](w04_14_vortex_in_unbaffled_tank.py) | The free-surface vortex in an unbaffled stirred tank | fluidmech only |
| [`w04_15_particle_impaction.py`](w04_15_particle_impaction.py) | Do particles follow the streamlines? Impaction in stagnation flow | fluidmech only |

Run a script from this folder, e.g. `python w04_01_kinematics_with_sympy.py`. Figures are saved as PNG files
in the current directory.

## Suggested student exercises

1. Use `w04_01` to check the fields in your homework problems.
2. Superpose a source and a sink (Rankine oval) and plot its streamlines.
3. Compute the surface pressure coefficient on a spinning cylinder and find where the stagnation points merge.
