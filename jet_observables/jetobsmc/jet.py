"""Jet object API for computing core observables."""

from __future__ import annotations

from typing import Iterable

import numpy as np

from .fourvector import (
    FourVector,
    boost_to_jet_rest_frame,
    rest_frame_momentum_residual,
)


class Jet:
    """Container for jet constituents and aggregate 4-vector.

    Constituents are shape (N, 4) with ordering (E, px, py, pz).
    """

    def __init__(self, particles: np.ndarray | Iterable[Iterable[float]]) -> None:
        particles_arr = np.asarray(particles, dtype=float)

        if particles_arr.ndim == 1 and particles_arr.shape[0] == 0:
            particles_arr = particles_arr.reshape(0, 4)

        if particles_arr.ndim != 2:
            raise ValueError(
                "Expected particles as a 2D array with shape (N, 4) in (E, px, py, pz) format."
            )
        if particles_arr.shape[1] != 4:
            raise ValueError(
                f"Expected particles with shape (N, 4), got {particles_arr.shape}."
            )

        self.particles: np.ndarray = particles_arr

        if self.particles.shape[0] == 0:
            self.p4 = FourVector(0.0, 0.0, 0.0, 0.0)
        else:
            total = self.particles.sum(axis=0)
            self.p4 = FourVector.from_array(total)

    def pt(self) -> float:
        return self.p4.pt()

    def mass(self) -> float:
        return self.p4.mass()

    def eta(self) -> float:
        return self.p4.eta()

    def phi(self) -> float:
        return self.p4.phi()

    def delta_r(self, other: "Jet") -> float:
        from .observables.kinematics import delta_r

        if not isinstance(other, Jet):
            raise TypeError("delta_r expects another Jet instance")
        return delta_r(self, other)

    def boosted_constituents_rest_frame(self) -> np.ndarray:
        """Return constituents boosted into the jet rest frame."""
        return boost_to_jet_rest_frame(self.particles)

    def rest_frame_momentum_residual(self) -> float:
        """Return ||sum_i p_i|| after rest-frame boost (should be ~0)."""
        return rest_frame_momentum_residual(self.particles)

    @classmethod
    def from_ptyphipdg(
        cls,
        particles: np.ndarray | Iterable[Iterable[float]],
        *,
        apply_padding_mask: bool = True,
        assume_massless: bool = True,
        atol: float = 0.0,
    ) -> "Jet":
        """Construct Jet from HEPSIM-style (pT, y, phi, pdgid) constituents."""
        from .evaluation import ptyphipdg_to_p4

        particles_arr = np.asarray(particles, dtype=float)
        p4 = ptyphipdg_to_p4(
            particles_arr,
            apply_padding_mask=apply_padding_mask,
            assume_massless=assume_massless,
            atol=atol,
        )
        return cls(p4)
