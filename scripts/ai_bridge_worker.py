#!/usr/bin/env python3
"""Watch ~/ai-bridge/inbox and auto-process TASK-*.md with Codex.

This worker is intentionally simple:
- Polls inbox at a short interval for new TASK files.
- Sends a macOS notification when a task is picked up and completed.
- Calls `codex exec` to execute the task instructions.
- Writes fallback failed result if Codex exits without producing outbox result.
- Maintains ~/ai-bridge/status.json active_task and queue fields.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable


TASK_RE = re.compile(r"^TASK-\d+\.md$")


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_bridge_dirs(bridge_dir: Path) -> None:
    (bridge_dir / "inbox").mkdir(parents=True, exist_ok=True)
    (bridge_dir / "outbox").mkdir(parents=True, exist_ok=True)
    (bridge_dir / "archive").mkdir(parents=True, exist_ok=True)


def list_task_files(inbox_dir: Path) -> list[Path]:
    if not inbox_dir.exists():
        return []
    tasks = [p for p in inbox_dir.iterdir() if p.is_file() and TASK_RE.match(p.name)]
    return sorted(tasks, key=lambda p: p.name)


def task_id(task_file: Path) -> str:
    return task_file.stem


def result_file_for(task_file: Path, outbox_dir: Path) -> Path:
    return outbox_dir / f"{task_id(task_file)}.result.md"


def load_status(status_file: Path) -> dict:
    if status_file.exists():
        try:
            return json.loads(status_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"last_updated": utc_now_iso(), "active_task": None, "queue": []}


def save_status(status_file: Path, active_task: str | None, queue: Iterable[str]) -> None:
    payload = {
        "last_updated": utc_now_iso(),
        "active_task": active_task,
        "queue": list(queue),
    }
    status_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def pending_task_ids(inbox_dir: Path, outbox_dir: Path) -> list[str]:
    pending: list[str] = []
    for file in list_task_files(inbox_dir):
        if not result_file_for(file, outbox_dir).exists():
            pending.append(task_id(file))
    return pending


def notify(title: str, message: str, enabled: bool) -> None:
    if not enabled:
        return
    script = f"display notification {json.dumps(message)} with title {json.dumps(title)}"
    subprocess.run(
        ["osascript", "-e", script],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def wait_until_file_stable(file: Path, timeout_seconds: float = 3.0, check_interval: float = 0.2) -> bool:
    deadline = time.time() + timeout_seconds
    last_size = -1
    stable_reads = 0

    while time.time() < deadline:
        try:
            size = file.stat().st_size
        except FileNotFoundError:
            return False
        if size == last_size:
            stable_reads += 1
            if stable_reads >= 2:
                return True
        else:
            stable_reads = 0
            last_size = size
        time.sleep(check_interval)
    return False


def fallback_failed_result(task_file: Path, outbox_file: Path, error_summary: str) -> None:
    content = (
        f"---\n"
        f"task_id: {task_id(task_file)}\n"
        f"completed: {utc_now_iso()}\n"
        f"status: failed\n"
        f"---\n\n"
        f"## Changes Made\n"
        f"No changes were completed.\n\n"
        f"## Files Changed\n"
        f"- none\n\n"
        f"## Tests Run\n"
        f"- none\n\n"
        f"## Notes / Blockers\n"
        f"{error_summary}\n"
    )
    outbox_file.write_text(content, encoding="utf-8")


def build_codex_prompt(task_file: Path, outbox_file: Path, status_file: Path, instructions_file: Path) -> str:
    return (
        "You are the Codex execution worker for the bridge protocol.\n"
        f"Read and follow instructions in: {instructions_file}\n"
        f"Process task file: {task_file}\n"
        f"Write result file exactly here: {outbox_file}\n"
        f"Update bridge status at: {status_file}\n"
        "Execution rules:\n"
        "- Read task fully before changes.\n"
        "- Execute steps in order.\n"
        "- Do not modify/delete inbox task file.\n"
        "- Run required tests if task asks.\n"
        "- Use status: done | failed | needs_review.\n"
        "- Ensure result markdown contains required sections.\n"
        "When complete, finish with a short confirmation."
    )


def run_codex_for_task(
    *,
    task_file: Path,
    outbox_file: Path,
    status_file: Path,
    instructions_file: Path,
    workspace_dir: Path,
    codex_bin: str,
    log_file: Path,
    dry_run: bool,
) -> int:
    prompt = build_codex_prompt(task_file, outbox_file, status_file, instructions_file)

    if dry_run:
        log_file.write_text("[DRY RUN] Codex execution skipped.\n", encoding="utf-8")
        return 0

    cmd = [
        codex_bin,
        "exec",
        "--full-auto",
        "-s",
        "workspace-write",
        "-C",
        str(workspace_dir),
        prompt,
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    output = (
        f"$ {' '.join(cmd)}\n\n"
        f"exit_code={proc.returncode}\n\n"
        f"--- STDOUT ---\n{proc.stdout}\n"
        f"--- STDERR ---\n{proc.stderr}\n"
    )
    log_file.write_text(output, encoding="utf-8")
    return proc.returncode


def process_one_task(
    *,
    task_file: Path,
    bridge_dir: Path,
    workspace_dir: Path,
    codex_bin: str,
    notifications: bool,
    dry_run: bool,
) -> None:
    inbox_dir = bridge_dir / "inbox"
    outbox_dir = bridge_dir / "outbox"
    archive_dir = bridge_dir / "archive"
    status_file = bridge_dir / "status.json"
    instructions_file = workspace_dir / "CODEX-INSTRUCTIONS.md"
    outbox_file = result_file_for(task_file, outbox_dir)
    log_file = archive_dir / f"{task_id(task_file)}.worker.log"

    if not wait_until_file_stable(task_file):
        return

    queue = [tid for tid in pending_task_ids(inbox_dir, outbox_dir) if tid != task_id(task_file)]
    save_status(status_file, task_id(task_file), queue)
    notify("Codex Bridge", f"Picked up {task_id(task_file)}", notifications)

    return_code = run_codex_for_task(
        task_file=task_file,
        outbox_file=outbox_file,
        status_file=status_file,
        instructions_file=instructions_file,
        workspace_dir=workspace_dir,
        codex_bin=codex_bin,
        log_file=log_file,
        dry_run=dry_run,
    )

    if dry_run and not outbox_file.exists():
        save_status(status_file, None, pending_task_ids(inbox_dir, outbox_dir))
        notify("Codex Bridge", f"Dry-run completed for {task_id(task_file)}", notifications)
        return

    if not outbox_file.exists():
        summary = f"Worker failed before result file was produced (exit code {return_code})."
        fallback_failed_result(task_file, outbox_file, summary)

    save_status(status_file, None, pending_task_ids(inbox_dir, outbox_dir))
    notify("Codex Bridge", f"Finished {task_id(task_file)}", notifications)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Watch ~/ai-bridge/inbox and auto-run Codex tasks.")
    parser.add_argument(
        "--bridge-dir",
        default=str(Path.home() / "ai-bridge"),
        help="Bridge directory containing inbox/outbox/archive/status.json",
    )
    parser.add_argument(
        "--workspace-dir",
        default=str(Path.home() / "GAB-S-OPENCODE-WORKFLOW"),
        help="Workspace directory to pass to codex exec (-C).",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.5,
        help="Inbox poll interval in seconds.",
    )
    parser.add_argument(
        "--codex-bin",
        default="codex",
        help="Codex CLI binary path/name.",
    )
    parser.add_argument(
        "--lock-file",
        default="",
        help="Optional lock file path. Defaults to <bridge-dir>/.worker.lock",
    )
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="Disable desktop notifications.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not invoke codex; only simulate processing and status updates.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process current pending tasks once, then exit.",
    )
    return parser.parse_args()


def acquire_single_instance_lock(lock_file: Path) -> object:
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_file.open("w", encoding="utf-8")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"[bridge-worker] another worker is already running (lock: {lock_file}).")
        raise SystemExit(1)
    handle.write(f"{os.getpid()}\n")
    handle.flush()
    return handle


def main() -> int:
    args = parse_args()
    bridge_dir = Path(args.bridge_dir).expanduser().resolve()
    workspace_dir = Path(args.workspace_dir).expanduser().resolve()
    notify_enabled = not args.no_notify

    ensure_bridge_dirs(bridge_dir)
    lock_path = Path(args.lock_file).expanduser() if args.lock_file else (bridge_dir / ".worker.lock")
    _lock_handle = acquire_single_instance_lock(lock_path)
    status_file = bridge_dir / "status.json"
    if not status_file.exists():
        save_status(status_file, None, [])
    else:
        existing = load_status(status_file)
        save_status(status_file, existing.get("active_task"), existing.get("queue", []))

    inbox_dir = bridge_dir / "inbox"
    outbox_dir = bridge_dir / "outbox"

    print(f"[bridge-worker] watching: {inbox_dir}")
    print(f"[bridge-worker] workspace: {workspace_dir}")
    print(f"[bridge-worker] codex: {args.codex_bin}")

    try:
        while True:
            pending = [f for f in list_task_files(inbox_dir) if not result_file_for(f, outbox_dir).exists()]
            for task_file in pending:
                process_one_task(
                    task_file=task_file,
                    bridge_dir=bridge_dir,
                    workspace_dir=workspace_dir,
                    codex_bin=args.codex_bin,
                    notifications=notify_enabled,
                    dry_run=args.dry_run,
                )
            if args.once:
                break
            time.sleep(max(0.1, args.poll_interval))
    except KeyboardInterrupt:
        print("\n[bridge-worker] stopped.")
        save_status(status_file, None, pending_task_ids(inbox_dir, outbox_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
