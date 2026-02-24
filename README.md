# JetObsMC

[![Tests](https://github.com/Atharva12081/JetObsMC/actions/workflows/tests.yml/badge.svg)](https://github.com/Atharva12081/JetObsMC/actions/workflows/tests.yml)

**JetObsMC** is a unified scientific Python library for jet observables in the **HEPSIM / ML4SCI** context.
The project is built for reproducible Monte Carlo validation workflows with one API, one metadata schema, and one testing strategy.

## Project Page (GitHub Pages)

- Main page: `docs/index.md`
- Observable catalog: `docs/observables.md`
- Expected URL (Pages source = `docs/`): `https://atharva12081.github.io/JetObsMC/`

## Current Delivery Status

- Pip-installable package via `setup.py`
- **30 observables** implemented across kinematic, shape, substructure, and groomed-proxy categories
- Metadata registry with IRC safety, category, dependencies, and complexity
- CI + pytest validation, including loop-based reference implementation checks
- Multiple notebooks for Monte Carlo validation workflows
- Canonical import path: `jetobsmc`

## Installation

Use standard (non-editable) installation:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install .
```

If your environment is offline or has restricted network access, use:

```bash
pip install . --no-build-isolation
```

Or install directly from GitHub:

```bash
pip install "git+https://github.com/Atharva12081/JetObsMC.git#egg=jetobsmc"
```

## Quick Verification

Run tests locally:

```bash
pytest -q
```

Run the HEPSIM evaluation notebook end-to-end:

```bash
jupyter nbconvert --to notebook --execute --inplace examples/hepsim_evaluation_submission.ipynb
```

Smoke-test the installed package:

```bash
python -c "import jetobsmc; print(jetobsmc.__version__)"
```

## Core API

```python
import numpy as np
from jetobsmc.jet import Jet
from jetobsmc.observables import (
    pt,
    mass,
    jet_width,
    nsubjettiness_tau21,
    energy_correlation_d2,
)

particles = np.array([
    [40.0, 20.0, 5.0, 34.0],
    [25.0, 7.0, 4.0, 23.0],
    [18.0, -5.0, 2.0, 16.0],
])

jet = Jet(particles)
features = {
    "pt": pt(jet),
    "mass": mass(jet),
    "width": jet_width(jet),
    "tau21": nsubjettiness_tau21(jet),
    "d2": energy_correlation_d2(jet),
}
```

## Observable Coverage (30 total)

### Kinematic (5)
- `pt`, `mass`, `eta`, `phi`, `delta_r`

### Shape (12)
- `multiplicity`, `constituent_pt_sum`, `leading_constituent_pt`, `leading_pt_fraction`
- `jet_width`, `girth`, `radial_moment_2`, `radial_moment_3`
- `lha`, `thrust_angularity`, `ptd_angularity`, `ptd` (`pt_dispersion`)

### Substructure (9)
- `tau1`, `tau2`, `tau3`, `tau21`, `tau32` (proxy N-subjettiness family)
- `e2`, `e3`, `c2`, `d2` (energy correlator family)

### Groomed proxies (4)
- `soft_drop_zg_proxy`, `soft_drop_rg_proxy`
- `soft_drop_pass_fraction_proxy`, `groomed_pair_mass_proxy`

Notes:
- Entries marked as proxy are intentionally lightweight baselines and are documented as such.
- Full definitions and references: `docs/observables.md`.

## Validation and Testing

Run tests:

```bash
pytest -q
```

What is validated:
- 4-vector correctness (Minkowski dot, invariant mass behaviors, symmetry)
- Edge-case robustness (empty jets, near-lightlike boosts, finite outputs)
- Zero-padding contract for HEPSIM-style constituent arrays
- **Reference implementation checks**: vectorized observables cross-checked against explicit loop-based baseline implementations

## Monte Carlo Validation Notebooks

- `examples/hepsim_evaluation_submission.ipynb`
- `examples/hepsim_evaluation_colab.ipynb`
- `examples/mc_validation_workflow.ipynb`
- `examples/evaluation_template.ipynb`
- `examples/benchmark_e2_scaling.ipynb`

## Open Source and Contributions

- JetObsMC is fully open source under the MIT License (`LICENSE`).
- Anyone can use, modify, and redistribute the code under the license terms.
- Community contributions are welcome through issues and pull requests.
- See `CONTRIBUTING.md` for contribution workflow details.

## Physics Assumptions

- 4-vector convention: `(E, px, py, pz)`
- HEPSIM-style conversion from `(pT, y, phi, pdgid)` currently assumes massless constituents
- `y` is used for reconstruction (`pz = pT*sinh(y)`, `E = pT*cosh(y)`)
- `eta` is computed from reconstructed momentum; for massless constituents `y ≈ eta`

## References

- [FastJet](https://fastjet.fr/)
- [EnergyFlow](https://energyflow.network/)
- [N-subjettiness (arXiv:1011.2268)](https://arxiv.org/abs/1011.2268)
- [Energy correlators (arXiv:1305.0007)](https://arxiv.org/abs/1305.0007)
- [Lund jet plane (arXiv:1807.04758)](https://arxiv.org/abs/1807.04758)
- [Soft Drop (arXiv:1402.2657)](https://arxiv.org/abs/1402.2657)
