"""Evaluation-oriented utilities for padded HEPSIM-style jet inputs."""

from __future__ import annotations

import numpy as np


def canonical_constituent_mask(particles: np.ndarray, atol: float = 0.0) -> np.ndarray:
    """Return canonical mask for real constituents in padded (pT, y, phi, pdgid) arrays.

    A row is considered valid when:
    - at least one feature is non-zero,
    - pT is positive,
    - pdgid is non-zero.
    """
    arr = np.asarray(particles, dtype=float)
    if arr.ndim == 1 and arr.shape[0] == 0:
        arr = arr.reshape(0, 4)
    if arr.ndim != 2 or arr.shape[1] != 4:
        raise ValueError(
            f"Expected particles with shape (N, 4) as (pT, y, phi, pdgid), got {arr.shape}."
        )

    nonzero_row = np.any(np.abs(arr) > atol, axis=1)
    positive_pt = arr[:, 0] > atol
    nonzero_pdgid = arr[:, 3] != 0.0
    return nonzero_row & positive_pt & nonzero_pdgid


def strip_padding(particles: np.ndarray, atol: float = 0.0) -> np.ndarray:
    """Drop padded rows from a (pT, y, phi, pdgid) constituent array."""
    arr = np.asarray(particles, dtype=float)
    if arr.ndim == 1 and arr.shape[0] == 0:
        arr = arr.reshape(0, 4)
    return arr[canonical_constituent_mask(arr, atol=atol)]


def constituent_multiplicity(particles: np.ndarray, atol: float = 0.0) -> int:
    """Constituent multiplicity after canonical zero-padding removal."""
    return int(np.count_nonzero(canonical_constituent_mask(particles, atol=atol)))


def leading_constituent_pt(particles: np.ndarray, atol: float = 0.0) -> float:
    """Leading pT after canonical zero-padding removal."""
    valid = strip_padding(particles, atol=atol)
    if valid.shape[0] == 0:
        return 0.0
    return float(np.max(valid[:, 0]))


def ptyphipdg_to_p4(
    particles: np.ndarray,
    *,
    apply_padding_mask: bool = True,
    assume_massless: bool = True,
    atol: float = 0.0,
) -> np.ndarray:
    """Convert (pT, y, phi, pdgid) constituents to (E, px, py, pz).

    This uses rapidity y from the dataset. Under ``assume_massless=True``,
    E = pT * cosh(y) and pz = pT * sinh(y).
    """
    arr = np.asarray(particles, dtype=float)
    if arr.ndim == 1 and arr.shape[0] == 0:
        arr = arr.reshape(0, 4)
    if arr.ndim != 2 or arr.shape[1] != 4:
        raise ValueError(
            f"Expected particles with shape (N, 4) as (pT, y, phi, pdgid), got {arr.shape}."
        )

    if apply_padding_mask:
        arr = strip_padding(arr, atol=atol)

    if arr.shape[0] == 0:
        return np.empty((0, 4), dtype=float)

    pt = arr[:, 0]
    rapidity = arr[:, 1]
    azimuth = arr[:, 2]

    px = pt * np.cos(azimuth)
    py = pt * np.sin(azimuth)
    pz = pt * np.sinh(rapidity)

    if assume_massless:
        energy = pt * np.cosh(rapidity)
    else:
        raise NotImplementedError(
            "Non-massless conversion is not implemented yet; provide four-vectors directly."
        )

    return np.column_stack([energy, px, py, pz]).astype(float)
