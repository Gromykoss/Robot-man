"""Public write and follow limit gate."""

from __future__ import annotations

try:
    from .verdict import CheckResult, Verdict
except ImportError:
    from verdict import CheckResult, Verdict


PUBLIC_WRITE_ACTIONS = {"post", "reply", "like", "repost"}
KNOWN_ACTIONS = PUBLIC_WRITE_ACTIONS | {"follow"}


def _as_non_negative_int(value: int, name: str) -> tuple[int | None, CheckResult | None]:
    if isinstance(value, bool) or not isinstance(value, int):
        return None, CheckResult(Verdict.INCONCLUSIVE, f"{name} is not an integer")
    if value < 0:
        return None, CheckResult(Verdict.INCONCLUSIVE, f"{name} is negative")
    return value, None


def check_limits(
    writes_used_today: int,
    follow_used_today: int,
    action_type: str,
    public_write_limit: int = 3,
    follow_limit: int = 10,
) -> CheckResult:
    writes_used_today, error = _as_non_negative_int(writes_used_today, "writes_used_today")
    if error:
        return error

    follow_used_today, error = _as_non_negative_int(follow_used_today, "follow_used_today")
    if error:
        return error

    public_write_limit, error = _as_non_negative_int(public_write_limit, "public_write_limit")
    if error:
        return error

    follow_limit, error = _as_non_negative_int(follow_limit, "follow_limit")
    if error:
        return error

    if not isinstance(action_type, str) or action_type not in KNOWN_ACTIONS:
        return CheckResult(Verdict.INCONCLUSIVE, "unknown action_type")

    if action_type in PUBLIC_WRITE_ACTIONS:
        if writes_used_today < public_write_limit:
            return CheckResult(Verdict.SATISFIED, "public write limit available")
        return CheckResult(Verdict.NOT_SATISFIED, "public write limit exhausted")

    if follow_used_today < follow_limit:
        return CheckResult(Verdict.SATISFIED, "follow limit available")

    if follow_used_today >= 10:
        return CheckResult(Verdict.NOT_SATISFIED, "hard follow limit reached")

    return CheckResult(Verdict.NOT_SATISFIED, "follow limit reached")
