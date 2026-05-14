from pgfound.content import seed_doctor


def test_seed_doctor_all_domains_reports_zero_errors() -> None:
    report = seed_doctor.run_seed_doctor()
    assert report.ok, [
        f"{issue.exercise_id} {issue.seed_pack_id} phase {issue.phase}: {issue.message}"
        for issue in report.issues
    ]
