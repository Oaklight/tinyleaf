"""Git operations via subprocess for tinyleaf."""

import os
import subprocess


def _run_git(project_dir, *args):
    """Run a git command in the project directory.

    Returns:
        Tuple of (returncode, stdout, stderr).
    """
    result = subprocess.run(
        ["git", *args],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode, result.stdout, result.stderr


def has_git(project_dir):
    """Check if a directory is a git repository."""
    return os.path.isdir(os.path.join(project_dir, ".git"))


def status(project_dir):
    """Get git status as structured data.

    Returns:
        Dict with branch, files (list of {path, status}), ahead, behind.
    """
    if not has_git(project_dir):
        return {"git": False}

    result = {"git": True, "branch": "", "files": [], "ahead": 0, "behind": 0}

    # Current branch
    rc, out, _ = _run_git(project_dir, "branch", "--show-current")
    if rc == 0:
        result["branch"] = out.strip()

    # Ahead/behind
    rc, out, _ = _run_git(project_dir, "rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if rc == 0:
        parts = out.strip().split("\t")
        if len(parts) == 2:
            result["behind"] = int(parts[0])
            result["ahead"] = int(parts[1])

    # File status
    rc, out, _ = _run_git(project_dir, "status", "--porcelain", "-u")
    if rc == 0:
        for line in out.strip().split("\n"):
            if not line:
                continue
            status_code = line[:2].strip()
            filepath = line[3:]
            result["files"].append({"path": filepath, "status": status_code})

    return result


def diff(project_dir):
    """Get git diff output."""
    if not has_git(project_dir):
        return ""
    rc, out, _ = _run_git(project_dir, "diff")
    # Also include staged diff
    rc2, out2, _ = _run_git(project_dir, "diff", "--cached")
    return out + out2


def commit(project_dir, message, files=None):
    """Stage files and commit.

    Args:
        project_dir: Project directory.
        message: Commit message.
        files: List of files to stage, or None for all.

    Returns:
        Dict with success and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    if files:
        for f in files:
            rc, _, err = _run_git(project_dir, "add", f)
            if rc != 0:
                return {"success": False, "message": f"Failed to stage {f}: {err}"}
    else:
        rc, _, err = _run_git(project_dir, "add", "-A")
        if rc != 0:
            return {"success": False, "message": f"Failed to stage: {err}"}

    rc, out, err = _run_git(project_dir, "commit", "-m", message)
    if rc != 0:
        return {"success": False, "message": err or out}

    return {"success": True, "message": out.strip()}


def push(project_dir):
    """Push to remote."""
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    rc, out, err = _run_git(project_dir, "push")
    if rc != 0:
        return {"success": False, "message": err or out}
    return {"success": True, "message": (out + err).strip()}


def pull(project_dir):
    """Pull from remote."""
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    rc, out, err = _run_git(project_dir, "pull")
    if rc != 0:
        return {"success": False, "message": err or out}
    return {"success": True, "message": (out + err).strip()}


def log(project_dir, count=20):
    """Get recent git log.

    Returns:
        List of {hash, message, author, date}.
    """
    if not has_git(project_dir):
        return []

    rc, out, _ = _run_git(
        project_dir,
        "log",
        f"-{count}",
        "--format=%H%n%s%n%an%n%aI",
    )
    if rc != 0:
        return []

    entries = []
    lines = out.strip().split("\n")
    for i in range(0, len(lines) - 3, 4):
        entries.append(
            {
                "hash": lines[i][:8],
                "message": lines[i + 1],
                "author": lines[i + 2],
                "date": lines[i + 3],
            }
        )
    return entries
