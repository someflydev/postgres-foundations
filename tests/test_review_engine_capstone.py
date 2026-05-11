from pgfound import paths
from pgfound.review import engine
from pgfound.review.models import EvaluationContext, EvaluationRequest
from pgfound.review.runners import capstone as capstone_runner


def test_capstone_review_scores_fixture_attempt_in_expected_band() -> None:
    result = engine.evaluate(
        EvaluationRequest(
            target_id="01-multi-tenant-saas-crm",
            artifact_path=paths.REPO_ROOT / "tests/fixtures/capstone-attempt",
            context=EvaluationContext(repo_root=paths.REPO_ROOT),
            target_kind="capstone",
        )
    )

    assert result.target_kind == "capstone"
    assert 0.90 <= result.overall_score <= 1.0
    assert result.passed is True
    assert any(dimension.manual_review for dimension in result.dimensions)
    assert ("rls_policies_present", "present_and_strict") in {
        (signal.key, signal.value) for signal in result.signals
    }


def test_capstone_full_review_without_db_reports_skipped_database_checks() -> None:
    result = engine.evaluate(
        EvaluationRequest(
            target_id="01-multi-tenant-saas-crm",
            artifact_path=paths.REPO_ROOT / "tests/fixtures/capstone-attempt",
            context=EvaluationContext(repo_root=paths.REPO_ROOT, db_url=None),
            mode="full",
            target_kind="capstone",
        )
    )

    assert ("capstone_database_checks", "skipped") in {
        (signal.key, signal.value) for signal in result.signals
    }
    assert any("database checks skipped" in finding.title.lower() for finding in result.findings)


def test_capstone_runner_preprocesses_psql_set_variables() -> None:
    sql = "\\set tenant_id '00000000-0000-0000-0000-000000000001'\nSELECT :'tenant_id'::uuid;"

    processed = capstone_runner._preprocess_psql_vars(sql)

    assert "\\set" not in processed
    assert "'00000000-0000-0000-0000-000000000001'::uuid" in processed
