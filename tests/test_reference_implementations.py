import itertools

import numpy as np

from jetobsmc.jet import Jet
from jetobsmc.metadata import OBSERVABLES
from jetobsmc.observables.groomed import (
    groomed_pair_mass_proxy,
    soft_drop_pass_fraction_proxy,
    soft_drop_rg_proxy,
    soft_drop_zg_proxy,
)
from jetobsmc.observables.kinematics import wrap_delta_phi
from jetobsmc.observables.shapes import jet_width, multiplicity
from jetobsmc.observables.substructure import (
    energy_correlation_c2,
    energy_correlation_d2,
    energy_correlation_e2,
    energy_correlation_e3,
    nsubjettiness_tau1,
    nsubjettiness_tau2,
    nsubjettiness_tau21,
)


def _pts(p):
    return np.hypot(p[:, 1], p[:, 2])


def _eta_phi(p):
    px, py, pz = p[:, 1], p[:, 2], p[:, 3]
    pabs = np.sqrt(px * px + py * py + pz * pz)
    eta = 0.5 * np.log((pabs + pz) / np.maximum(pabs - pz, 1e-15))
    phi = np.arctan2(py, px)
    return eta, phi


def _reference_width(jet: Jet) -> float:
    if jet.particles.shape[0] == 0:
        return 0.0
    p = jet.particles
    pts = _pts(p)
    denom = float(np.sum(pts))
    if denom == 0.0:
        return 0.0

    etas, phis = _eta_phi(p)
    jet_eta = jet.eta()
    jet_phi = jet.phi()

    accum = 0.0
    for i in range(p.shape[0]):
        dphi = float(wrap_delta_phi(phis[i] - jet_phi))
        dr = float(np.hypot(etas[i] - jet_eta, dphi))
        accum += pts[i] * dr
    return float(accum / denom)


def _reference_e2(jet: Jet) -> float:
    p = jet.particles
    n = p.shape[0]
    if n < 2:
        return 0.0

    pts = _pts(p)
    etas, phis = _eta_phi(p)
    total = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            dphi = float(wrap_delta_phi(phis[i] - phis[j]))
            dr = float(np.hypot(etas[i] - etas[j], dphi))
            total += pts[i] * pts[j] * dr
    return float(total)


def _reference_e3(jet: Jet) -> float:
    p = jet.particles
    n = p.shape[0]
    if n < 3:
        return 0.0

    pts = _pts(p)
    etas, phis = _eta_phi(p)
    total = 0.0
    for i, j, k in itertools.combinations(range(n), 3):
        dij = np.hypot(etas[i] - etas[j], wrap_delta_phi(phis[i] - phis[j]))
        dik = np.hypot(etas[i] - etas[k], wrap_delta_phi(phis[i] - phis[k]))
        djk = np.hypot(etas[j] - etas[k], wrap_delta_phi(phis[j] - phis[k]))
        total += pts[i] * pts[j] * pts[k] * dij * dik * djk
    return float(total)


def _reference_tau_n(jet: Jet, n_axes: int) -> float:
    p = jet.particles
    n = p.shape[0]
    if n == 0 or n_axes >= n:
        return 0.0

    pts = _pts(p)
    etas, phis = _eta_phi(p)

    axis_idx = np.argsort(pts)[-n_axes:]
    total = 0.0
    for i in range(n):
        dr_min = float("inf")
        for a in axis_idx:
            dr = np.hypot(etas[i] - etas[a], wrap_delta_phi(phis[i] - phis[a]))
            dr_min = min(dr_min, dr)
        total += pts[i] * dr_min
    return float(total)


def test_width_matches_reference_loop() -> None:
    jet = Jet(
        np.array(
            [
                [50.0, 28.0, 6.0, 40.0],
                [35.0, 12.0, 8.0, 30.0],
                [15.0, 5.0, 2.0, 12.0],
            ]
        )
    )
    assert np.isclose(jet_width(jet), _reference_width(jet), rtol=1e-12, atol=1e-12)


