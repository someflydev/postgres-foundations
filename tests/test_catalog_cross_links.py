from pgfound.decision import engine as decision_engine


def test_decision_catalog_cross_links_are_clean() -> None:
    result = decision_engine.check_catalogs()

    assert result["errors"] == []
    assert result["warnings"] == []
