"""Tests for symlink handling in handlers._build_file_tree (issue #89)."""

import os
import sys

import pytest

from tinyleaf import handlers

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="symlink tests need POSIX")


def _find(entries, name):
    for entry in entries:
        if entry["name"] == name:
            return entry
    return None


def test_self_referential_symlink_does_not_recurse(tmp_path):
    (tmp_path / "main.tex").write_text("hello", encoding="utf-8")
    os.symlink(tmp_path, tmp_path / "loop")

    tree = handlers._build_file_tree(str(tmp_path), str(tmp_path))

    loop = _find(tree, "loop")
    assert loop is not None
    assert loop["type"] == "dir"
    assert loop["children"] == []
    assert _find(tree, "main.tex") is not None


def test_symlink_to_outside_dir_is_not_traversed(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret", encoding="utf-8")
    os.symlink(outside, project / "link")

    tree = handlers._build_file_tree(str(project), str(project))

    link = _find(tree, "link")
    assert link["type"] == "dir"
    assert link["children"] == []


def test_regular_nested_directory_still_recurses(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "chapter.tex").write_text("x", encoding="utf-8")

    tree = handlers._build_file_tree(str(tmp_path), str(tmp_path))

    sub_entry = _find(tree, "sub")
    assert [child["name"] for child in sub_entry["children"]] == ["chapter.tex"]


def test_symlink_to_file_is_listed_as_file(tmp_path):
    target = tmp_path / "target.tex"
    target.write_text("x", encoding="utf-8")
    os.symlink(target, tmp_path / "alias.tex")

    tree = handlers._build_file_tree(str(tmp_path), str(tmp_path))

    alias = _find(tree, "alias.tex")
    assert alias["type"] == "file"
    assert "mtime" in alias


def test_broken_symlink_does_not_raise(tmp_path):
    os.symlink(tmp_path / "missing", tmp_path / "dangling")

    tree = handlers._build_file_tree(str(tmp_path), str(tmp_path))

    dangling = _find(tree, "dangling")
    assert dangling["type"] == "file"
