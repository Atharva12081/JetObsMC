# Jet Observable Library

[![Tests](https://github.com/Atharva12081/jet-observables-lib/actions/workflows/tests.yml/badge.svg)](https://github.com/Atharva12081/jet-observables-lib/actions/workflows/tests.yml)

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
    pt_dispersion,
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
print(pt_dispersion(jet))
```

## Implemented Observables (v0.2-dev)

- Kinematics: `pt`, `mass`, `eta`, `phi`, `delta_r`
- Shapes/Substructure: `jet_width`, `e2` (two-point energy correlation), `tau1` (basic one-axis N-subjettiness proxy), `pTD` (pT dispersion)

## Safety and Delivery Baseline

- Stable core abstractions: `FourVector` + `Jet`
- Focused observable set (not over-expanded) with scientific metadata
- CI-backed quality gate and reproducible local test workflow
- 15+ tests for correctness, symmetry, edge cases, and numerical sanity

## Design Notes

- 4-vector convention is `(E, px, py, pz)`.
- `FourVector` exposes `.mass()`, `.pt()`, `.eta()`, `.phi()`, `.dot(other)`.
- Pairwise observables use NumPy broadcasting to avoid Python nested loops.
- FastJet is not integrated yet; this package is designed so adapter layers can be added later.
- Extension stub available via `Observable` base interface for future plugin-style scaling.

## Evaluation Readiness (HEPSIM Task)

- Canonical zero-padding contract for dataset rows `(pT, y, phi, pdgid)` is implemented in `canonical_constituent_mask` and reused by conversion/multiplicity/leading-pT helpers.
- `Jet.from_ptyphipdg(...)` converts padded HEPSIM-style inputs into clean constituent 4-vectors before observable computation.
- Rest-frame boosting utilities include stability guards near `beta^2 -> 1` and a residual check: `rest_frame_momentum_residual`.
- `pTD` is implemented to match the required evaluation observable set.
- Clean grading notebook scaffold is provided at `/Users/atharva/Documents/Code/ML4SCI/jet-observables-lib/examples/evaluation_template.ipynb`, including a lab-vs-rest AUC comparison table stub.

## Physics Assumptions

- Constituent input conversion from `(pT, y, phi, pdgid)` currently assumes massless constituents.
- Dataset `y` is treated as rapidity for 4-vector reconstruction (`pz = pT*sinh(y)`, `E = pT*cosh(y)`).
- `eta` used in angular observables is derived from reconstructed momentum and is approximately equal to `y` in the massless/high-energy limit.

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

Benchmark notebook:
- `/Users/atharva/Documents/Code/ML4SCI/jet-observables-lib/examples/benchmark_e2_scaling.ipynb`
- Includes empirical timing study for `N=10, 50, 100` and higher.

## Roadmap to GSoC

This prototype serves as a foundational implementation aligned with the HEPSIM Jet Observable Library project under Machine Learning for Science. Planned expansions include grooming observables, plugin architecture, and Monte Carlo validation workflows.

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
