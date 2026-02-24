import numpy as np

from jetobsmc.evaluation import (
    canonical_constituent_mask,
    constituent_multiplicity,
    leading_constituent_pt,
    ptyphipdg_to_p4,
    strip_padding,
)
from jetobsmc.fourvector import (
    boost_to_jet_rest_frame,
    invariant_mass,
    rest_frame_momentum_residual,
)
from jetobsmc.jet import Jet
from jetobsmc.observables.shapes import pt_dispersion


def test_padding_mask_identifies_only_real_constituents() -> None:
    padded = np.array(
        [
            [80.0, 0.2, 1.0, 211.0],
            [0.0, 0.0, 0.0, 0.0],
            [12.0, -0.3, -1.2, 22.0],
            [0.0, 0.0, 0.0, 130.0],
        ]
    )
    mask = canonical_constituent_mask(padded)
    assert np.array_equal(mask, np.array([True, False, True, False]))


def test_padding_contract_drives_multiplicity_and_leading_pt() -> None:
    padded = np.array(
        [
            [80.0, 0.2, 1.0, 211.0],
            [0.0, 0.0, 0.0, 0.0],
            [12.0, -0.3, -1.2, 22.0],
        ]
    )
    assert constituent_multiplicity(padded) == 2
    assert leading_constituent_pt(padded) == 80.0
    assert strip_padding(padded).shape[0] == 2


def test_from_ptyphipdg_removes_padding_before_conversion() -> None:
    padded = np.array(
        [
            [10.0, 0.0, 0.0, 211.0],
            [0.0, 0.0, 0.0, 0.0],
            [5.0, 0.0, np.pi / 2.0, 22.0],
        ]
    )
    jet = Jet.from_ptyphipdg(padded)
    assert jet.particles.shape == (2, 4)
    assert np.allclose(jet.particles[0], np.array([10.0, 10.0, 0.0, 0.0]))
    assert np.allclose(jet.particles[1], np.array([5.0, 0.0, 5.0, 0.0]), atol=1e-12)


def test_pt_dispersion_matches_reference_value() -> None:
    jet = Jet(
        np.array(
            [
                [6.0, 3.0, 0.0, 5.0],
                [7.0, 0.0, 4.0, 5.0],
            ]
        )
    )
    assert np.isclose(pt_dispersion(jet), 5.0 / 7.0)


def test_boost_to_rest_frame_closes_total_three_momentum() -> None:
    particles = np.array(
        [
            [80.0, 30.0, 10.0, 60.0],
            [50.0, -20.0, 5.0, -35.0],
            [30.0, 4.0, -3.0, 20.0],
        ]
    )
    boosted = boost_to_jet_rest_frame(particles)
    residual = np.linalg.norm(boosted[:, 1:4].sum(axis=0))
    assert residual < 1e-9


def test_boost_preserves_jet_invariant_mass() -> None:
    particles = np.array(
        [
            [80.0, 30.0, 10.0, 60.0],
            [50.0, -20.0, 5.0, -35.0],
            [30.0, 4.0, -3.0, 20.0],
        ]
    )
    total_lab = particles.sum(axis=0)
    total_rest = boost_to_jet_rest_frame(particles).sum(axis=0)
    assert np.isclose(
        invariant_mass(total_lab), invariant_mass(total_rest), rtol=1e-10, atol=1e-10
    )


def test_boost_is_finite_for_near_lightlike_jet() -> None:
    p1 = np.array([np.sqrt(500.0**2 + 0.2**2 + 1.0), 0.2, 0.0, 500.0])
    p2 = np.array([np.sqrt(400.0**2 + 0.1**2 + 0.5), 0.1, 0.0, 400.0])
    particles = np.vstack([p1, p2])

    boosted = boost_to_jet_rest_frame(particles)
    assert np.all(np.isfinite(boosted))
    assert rest_frame_momentum_residual(particles) < 1e-6


def test_empty_jet_rest_frame_helpers_are_safe() -> None:
    jet = Jet(np.empty((0, 4), dtype=float))
    assert jet.boosted_constituents_rest_frame().shape == (0, 4)
    assert jet.rest_frame_momentum_residual() == 0.0


def test_direct_conversion_function_matches_constructor_path() -> None:
    padded = np.array(
        [
            [25.0, 0.1, 0.5, 211.0],
            [0.0, 0.0, 0.0, 0.0],
            [10.0, -0.2, -1.0, 22.0],
        ]
    )
    p4 = ptyphipdg_to_p4(padded)
    jet = Jet.from_ptyphipdg(padded)
    assert np.allclose(jet.particles, p4)
