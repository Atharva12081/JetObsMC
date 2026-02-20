"""Jet object API for computing core observables."""

from __future__ import annotations

from typing import Iterable

import numpy as np

from .fourvector import FourVector


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
