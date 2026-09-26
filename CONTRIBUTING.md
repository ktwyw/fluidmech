# Contributing

Contributions are welcome — bug reports, new correlations, worked examples, or better explanations.

## Development setup

```bash
git clone https://github.com/ktwyw/fluidmech.git
cd fluidmech
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev,examples,course,showcase,apps]"
pre-commit install               # optional: lint automatically on every commit
```

## Before opening a pull request

```bash
ruff check . && ruff format .    # lint and format
pytest                           # unit tests, doctests and all examples
python docs/validate.py          # validation against reference data
```

## Guidelines

- **Units:** SI everywhere; state the units of every argument and return value in the docstring.
- **Sources:** cite the origin of any correlation (textbook, paper or standard) in the module
  docstring and add it to `docs/THEORY.md`.
- **Tests:** add a test for every new function, ideally checked against a textbook value or an
  independent analytical result. If a published reference value exists, add it to `docs/validate.py`.
- **No dependencies:** keep the core package pure Python; examples and notebooks may use numpy/matplotlib.
- **Examples:** new example scripts are numbered `NN_short_name.py`, print their results, and are
  listed in `examples/README.md`. They run automatically in CI.

## Showcase scripts

Advanced, animation and figure scripts must honour `FLUIDMECH_QUICK=1` (a fast, coarse run)
so that the test suite can run them on every push; long simulations belong behind that switch.

## Regenerating documentation assets

```bash
python docs/make_figures.py      # README gallery images
python docs/validate.py          # docs/VALIDATION.md
```
