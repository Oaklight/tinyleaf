"""Tests for LaTeX artifact filtering in git status and commit (#117)."""

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


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / "main.tex").write_text("hello", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    return tmp_path


def _add_artifacts(path):
    (path / "main.tex").write_text("changed", encoding="utf-8")
    for name in ("main.aux", "main.log", "main.synctex.gz", "main.run.xml"):
        (path / name).write_text("artifact", encoding="utf-8")


class TestArtifactSet:
    @pytest.mark.parametrize(
        "name, extension",
        [
            ("main.aux", ".aux"),
            ("MAIN.AUX", ".aux"),
            ("main.synctex.gz", ".synctex.gz"),
            ("main.run.xml", ".run.xml"),
            ("main.fdb_latexmk", ".fdb_latexmk"),
            ("main.tex", ".tex"),
            ("figure.pdf", ".pdf"),
        ],
    )
    def test_artifact_extension(self, name, extension):
        assert git_ops.artifact_extension(name) == extension

    @pytest.mark.parametrize(
        "name",
        ["main.aux", "main.log", "main.synctex.gz", "main.run.xml", "main.xdv"],
    )
    def test_is_build_artifact(self, name):
        assert git_ops.is_build_artifact(name) is True

    @pytest.mark.parametrize("name", ["main.tex", "refs.bib", "figure.pdf"])
    def test_source_files_are_not_artifacts(self, name):
        assert git_ops.is_build_artifact(name) is False


class TestStatusFiltering:
    def test_artifacts_hidden_by_default(self, repo):
        _add_artifacts(repo)

        status = git_ops.status(str(repo))

        assert {entry["path"] for entry in status["files"]} == {"main.tex"}

    def test_include_artifacts_flag(self, repo):
        _add_artifacts(repo)

        status = git_ops.status(str(repo), include_artifacts=True)

        assert {entry["path"] for entry in status["files"]} == {
            "main.tex",
            "main.aux",
            "main.log",
            "main.synctex.gz",
            "main.run.xml",
        }

    def test_handler_reads_query_flag(self, repo):
        _add_artifacts(repo)
        config = _single_config(repo)

        default = handlers.handle_git_status({}, config, "project")
        included = handlers.handle_git_status({"include_artifacts": ["1"]}, config, "project")

        assert {entry["path"] for entry in default["files"]} == {"main.tex"}
        assert "main.aux" in {entry["path"] for entry in included["files"]}


class TestCommitGuard:
    def test_explicit_artifact_is_rejected(self, repo):
        config = _single_config(repo)

        with pytest.raises(APIError) as excinfo:
            handlers.handle_git_commit(
                {"message": "x", "files": ["main.tex", "main.aux"]}, config, "project"
            )

        assert excinfo.value.status_code == 400
        assert excinfo.value.code == "artifacts_not_allowed"
        assert excinfo.value.detail == {"paths": ["main.aux"]}

    def test_allow_artifacts_passes_paths_through(self, repo, monkeypatch):
        calls = []

        def fake_commit(project_dir, message, files=None):
            calls.append(files)
            return {"success": True, "message": "ok"}

        monkeypatch.setattr(handlers.git_ops, "commit", fake_commit)

        result = handlers.handle_git_commit(
            {"message": "x", "files": ["main.aux"], "allow_artifacts": True},
            _single_config(repo),
            "project",
        )

        assert result["success"] is True
        assert calls == [["main.aux"]]

    def test_default_commit_filters_artifacts(self, repo, monkeypatch):
        status = {
            "files": [
                {"path": "main.tex", "status": "M"},
                {"path": "main.aux", "status": "??"},
                {"path": "main.log", "status": "??"},
            ]
        }
        calls = []
        monkeypatch.setattr(handlers.git_ops, "status", lambda *a, **k: status)
        monkeypatch.setattr(
            handlers.git_ops,
            "commit",
            lambda project_dir, message, files=None: (
                calls.append(files) or {"success": True, "message": "ok"}
            ),
        )

        handlers.handle_git_commit({"message": "x"}, _single_config(repo), "project")

        assert calls == [["main.tex"]]

    def test_default_commit_with_only_artifacts_is_a_noop(self, repo, monkeypatch):
        monkeypatch.setattr(
            handlers.git_ops,
            "status",
            lambda *a, **k: {"files": [{"path": "main.aux", "status": "??"}]},
        )
        called = []
        monkeypatch.setattr(handlers.git_ops, "commit", lambda *a, **k: called.append(True))

        result = handlers.handle_git_commit({"message": "x"}, _single_config(repo), "project")

        assert result == {"success": False, "message": "No files to commit"}
        assert called == []


class TestCleanUsesSharedSet:
    def test_clean_removes_compound_artifact(self, tmp_path):
        (tmp_path / "main.tex").write_text("x", encoding="utf-8")
        (tmp_path / "main.run.xml").write_text("x", encoding="utf-8")
        (tmp_path / "main.aux").write_text("x", encoding="utf-8")

        result = handlers.handle_clean(_single_config(tmp_path), "project")

        assert set(result["removed"]) == {"main.run.xml", "main.aux"}
        assert (tmp_path / "main.tex").exists()
