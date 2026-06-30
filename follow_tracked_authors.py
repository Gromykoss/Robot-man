#!/usr/bin/env python3
"""Gradually follow tracked X authors for @RobotsTJ500.

Dry-run is the default. Follow side effects require --execute.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
QUEUE_PATH = ROOT / "data" / "tracked_follow_queue.json"
ACCOUNT = "RobotsTJ500"
APP = "my-app"
AUTH = "oauth1"
DEFAULT_LIMIT = 2
HARD_CAP = 3
STOP_ERROR_MARKERS = (
    "429",
    "403",
    "unauthorized",
    "unauthorised",
    "forbidden",
    "auth",
    "authentication",
    "authorization",
    "rate limit",
    "rate-limit",
)


class XurlError(Exception):
    def __init__(self, message: str, returncode: int | None = None) -> None:
        super().__init__(message)
        self.returncode = returncode


def normalize_handle(handle: str) -> str:
    return handle.strip().lstrip("@")


def profile_url(handle: str) -> str:
    return f"https://x.com/{normalize_handle(handle)}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_day() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def followed_today_count(queue: list[dict[str, Any]]) -> int:
    today = utc_day()
    total = 0
    for item in queue:
        if item.get("status") != "followed":
            continue
        followed_at = str(item.get("followed_at") or "")
        if followed_at.startswith(today):
            total += 1
    return total


def load_queue(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    return data


def save_queue_atomic(path: Path, queue: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def xurl(args: list[str], timeout: int = 30) -> dict[str, Any]:
    cmd = ["xurl", "--app", APP, "--auth", AUTH, "-u", ACCOUNT] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise XurlError(message or f"xurl exited {result.returncode}", result.returncode)
    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise XurlError(f"xurl returned non-JSON output: {result.stdout[:200]}") from exc
    return parsed


def is_stop_error(error: Exception | str) -> bool:
    text = str(error).lower()
    return any(marker in text for marker in STOP_ERROR_MARKERS)


def get_account_id() -> str | None:
    data = xurl([f"/2/users/by/username/{ACCOUNT}?user.fields=id,username"], timeout=20)
    user = data.get("data", {})
    user_id = user.get("id")
    return str(user_id) if user_id else None


def fetch_following_handles() -> set[str]:
    """Best-effort read-only following lookup."""
    user_id = get_account_id()
    if not user_id:
        return set()

    handles: set[str] = set()
    pagination_token: str | None = None
    while True:
        endpoint = f"/2/users/{user_id}/following?max_results=1000&user.fields=username"
        if pagination_token:
            endpoint += f"&pagination_token={pagination_token}"
        data = xurl([endpoint], timeout=30)
        for user in data.get("data", []) or []:
            username = user.get("username")
            if username:
                handles.add(username.lower())
        pagination_token = (data.get("meta") or {}).get("next_token")
        if not pagination_token:
            break
    return handles


def mark_already_following(queue: list[dict[str, Any]], following: set[str]) -> list[str]:
    changed: list[str] = []
    for item in queue:
        if item.get("status") != "pending":
            continue
        handle = normalize_handle(str(item.get("handle", "")))
        if handle.lower() in following:
            item["status"] = "already_following"
            item["followed_at"] = item.get("followed_at") or utc_now()
            item["last_error"] = None
            changed.append(handle)
    return changed


def pending_items(queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indexed = list(enumerate(queue))
    indexed.sort(key=lambda pair: (0 if pair[1].get("priority") == "high" else 1, pair[0]))
    return [item for _, item in indexed if item.get("status") == "pending"]


def follow_handle(handle: str) -> dict[str, Any]:
    return xurl(["follow", f"@{normalize_handle(handle)}"], timeout=30)


def validate_limit(limit: int, force_over_cap: bool) -> None:
    if limit < 1:
        raise SystemExit("--limit must be at least 1")
    if limit > HARD_CAP and not force_over_cap:
        raise SystemExit(f"Refusing --limit {limit}; max is {HARD_CAP} unless --force-over-cap is explicit")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Plan only; this is also the default")
    mode.add_argument("--execute", action="store_true", help="Actually follow selected pending handles")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max follows this run; default {DEFAULT_LIMIT}")
    parser.add_argument("--force-over-cap", action="store_true", help=f"Allow --limit above {HARD_CAP}; requires explicit user instruction")
    parser.add_argument("--queue", type=Path, default=QUEUE_PATH, help="Queue JSON path")
    parser.add_argument("--skip-following-check", action="store_true", help="Skip read-only already-following detection")
    parser.add_argument("--min-sleep", type=float, default=45.0, help="Minimum seconds between execute follows")
    parser.add_argument("--max-sleep", type=float, default=120.0, help="Maximum seconds between execute follows")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    execute = bool(args.execute)
    validate_limit(args.limit, args.force_over_cap)
    if args.max_sleep < args.min_sleep:
        raise SystemExit("--max-sleep must be greater than or equal to --min-sleep")

    queue = load_queue(args.queue)
    changed = False
    already: list[str] = []

    if not args.skip_following_check:
        try:
            following = fetch_following_handles()
            already = mark_already_following(queue, following)
            changed = bool(already)
        except Exception as exc:
            if is_stop_error(exc):
                print(f"STOP: following check failed with auth/rate-limit error: {exc}", file=sys.stderr)
                return 2
            print(f"WARN: could not check current following; continuing without skip detection: {exc}", file=sys.stderr)

    today_count = followed_today_count(queue)
    remaining_today = max(args.limit - today_count, 0)
    actionable = pending_items(queue)
    selected = actionable[:remaining_today]

    if not selected and not already and not actionable:
        if changed:
            save_queue_atomic(args.queue, queue)
        print("[SILENT]")
        return 0

    if already:
        for handle in already:
            print(f"already_following @{handle} {profile_url(handle)}")

    if not execute:
        if changed:
            save_queue_atomic(args.queue, queue)
        if actionable and not selected:
            print(f"DRY RUN: daily follow cap reached ({today_count}/{args.limit}/day)")
        elif selected:
            print(f"DRY RUN: would follow {len(selected)} tracked author(s), daily={today_count}/{args.limit}")
            for idx, item in enumerate(selected, 1):
                handle = normalize_handle(str(item["handle"]))
                print(f"would_follow @{handle} {profile_url(handle)} {today_count + idx}/day")
        return 0

    if actionable and not selected:
        if changed:
            save_queue_atomic(args.queue, queue)
        print(f"daily follow cap reached ({today_count}/{args.limit}/day)")
        return 0

    followed_count = 0
    for item in selected:
        handle = normalize_handle(str(item["handle"]))
        try:
            follow_handle(handle)
        except Exception as exc:
            item["last_error"] = str(exc)
            changed = True
            save_queue_atomic(args.queue, queue)
            print(f"STOP: failed @{handle} {profile_url(handle)}: {exc}", file=sys.stderr)
            if is_stop_error(exc):
                return 2
            return 1

        followed_count += 1
        item["status"] = "followed"
        item["followed_at"] = utc_now()
        item["last_error"] = None
        changed = True
        print(f"followed @{handle} {profile_url(handle)} {today_count + followed_count}/day")
        save_queue_atomic(args.queue, queue)

        if followed_count < len(selected):
            delay = random.uniform(args.min_sleep, args.max_sleep)
            print(f"sleeping {delay:.1f}s before next follow")
            time.sleep(delay)

    if changed:
        save_queue_atomic(args.queue, queue)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
