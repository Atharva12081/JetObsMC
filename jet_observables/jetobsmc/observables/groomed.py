"""Lightweight groomed-observable proxies."""

from __future__ import annotations

import numpy as np

from ..fourvector import eta_array, invariant_mass, phi_array
from ..jet import Jet
from .kinematics import wrap_delta_phi


def _constituent_pts(particles: np.ndarray) -> np.ndarray:
    return np.hypot(particles[:, 1], particles[:, 2])


def _hardest_pair_indices(jet: Jet) -> tuple[int, int] | None:
    n = jet.particles.shape[0]
    if n < 2:
        return None
    pts = _constituent_pts(jet.particles)
    top2 = np.argsort(pts)[-2:]
    return int(top2[0]), int(top2[1])


def soft_drop_zg_proxy(jet: Jet) -> float:
    """Proxy for Soft Drop zg using top-2 pT constituents."""
    pair = _hardest_pair_indices(jet)
    if pair is None:
        return 0.0

    pts = _constituent_pts(jet.particles)
    i, j = pair
    denom = pts[i] + pts[j]
    if denom <= 0.0:
        return 0.0
    return float(min(pts[i], pts[j]) / denom)


def soft_drop_rg_proxy(jet: Jet) -> float:
    """Proxy for Soft Drop rg using angular distance of top-2 pT constituents."""
    pair = _hardest_pair_indices(jet)
    if pair is None:
        return 0.0

    etas = eta_array(jet.particles)
    phis = phi_array(jet.particles)
    i, j = pair
    deta = etas[i] - etas[j]
    dphi = float(wrap_delta_phi(phis[i] - phis[j]))
    return float(np.hypot(deta, dphi))


def soft_drop_pass_fraction_proxy(
    jet: Jet, zcut: float = 0.1, beta: float = 0.0, r0: float = 1.0
) -> float:
    """Binary Soft Drop condition proxy (1 if pass, else 0) on hardest pair."""
    if r0 <= 0.0:
        return 0.0
    zg = soft_drop_zg_proxy(jet)
    rg = soft_drop_rg_proxy(jet)
    threshold = float(zcut * ((rg / r0) ** beta))
    return float(1.0 if zg > threshold else 0.0)


def groomed_pair_mass_proxy(jet: Jet) -> float:
    """Invariant mass of top-2 pT constituent pair."""
    pair = _hardest_pair_indices(jet)
    if pair is None:
        return 0.0
    i, j = pair
    pair_p4 = jet.particles[i] + jet.particles[j]
    return invariant_mass(pair_p4)


__all__ = [
    "soft_drop_zg_proxy",
    "soft_drop_rg_proxy",
    "soft_drop_pass_fraction_proxy",
    "groomed_pair_mass_proxy",
]
