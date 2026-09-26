# CHME 202 Fluid Mechanics - weekly Python materials

**Author:** Yanwei Wang ([GitHub @ktwyw](https://github.com/ktwyw),
[ORCID 0000-0002-8488-9833](https://orcid.org/0000-0002-8488-9833)).

Python scripts that follow the weekly lecture plan of **CHME 202 Fluid Mechanics** (Spring 2026
syllabus). Every teaching week has **15 worked
lecture examples**; Weeks 3, 9 and 11 add Python versions of the three lab assignments, and Weeks 7 and 15
provide review problems with computed solutions.
The scripts use the `fluidmech` library in this repository and complement the COMSOL, Mathematica and
Excel resources listed in the syllabus.

| Week | Topic | CLOs | Assessment | Lecture examples | Labs |
|:-:|---|:-:|---|:-:|:-:|
| 1 | [Introduction to fluids and fluid properties](week01_fluid_properties/) | 1, 2 |  | 15 |  |
| 2 | [Fluid statics](week02_fluid_statics/) | 1, 2, 4 | HW-1 | 15 |  |
| 3 | [Elementary fluid dynamics: the Bernoulli equation](week03_bernoulli/) | 1, 2, 3, 4 | Lab Assignment #1 | 15 | 1 |
| 4 | [Differential analysis I: Euler equations for inviscid flow](week04_euler_equations/) | 3, 4 | HW-2 | 15 |  |
| 5 | [Differential analysis II: Navier-Stokes equations](week05_navier_stokes/) | 3, 4 | HW-3 | 15 |  |
| 6 | [Exact solutions: plates, Couette flow, tubes and annuli](week06_exact_viscous_solutions/) | 2, 3, 4 | HW-4 | 15 |  |
| 7 | [Midterm review](week07_midterm_review/) | 1, 2, 3, 4 |  | 1 |  |
| 9 | [Viscous flow and pipe systems I: turbulence and head losses](week09_turbulence_head_losses/) | 2, 3, 4, 5 | Lab Assignment #2 | 15 | 1 |
| 10 | [Viscous flow and pipe systems II: multiple pipes and pumps](week10_pipe_systems_pumps/) | 2, 3, 4, 5 | HW-5 | 15 |  |
| 11 | [Flow over immersed bodies](week11_immersed_bodies/) | 2, 3, 4, 5 | Lab Assignment #3 | 15 | 1 |
| 12 | [Flow through porous media](week12_porous_media/) | 2, 3, 4, 5 | HW-6 | 15 |  |
| 13 | [Dimensional analysis and similarity](week13_dimensional_analysis/) | 1, 2, 3, 4, 5 | HW-7 | 15 |  |
| 14 | [Fluid mechanics in ChemE unit operations: mixing](week14_mixing_unit_operations/) | 2, 3, 4, 5 |  | 15 |  |
| 15 | [Course recap](week15_course_recap/) | 1, 2, 3, 4, 5 |  | 2 |  |

Week 8 is the spring break. **186 scripts in total.**

## Getting started

```bash
pip install -e ".[course]"      # fluidmech + numpy, matplotlib, sympy
cd course/week06_exact_viscous_solutions
python w06_04_annulus_double_pipe.py
python ../run_all.py          # run every course script (figures -> course/output/)
```

## How the scripts are written

- Every script starts with a docstring stating the week, the learning goal and the reading in White (7th ed.)
  or the recommended texts, and prints its results with a short interpretation.
- Scripts are short and self-contained so they can be shown in lectures and modified by students.
- Data labelled *illustrative* are invented but physically consistent; replace them with your own lab data.
- Scripts marked `# requires: ...` need the named package (all included in the `course` extra).
- The midterm (Week 7) and recap (Week 15) scripts print problems; add `--solutions` for the answers.

## Link to industry: pump selection (Grundfos alignment)

Week 10 includes `w10_08_grundfos_bridge_project.py`, which implements the joint exercise proposed in the
CHME 202 / Grundfos alignment statement: system head across an operating range, comparison with a pump
curve, fixed-speed versus variable-speed energy use, an NPSH check, and a list of assumptions and checks
requiring supervision. Scripts `w10_06` (closed-loop circulator) and `w10_07` (submersible well pump)
cover the other pump families discussed in that statement. All pump curves in this course are
**illustrative**, not manufacturer data.

## Mapping to course learning outcomes

1. Apply static and fluid-system principles - Weeks 1-3
2. Dimensional analysis and similarity for scaling and equipment selection - Weeks 1, 13, 14 (and throughout)
3. Solve basic fluid-flow problems - Weeks 3-6, 9, 11, 12
4. Flow rate, pressure drop and pump characteristics for tank/pipe/pump/fitting systems - Weeks 9-10, 15
5. Effect of flow on mixing processes and chemical reactions - Weeks 12, 14
