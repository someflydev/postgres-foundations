from pgfound.content import lint


def test_content_lint_strict_all_active_content() -> None:
    report = lint.lint_content(path_globs=())
    assert not report.warnings, [f"{issue.path}: {issue.message}" for issue in report.warnings]
