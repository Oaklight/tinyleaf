"""Tests for --browse-root resolution (#114)."""

from tinyleaf.cli import _resolve_browse_roots


def _home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home


def test_default_includes_home_and_project(tmp_path, monkeypatch):
    home = _home(tmp_path, monkeypatch)
    project = tmp_path / "project"
    project.mkdir()

    roots = _resolve_browse_roots(None, str(project), None)

    assert roots[0] == str(home)
    assert str(project) in roots


def test_default_includes_projects_dir(tmp_path, monkeypatch):
    home = _home(tmp_path, monkeypatch)
    projects = tmp_path / "projects"
    projects.mkdir()

    roots = _resolve_browse_roots(None, None, str(projects))

    assert roots == [str(home), str(projects)]


def test_default_skips_missing_extra(tmp_path, monkeypatch):
    home = _home(tmp_path, monkeypatch)

    roots = _resolve_browse_roots(None, str(tmp_path / "missing"), None)

    assert roots == [str(home)]


def test_explicit_replaces_defaults(tmp_path, monkeypatch):
    _home(tmp_path, monkeypatch)
    extra = tmp_path / "extra"
    extra.mkdir()

    roots = _resolve_browse_roots([str(extra)], str(tmp_path), str(tmp_path))

    assert roots == [str(extra)]


def test_deduplicates(tmp_path, monkeypatch):
    home = _home(tmp_path, monkeypatch)

    roots = _resolve_browse_roots(None, str(home), str(home))

    assert roots == [str(home)]
