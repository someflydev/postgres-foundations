from pgfound.content import validate


def test_default_rubrics_load_and_validate() -> None:
    report = validate.validate_content(path_globs=("rubrics/default/*.rubric.json",))

    assert report.ok
    assert report.by_kind["rubric"] == 5
