"""Git operations via subprocess for tinyleaf."""

import os
import re
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


def list_branches(project_dir):
    """List local and remote branches.

    Returns:
        Dict with current branch name, local branch list, and remote branch list.
    """
    if not has_git(project_dir):
        return {"current": "", "local": [], "remote": []}

    # Current branch
    rc, out, _ = _run_git(project_dir, "branch", "--show-current")
    current = out.strip() if rc == 0 else ""

    # Local branches
    local = []
    rc, out, _ = _run_git(project_dir, "branch", "--list", "--no-color")
    if rc == 0:
        for line in out.split("\n"):
            line = line.lstrip("* ").strip()
            if line:
                local.append(line)

    # Remote branches
    remote = []
    rc, out, _ = _run_git(project_dir, "branch", "-r", "--list", "--no-color")
    if rc == 0:
        for line in out.split("\n"):
            line = line.strip()
            if line and "HEAD ->" not in line:
                remote.append(line)

    return {"current": current, "local": local, "remote": remote}


def fetch(project_dir):
    """Fetch from all remotes.

    Returns:
        Dict with success status and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    rc, out, err = _run_git(project_dir, "fetch", "--all")
    if rc != 0:
        return {"success": False, "message": err or out}
    return {"success": True, "message": (out + err).strip()}


def switch_branch(project_dir, branch):
    """Switch to an existing branch.

    Returns:
        Dict with success status and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    rc, out, err = _run_git(project_dir, "switch", branch)
    if rc != 0:
        return {"success": False, "message": (err or out).strip()}
    return {"success": True, "message": (out + err).strip()}


def create_branch(project_dir, name, start_point=None):
    """Create and switch to a new branch.

    Returns:
        Dict with success status and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    # Validate branch name
    rc, _, err = _run_git(project_dir, "check-ref-format", "--branch", name)
    if rc != 0:
        return {"success": False, "message": f"Invalid branch name: {name}"}

    args = ["switch", "-c", name]
    if start_point:
        args.append(start_point)

    rc, out, err = _run_git(project_dir, *args)
    if rc != 0:
        return {"success": False, "message": (err or out).strip()}
    return {"success": True, "message": (out + err).strip()}


def delete_branch(project_dir, name, force=False):
    """Delete a branch.

    Returns:
        Dict with success status and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    # Refuse to delete the current branch
    rc, out, _ = _run_git(project_dir, "branch", "--show-current")
    if rc == 0 and out.strip() == name:
        return {"success": False, "message": f"Cannot delete the current branch: {name}"}

    flag = "-D" if force else "-d"
    rc, out, err = _run_git(project_dir, "branch", flag, name)
    if rc != 0:
        return {"success": False, "message": (err or out).strip()}
    return {"success": True, "message": (out + err).strip()}


def stash(project_dir):
    """Stash working directory changes.

    Returns:
        Dict with success status and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    rc, out, err = _run_git(project_dir, "stash")
    if rc != 0:
        return {"success": False, "message": (err or out).strip()}
    return {"success": True, "message": (out + err).strip()}


def stash_pop(project_dir):
    """Pop the latest stash.

    Returns:
        Dict with success status and message.
    """
    if not has_git(project_dir):
        return {"success": False, "message": "Not a git repository"}

    rc, out, err = _run_git(project_dir, "stash", "pop")
    if rc != 0:
        return {"success": False, "message": (err or out).strip()}
    return {"success": True, "message": (out + err).strip()}


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
        for line in out.split("\n"):
            line = line.rstrip()
            if not line:
                continue
            status_code = line[:2].strip()
            filepath = line[3:]
            result["files"].append({"path": filepath, "status": status_code})

    return result


def diff(project_dir, file_path=None, staged="both", fmt="text"):
    """Get git diff output.

    Args:
        project_dir: Project directory.
        file_path: Optional file path to diff. If None, diffs all files.
        staged: Which changes to include — ``"both"`` (default), ``"staged"``,
            or ``"unstaged"``.
        fmt: Output format — ``"text"`` (default, plain unified diff) or
            ``"json"`` (dict with ``staged`` and ``unstaged`` keys).

    Returns:
        When ``fmt="text"``: a plain-text unified diff string (backwards
        compatible).  When ``fmt="json"``: a dict with keys ``"staged"`` and
        ``"unstaged"``, each containing the corresponding diff text (empty
        string when nothing to show).
    """
    if not has_git(project_dir):
        if fmt == "json":
            return {"staged": "", "unstaged": ""}
        return ""

    def _untracked_pseudo_diff(fp):
        """Build a pseudo unified-diff for an untracked file."""
        full = os.path.join(project_dir, fp)
        try:
            with open(full, encoding="utf-8", errors="replace") as fh:
                content = fh.read()
        except OSError:
            return ""
        lines = content.split("\n")
        diff_lines = ["--- /dev/null", f"+++ b/{fp}", f"@@ -0,0 +1,{len(lines)} @@"]
        diff_lines.extend(f"+{line}" for line in lines)
        return "\n".join(diff_lines)

    # Build base args for unstaged/staged diffs.
    def _build_args(cached):
        args = ["diff"]
        if cached:
            args.append("--cached")
        if file_path:
            args += ["--", file_path]
        return args

    unstaged_text = ""
    staged_text = ""

    if staged in ("both", "unstaged"):
        _, unstaged_text, _ = _run_git(project_dir, *_build_args(cached=False))

    if staged in ("both", "staged"):
        _, staged_text, _ = _run_git(project_dir, *_build_args(cached=True))

    # Handle untracked files: no unstaged or staged diff exists.
    if not unstaged_text and not staged_text and file_path:
        _, out3, _ = _run_git(project_dir, "status", "--porcelain", "-u", "--", file_path)
        if out3.strip().startswith("??"):
            pseudo = _untracked_pseudo_diff(file_path)
            if fmt == "json":
                return {"staged": "", "unstaged": pseudo}
            return pseudo

    if fmt == "json":
        return {"staged": staged_text, "unstaged": unstaged_text}

    # Default text mode: concatenate (backwards compatible).
    return unstaged_text + staged_text


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


def show_commit(project_dir, commit_hash):
    """Get the diff for a specific commit.

    Args:
        project_dir: Project directory.
        commit_hash: Git commit hash (short or full).

    Returns:
        Unified diff text for the commit.
    """
    if not has_git(project_dir):
        return ""
    if not re.match(r"^[0-9a-fA-F]{4,40}$", commit_hash):
        return ""
    rc, out, _ = _run_git(project_dir, "show", "--format=", "--patch", "--", commit_hash)
    return out if rc == 0 else ""
