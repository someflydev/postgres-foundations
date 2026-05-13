from pgfound.decision import rules


def test_all_decision_rules_validate_against_schema() -> None:
    loaded = rules.load_rules()

    assert len(loaded) >= 40
    assert all(rule["status"] == "active" for rule in loaded)


def test_decision_rule_lint_is_clean() -> None:
    result = rules.lint_rules()

    assert result["errors"] == []
    assert result["warnings"] == []
