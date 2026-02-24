"""Kinematic jet observables."""

from __future__ import annotations

import numpy as np

from ..jet import Jet


def wrap_delta_phi(dphi: np.ndarray | float) -> np.ndarray | float:
    """Wrap azimuthal angle difference into [-pi, pi]."""
    wrapped = (np.asarray(dphi) + np.pi) % (2.0 * np.pi) - np.pi
    if np.isscalar(dphi):
        return float(wrapped)
    return wrapped


def pt(jet: Jet) -> float:
    return jet.p4.pt()


def mass(jet: Jet) -> float:
    return jet.p4.mass()


def eta(jet: Jet) -> float:
    return jet.p4.eta()


def phi(jet: Jet) -> float:
    return jet.p4.phi()


def delta_r(jet_a: Jet, jet_b: Jet) -> float:
    deta = eta(jet_a) - eta(jet_b)
    dphi = float(wrap_delta_phi(phi(jet_a) - phi(jet_b)))
    return float(np.hypot(deta, dphi))
