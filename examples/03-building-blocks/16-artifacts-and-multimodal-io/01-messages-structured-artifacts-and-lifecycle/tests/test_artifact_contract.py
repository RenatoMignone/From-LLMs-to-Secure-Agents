from dataclasses import replace
import json
from pathlib import Path
import runpy
import pytest

M = runpy.run_path(str(Path(__file__).parents[1] / "main.py"))

def test_manifest_checks_report_and_actual_local_image(tmp_path):
    artifacts = M["build_manifest"](tmp_path)
    assert len(artifacts) == 2
    for artifact in artifacts:
        assert M["read_verified"](artifact)
    assert json.loads((tmp_path / "manifest.json").read_text())[0]["source"] == "mock-snapshot-S17"

def test_changed_content_is_not_the_recorded_version(tmp_path):
    report, _ = M["build_manifest"](tmp_path)
    Path(report.storage_ref).write_text('{"quantity":999}')
    with pytest.raises(ValueError, match="bytes changed"):
        M["read_verified"](report)

def test_matching_digest_does_not_prove_semantics(tmp_path):
    artifacts = M["build_manifest"](tmp_path)
    path = Path(artifacts[0].storage_ref)
    path.write_text(json.dumps({"product":"blue-mug", "quantity":9, "snapshot_id":"S17"}))
    new_record = M["describe"](path, "stock-report", "application/json", "mock-snapshot-S17")
    payload = M["read_verified"](new_record)
    with pytest.raises(ValueError, match="disagrees"):
        M["check_report"](json.loads(payload), M["SNAPSHOT"])

def test_expiry_is_distinct_from_file_deletion(tmp_path):
    artifact, _ = M["build_manifest"](tmp_path)
    expired = replace(artifact, lifecycle="expired")
    assert Path(expired.storage_ref).exists()
    with pytest.raises(ValueError, match="lifecycle"):
        M["read_verified"](expired)

def test_boolean_is_not_an_inventory_integer():
    with pytest.raises(ValueError, match="nonnegative integer"):
        M["check_report"]({"product":"blue-mug", "quantity":True, "snapshot_id":"S17"}, M["SNAPSHOT"])
