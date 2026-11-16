"""Tests for project path containment and destructive file operations."""

import os

import pytest

from tinyleaf import handlers
from tinyleaf._vendor.httpserver import HTTPException


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "proj"
    root.mkdir()
    (root / "notes.txt").write_text("hello", encoding="utf-8")
    (root / "sub").mkdir()
    (root / "sub" / "nested.txt").write_text("nested", encoding="utf-8")
    return root


def _single_config(project):
    return {"mode": "single", "project_path": str(project)}


def test_ensure_within_project_allows_inside(project):
    full = handlers._ensure_within_project(str(project), "sub/nested.txt")
    assert full == os.path.join(str(project), "sub", "nested.txt")


def test_ensure_within_project_rejects_sibling_prefix(tmp_path, project):
    sibling = tmp_path / "proj-secret"
    sibling.mkdir()
    (sibling / "secret.txt").write_text("secret", encoding="utf-8")

    with pytest.raises(HTTPException) as exc:
        handlers._ensure_within_project(str(project), "../proj-secret/secret.txt")
    assert exc.value.status_code == 403


def test_ensure_within_project_rejects_symlink_escape(tmp_path, project):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret", encoding="utf-8")
    try:
        os.symlink(str(outside), str(project / "link"), target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not supported")

    with pytest.raises(HTTPException) as exc:
        handlers._ensure_within_project(str(project), "link/secret.txt")
    assert exc.value.status_code == 403


@pytest.mark.parametrize("path", [".", "sub/.."])
def test_delete_file_refuses_project_root(project, path):
    before = sorted(os.listdir(project))

    with pytest.raises(HTTPException) as exc:
        handlers.handle_delete_file(_single_config(project), "proj", path)

    assert exc.value.status_code == 400
    assert sorted(os.listdir(project)) == before


def test_delete_file_removes_inside_file(project):
    result = handlers.handle_delete_file(_single_config(project), "proj", "notes.txt")

    assert result == {"path": "notes.txt", "deleted": True}
    assert not (project / "notes.txt").exists()


def test_write_file_rejects_escape(project):
    with pytest.raises(HTTPException) as exc:
        handlers.handle_write_file(
            {"content": "x"}, _single_config(project), "proj", "../escape.txt"
        )
    assert exc.value.status_code == 403


def test_rename_refuses_project_root(project):
    with pytest.raises(HTTPException) as exc:
        handlers.handle_rename_path(
            {"old_path": ".", "new_path": "moved"}, _single_config(project), "proj"
        )
    assert exc.value.status_code == 400
