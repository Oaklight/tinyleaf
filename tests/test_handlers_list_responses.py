"""Regression tests: list-returning handlers must produce JSON arrays.

zerodep httpserver 0.7.2 removed the list -> JSONResponse coercion. These
handlers are the endpoints that return a bare list.
"""

import json

from tinyleaf import handlers
from tinyleaf._vendor.httpserver import JSONResponse


def _body(response):
    assert isinstance(response, JSONResponse)
    return json.loads(response.body)


def test_list_projects_single_returns_json_array(tmp_path):
    config = {"mode": "single", "project_path": str(tmp_path)}

    data = _body(handlers.handle_list_projects(config))

    assert isinstance(data, list)
    assert data[0]["name"] == tmp_path.name


def test_list_files_returns_json_array(tmp_path):
    (tmp_path / "main.tex").write_text("x", encoding="utf-8")
    config = {"mode": "single", "project_path": str(tmp_path)}

    data = _body(handlers.handle_list_files(config, "proj"))

    assert isinstance(data, list)
    assert any(item["name"] == "main.tex" for item in data)


def test_list_docker_images_returns_json_array():
    data = _body(handlers.handle_list_docker_images())

    assert isinstance(data, list)
    assert data and "tag" in data[0]


def test_git_log_returns_json_array(tmp_path):
    config = {"mode": "single", "project_path": str(tmp_path)}

    data = _body(handlers.handle_git_log(config, "proj"))

    assert data == []


def test_worktree_list_returns_json_array(tmp_path):
    config = {"mode": "single", "project_path": str(tmp_path)}

    data = _body(handlers.handle_git_worktree_list(config, "proj"))

    assert data == []
