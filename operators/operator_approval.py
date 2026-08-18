"""Human approval gate."""

from __future__ import annotations

try:
    from .verdict import CheckResult, Verdict
except ImportError:
    from verdict import CheckResult, Verdict


KNOWN_TARGETS = {"RobotsTJ500", "@RobotsTJ500", "gromykoss", "@gromykoss"}


def check_approval(
    approval_token: str | None,
    target: str | None,
    is_production: bool,
) -> CheckResult:
    if target not in KNOWN_TARGETS:
        return CheckResult(Verdict.NOT_SATISFIED, "unknown target")

    if not is_production:
        return CheckResult(Verdict.SATISFIED, "non-production target")

    if approval_token is None:
        return CheckResult(Verdict.NOT_SATISFIED, "missing approval token")

    if not isinstance(approval_token, str):
        return CheckResult(Verdict.INCONCLUSIVE, "invalid approval token type")

    if not approval_token.strip():
        return CheckResult(Verdict.NOT_SATISFIED, "empty approval token")

    return CheckResult(Verdict.SATISFIED, "approval token present")
