"""Deterministic numeric/date fact gate."""

from __future__ import annotations

import re

try:
    from .verdict import CheckResult, Verdict
except ImportError:
    from verdict import CheckResult, Verdict


FACT_TOKEN_RE = re.compile(
    r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}\.\d{1,2}\.\d{4}|\d{4}|\d+)\b"
)


def extract_fact_tokens(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return FACT_TOKEN_RE.findall(text)


def check_fact_coverage(
    draft_text: str,
    allowed_facts: list[str] | tuple[str, ...] | None,
) -> CheckResult:
    if not isinstance(draft_text, str):
        return CheckResult(Verdict.INCONCLUSIVE, "draft_text invalid")

    tokens = extract_fact_tokens(draft_text)
    if not tokens:
        return CheckResult(Verdict.SATISFIED, "no numeric/date facts to check")

    if not allowed_facts:
        return CheckResult(Verdict.INCONCLUSIVE, "allowed_facts empty")

    try:
        facts_blob = "\n".join(str(fact) for fact in allowed_facts)
    except TypeError:
        return CheckResult(Verdict.INCONCLUSIVE, "allowed_facts invalid")

    uncovered = [token for token in tokens if token not in facts_blob]
    if uncovered:
        unique = sorted(set(uncovered), key=uncovered.index)
        return CheckResult(
            Verdict.NOT_SATISFIED,
            "uncovered fact tokens: " + ", ".join(unique),
        )

    return CheckResult(Verdict.SATISFIED, "all numeric/date facts covered")
