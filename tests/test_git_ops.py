"""Tests for git_ops.show_commit argument handling."""

import shutil
import subprocess

import pytest

from tinyleaf import git_ops


pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git executable not available")


@pytest.fixture
def repo(tmp_path):
    """Create a repository with a single commit."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / "hello.txt").write_text("hello world\n", encoding="utf-8")
    subprocess.run(["git", "add", "hello.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=tmp_path, check=True)
    return tmp_path


def _head(repo):
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def test_show_commit_returns_diff(repo):
    diff = git_ops.show_commit(str(repo), _head(repo))
    assert diff.startswith("diff --git"), diff
    assert "+hello world" in diff


def test_show_commit_argument_order(repo):
    """The revision must come before the "--" path separator."""
    recorded = []

    def fake_run_git(project_dir, *args):
        recorded.append(args)
        return 0, "", ""

    original = git_ops._run_git
    git_ops._run_git = fake_run_git
    try:
        git_ops.show_commit(str(repo), "abc1234")
    finally:
        git_ops._run_git = original
    assert recorded == [("show", "--format=", "--patch", "abc1234", "--")]


def test_show_commit_rejects_invalid_hash(repo):
    assert git_ops.show_commit(str(repo), "not-a-hash") == ""


def test_show_commit_outside_repo(tmp_path):
    assert git_ops.show_commit(str(tmp_path), "abc1234") == ""
