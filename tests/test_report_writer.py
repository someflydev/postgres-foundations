from pgfound import paths
from pgfound.decision import engine, report_writer


def test_markdown_report_contains_expected_sections() -> None:
    intake = paths.DECISION_ENGINE_DIR / "fixtures" / "intakes" / "logistics-geo-minimal.json"
    report = engine.run_decision(intake)

    markdown = report_writer.render_markdown(report, show_scores=True)

    assert "# PostgreSQL Architecture Recommendation" in markdown
    assert "## Summary" in markdown
    assert "## Recommend now" in markdown
    assert "## Candidate later" in markdown
    assert "## Not enough evidence" in markdown
    assert "## Avoid for now" in markdown
    assert "## Score breakdown" in markdown
    assert "## Cited rules" in markdown
    assert "## Appendix: full intake" in markdown
    assert "| Recommendation | Domain | Data | Workload | Ops | Growth |" in markdown


def test_markdown_report_can_hide_score_table() -> None:
    intake = paths.DECISION_ENGINE_DIR / "fixtures" / "intakes" / "saas-multi-tenant-minimal.json"
    report = engine.run_decision(intake)

    markdown = report_writer.render_markdown(report, show_scores=False)

    assert "## Score breakdown" not in markdown
    assert "## Cited rules" in markdown
