import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

from pgfound import paths
from pgfound.content import validate


def _load_json(relative_path: str) -> dict:
    return json.loads((paths.REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_curriculum_map_validates_against_schema() -> None:
    schema = _load_json("content-schemas/curriculum.schema.json")
    resolver = RefResolver(
        base_uri=f"{validate.schema_dir().resolve().as_uri()}/",
        referrer=schema,
        store=validate.schema_store(),
    )
    validator = Draft202012Validator(schema, resolver=resolver)

    errors = sorted(
        validator.iter_errors(_load_json("curriculum/map.json")), key=lambda item: item.path
    )

    assert errors == []


def test_curriculum_phase_numbers_are_monotonic() -> None:
    curriculum = _load_json("curriculum/map.json")

    assert [phase["number"] for phase in curriculum["phases"]] == list(range(11))


def test_curriculum_capability_layers_are_common_enum_values() -> None:
    curriculum = _load_json("curriculum/map.json")
    common = _load_json("content-schemas/common.json")
    allowed = set(common["$defs"]["capability_layer"]["enum"])

    used = {phase["capability_layer"] for phase in curriculum["phases"]}

    assert used <= allowed


def test_curriculum_cross_checks_reject_duplicate_and_nonmonotonic_values(
    tmp_path: Path,
) -> None:
    curriculum = deepcopy(_load_json("curriculum/map.json"))
    curriculum["phases"][1]["number"] = 2
    curriculum["phases"][1]["slug"] = curriculum["phases"][0]["slug"]
    curriculum["domains"][1]["slug"] = curriculum["domains"][0]["slug"]
    curriculum["capstones"][1]["id"] = curriculum["capstones"][0]["id"]

    map_path = tmp_path / "curriculum" / "map.json"
    map_path.parent.mkdir()
    map_path.write_text(json.dumps(curriculum), encoding="utf-8")

    report = validate.validate_content(path_globs=(str(map_path),))
    messages = "\n".join(issue.message for issue in report.errors)

    assert not report.ok
    assert "phase numbers must be monotonic 0..10" in messages
    assert "phase slugs must be unique" in messages
    assert "domain slugs must be unique" in messages
    assert "capstone ids must be unique" in messages
