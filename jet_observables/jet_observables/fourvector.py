"""Core 4-vector utilities and class using the (+, -, -, -) Minkowski metric."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

EPS = 1e-12


@dataclass(frozen=True)
class FourVector:
    """Lorentz 4-vector in (E, px, py, pz) convention."""

    E: float
    px: float
    py: float
    pz: float

    def as_array(self) -> np.ndarray:
        """Return vector as NumPy array [E, px, py, pz]."""
        return np.array([self.E, self.px, self.py, self.pz], dtype=float)

    def dot(self, other: "FourVector") -> float:
        """Minkowski dot product with signature (+, -, -, -)."""
        if not isinstance(other, FourVector):
            raise TypeError("dot expects another FourVector")
        return float(
            self.E * other.E
            - self.px * other.px
            - self.py * other.py
            - self.pz * other.pz
        )

    def mass(self) -> float:
        """Invariant mass m = sqrt(max(p·p, 0))."""
        m2 = self.dot(self)
        return float(np.sqrt(max(m2, 0.0)))

    def pt(self) -> float:
        """Transverse momentum sqrt(px^2 + py^2)."""
        return float(np.hypot(self.px, self.py))

    def eta(self) -> float:
        """Pseudorapidity eta = 0.5 * ln((|p| + pz) / (|p| - pz))."""
        p_abs = float(
            np.sqrt(self.px * self.px + self.py * self.py + self.pz * self.pz)
        )
        numer = p_abs + self.pz
        denom = p_abs - self.pz

        if abs(denom) < EPS or numer <= 0.0 or denom <= 0.0:
            return float(np.sign(self.pz) * np.inf)

        return float(0.5 * np.log(numer / denom))

    def phi(self) -> float:
        """Azimuthal angle in [-pi, pi]."""
        return float(np.arctan2(self.py, self.px))

    @classmethod
    def from_array(cls, p: np.ndarray | Iterable[float]) -> "FourVector":
        """Build FourVector from array-like with shape (4,)."""
        vec = _as_vector(p)
        return cls(
            E=float(vec[0]), px=float(vec[1]), py=float(vec[2]), pz=float(vec[3])
        )


def _as_vector(p: np.ndarray | Iterable[float]) -> np.ndarray:
    vec = np.asarray(p, dtype=float)
    if vec.shape != (4,):
        raise ValueError(f"Expected a 4-vector with shape (4,), got {vec.shape}")
    return vec


def eta_array(vectors: np.ndarray) -> np.ndarray:
    """Vectorized eta for arrays of shape (N, 4)."""
    arr = np.asarray(vectors, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 4:
        raise ValueError(f"Expected vectors with shape (N, 4), got {arr.shape}")

    px = arr[:, 1]
    py = arr[:, 2]
    pz = arr[:, 3]
    p_abs = np.sqrt(px * px + py * py + pz * pz)

    numer = p_abs + pz
    denom = p_abs - pz

    eta = np.empty(arr.shape[0], dtype=float)
    bad = (np.abs(denom) < EPS) | (numer <= 0.0) | (denom <= 0.0)
    eta[~bad] = 0.5 * np.log(numer[~bad] / denom[~bad])
    eta[bad] = np.sign(pz[bad]) * np.inf
    return eta


def phi_array(vectors: np.ndarray) -> np.ndarray:
    """Vectorized phi for arrays of shape (N, 4)."""
    arr = np.asarray(vectors, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 4:
        raise ValueError(f"Expected vectors with shape (N, 4), got {arr.shape}")
    return np.arctan2(arr[:, 2], arr[:, 1]).astype(float)


def minkowski_dot(
    a: np.ndarray | Iterable[float], b: np.ndarray | Iterable[float]
) -> float:
    """Compatibility helper returning a·b with signature (+, -, -, -)."""
    return FourVector.from_array(a).dot(FourVector.from_array(b))


def invariant_mass(p: np.ndarray | Iterable[float]) -> float:
    """Compatibility helper for invariant mass."""
    return FourVector.from_array(p).mass()


def pt(p: np.ndarray | Iterable[float]) -> float:
    """Compatibility helper for transverse momentum."""
    return FourVector.from_array(p).pt()


def eta(p: np.ndarray | Iterable[float]) -> float:
    """Compatibility helper for pseudorapidity."""
    return FourVector.from_array(p).eta()


def phi(p: np.ndarray | Iterable[float]) -> float:
    """Compatibility helper for azimuth."""
    return FourVector.from_array(p).phi()
