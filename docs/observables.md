---
layout: default
title: Observable Catalog
---

## Observable Catalog (v0.3)

This catalog lists the implemented observables grouped by category, with metadata-facing naming and complexity.
Function entry points are exported from `jetobsmc.observables`.

### Usage example

```python
from jetobsmc.jet import Jet
from jetobsmc.observables import (
    pt,
    mass,
    jet_width,
    nsubjettiness_tau21,
    energy_correlation_d2,
)

jet = Jet(particles_e_px_py_pz)
features = {
    "pt": pt(jet),
    "mass": mass(jet),
    "width": jet_width(jet),
    "tau21": nsubjettiness_tau21(jet),
    "d2": energy_correlation_d2(jet),
}
```

## Kinematic observables

| Name | Function | IRC safe | Complexity | Definition |
|---|---|---:|---|---|
| `pt` | `pt(jet)` | Yes | `O(1)` | Jet transverse momentum |
| `mass` | `mass(jet)` | Yes | `O(1)` | Jet invariant mass |
| `eta` | `eta(jet)` | Yes | `O(1)` | Jet pseudorapidity |
| `phi` | `phi(jet)` | Yes | `O(1)` | Jet azimuth |
| `delta_r` | `delta_r(jet_a, jet_b)` | Yes | `O(1)` | Angular distance in `(eta, phi)` |

## Shape observables

| Name | Function | IRC safe | Complexity | Definition |
|---|---|---:|---|---|
| `multiplicity` | `multiplicity(jet)` | No | `O(1)` | Number of constituents |
| `constituent_pt_sum` | `constituent_pt_sum(jet)` | Yes | `O(N)` | Scalar sum of constituent `pT` |
| `leading_constituent_pt` | `leading_constituent_pt(jet)` | No | `O(N)` | Hardest constituent `pT` |
| `leading_pt_fraction` | `leading_pt_fraction(jet)` | No | `O(N)` | `pT_lead / sum_i pT_i` |
| `jet_width` | `jet_width(jet)` | Yes | `O(N)` | `sum_i pT_i DeltaR_i / sum_i pT_i` |
| `girth` | `girth(jet)` | Yes | `O(N)` | Alias of width |
| `radial_moment_2` | `radial_moment_2(jet)` | Yes | `O(N)` | `sum_i pT_i DeltaR_i^2 / sum_i pT_i` |
| `radial_moment_3` | `radial_moment_3(jet)` | Yes | `O(N)` | `sum_i pT_i DeltaR_i^3 / sum_i pT_i` |
| `lha` | `lha(jet)` | Yes | `O(N)` | Les Houches angularity `lambda^1_{0.5}` |
| `thrust_angularity` | `thrust_angularity(jet)` | Yes | `O(N)` | Generalized angularity `lambda^1_2` |
| `ptd_angularity` | `ptd_angularity(jet)` | No | `O(N)` | Generalized angularity `lambda^2_0` |
| `ptd` | `pt_dispersion(jet)` | No | `O(N)` | `sqrt(sum_i pT_i^2) / sum_i pT_i` |

## Substructure observables

| Name | Function | IRC safe | Complexity | Definition |
|---|---|---:|---|---|
| `tau1` | `nsubjettiness_tau1(jet)` | No (proxy) | `O(N)` | Proxy one-axis N-subjettiness |
| `tau2` | `nsubjettiness_tau2(jet)` | No (proxy) | `O(N)` | Proxy two-axis N-subjettiness |
| `tau3` | `nsubjettiness_tau3(jet)` | No (proxy) | `O(N)` | Proxy three-axis N-subjettiness |
| `tau21` | `nsubjettiness_tau21(jet)` | No (proxy) | `O(N)` | `tau2 / tau1` |
| `tau32` | `nsubjettiness_tau32(jet)` | No (proxy) | `O(N)` | `tau3 / tau2` |
| `e2` | `energy_correlation_e2(jet)` | Yes | `O(N^2)` | Two-point energy correlation |
| `e3` | `energy_correlation_e3(jet)` | Yes | `O(N^3)` | Three-point energy correlation |
| `c2` | `energy_correlation_c2(jet)` | Yes | `O(N^3)` | `e3 / e2^2` |
| `d2` | `energy_correlation_d2(jet)` | Yes | `O(N^3)` | `e3 / e2^3` |

## Groomed proxies

| Name | Function | IRC safe | Complexity | Definition |
|---|---|---:|---|---|
| `soft_drop_zg_proxy` | `soft_drop_zg_proxy(jet)` | No (proxy) | `O(N)` | `zg` using top-2 `pT` constituents |
| `soft_drop_rg_proxy` | `soft_drop_rg_proxy(jet)` | No (proxy) | `O(N)` | `rg` from top-2 `pT` constituents |
| `soft_drop_pass_fraction_proxy` | `soft_drop_pass_fraction_proxy(jet)` | No (proxy) | `O(N)` | Binary Soft Drop condition proxy |
| `groomed_pair_mass_proxy` | `groomed_pair_mass_proxy(jet)` | No (proxy) | `O(N)` | Mass of top-2 `pT` constituent pair |

## Primary references

- [FastJet](https://fastjet.fr/)
- [EnergyFlow](https://energyflow.network/)
- [N-subjettiness (arXiv:1011.2268)](https://arxiv.org/abs/1011.2268)
- [Energy correlators (arXiv:1305.0007)](https://arxiv.org/abs/1305.0007)
- [Lund jet plane (arXiv:1807.04758)](https://arxiv.org/abs/1807.04758)
- [Soft Drop (arXiv:1402.2657)](https://arxiv.org/abs/1402.2657)

Notes:
- Entries marked as proxy are intentionally lightweight baseline implementations intended for reproducible benchmarking and API design; they are not drop-in replacements for full FastJet contrib algorithms.
