from __future__ import annotations

from pgfound.review.normalize import normalize_for_comparison, normalize_range_text


def test_array_canonicalization_sorts_equivalent_values() -> None:
    assert normalize_for_comparison(["beta", "alpha"]) == normalize_for_comparison(
        ["alpha", "beta"]
    )
    assert normalize_for_comparison("{beta,alpha}") == normalize_for_comparison("{alpha,beta}")


def test_range_canonicalization_preserves_bounds() -> None:
    assert normalize_range_text(" [ 1 , 5 ) ") == "[1,5)"
    assert normalize_for_comparison("[1,5)") == normalize_for_comparison(" [ 1 , 5 ) ")
    assert normalize_for_comparison("[1,4]") != normalize_for_comparison("[1,5)")
