"""Jet substructure observables."""

from __future__ import annotations

import itertools

import numpy as np

from ..fourvector import eta_array, phi_array
from ..jet import Jet
from .kinematics import wrap_delta_phi


def _constituent_pts(particles: np.ndarray) -> np.ndarray:
    return np.hypot(particles[:, 1], particles[:, 2])


def _constituent_eta_phi(particles: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return eta_array(particles), phi_array(particles)


def _tau_n_proxy(jet: Jet, n_axes: int) -> float:
    """Lightweight N-subjettiness proxy using top-pT constituent axes."""
    p = jet.particles
    n = p.shape[0]
    if n == 0:
        return 0.0
    if n_axes <= 0:
        raise ValueError("n_axes must be positive")
    if n_axes >= n:
        return 0.0

    pts = _constituent_pts(p)
    if float(np.sum(pts)) == 0.0:
        return 0.0

    etas, phis = _constituent_eta_phi(p)
    axis_idx = np.argsort(pts)[-n_axes:]
    axis_eta = etas[axis_idx]
    axis_phi = phis[axis_idx]

    deta = etas[:, None] - axis_eta[None, :]
    dphi = wrap_delta_phi(phis[:, None] - axis_phi[None, :])
    dr = np.hypot(deta, dphi)
    dr_min = np.min(dr, axis=1)
    return float(np.sum(pts * dr_min))


def nsubjettiness_tau1(jet: Jet) -> float:
    """Basic tau1 proxy."""
    return _tau_n_proxy(jet, n_axes=1)


def nsubjettiness_tau2(jet: Jet) -> float:
    """Basic tau2 proxy."""
    return _tau_n_proxy(jet, n_axes=2)


def nsubjettiness_tau3(jet: Jet) -> float:
    """Basic tau3 proxy."""
    return _tau_n_proxy(jet, n_axes=3)


def nsubjettiness_tau21(jet: Jet) -> float:
    """Tau21 ratio from proxy tau2/tau1."""
    tau1 = nsubjettiness_tau1(jet)
    if tau1 <= 0.0:
        return 0.0
    return float(nsubjettiness_tau2(jet) / tau1)


def nsubjettiness_tau32(jet: Jet) -> float:
    """Tau32 ratio from proxy tau3/tau2."""
    tau2 = nsubjettiness_tau2(jet)
    if tau2 <= 0.0:
        return 0.0
    return float(nsubjettiness_tau3(jet) / tau2)


def energy_correlation_e2(jet: Jet) -> float:
    """Two-point energy correlation: e2 = sum_{i<j} pT_i pT_j DeltaR_ij."""
    n = jet.particles.shape[0]
    if n < 2:
        return 0.0

    pts = _constituent_pts(jet.particles)
    etas, phis = _constituent_eta_phi(jet.particles)

    deta = etas[:, None] - etas[None, :]
    dphi = wrap_delta_phi(phis[:, None] - phis[None, :])
    dr = np.hypot(deta, dphi)

    weight = pts[:, None] * pts[None, :]
    upper = np.triu_indices(n, k=1)
    return float(np.sum(weight[upper] * dr[upper]))


def energy_correlation_e3(jet: Jet) -> float:
    """Three-point energy correlation with full triangle weighting."""
    n = jet.particles.shape[0]
    if n < 3:
        return 0.0

    pts = _constituent_pts(jet.particles)
    etas, phis = _constituent_eta_phi(jet.particles)

    deta = etas[:, None] - etas[None, :]
    dphi = wrap_delta_phi(phis[:, None] - phis[None, :])
    dr = np.hypot(deta, dphi)

    total = 0.0
    for i, j, k in itertools.combinations(range(n), 3):
        total += pts[i] * pts[j] * pts[k] * dr[i, j] * dr[i, k] * dr[j, k]
    return float(total)


def energy_correlation_c2(jet: Jet) -> float:
    """C2 ratio: e3 / e2^2."""
    e2 = energy_correlation_e2(jet)
    if e2 <= 0.0:
        return 0.0
    e3 = energy_correlation_e3(jet)
    return float(e3 / (e2 * e2))


def energy_correlation_d2(jet: Jet) -> float:
    """D2 ratio: e3 / e2^3."""
    e2 = energy_correlation_e2(jet)
    if e2 <= 0.0:
        return 0.0
    e3 = energy_correlation_e3(jet)
    return float(e3 / (e2 * e2 * e2))


__all__ = [
    "nsubjettiness_tau1",
    "nsubjettiness_tau2",
    "nsubjettiness_tau3",
    "nsubjettiness_tau21",
    "nsubjettiness_tau32",
    "energy_correlation_e2",
    "energy_correlation_e3",
    "energy_correlation_c2",
    "energy_correlation_d2",
]
