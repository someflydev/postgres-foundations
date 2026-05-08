import json
from pathlib import Path

from jsonschema import Draft202012Validator

from pgfound import paths


def _json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_each_domain_manifest_validates() -> None:
    schema = _json(paths.REPO_ROOT / "content-schemas" / "manifest.schema.json")
    validator = Draft202012Validator(schema)

    for manifest_path in sorted((paths.SEED_DATA_DIR / "packs").glob("*/manifest.json")):
        manifest = _json(manifest_path)
        errors = sorted(validator.iter_errors(manifest), key=lambda error: error.json_path)
        assert errors == []
        assert manifest["domain"] == manifest_path.parent.name


def test_curriculum_domains_have_seed_packs() -> None:
    curriculum = _json(paths.CURRICULUM_DIR / "map.json")
    curriculum_domains = {domain["slug"] for domain in curriculum["domains"]}
    pack_domains = {
        manifest_path.parent.name
        for manifest_path in (paths.SEED_DATA_DIR / "packs").glob("*/manifest.json")
    }

    assert curriculum_domains <= pack_domains
