"""Tests for settings persistence locking (issue #91)."""

import json
import threading

from tinyleaf import handlers


def _config(tmp_path):
    return {"config_dir": str(tmp_path)}


def test_put_settings_holds_lock_during_write(tmp_path, monkeypatch):
    observed = []
    original_write = handlers._write_settings

    def spy(config_dir, data):
        observed.append(handlers._settings_lock.locked())
        return original_write(config_dir, data)

    monkeypatch.setattr(handlers, "_write_settings", spy)
    handlers.handle_put_settings({"theme": "dark"}, _config(tmp_path))
    assert observed == [True]


def test_concurrent_updates_merge(tmp_path):
    config = _config(tmp_path)
    barrier = threading.Barrier(8)
    errors = []

    def worker(index):
        barrier.wait()
        try:
            handlers.handle_put_settings({f"key{index}": index}, config)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(index,)) for index in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors
    settings = json.loads((tmp_path / handlers.SETTINGS_FILE).read_text(encoding="utf-8"))
    assert settings == {f"key{index}": index for index in range(8)}


def test_write_leaves_no_temp_file(tmp_path):
    handlers.handle_put_settings({"a": 1}, _config(tmp_path))
    assert (tmp_path / handlers.SETTINGS_FILE).exists()
    assert not (tmp_path / (handlers.SETTINGS_FILE + ".tmp")).exists()
