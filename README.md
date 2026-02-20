# Jet Observable Library

[![Tests](https://github.com/atharva/jet-observables-lib/actions/workflows/tests.yml/badge.svg)](https://github.com/atharva/jet-observables-lib/actions/workflows/tests.yml)

Early-stage scientific Python library for jet-level observables in the **HEPSIM** context, inspired by the **Machine Learning for Science** project direction.

## Motivation

Jet analysis often starts as notebook-local functions, which makes reproducibility and validation hard.
This library provides a typed, testable core API built around a `Jet` object and explicit relativistic 4-vector handling.

## Core API

```python
import numpy as np
from jet_observables.jet import Jet
from jet_observables.observables.shapes import (
    jet_width,
    energy_correlation_e2,
    nsubjettiness_tau1,
)

particles = np.array([
    [40.0, 20.0, 5.0, 34.0],
    [25.0, 7.0, 4.0, 23.0],
])

jet = Jet(particles)

print(jet.pt())
print(jet.mass())
print(jet.eta())
print(jet.phi())
print(jet.delta_r(jet))
print(jet_width(jet))
print(energy_correlation_e2(jet))
print(nsubjettiness_tau1(jet))
```

## Implemented Observables (v0.2-dev)

- Kinematics: `pt`, `mass`, `eta`, `phi`, `delta_r`
- Shapes/Substructure: `jet_width`, `e2` (two-point energy correlation), `tau1` (basic one-axis N-subjettiness proxy)

## Design Notes

- 4-vector convention is `(E, px, py, pz)`.
- `FourVector` exposes `.mass()`, `.pt()`, `.eta()`, `.phi()`, `.dot(other)`.
- Pairwise observables use NumPy broadcasting to avoid Python nested loops.
- FastJet is not integrated yet; this package is designed so adapter layers can be added later.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Tests

```bash
PYTHONPATH=jet_observables pytest -q
```

## Validation Strategy

- Invariant mass validation: unit tests verify analytic rest-frame and scaling behaviors for 4-vectors.
- Massless particle checks: test vectors with `E^2 = |p|^2` are required to return near-zero invariant mass.
- Numerical stability handling: mass uses `sqrt(max(m^2, 0))` to avoid negative values from floating-point noise near zero.
- IRC safety metadata policy: each observable is annotated in `OBSERVABLES` with explicit IRC-safety tagging to make downstream analysis choices auditable.

## Performance Note

`e2` is implemented as an `O(N^2)` pairwise observable using NumPy broadcasting (no Python nested loops).

Suggested micro-benchmark reference points:
- `N=10`: effectively instantaneous on laptop CPU.
- `N=50`: still interactive for analysis workflows.
- `N=100`: cost grows quadratically as expected and becomes the dominant observable in a per-jet loop.

Planned optimization path:
- Keep vectorized NumPy kernel as baseline.
- Add optional JIT acceleration (for example with `numba`) for large-scale scans.

## Roadmap to ~30 Observables

- Extend substructure set: higher-point ECFs, angularities, grooming-sensitive observables
- Add plugin architecture for user-defined observables
- Add dataset adapters and batched evaluation APIs

### Version 0.2

- Grooming-oriented observables
- Observable plugin registry
- Better notebook-to-library pathways

### Version 0.3

- FastJet bindings/adapters
- Benchmarking against Monte Carlo pipelines
- Performance profiling and vectorized batch kernels
