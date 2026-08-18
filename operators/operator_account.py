"""Account allow-list gate."""

from __future__ import annotations

from collections.abc import Iterable

try:
    from .verdict import CheckResult, Verdict
except ImportError:
    from verdict import CheckResult, Verdict


def _normalize_account(account: str) -> str:
    return account.strip().lstrip("@")


def check_account(
    requested_account: str | None,
    allowed_accounts: Iterable[str] | None,
) -> CheckResult:
    if allowed_accounts is None:
        return CheckResult(Verdict.INCONCLUSIVE, "allowed_accounts missing")

    if isinstance(allowed_accounts, str):
        allowed_accounts = [allowed_accounts]

    try:
        allowed = {
            _normalize_account(account)
            for account in allowed_accounts
            if isinstance(account, str) and account.strip()
        }
    except TypeError:
        return CheckResult(Verdict.INCONCLUSIVE, "allowed_accounts invalid")

    if not allowed:
        return CheckResult(Verdict.INCONCLUSIVE, "allowed_accounts empty")

    if requested_account is None:
        return CheckResult(Verdict.NOT_SATISFIED, "requested_account missing")

    if not isinstance(requested_account, str) or not requested_account.strip():
        return CheckResult(Verdict.NOT_SATISFIED, "requested_account empty")

    normalized = _normalize_account(requested_account)
    if normalized in allowed:
        return CheckResult(Verdict.SATISFIED, "account allowed")

    return CheckResult(Verdict.NOT_SATISFIED, "account not allowed")
