import json

from pgfound import paths
from pgfound.review.runners.query import diff_plans, plan_signals


def test_plan_diff_is_deterministic_for_fixture_explain_json() -> None:
    seq_scan = json.loads((paths.REPO_ROOT / "tests/fixtures/plans/seq_scan.json").read_text())
    index_scan = json.loads((paths.REPO_ROOT / "tests/fixtures/plans/index_scan.json").read_text())

    diff = diff_plans(seq_scan, index_scan)

    assert diff["reference_node_types"] == ["Seq Scan"]
    assert diff["learner_node_types"] == ["Index Scan"]
    assert diff["node_count_delta"] == 0
    assert "execution_time_ms_delta" in diff


def test_plan_signals_flag_unexpected_seq_scan() -> None:
    seq_scan = json.loads((paths.REPO_ROOT / "tests/fixtures/plans/seq_scan.json").read_text())
    index_scan = json.loads((paths.REPO_ROOT / "tests/fixtures/plans/index_scan.json").read_text())

    diff = diff_plans(index_scan, seq_scan)
    signals, findings = plan_signals(diff, pointer="answer.sql")

    assert ("seq_scan_where_index_expected", "present") in {
        (signal.key, signal.value) for signal in signals
    }
    assert any("Sequential scan" in finding.title for finding in findings)
