"""Tests for git operation timeouts in git_ops."""

import subprocess
from unittest.mock import patch

import pytest

from tinyleaf import git_ops


@pytest.fixture
def repo(tmp_path):
    """A directory that passes the ``has_git`` check."""
    (tmp_path / ".git").mkdir()
    return tmp_path


def _timeout(*args, **kwargs):
    raise subprocess.TimeoutExpired(cmd=kwargs.get("args", "git"), timeout=1)


def test_run_git_returns_structured_timeout_error(repo):
    with patch("tinyleaf.git_ops.subprocess.run", side_effect=_timeout):
        rc, out, err = git_ops._run_git(str(repo), "fetch", "--all")
    assert rc == 124
    assert out == ""
    assert "fetch" in err
    assert "timed out" in err


def test_run_git_uses_local_timeout_by_default(repo):
    with patch("tinyleaf.git_ops.subprocess.run") as run:
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = ""
        git_ops._run_git(str(repo), "status")
    assert run.call_args.kwargs["timeout"] == git_ops.LOCAL_TIMEOUT


@pytest.mark.parametrize("operation", ["fetch", "push", "pull"])
def test_network_operations_use_network_timeout(repo, operation):
    with patch("tinyleaf.git_ops._run_git", return_value=(0, "", "")) as run:
        getattr(git_ops, operation)(str(repo))
    assert run.call_args.kwargs["timeout"] == git_ops.NETWORK_TIMEOUT


def test_fetch_timeout_reports_failure(repo):
    with patch("tinyleaf.git_ops.subprocess.run", side_effect=_timeout):
        result = git_ops.fetch(str(repo))
    assert result["success"] is False
    assert "timed out" in result["message"]
