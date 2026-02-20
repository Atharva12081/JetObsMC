"""Jet shape and substructure observables."""

from __future__ import annotations

import numpy as np

from ..fourvector import eta_array, phi_array
from ..jet import Jet
from .kinematics import wrap_delta_phi


def _constituent_pts(particles: np.ndarray) -> np.ndarray:
    return np.hypot(particles[:, 1], particles[:, 2])


def _constituent_eta_phi(particles: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return eta_array(particles), phi_array(particles)


def jet_width(jet: Jet) -> float:
    """Compute jet width: sum_i pT_i * DeltaR_i / sum_i pT_i."""
    if jet.particles.shape[0] == 0:
        return 0.0

    pts = _constituent_pts(jet.particles)
    denom = float(np.sum(pts))
    if denom == 0.0:
        return 0.0

    etas, phis = _constituent_eta_phi(jet.particles)
    dphi = wrap_delta_phi(phis - jet.phi())
    dr = np.hypot(etas - jet.eta(), dphi)
    return float(np.sum(pts * dr) / denom)


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


def nsubjettiness_tau1(jet: Jet) -> float:
    """Basic tau1 proxy: tau1 = sum_i pT_i * DeltaR_i to jet axis."""
    if jet.particles.shape[0] == 0:
        return 0.0

    pts = _constituent_pts(jet.particles)
    etas, phis = _constituent_eta_phi(jet.particles)
    dphi = wrap_delta_phi(phis - jet.phi())
    dr = np.hypot(etas - jet.eta(), dphi)
    return float(np.sum(pts * dr))
