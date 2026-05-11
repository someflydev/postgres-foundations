import json

from pgfound import paths


def test_every_capstone_rubric_references_extension_posture() -> None:
    for rubric_path in sorted(paths.CAPSTONES_DIR.glob("*/rubric.json")):
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        extended = {entry["rubric_id"] for entry in rubric.get("extends", [])}
        assert "extension-posture" in extended, rubric_path
