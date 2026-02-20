import numpy as np
import pytest

from jet_observables.fourvector import FourVector, invariant_mass, minkowski_dot
from jet_observables.jet import Jet
from jet_observables.observables.shapes import (
    energy_correlation_e2,
    jet_width,
    nsubjettiness_tau1,
)


def test_mass_of_single_particle_at_rest() -> None:
    p = np.array([10.0, 0.0, 0.0, 0.0])
    assert invariant_mass(p) == 10.0


def test_minkowski_dot_is_symmetric() -> None:
    a = np.array([20.0, 3.0, 4.0, 5.0])
    b = np.array([10.0, -1.0, 2.0, -3.0])
    assert minkowski_dot(a, b) == minkowski_dot(b, a)


def test_massless_particle_has_zero_invariant_mass() -> None:
    p = np.array([10.0, 6.0, 8.0, 0.0])
    assert np.isclose(invariant_mass(p), 0.0)


def test_mass_scales_linearly_with_global_fourvector_scaling() -> None:
    p = FourVector(12.0, 3.0, 4.0, 5.0)
    scaled = FourVector(24.0, 6.0, 8.0, 10.0)
    assert np.isclose(scaled.mass(), 2.0 * p.mass())


def test_delta_r_is_symmetric() -> None:
    jet_a = Jet(np.array([[30.0, 10.0, 5.0, 27.0], [15.0, 2.0, 1.0, 14.0]]))
    jet_b = Jet(np.array([[25.0, -9.0, 3.0, 22.0], [12.0, -4.0, 1.0, 10.0]]))
    assert np.isclose(jet_a.delta_r(jet_b), jet_b.delta_r(jet_a))


def test_empty_jet_returns_zero_for_scalar_observables() -> None:
    jet = Jet(np.empty((0, 4), dtype=float))
    assert jet.pt() == 0.0
    assert jet.mass() == 0.0
    assert jet_width(jet) == 0.0
    assert energy_correlation_e2(jet) == 0.0
    assert nsubjettiness_tau1(jet) == 0.0


def test_jet_rejects_bad_shape() -> None:
    with pytest.raises(ValueError):
        Jet(np.array([1.0, 2.0, 3.0]))


def test_jet_rejects_wrong_component_count() -> None:
    with pytest.raises(ValueError):
        Jet(np.array([[1.0, 2.0, 3.0]]))


def test_jet_width_non_negative() -> None:
    jet = Jet(np.array([[40.0, 20.0, 5.0, 34.0], [25.0, 7.0, 4.0, 23.0]]))
    assert jet_width(jet) >= 0.0


def test_e2_is_non_negative_for_physical_input() -> None:
    jet = Jet(np.array([[40.0, 20.0, 5.0, 34.0], [25.0, 7.0, 4.0, 23.0]]))
    assert energy_correlation_e2(jet) >= 0.0


def test_tau1_is_non_negative_for_physical_input() -> None:
    jet = Jet(np.array([[40.0, 20.0, 5.0, 34.0], [25.0, 7.0, 4.0, 23.0]]))
    assert nsubjettiness_tau1(jet) >= 0.0


def test_large_random_batch_produces_finite_values() -> None:
    rng = np.random.default_rng(7)
    for _ in range(100):
        n = int(rng.integers(2, 40))
        px = rng.normal(0.0, 30.0, size=n)
        py = rng.normal(0.0, 30.0, size=n)
        pz = rng.normal(0.0, 40.0, size=n)
        p2 = px * px + py * py + pz * pz
        E = np.sqrt(p2 + rng.uniform(0.0, 25.0, size=n))
        particles = np.column_stack([E, px, py, pz])
        jet = Jet(particles)

        assert np.isfinite(jet.pt())
        assert np.isfinite(jet.mass())
        assert np.isfinite(jet_width(jet))
        assert np.isfinite(energy_correlation_e2(jet))
        assert np.isfinite(nsubjettiness_tau1(jet))


def test_fourvector_dot_matches_function() -> None:
    a = FourVector(20.0, 3.0, 4.0, 5.0)
    b = FourVector(10.0, -1.0, 2.0, -3.0)
    assert np.isclose(a.dot(b), minkowski_dot(a.as_array(), b.as_array()))
