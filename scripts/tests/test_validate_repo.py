#!/usr/bin/env python3
"""Regression tests for repository validation controls."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "tmp", "__pycache__", "*.pyc"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/main.py", "validate"],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def run_state(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/main.py", "state", *arguments],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def run_main(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/main.py", *arguments],
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
        status_path = self.repo / "PROJECT_STATUS.md"
        status = status_path.read_text(encoding="utf-8")
        status_path.write_text(re.sub(r"next_recommended_unit: .*", "next_recommended_unit: P1-99-99", status), encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("next_recommended_unit must be", result.stdout)

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

    def test_svg_visual_fails(self) -> None:
        path = self.repo / "assets/images/repo-images/test.svg"
        path.write_text("<svg></svg>", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SVG is not allowed", result.stdout)

    def test_oversized_visual_fails(self) -> None:
        path = self.repo / "assets/images/repo-images/oversized.png"
        path.write_bytes(b"0" * (2_500 * 1024 + 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("visual asset exceeds 2.5 MiB source budget", result.stdout)

    def test_source_missing_field_fails(self) -> None:
        self.replace("sources/project/w3c-images-tutorial.yml", "claims_supported:", "unsupported_claims:")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source record missing field", result.stdout)

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
        path.write_text(path.read_text(encoding="utf-8") + (" noise" * 400), encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("instruction word budget exceeded", result.stdout)

    def reset_to_idle(self) -> None:
        status_path = self.repo / "PROJECT_STATUS.md"
        status = status_path.read_text(encoding="utf-8")
        status = re.sub(r"current_unit: .*", "current_unit: null", status)
        status = re.sub(r"current_unit_path: .*", "current_unit_path: null", status)
        status = re.sub(r"current_unit_state: .*", "current_unit_state: idle", status)
        status = re.sub(r"blocked_from: .*", "blocked_from: null", status)
        status = re.sub(r"completed_through: .*", "completed_through: P1-00-04", status)
        status = re.sub(r"next_recommended_unit: .*", "next_recommended_unit: P1-01-01", status)
        status = re.sub(r"units_in_review:.*", "units_in_review: []", status)
        status_path.write_text(status, encoding="utf-8")
        target = self.repo / "knowledge/01-agent-foundations/01-what-is-an-agent.md"
        if target.is_file():
            target.unlink()

    def test_state_start_resolves_and_scaffolds_next_unit(self) -> None:
        self.reset_to_idle()
        result = self.run_state("start")
        self.assertEqual(result.returncode, 0, result.stdout)
        status = (self.repo / "PROJECT_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("current_unit: P1-01-01", status)
        self.assertIn("current_unit_state: researching", status)
        chapter = self.repo / "knowledge/01-agent-foundations/01-what-is-an-agent.md"
        self.assertTrue(chapter.is_file())
        self.assertIn("learning_path: main", chapter.read_text(encoding="utf-8"))

    def test_state_resolve_returns_compact_next_unit(self) -> None:
        self.reset_to_idle()
        result = self.run_state("resolve")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("unit_id: P1-01-01", result.stdout)
        self.assertIn("chapter_path: knowledge/01-agent-foundations/01-what-is-an-agent.md", result.stdout)
        self.assertIn("local_instructions_path: knowledge/01-agent-foundations/AGENTS.md", result.stdout)
        self.assertIn("plan_path: knowledge/01-agent-foundations/chapter-plan.md", result.stdout)
        self.assertIn("mode: author", result.stdout)
        self.assertIn("learning_path: main", result.stdout)
        self.assertNotIn("P1-01-02", result.stdout)

    def test_state_resolve_reports_deep_dive_classification(self) -> None:
        self.reset_to_idle()
        status_path = self.repo / "PROJECT_STATUS.md"
        status = status_path.read_text(encoding="utf-8")
        status = re.sub(r"completed_through: .*", "completed_through: P1-03-06-03", status)
        status_path.write_text(status, encoding="utf-8")
        result = self.run_state("resolve")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("unit_id: P1-03-06-04", result.stdout)
        self.assertIn("learning_path: deep-dive", result.stdout)

    def test_state_resolve_reports_review_mode(self) -> None:
        self.reset_to_idle()
        self.assertEqual(self.run_state("start").returncode, 0)
        self.assertEqual(self.run_state("set", "drafting").returncode, 0)
        self.assertEqual(self.run_state("set", "building-assets").returncode, 0)
        self.assertEqual(self.run_state("set", "validating").returncode, 0)
        status_path = self.repo / "PROJECT_STATUS.md"
        status = status_path.read_text(encoding="utf-8")
        status = status.replace("current_unit_state: validating", "current_unit_state: review")
        status = status.replace("units_in_review: []", "units_in_review:\n- P1-00-01")
        status_path.write_text(status, encoding="utf-8")
        chapter_path = self.repo / "knowledge/00-prerequisites/02-data-control-and-trust-boundaries.md"
        chapter = chapter_path.read_text(encoding="utf-8")
        chapter = re.sub(r"status: \w+", "status: review", chapter)
        chapter_path.write_text(chapter, encoding="utf-8")
        result = self.run_state("resolve")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("mode: review", result.stdout)

    def test_state_does_not_start_two_units(self) -> None:
        self.reset_to_idle()
        self.assertEqual(self.run_state("start").returncode, 0)
        result = self.run_state("start")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already active", result.stdout)

    def test_state_block_and_resume_restore_stage(self) -> None:
        self.reset_to_idle()
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
        result = self.run_main(
            "source",
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

    def test_missing_chapter_image_folder_fails(self) -> None:
        shutil.rmtree(self.repo / "assets/images/01-agent-foundations/01-what-is-an-agent")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing chapter image folder", result.stdout)

    def test_missing_chapter_source_folder_fails(self) -> None:
        shutil.rmtree(self.repo / "sources/01-agent-foundations/01-what-is-an-agent")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing chapter source folder", result.stdout)

    def test_missing_chapter_example_folder_fails(self) -> None:
        shutil.rmtree(self.repo / "examples/01-agent-foundations/01-what-is-an-agent")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing chapter example folder", result.stdout)

    def test_omitting_optional_heading_passes(self) -> None:
        chapter = self.repo / "knowledge/01-agent-foundations/01-what-is-an-agent.md"
        content = chapter.read_text(encoding="utf-8")
        # Remove the optional Open research questions section
        trimmed = re.sub(r"## Open research questions\n\n.*?\n\n(?=## )", "", content, flags=re.DOTALL)
        chapter.write_text(trimmed, encoding="utf-8")
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_core_heading_fails(self) -> None:
        chapter = self.repo / "knowledge/01-agent-foundations/01-what-is-an-agent.md"
        content = chapter.read_text(encoding="utf-8")
        # Remove the core Why this matters section
        trimmed = re.sub(r"## Why this matters\n\n.*?\n\n(?=## )", "", content, flags=re.DOTALL)
        chapter.write_text(trimmed, encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing core heading 'Why this matters'", result.stdout)


if __name__ == "__main__":
    unittest.main()
