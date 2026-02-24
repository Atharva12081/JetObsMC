"""Jet shape observables built from constituent-level geometry."""

from __future__ import annotations

import numpy as np

from ..fourvector import eta_array, phi_array
from ..jet import Jet
from .kinematics import wrap_delta_phi
from .substructure import energy_correlation_e2, nsubjettiness_tau1


def _constituent_pts(particles: np.ndarray) -> np.ndarray:
    return np.hypot(particles[:, 1], particles[:, 2])


def _constituent_eta_phi(particles: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return eta_array(particles), phi_array(particles)


def multiplicity(jet: Jet) -> int:
    """Number of constituents in the jet."""
    return int(jet.particles.shape[0])


def constituent_pt_sum(jet: Jet) -> float:
    """Scalar sum of constituent transverse momenta."""
    if jet.particles.shape[0] == 0:
        return 0.0
    return float(np.sum(_constituent_pts(jet.particles)))


def leading_constituent_pt(jet: Jet) -> float:
    """Largest constituent transverse momentum."""
    if jet.particles.shape[0] == 0:
        return 0.0
    return float(np.max(_constituent_pts(jet.particles)))


def leading_pt_fraction(jet: Jet) -> float:
    """Leading constituent pT divided by scalar pT sum."""
    denom = constituent_pt_sum(jet)
    if denom == 0.0:
        return 0.0
    return float(leading_constituent_pt(jet) / denom)


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


def girth(jet: Jet) -> float:
    """Alias for jet width frequently used in phenomenology."""
    return jet_width(jet)


def radial_moment(jet: Jet, beta: float) -> float:
    """Generalized radial moment: sum_i pT_i * (DeltaR_i^beta) / sum_i pT_i."""
    if jet.particles.shape[0] == 0:
        return 0.0

    pts = _constituent_pts(jet.particles)
    denom = float(np.sum(pts))
    if denom == 0.0:
        return 0.0

    etas, phis = _constituent_eta_phi(jet.particles)
    dphi = wrap_delta_phi(phis - jet.phi())
    dr = np.hypot(etas - jet.eta(), dphi)
    return float(np.sum(pts * (dr**beta)) / denom)


def radial_moment_2(jet: Jet) -> float:
    """Second radial moment (beta=2)."""
    return radial_moment(jet, beta=2.0)


def radial_moment_3(jet: Jet) -> float:
    """Third radial moment (beta=3)."""
    return radial_moment(jet, beta=3.0)


def generalized_angularity(
    jet: Jet, kappa: float, beta: float, r0: float = 1.0
) -> float:
    """Generalized angularity lambda^kappa_beta.

    Definition:
        z_i = pT_i / sum_j pT_j
        theta_i = DeltaR_i / r0
        lambda = sum_i z_i^kappa * theta_i^beta
    """
    if jet.particles.shape[0] == 0 or r0 <= 0.0:
        return 0.0

    pts = _constituent_pts(jet.particles)
    pt_sum = float(np.sum(pts))
    if pt_sum == 0.0:
        return 0.0

    etas, phis = _constituent_eta_phi(jet.particles)
    dphi = wrap_delta_phi(phis - jet.phi())
    theta = np.hypot(etas - jet.eta(), dphi) / float(r0)
    z = pts / pt_sum
    return float(np.sum((z**kappa) * (theta**beta)))


def lha(jet: Jet) -> float:
    """Les Houches angularity: lambda^1_{0.5}."""
    return generalized_angularity(jet, kappa=1.0, beta=0.5, r0=1.0)


def thrust_angularity(jet: Jet) -> float:
    """Thrust-like angularity: lambda^1_{2}."""
    return generalized_angularity(jet, kappa=1.0, beta=2.0, r0=1.0)


def ptd_angularity(jet: Jet) -> float:
    """pTD-like angularity: lambda^2_0."""
    return generalized_angularity(jet, kappa=2.0, beta=0.0, r0=1.0)


def pt_dispersion(jet: Jet) -> float:
    """pT dispersion: sqrt(sum_i pT_i^2) / sum_i pT_i."""
    if jet.particles.shape[0] == 0:
        return 0.0

    pts = _constituent_pts(jet.particles)
    denom = float(np.sum(pts))
    if denom == 0.0:
        return 0.0

    return float(np.sqrt(np.sum(pts * pts)) / denom)


__all__ = [
    "multiplicity",
    "constituent_pt_sum",
    "leading_constituent_pt",
    "leading_pt_fraction",
    "jet_width",
    "girth",
    "radial_moment",
    "radial_moment_2",
    "radial_moment_3",
    "generalized_angularity",
    "lha",
    "thrust_angularity",
    "ptd_angularity",
    "pt_dispersion",
    "energy_correlation_e2",
    "nsubjettiness_tau1",
]
