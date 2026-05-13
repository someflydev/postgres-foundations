import json

from pgfound import paths
from pgfound.decision import engine


def _run_fixture(name: str) -> dict:
    intake = paths.DECISION_ENGINE_DIR / "fixtures" / "intakes" / f"{name}.json"
    return engine.run_decision(intake)


def test_each_fixture_produces_recommendations_with_valid_confidence() -> None:
    for intake in sorted((paths.DECISION_ENGINE_DIR / "fixtures" / "intakes").glob("*.json")):
        report = engine.run_decision(intake)
        assert report["recommendations"], intake.name
        for recommendation in report["recommendations"]:
            assert 0.4 <= recommendation["confidence"] <= 0.95
            if recommendation["verdict"] == "recommend_now":
                assert recommendation["confidence"] >= 0.4


def test_saas_fixture_triggers_rls_rule() -> None:
    report = _run_fixture("saas-multi-tenant-minimal")
    rls = next(
        item
        for item in report["recommendations"]
        if item["target_slug"] == "row_level_security"
    )

    assert rls["verdict"] == "recommend_now"
    assert any(
        source["rule_id"] == "rule-rls-when-multi-tenant-and-shared-schema"
        for source in rls["sources"]
    )


def test_logistics_fixture_recommends_postgis_and_defers_pgvector() -> None:
    report = _run_fixture("logistics-geo-minimal")
    by_slug = {item["target_slug"]: item for item in report["recommendations"]}

    assert by_slug["postgis"]["verdict"] == "recommend_now"
    assert by_slug["postgis"]["confidence"] >= 0.8
    assert by_slug["pgvector"]["verdict"] == "not_enough_evidence"
    assert by_slug["pgvector"]["why_not_yet"]


def test_golden_reports_match_current_engine_shape() -> None:
    report_dir = paths.DECISION_ENGINE_DIR / "fixtures" / "reports"
    for intake in sorted((paths.DECISION_ENGINE_DIR / "fixtures" / "intakes").glob("*.json")):
        report = engine.run_decision(intake)
        report["generated_at"] = "2026-05-12T00:00:00Z"
        golden = json.loads(
            (report_dir / f"{report['intake_id']}.report.json").read_text(encoding="utf-8")
        )
        assert report == golden
