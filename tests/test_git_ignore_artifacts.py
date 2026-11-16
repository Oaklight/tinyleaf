"""Tests for the ignore-artifacts endpoint (part of #119)."""

import shutil
import subprocess

import pytest

from tinyleaf import git_ops, handlers
from tinyleaf.server import APIError

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git executable not available")


def _single_config(tmp_path):
    return {
        "mode": "single",
        "project_path": str(tmp_path),
        "config_dir": str(tmp_path),
        "use_docker": False,
        "docker_image": "oaklight/texlive:latest",
    }


def _tracked(repo):
    out = subprocess.run(
        ["git", "ls-files"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout
    return set(out.splitlines())


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / "main.tex").write_text("hello", encoding="utf-8")
    (tmp_path / "main.aux").write_text("artifact", encoding="utf-8")
    (tmp_path / "figure.pdf").write_text("pdf", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    return tmp_path


class TestDryRun:
    def test_reports_without_touching_disk_or_index(self, repo):
        result = git_ops.ignore_build_artifacts(str(repo), dry_run=True)

        assert result["dry_run"] is True
        assert result["gitignore"] == {
            "created": True,
            "added": git_ops.artifact_gitignore_patterns(),
        }
        assert result["removed_from_index"] == ["main.aux"]
        assert result["failed"] == []
        assert not (repo / ".gitignore").exists()
        assert "main.aux" in _tracked(repo)


class TestApply:
    def test_writes_gitignore_and_untracks_but_keeps_files(self, repo):
        result = git_ops.ignore_build_artifacts(str(repo))

        content = (repo / ".gitignore").read_text(encoding="utf-8")
        assert git_ops._GITIGNORE_HEADER in content
        for pattern in git_ops.artifact_gitignore_patterns():
            assert pattern in content

        assert result["gitignore"] == {
            "created": True,
            "added": git_ops.artifact_gitignore_patterns(),
        }
        assert result["removed_from_index"] == ["main.aux"]
        assert "main.aux" not in _tracked(repo)
        assert (repo / "main.aux").exists()
        assert {"main.tex", "figure.pdf"} <= _tracked(repo)

    def test_is_idempotent(self, repo):
        git_ops.ignore_build_artifacts(str(repo))

        second = git_ops.ignore_build_artifacts(str(repo))

        assert second["gitignore"] == {"created": False, "added": []}
        assert second["removed_from_index"] == []
        content = (repo / ".gitignore").read_text(encoding="utf-8")
        assert content.count(git_ops._GITIGNORE_HEADER) == 1
        assert content.count("*.aux") == 1

    def test_preserves_existing_gitignore(self, repo):
        (repo / ".gitignore").write_text("node_modules/\n*.aux\n", encoding="utf-8")

        result = git_ops.ignore_build_artifacts(str(repo))

        content = (repo / ".gitignore").read_text(encoding="utf-8")
        assert content.startswith("node_modules/\n")
        assert "*.aux" not in result["gitignore"]["added"]
        assert content.count("*.aux") == 1
        assert content.count(git_ops._GITIGNORE_HEADER) == 1

    def test_untrack_false_leaves_index_alone(self, repo):
        result = git_ops.ignore_build_artifacts(str(repo), untrack=False)

        assert result["removed_from_index"] == []
        assert "main.aux" in _tracked(repo)
        assert (repo / ".gitignore").exists()


class TestHandler:
    def test_rejects_non_git_directory(self, tmp_path):
        with pytest.raises(APIError) as excinfo:
            handlers.handle_git_ignore_artifacts({}, _single_config(tmp_path), "project")

        assert excinfo.value.status_code == 400
        assert excinfo.value.code == "not_a_git_repository"

    def test_rejects_non_object_body(self, repo):
        with pytest.raises(APIError) as excinfo:
            handlers.handle_git_ignore_artifacts([], _single_config(repo), "project")

        assert excinfo.value.status_code == 400
        assert excinfo.value.code == "bad_request"

    def test_defaults_to_real_run(self, repo):
        result = handlers.handle_git_ignore_artifacts({}, _single_config(repo), "project")

        assert result["dry_run"] is False
        assert result["removed_from_index"] == ["main.aux"]

    def test_dry_run_without_untrack(self, repo):
        result = handlers.handle_git_ignore_artifacts(
            {"dry_run": True, "untrack": False}, _single_config(repo), "project"
        )

        assert result["dry_run"] is True
        assert result["gitignore"]["created"] is True
        assert result["removed_from_index"] == []
        assert not (repo / ".gitignore").exists()