def test_e2_matches_reference_loop() -> None:
    jet = Jet(
        np.array(
            [
                [40.0, 20.0, 5.0, 34.0],
                [25.0, 7.0, 4.0, 23.0],
                [18.0, -5.0, 2.0, 16.0],
            ]
        )
    )
    assert np.isclose(energy_correlation_e2(jet), _reference_e2(jet), rtol=1e-12)


def test_e3_matches_reference_loop() -> None:
    jet = Jet(
        np.array(
            [
                [42.0, 18.0, 3.0, 38.0],
                [33.0, 10.0, 6.0, 30.0],
                [19.0, -4.0, 3.0, 17.0],
                [14.0, 2.0, -1.0, 12.0],
            ]
        )
    )
    assert np.isclose(energy_correlation_e3(jet), _reference_e3(jet), rtol=1e-12)


def test_tau_proxies_match_reference_loop() -> None:
    jet = Jet(
        np.array(
            [
                [42.0, 18.0, 3.0, 38.0],
                [33.0, 10.0, 6.0, 30.0],
                [19.0, -4.0, 3.0, 17.0],
                [14.0, 2.0, -1.0, 12.0],
            ]
        )
    )
    tau1_ref = _reference_tau_n(jet, 1)
    tau2_ref = _reference_tau_n(jet, 2)

    assert np.isclose(nsubjettiness_tau1(jet), tau1_ref, rtol=1e-12)
    assert np.isclose(nsubjettiness_tau2(jet), tau2_ref, rtol=1e-12)

    if tau1_ref > 0.0:
        assert np.isclose(nsubjettiness_tau21(jet), tau2_ref / tau1_ref, rtol=1e-12)


def test_correlator_ratios_match_definitions() -> None:
    jet = Jet(
        np.array(
            [
                [42.0, 18.0, 3.0, 38.0],
                [33.0, 10.0, 6.0, 30.0],
                [19.0, -4.0, 3.0, 17.0],
                [14.0, 2.0, -1.0, 12.0],
            ]
        )
    )
    e2 = energy_correlation_e2(jet)
    e3 = energy_correlation_e3(jet)
    if e2 > 0.0:
        assert np.isclose(energy_correlation_c2(jet), e3 / (e2 * e2), rtol=1e-12)
        assert np.isclose(energy_correlation_d2(jet), e3 / (e2 * e2 * e2), rtol=1e-12)


def test_groomed_proxies_match_manual_hardest_pair() -> None:
    p = np.array(
        [
            [40.0, 20.0, 0.0, 34.0],
            [25.0, 0.0, 15.0, 20.0],
            [12.0, 2.0, 1.0, 11.0],
        ]
    )
    jet = Jet(p)

    pts = _pts(p)
    i, j = np.argsort(pts)[-2:]
    zg_ref = min(pts[i], pts[j]) / (pts[i] + pts[j])

    etas, phis = _eta_phi(p)
    rg_ref = np.hypot(etas[i] - etas[j], wrap_delta_phi(phis[i] - phis[j]))

    assert np.isclose(soft_drop_zg_proxy(jet), zg_ref)
    assert np.isclose(soft_drop_rg_proxy(jet), rg_ref)
    assert soft_drop_pass_fraction_proxy(jet, zcut=0.1, beta=0.0, r0=1.0) in (0.0, 1.0)
    assert groomed_pair_mass_proxy(jet) >= 0.0


def test_metadata_has_expected_minimum_catalog_size() -> None:
    assert len(OBSERVABLES) >= 30


def test_metadata_schema_is_consistent() -> None:
    required = {"irc_safe", "category", "description", "depends_on", "complexity"}
    for name, meta in OBSERVABLES.items():
        assert required.issubset(meta.keys()), name


def test_multiplicity_matches_constituent_count() -> None:
    jet = Jet(np.array([[10.0, 3.0, 1.0, 9.0], [8.0, -1.0, 2.0, 7.0]]))
    assert multiplicity(jet) == 2
