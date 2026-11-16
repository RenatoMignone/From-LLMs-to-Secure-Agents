"""Local artifact contract demonstration. No SDK, model calls or uploads."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[4]
IMAGE = ROOT / "assets/images/03-building-blocks/16-artifacts-and-multimodal-io/01-messages-structured-artifacts-and-lifecycle/01-artifact-lifecycle.webp"
SNAPSHOT = {"id": "S17", "product": "blue-mug", "quantity": 2}

@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    owner: str
    version: int
    media_type: str
    byte_size: int
    sha256_digest: str
    source: str
    producer: str
    storage_ref: str
    lifecycle: str
    renderer: str
    retention_policy: str

def check_report(report: dict, snapshot: dict) -> None:
    if set(report) != {"product", "quantity", "snapshot_id"}:
        raise ValueError("report fields do not match the local contract")
    if not isinstance(report["product"], str) or not isinstance(report["snapshot_id"], str):
        raise ValueError("product and snapshot ID must be strings")
    if type(report["quantity"]) is not int or report["quantity"] < 0:
        raise ValueError("quantity must be a nonnegative integer")
    if (report["product"], report["quantity"], report["snapshot_id"]) != (
        snapshot["product"], snapshot["quantity"], snapshot["id"]
    ):
        raise ValueError("report disagrees with source snapshot")

def describe(path: Path, artifact_id: str, media_type: str, source: str) -> Artifact:
    payload = path.read_bytes()
    renderers = {"application/json": "plain-json", "image/webp": "image-reference"}
    if media_type not in renderers:
        raise ValueError("unsupported renderer")
    return Artifact(artifact_id, "lee-shop" if media_type == "application/json" else "guide-maintainers",
                    1, media_type, len(payload), sha256(payload).hexdigest(), source,
                    "offline-example-v1" if media_type == "application/json" else "built-in-imagegen; guide review",
                    str(path), "active", renderers[media_type],
                    "temporary demo context" if media_type == "application/json" else "retained with repository version")

def read_verified(artifact: Artifact) -> bytes:
    if artifact.lifecycle != "active":
        raise ValueError("artifact unavailable under lifecycle policy")
    payload = Path(artifact.storage_ref).read_bytes()
    if len(payload) != artifact.byte_size or sha256(payload).hexdigest() != artifact.sha256_digest:
        raise ValueError("artifact bytes changed")
    if artifact.media_type == "application/json":
        json.loads(payload)
    elif artifact.media_type == "image/webp":
        if not (payload[:4] == b"RIFF" and payload[8:12] == b"WEBP"):
            raise ValueError("declared WebP format does not match signature")
    else:
        raise ValueError("unsupported content type")
    return payload

def build_manifest(directory: Path) -> list[Artifact]:
    report = {"product": "blue-mug", "quantity": 2, "snapshot_id": "S17"}
    check_report(report, SNAPSHOT)
    path = directory / "stock-report-v1.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    artifacts = [describe(path, "stock-report", "application/json", "mock-snapshot-S17"),
                 describe(IMAGE, "guide-illustration", "image/webp", str(IMAGE.parent / "source/01-artifact-lifecycle-prompt.txt"))]
    (directory / "manifest.json").write_text(json.dumps([asdict(a) for a in artifacts], indent=2) + "\n")
    return artifacts

def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        artifacts = build_manifest(Path(directory))
        report = json.loads(read_verified(artifacts[0]))
        check_report(report, SNAPSHOT)
        read_verified(artifacts[1])
        print("2 artifact records: report JSON and local WebP reference")
        print("size, digest, format and report/source checks passed")
        print("renderers: plain-json; image-reference (UI rendering is not implemented)")
        print("Temporary report and manifest removed on exit; repository image unchanged.")

if __name__ == "__main__":
    main()
