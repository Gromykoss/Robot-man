"""Shared operator verdict contract."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Verdict(Enum):
    SATISFIED = "SATISFIED"
    NOT_SATISFIED = "NOT_SATISFIED"
    INCONCLUSIVE = "INCONCLUSIVE"

    @property
    def passes(self) -> bool:
        return self is Verdict.SATISFIED


@dataclass(frozen=True)
class CheckResult:
    verdict: Verdict
    message: str

    @property
    def passes(self) -> bool:
        return self.verdict.passes
