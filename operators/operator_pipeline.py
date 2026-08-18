"""Runtime publication precheck for post_with_log.sh."""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

from .operator_account import check_account
from .operator_approval import check_approval
from .operator_factcheck import check_fact_coverage
from .operator_limits import check_limits


PROJECT_DIR = Path(__file__).resolve().parents[1]
WRITE_COUNTER_PATH = PROJECT_DIR / "data" / "write_counter.json"
APPROVAL_TOKEN_PATH = PROJECT_DIR / "data" / "approval.token"
CONTENT_BRIEF_PATH = PROJECT_DIR / "CONTENT_BRIEF.md"
DEFAULT_ALLOWED_ACCOUNTS = {"RobotsTJ500"}


def approve_post(
    draft_text: str,
    approval_token: str | None,
    account: str,
    writes_used_today: int,
    allowed_facts: list[str] | None = None,
    follow_used_today: int = 0,
    allowed_accounts: set[str] | list[str] | tuple[str, ...] = DEFAULT_ALLOWED_ACCOUNTS,
) -> tuple[bool, str]:
    checks = [
        ("account", check_account(account, allowed_accounts)),
        ("approval", check_approval(approval_token, account, is_production=True)),
        ("limits", check_limits(writes_used_today, follow_used_today, "post")),
        ("factcheck", check_fact_coverage(draft_text, allowed_facts)),
    ]

    for name, result in checks:
        if not result.passes:
            return False, f"{name}: {result.verdict.value}: {result.message}"

    return True, "all operator gates satisfied"


def _today() -> str:
    return date.today().isoformat()


def read_writes_used_today(path: Path = WRITE_COUNTER_PATH) -> int:
    if not path.exists():
        return 0

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 3

    # Valid JSON but wrong shape → fail-closed (limit exhausted), never a free pass.
    if not isinstance(data, dict) or "date" not in data:
        return 3

    # Valid dict with a stale date → new day, counter resets to 0.
    if data.get("date") != _today():
        return 0

    writes = data.get("writes", 0)
    if isinstance(writes, bool) or not isinstance(writes, int) or writes < 0:
        return 3
    return writes


def increment_writes(path: Path = WRITE_COUNTER_PATH) -> None:
    today = _today()
    writes = read_writes_used_today(path) + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"date": today, "writes": writes}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def consume_approval_token(path: Path = APPROVAL_TOKEN_PATH) -> None:
    """One-shot approval: erase the token after a successful post so a single
    'ok' from the human authorizes exactly one publication, not a window."""
    try:
        path.unlink(missing_ok=True)
    except OSError:
        # Never fail the post over a cleanup error; approval is already spent.
        pass


def read_approval_token(cli_token: str | None) -> str | None:
    if cli_token and cli_token.strip():
        return cli_token

    env_token = os.environ.get("APPROVAL_TOKEN")
    if env_token and env_token.strip():
        return env_token

    try:
        token = APPROVAL_TOKEN_PATH.read_text(encoding="utf-8")
    except OSError:
        return cli_token

    return token.strip()


def read_allowed_facts(path: Path = CONTENT_BRIEF_PATH) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return []

    return [line.strip() for line in content.splitlines() if line.strip()]


def _usage() -> str:
    return (
        "Usage: operator_pipeline.py TEXT [APPROVAL_TOKEN]\n"
        "       operator_pipeline.py --increment-write"
    )


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--increment-write":
        try:
            increment_writes()
            consume_approval_token()
        except OSError as exc:
            print(f"operator pipeline: failed to increment write counter: {exc}", file=sys.stderr)
            return 1
        return 0

    if len(argv) < 2:
        print(_usage(), file=sys.stderr)
        return 1

    draft_text = argv[1]
    cli_token = argv[2] if len(argv) > 2 else None
    account = os.environ.get("POST_ACCOUNT", "RobotsTJ500")
    token = read_approval_token(cli_token)
    writes_used_today = read_writes_used_today()
    allowed_facts = read_allowed_facts()

    ok, reason = approve_post(
        draft_text=draft_text,
        approval_token=token,
        account=account,
        writes_used_today=writes_used_today,
        allowed_facts=allowed_facts,
    )
    if ok:
        return 0

    print(f"operator pipeline blocked post: {reason}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
