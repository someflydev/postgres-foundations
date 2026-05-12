from pathlib import Path

from pgfound import paths
from pgfound.review.engine import evaluate_capstone
from pgfound.review.models import EvaluationContext, EvaluationRequest


def test_deficient_extension_writeups_emit_posture_signals(tmp_path: Path) -> None:
    cases = [
        (
            "05-geo-logistics-platform",
            "CREATE EXTENSION postgis;",
            "",
            "# Extension posture\nToo short.\n",
            "postgis_without_justification",
        ),
        (
            "06-ai-knowledge-platform",
            "CREATE EXTENSION vector;\nCREATE TABLE x (embedding vector(1536));",
            "",
            "# Extension posture\npgvector now because vectors are useful.\n",
            "pgvector_without_lexical_baseline",
        ),
        (
            "08-modernization-bridge-extensions",
            "",
            "",
            "# Extension posture\nCitus now because scale is possible.\n",
            "citus_without_distribution_key_justification",
        ),
        (
            "07-observability-event-analytics",
            "",
            "",
            "# Extension posture\nTimescaleDB now because time-series data is large.\n",
            "timescale_without_partition_comparison",
        ),
    ]

    for capstone_id, schema_sql, indexes_sql, writeup_md, expected_signal in cases:
        artifact_dir = tmp_path / capstone_id
        artifact_dir.mkdir()
        (artifact_dir / "schema.sql").write_text(schema_sql, encoding="utf-8")
        (artifact_dir / "indexes.sql").write_text(indexes_sql, encoding="utf-8")
        (artifact_dir / "rls-policies.sql").write_text(
            "-- intentionally deficient\n",
            encoding="utf-8",
        )
        (artifact_dir / "critical-queries.sql").write_text("SELECT 1;\n", encoding="utf-8")
        (artifact_dir / "writeup.md").write_text(writeup_md, encoding="utf-8")

        result = evaluate_capstone(
            EvaluationRequest(
                target_id=capstone_id,
                artifact_path=artifact_dir,
                context=EvaluationContext(repo_root=paths.REPO_ROOT),
                target_kind="capstone",
            )
        )

        signals = {(signal.key, signal.value) for signal in result.signals}
        assert (expected_signal, "present") in signals
