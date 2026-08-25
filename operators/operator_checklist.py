"""Final publication checklist gate.

Root cause (25.08 incident): both post errors (RU final instead of EN, missing
hashtags) came from the SAME defect — the final pre-publication checklist lived
only as text in CHRONOLOGY.md, so the agent could skip it. This operator makes
the deterministic part of that checklist enforced code (BLOCK), and the
heuristic part a WARN (never a false-DROP).

Deterministic → BLOCK:
  1. Language: @RobotsTJ500 auto-posts are EN-only. Cyrillic in the final text
     means an RU working draft slipped through → block.
  2. Mentions: every @handle listed in CONTENT_BRIEF.md "Mentions" must appear
     in the final text → block if missing.
  3. Media: if the brief names a concrete cover file (or "да"/"yes"), the cover
     must be provided and (for a local path) exist → block if absent.

Heuristic → WARN (never blocks):
  4. Hashtags: presence/count is quality guidance ("3-5 optional"), so absence
     is reported as a warning, not a block.
"""

from __future__ import annotations

import re
from pathlib import Path

from .verdict import CheckResult, Verdict

CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
MENTION_RE = re.compile(r"@(\w+)")
# A hashtag must start with a LETTER, not a digit: "#2 ranked" (a rank/index
# in war-story text) is not a hashtag; "#AIAgents" is. This prevents false
# "hashtags present" positives that would silence the missing-hashtags WARN.
HASHTAG_RE = re.compile(r"#[A-Za-z][\w]*")

# The only account that auto-publishes through post_with_log.sh.
EN_ONLY_ACCOUNT = "RobotsTJ500"

# Cyrillic ratio above this fraction of alphabetic chars → treat as RU text.
CYRILLIC_RATIO_BLOCK = 0.05

_BRIEF_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")

NO_MEDIA_VALUES = {"нет", "no", "none", ""}
YES_MEDIA_VALUES = {"да", "yes"}


def _normalize_account(account: str) -> str:
    return (account or "").strip().lstrip("@")


def _cyrillic_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    cyrillic = sum(1 for c in letters if CYRILLIC_RE.match(c))
    return cyrillic / len(letters)


def parse_brief_fields(brief_content: str) -> dict[str, str]:
    """Parse the 'Формат и голос' markdown table into {key: value}.

    Only table rows of the form `| Key | Value |` are captured; the header row
    (| Параметр | Значение |) and separator (|---|---|) are skipped because
    their values are 'Параметр'/'Значение' and '---' respectively — see the
    explicit exclusions below.
    """
    fields: dict[str, str] = {}
    for raw_line in (brief_content or "").splitlines():
        m = _BRIEF_ROW_RE.match(raw_line.strip())
        if not m:
            continue
        key = m.group(1).strip()
        value = m.group(2).strip()
        if not key or not value:
            continue
        if key in {"Параметр", "Значение"} or value == "---":
            continue
        if set(key) <= {"-"} or set(value) <= {"-"}:
            continue
        fields[key] = value
    return fields


def _check_language(draft_text: str, account: str) -> CheckResult | None:
    if _normalize_account(account) != EN_ONLY_ACCOUNT:
        return None
    ratio = _cyrillic_ratio(draft_text)
    if ratio > CYRILLIC_RATIO_BLOCK:
        return CheckResult(
            Verdict.NOT_SATISFIED,
            f"final language not EN (cyrillic ratio {ratio:.2f}): "
            f"{EN_ONLY_ACCOUNT} auto-posts are EN-only; publish the EN final, "
            "not the RU working draft",
        )
    return None


def _check_mentions(draft_text: str, fields: dict[str, str]) -> CheckResult | None:
    mentions_value = fields.get("Mentions", "")
    required = MENTION_RE.findall(mentions_value)
    if not required:
        return None
    present = set(MENTION_RE.findall(draft_text))
    missing = [m for m in required if m not in present]
    if missing:
        return CheckResult(
            Verdict.NOT_SATISFIED,
            "missing required mentions: " + ", ".join("@" + m for m in missing),
        )
    return None


def _check_media(
    fields: dict[str, str],
    cover_path: str | None,
) -> CheckResult | None:
    image_value = fields.get("Изображение", "")
    if not image_value:
        return None

    lowered = image_value.strip().lower()
    if lowered in NO_MEDIA_VALUES:
        return None

    # "да"/"yes" → a cover must be supplied by the caller.
    if lowered in YES_MEDIA_VALUES:
        if not cover_path:
            return CheckResult(
                Verdict.NOT_SATISFIED,
                "brief requires a cover image but none was provided",
            )
        return None

    # Otherwise the brief names a concrete file (or URL). For a local path the
    # file must exist; a URL can't be verified on disk → fall through to the
    # caller-provided cover check without blocking on existence.
    if not cover_path:
        return CheckResult(
            Verdict.NOT_SATISFIED,
            f"brief requires cover '{image_value}' but none was provided",
        )

    if image_value.startswith(("http://", "https://")):
        return None

    target = Path(image_value)
    if not target.exists():
        # Resolve relative to the robot-man project root, matching where
        # post_with_log.sh looks for image files.
        project_dir = Path(__file__).resolve().parents[1]
        target = project_dir / image_value
    if not target.exists():
        return CheckResult(
            Verdict.NOT_SATISFIED,
            f"cover image not found: {image_value}",
        )
    return None


def check_checklist(
    draft_text: str,
    brief_content: str,
    account: str,
    cover_path: str | None = None,
) -> CheckResult:
    if not isinstance(draft_text, str) or not draft_text.strip():
        return CheckResult(Verdict.NOT_SATISFIED, "draft text empty")

    fields = parse_brief_fields(brief_content)

    for result in (
        _check_language(draft_text, account),
        _check_mentions(draft_text, fields),
        _check_media(fields, cover_path),
    ):
        if result is not None and not result.passes:
            return result

    return CheckResult(Verdict.SATISFIED, "publication checklist satisfied")


def collect_checklist_warnings(draft_text: str, fields: dict[str, str]) -> list[str]:
    """Heuristic checks that only WARN, never block.

    Kept separate so the caller can print them without affecting the blocking
    verdict (false-DROP is as bad as fail-open for a publishing pipeline).
    """
    warnings: list[str] = []
    hashtags = HASHTAG_RE.findall(draft_text or "")
    mentions_value = fields.get("Mentions", "")
    required = MENTION_RE.findall(mentions_value)
    external = [m for m in required if m not in {"RobotsTJ500", "gromykoss"}]

    if not hashtags and external:
        warnings.append(
            "no hashtags while post mentions external platforms "
            f"({', '.join('@' + m for m in external)}); rule: 3-5 hashtags "
            "recommended for findability",
        )
    elif not hashtags:
        warnings.append("no hashtags (optional by rule, 3-5 recommended)")

    return warnings
