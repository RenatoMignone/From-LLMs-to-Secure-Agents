#!/usr/bin/env python3
"""Regression tests for repository validation controls."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "tmp", "__pycache__", "*.pyc"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/validate_repo.py"],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def run_state(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/project_state.py", *arguments],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def run_script(self, script: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", f"scripts/{script}", *arguments],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.repo / relative
        content = path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def test_clean_repository_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_wrong_next_unit_fails(self) -> None:
        self.replace("PROJECT_STATUS.md", "next_recommended_unit: P1-00-04", "next_recommended_unit: P1-01-01")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("next_recommended_unit must be P1-00-04", result.stdout)

    def test_roadmap_plan_drift_fails(self) -> None:
        self.replace("ROADMAP.md", "Execution boundaries and threat-independent requirements", "Execution boundaries and requirements")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("roadmap and plan filename drift", result.stdout)

    def test_chapter_learning_path_mismatch_fails(self) -> None:
        self.replace(
            "knowledge/00-prerequisites/01-reader-contract-and-system-map.md",
            "learning_path: main",
            "learning_path: deep-dive",
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("chapter learning_path mismatch", result.stdout)

    def test_visual_checksum_fails(self) -> None:
        self.replace("assets/images/repo-images/manifest.yml", "4327b1a3", "0327b1a3")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("visual checksum mismatch", result.stdout)

    def test_visual_dimensions_fail(self) -> None:
        self.replace("assets/images/repo-images/manifest.yml", "width: 2172", "width: 2173")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("visual media metadata mismatch", result.stdout)

    def test_source_schema_fails(self) -> None:
        self.replace("sources/project/w3c-images-tutorial.yml", "claims_supported:", "unsupported_claims:")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema error", result.stdout)

    def test_source_record_cannot_belong_to_multiple_units(self) -> None:
        self.replace(
            "sources/project/w3c-images-tutorial.yml",
            "unit_ids: []",
            "unit_ids:\n  - P1-00-01\n  - P1-00-02",
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("more than one unit", result.stdout)

    def test_instruction_budget_fails(self) -> None:
        path = self.repo / "AGENTS.md"
        path.write_text(path.read_text(encoding="utf-8") + (" noise" * 100), encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("instruction word budget exceeded", result.stdout)

    def test_state_start_resolves_and_scaffolds_next_unit(self) -> None:
        result = self.run_state("start")
        self.assertEqual(result.returncode, 0, result.stdout)
        status = (self.repo / "PROJECT_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("current_unit: P1-00-04", status)
        self.assertIn("current_unit_state: researching", status)
        chapter = self.repo / "knowledge/00-prerequisites/04-identity-authority-and-least-privilege-primer.md"
        self.assertTrue(chapter.is_file())
        self.assertIn("learning_path: main", chapter.read_text(encoding="utf-8"))

    def test_state_resolve_returns_compact_next_unit(self) -> None:
        result = self.run_state("resolve")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("unit_id: P1-00-04", result.stdout)
        self.assertIn("chapter_path: knowledge/00-prerequisites/04-identity-authority-and-least-privilege-primer.md", result.stdout)
        self.assertIn("local_instructions_path: knowledge/00-prerequisites/AGENTS.md", result.stdout)
        self.assertIn("plan_path: knowledge/00-prerequisites/chapter-plan.md", result.stdout)
        self.assertIn("mode: author", result.stdout)
        self.assertIn("learning_path: main", result.stdout)
        self.assertNotIn("P1-01-01", result.stdout)

    def test_state_resolve_reports_deep_dive_classification(self) -> None:
        self.replace("PROJECT_STATUS.md", "completed_through: P1-00-03", "completed_through: P1-03-06-03")
        result = self.run_state("resolve")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("unit_id: P1-03-06-04", result.stdout)
        self.assertIn("learning_path: deep-dive", result.stdout)

    def test_state_resolve_reports_review_mode(self) -> None:
        self.assertEqual(self.run_state("start").returncode, 0)
        self.assertEqual(self.run_state("set", "drafting").returncode, 0)
        self.assertEqual(self.run_state("set", "building-assets").returncode, 0)
        self.assertEqual(self.run_state("set", "validating").returncode, 0)
        status_path = self.repo / "PROJECT_STATUS.md"
        status = status_path.read_text(encoding="utf-8")
        status_path.write_text(status.replace("current_unit_state: validating", "current_unit_state: review").replace("units_in_review: []", "units_in_review:\n- P1-00-01"), encoding="utf-8")
        chapter_path = self.repo / "knowledge/00-prerequisites/02-data-control-and-trust-boundaries.md"
        chapter = chapter_path.read_text(encoding="utf-8")
        chapter_path.write_text(chapter.replace("status: outline", "status: review"), encoding="utf-8")
        result = self.run_state("resolve")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("mode: review", result.stdout)

    def test_state_does_not_start_two_units(self) -> None:
        self.assertEqual(self.run_state("start").returncode, 0)
        result = self.run_state("start")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already active", result.stdout)

    def test_state_block_and_resume_restore_stage(self) -> None:
        self.assertEqual(self.run_state("start").returncode, 0)
        self.assertEqual(self.run_state("block", "Missing authoritative source").returncode, 0)
        blocked = (self.repo / "PROJECT_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("current_unit_state: blocked", blocked)
        self.assertIn("blocked_from: researching", blocked)
        self.assertIn("mode: blocked", self.run_state("resolve").stdout)
        self.assertEqual(self.run_state("resume").returncode, 0)
        resumed = (self.repo / "PROJECT_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("current_unit_state: researching", resumed)
        self.assertIn("blocked_from: null", resumed)

    def test_source_registration_generates_valid_record(self) -> None:
        result = self.run_script(
            "register_source.py",
            "--id", "example-source",
            "--title", "Example Source",
            "--organization", "Example Organization",
            "--source-type", "official documentation",
            "--url", "https://example.com/source",
            "--claim", "Supports the example claim.",
            "--limitation", "Used only to test metadata generation.",
            "--used-in", "README.md",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        validation = self.run_validator()
        self.assertEqual(validation.returncode, 0, validation.stdout)

    def test_visual_registration_generates_valid_manifest(self) -> None:
        result = self.run_script(
            "register_visual.py",
            "--unit-id", "project",
            "--id", "readme-banner",
            "--title", "From LLMs to Secure Agents banner",
            "--kind", "generated",
            "--file", "images/repo-images/banner.png",
            "--creator", "Project author",
            "--license", "Project-owned generated asset",
            "--alt", "A technical guide banner.",
            "--caption", "The project path from models to secure agents.",
            "--used-in", "README.md",
            "--prompt-file", "images/repo-images/source/prompt.txt",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        validation = self.run_validator()
        self.assertEqual(validation.returncode, 0, validation.stdout)

    def test_missing_chapter_image_folder_fails(self) -> None:
        shutil.rmtree(self.repo / "assets/images/01-agent-foundations/01-what-is-an-agent")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing chapter image folder", result.stdout)

    def test_visual_registration_rejects_flat_unit_folder(self) -> None:
        wrong_folder = self.repo / "assets/images/p1-00-01"
        wrong_folder.mkdir()
        shutil.copy2(
            self.repo / "assets/images/00-prerequisites/01-reader-contract-and-system-map/01-system-context.png",
            wrong_folder / "test.png",
        )
        result = self.run_script(
            "register_visual.py",
            "--unit-id", "P1-00-01",
            "--id", "wrong-folder",
            "--title", "Wrong folder",
            "--kind", "diagram",
            "--file", "images/p1-00-01/test.png",
            "--creator", "Test",
            "--license", "Test-only",
            "--alt", "Test",
            "--caption", "Test",
            "--used-in", "knowledge/00-prerequisites/01-reader-contract-and-system-map.md",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("visual must be directly under assets/images/00-prerequisites/01-reader-contract-and-system-map/", result.stdout)

    def test_visual_registration_rejects_svg(self) -> None:
        path = self.repo / "assets/images/repo-images/test.svg"
        path.write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
        result = self.run_script(
            "register_visual.py",
            "--unit-id", "project",
            "--id", "svg-test",
            "--title", "SVG test",
            "--kind", "diagram",
            "--file", "images/repo-images/test.svg",
            "--creator", "Test",
            "--license", "Test-only",
            "--alt", "Test",
            "--caption", "Test",
            "--used-in", "README.md",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SVG is not allowed", result.stdout)

    def test_downloaded_visual_requires_provenance(self) -> None:
        result = self.run_script(
            "register_visual.py",
            "--unit-id", "project",
            "--id", "download-test",
            "--title", "Download test",
            "--kind", "downloaded",
            "--file", "images/repo-images/banner.png",
            "--creator", "Test",
            "--license", "Test-only",
            "--alt", "Test",
            "--caption", "Test",
            "--used-in", "README.md",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("downloaded visual requires provenance fields", result.stdout)


if __name__ == "__main__":
    unittest.main()
