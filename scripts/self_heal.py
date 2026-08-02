#!/usr/bin/env python3
"""
Self-Heal Scanner — Proactive error detection + self-improvement agent.
Stages 4-5 (Proactive + Self-improving agent).
Runs daily. Scans logs across ALL 4 projects for error patterns,
classifies, proposes fixes, and learns from outcomes.

Usage:
  python3 scripts/self_heal.py                    # Normal scan
  python3 scripts/self_heal.py --verbose          # Verbose output
  python3 scripts/self_heal.py --hours 48         # Scan window (default 48h)
  python3 scripts/self_heal.py --no-registry-check # Skip registry (fresh scan)

Safety:
  - NEVER auto-applies fixes. Only PROPOSES.
  - NEVER modifies production code.
  - NEVER reads secrets from .env files (only checks existence).
  - Exit code 0 even when errors found (scanner, not enforcer).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOME = os.environ.get("HOME", "/home/hermes-workspace")
ROOT = Path(__file__).resolve().parent.parent  # scripts/../ = robot-man/
HERMES_SCRIPTS = Path(HOME) / "hermes-agent-lab" / "scripts"
sys.path.insert(0, str(HERMES_SCRIPTS))  # For task_finish import
DATA_DIR = ROOT / "data"
REGISTRY_PATH = DATA_DIR / "self_heal_registry.json"
LEARNED_DIR = DATA_DIR / "learned_fixes"
TODAY = datetime.now(timezone.utc).strftime("%d.%m.%Y")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LEARNED_DIR, exist_ok=True)

# ── Error classification patterns ──────────────────────────────────────────

TRANSIENT_PATTERNS = [
    r"(?i)(connection\s+timed?\s*out|connect\s+timed?\s*out)",
    r"(?i)(network\s+is\s+unreachable|no\s+route\s+to\s+host)",
    r"(?i)(temporary\s+failure\s+in\s+name\s+resolution)",
    r"(?i)(broken\s+pipe|connection\s+reset\s+by\s+peer)",
    r"(?i)(errno\s+10[14].*network|socket\.gaierror)",
    r"(?i)(502\s+bad\s+gateway|503\s+service\s+unavailable|504\s+gateway\s+timeout)",
    r"(?i)(timeout|timed\s+out)(?:\s+after\s+\d+)",
]

CONFIG_PATTERNS = [
    r"(?i)(environment\s+variable.*not\s+(?:set|found))",
    r"(?i)(missing.*env|config.*missing|no\s+such\s+file)",
    r"(?i)(key\s*error|keyerror).*env",
    r"(?i)(permission\s+denied|eacces|eaccess)",
    r"(?i)(authentication\s+failed|unauthorized|invalid\s+token|401)(?!.*403)",
    r"(?i)(invalid\s+(?:api\s+)?key|api\s+key.*invalid)",
    r"(?i)(database.*collation|no\s+collation)",
]

# 403/forbidden/blocked/suspended = PERMANENT (MGT_maccha #02.08: не верить тексту ошибки,
# смотреть HTTP-код; 403 ≠ «auth failed». 403 = запрет/бан провайдера → звать человека, не ретраить)
PERMANENT_PATTERNS = [
    r"(?i)(403\s+forbidden|forbidden|access\s+denied|blocked|suspended|banned)",
    r"(?i)(not\s+allowed|not\s+authorized|permission\s+denied.*403)",
    r"(?i)(x\s+api.*403|reply.*blocked|shadowban)",
]

LOGIC_PATTERNS = [
    r"(?i)(traceback\s*\(most\s+recent\s+call\s+last\))",
    r"(?i)(attributeerror|typeerror|valueerror|keyerror)(?!.*env)",
    r"(?i)(indexerror|zerodivisionerror|filenotfounderror)",
    r"(?i)(assertionerror|notimplementederror)",
    r"(?i)(import\s+error|modulenotfounderror|no\s+module\s+named)",
    r"(?i)(syntaxerror|indentationerror|nameerror)",
    r"(?i)(cannot\s+import|could\s+not\s+import)",
]

EXTERNAL_PATTERNS = [
    r"(?i)(rate\s+limit|too\s+many\s+requests|429)",
    r"(?i)(api\s+limit\s+exceeded|quota\s+exceeded)",
    r"(?i)(upstream.*error|remote.*refused|connection\s+refused)",
    r"(?i)(dns.*fail|name.*not.*resolve)",
    r"(?i)(service\s+unavailable|503|maintenance)",
    r"(?i)(address\s+already\s+in\s+use|errno\s+98)",
    r"(?i)(x\s+api.*403|reply.*blocked|not\s+allowed)",
    r"(?i)(http\s+error\s+404|404\s+not\s+found)",
    r"(?i)(send\s+err|send.*error).*404",
    r"(?i)(mcp\s+server.*fail|mcp.*connection\s+fail|unhandled\s+errors.*taskgroup)",
    r"(?i)(bridge\s+down.*failure)",
]

# Patterns that should NOT be treated as errors (report summaries, metrics lines)
SKIP_PATTERNS = [
    r"\d+ success, \d+ fail",             # "6 success, 4 fail" summary counts
    r"\d+:\d+ \(\d+ fails?\)",            # "7:00 (2 fails)" hour summary  
    r"^##\s+(Daily\s+Success|Error\s+Type|Per\s+Category|Patterns)",  # Section headers
    r"error_report_\d{4}-\d{2}-\d{2}\.md",  # "Report written to error_report_2026-06-26.md"
    r"^#\s+Error\s+Analysis\s+Report",   # Report title
    r"Most common error type:",           # Summary line
    r"Tasks failing >\d+ times:",         # Summary line
    r"(docker-\w+|delegate|inbox|test):\s*\d+\s+success.*\d+\s+fail",  # Summary category lines
    r"Worst hour for failures:",          # Hour summary header
]

# ── Error extraction functions ─────────────────────────────────────────────

def extract_errors_from_text(text, source_name):
    """Scan a block of text for error lines + surrounding context."""
    errors = []
    error_patterns = re.compile(
        r"(?i)(error|exception|traceback|fail|fatal|critical|crash|warn(?:ing)?)",
    )
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not error_patterns.search(line):
            continue
        # Skip report summary lines and other non-error patterns
        stripped = line.strip()
        if any(re.search(p, stripped) for p in SKIP_PATTERNS):
            continue
        # Grab up to 5 lines of context
        start = max(0, i - 2)
        end = min(len(lines), i + 3)
        context = "\n".join(lines[start:end])
        errors.append({
            "source": source_name,
            "line": stripped,
            "context": context,
            "line_number": i + 1,
        })
    return errors


def classify_error(error_text):
    """Classify an error string into: transient, permanent, config, logic, external, unknown."""
    for pattern in TRANSIENT_PATTERNS:
        if re.search(pattern, error_text):
            return "transient"
    for pattern in PERMANENT_PATTERNS:
        if re.search(pattern, error_text):
            return "permanent"
    for pattern in CONFIG_PATTERNS:
        if re.search(pattern, error_text):
            return "config"
    for pattern in EXTERNAL_PATTERNS:
        if re.search(pattern, error_text):
            return "external"
    for pattern in LOGIC_PATTERNS:
        if re.search(pattern, error_text):
            return "logic"
    return "unknown"


def normalize_error(line_text):
    """Normalize an error line into a fingerprint for deduplication."""
    # Remove timestamps, IDs, hex addresses
    cleaned = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?", "", line_text)
    cleaned = re.sub(r"[0-9a-fA-F]{8,}", "<ID>", cleaned)
    cleaned = re.sub(r"0x[0-9a-fA-F]+", "<ADDR>", cleaned)
    # Collapse MCP retry attempt variants into one fingerprint
    cleaned = re.sub(r"(attempt|attempts?)\s+\d+/\d+", r"\1 <N>/<N>", cleaned)
    cleaned = re.sub(r"after \d+ attempts", "after <N> attempts", cleaned)
    cleaned = re.sub(r"retrying in \d+s", "retrying in <N>s", cleaned)
    # Normalize remaining numbers
    cleaned = re.sub(r"\b\d+\b", "<N>", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().lower()
    # Truncate to reasonable fingerprint length
    return cleaned[:120]


# ── Log source discovery ───────────────────────────────────────────────────

def discover_log_sources():
    """Auto-discover log files across all 4 projects and system sources."""
    sources = []

    # 1. Project-specific log files
    project_logs = [
        ("alikhan", "/tmp/alikhan.log"),
        ("alikhan", "/tmp/alikhan-fresh.log"),
        ("alikhan", "/tmp/alikhan_watchdog.log"),
        ("alikhan", "/tmp/alikhan-document-extractor.log"),
        ("alikhan", "/tmp/alikhan_qa_audit.log"),
        ("rab9", f"{HOME}/rab9/rab9.log"),
        ("robot-man", f"{HOME}/robot-man/engagement_log.jsonl"),
        ("robot-man", f"{HOME}/.hermes/logs/error_analyzer.log"),
        ("hermes", f"{HOME}/.hermes/logs/agent.log"),
        ("hermes", f"{HOME}/.hermes/logs/agent.log.1"),
    ]

    for project, path_str in project_logs:
        p = Path(path_str)
        if p.exists() and p.stat().st_size > 0:
            sources.append({
                "project": project,
                "path": str(p),
                "type": "file",
                "size": p.stat().st_size,
                "mtime": p.stat().st_mtime,
            })

    # 2. Systemd user journal for known services
    user_services = ["alikhan.service", "rab9-crypto-hermes.service",
                     "alikhan-document-extractor.service"]
    for svc in user_services:
        sources.append({
            "project": svc.split(".")[0].split("-")[0],
            "path": f"journalctl:user:{svc}",
            "type": "journal_user",
            "service": svc,
        })

    # 3. Systemd system journal (for gooolag-related services if any)
    sources.append({
        "project": "system",
        "path": "journalctl:system:",
        "type": "journal_system",
    })

    # 4. Hermes cron output directory (recent outputs)
    cron_output_dir = Path(f"{HOME}/.hermes/cron/output")
    if cron_output_dir.exists():
        cutoff = datetime.now() - timedelta(hours=48)
        for entry in sorted(cron_output_dir.iterdir(), key=lambda e: e.stat().st_mtime, reverse=True)[:50]:
            if entry.is_file() and entry.stat().st_mtime > cutoff.timestamp():
                sources.append({
                    "project": "hermes-cron",
                    "path": str(entry),
                    "type": "file",
                    "size": entry.stat().st_size,
                    "mtime": entry.stat().st_mtime,
                })

    return sources


def read_source(source, hours_back=48):
    """Read content from a log source, respecting time window for journal sources."""
    source_type = source["type"]

    if source_type == "file":
        path = Path(source["path"])
        if not path.exists():
            return ""
        try:
            # For large files, read tail only
            size = path.stat().st_size
            if size > 500_000:
                # Read last ~200KB
                with open(path, "rb") as f:
                    f.seek(max(0, size - 200_000))
                    return f.read().decode("utf-8", errors="replace")
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""

    elif source_type == "journal_user":
        since = (datetime.now() - timedelta(hours=hours_back)).strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = subprocess.run(
                ["journalctl", "--user", "-u", source["service"],
                 "--since", since, "--no-pager", "-n", "200"],
                capture_output=True, text=True, timeout=15,
            )
            return result.stdout if result.returncode == 0 else ""
        except Exception:
            return ""

    elif source_type == "journal_system":
        since = (datetime.now() - timedelta(hours=hours_back)).strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = subprocess.run(
                ["journalctl", "--since", since, "--no-pager", "-p", "3", "-n", "200"],
                capture_output=True, text=True, timeout=15,
            )
            # Filter for known projects
            lines = []
            for line in result.stdout.splitlines():
                if any(k in line.lower() for k in ["gulag", "gooolag", "kpz", "receiver"]):
                    lines.append(line)
            return "\n".join(lines)
        except Exception:
            return ""

    return ""


# ── Fix proposal engine ────────────────────────────────────────────────────

def propose_fix(source_project, error_class, fingerprint, raw_error):
    """Propose a concrete fix based on error class and project context."""
    fixes = []

    if error_class == "transient":
        fixes.append({
            "action": f"Retry mechanism — transient error in {source_project}",
            "suggestion": "Add exponential backoff retry: sleep 15s, 30s, 60s before retry",
            "type": "retry-pattern",
        })

    elif error_class == "permanent":
        fixes.append({
            "action": f"STOP — permanent error in {source_project}. Call a human.",
            "suggestion": "403/forbidden/blocked = provider-level ban or permission change. Retries will NOT help. Check provider status, consent, or account suspension. Do NOT work around it.",
            "type": "human-gate",
        })

    elif error_class == "config":
        if "permission denied" in raw_error.lower():
            fixes.append({
                "action": f"Check file permissions in {source_project}",
                "suggestion": "Verify file ownership and chmod settings for the affected path",
                "type": "permissions",
            })
        elif "database" in raw_error.lower() and "collation" in raw_error.lower():
            fixes.append({
                "action": f"Fix PostgreSQL collation in {source_project} DB",
                "suggestion": "Run: ALTER DATABASE evolution_db REFRESH COLLATION VERSION; or restart alikhan service",
                "type": "db-collation",
            })
        elif "env" in raw_error.lower() or "environment variable" in raw_error.lower():
            fixes.append({
                "action": f"Check .env file for {source_project}",
                "suggestion": "Verify that required environment variables are set in .env and loaded by systemd",
                "type": "env-var",
            })
        elif "auth" in raw_error.lower() or "401" in raw_error or "403" in raw_error:
            fixes.append({
                "action": f"Check API credentials for {source_project}",
                "suggestion": "Verify API keys/tokens are valid and not expired. Check xurl auth status.",
                "type": "auth-check",
            })
        else:
            fixes.append({
                "action": f"Review config for {source_project}",
                "suggestion": "Check configuration files and environment for missing or invalid settings",
                "type": "config-review",
            })

    elif error_class == "external":
        if "rate limit" in raw_error.lower() or "429" in raw_error:
            fixes.append({
                "action": f"Add rate-limit handling for {source_project}",
                "suggestion": "Implement exponential backoff on 429 responses. Add request throttling.",
                "type": "rate-limit",
            })
        elif "address already in use" in raw_error.lower() or "errno 98" in raw_error.lower():
            svc_map = {"rab9": "rab9-crypto-hermes", "alikhan": "alikhan", "robot-man": "robot-man"}
            svc = svc_map.get(source_project, source_project)
            fixes.append({
                "action": f"Port conflict in {source_project}",
                "suggestion": f"Find conflicting process: `ss -tlnp | grep <PORT>`. Then restart: `systemctl --user restart {svc}`",
                "type": "port-conflict",
            })
        elif "dns" in raw_error.lower():
            fixes.append({
                "action": "DNS resolution failure",
                "suggestion": "Check /etc/resolv.conf, verify DNS servers are reachable",
                "type": "dns-check",
            })
        else:
            fixes.append({
                "action": f"External service issue affecting {source_project}",
                "suggestion": "Check upstream service status. Add circuit breaker pattern.",
                "type": "external-check",
            })

    elif error_class == "logic":
        # Match specific Python exceptions
        if "modulenotfounderror" in raw_error.lower() or "no module named" in raw_error.lower():
            fixes.append({
                "action": f"Missing Python dependency in {source_project}",
                "suggestion": "Run: pip install <missing_module> or activate the correct venv",
                "type": "missing-dep",
            })
        elif "attributeerror" in raw_error.lower():
            fixes.append({
                "action": f"AttributeError in {source_project}",
                "suggestion": "Check for None values or missing object attributes. Add hasattr() guard or None check.",
                "type": "null-check",
            })
        elif "keyerror" in raw_error.lower():
            fixes.append({
                "action": f"KeyError in {source_project}",
                "suggestion": "Use dict.get() with default value instead of direct key access",
                "type": "keyerror-fix",
            })
        elif "typeerror" in raw_error.lower():
            fixes.append({
                "action": f"TypeError in {source_project}",
                "suggestion": "Add type conversion (str(), int()) or isinstance() check before operations",
                "type": "type-check",
            })
        elif "indexerror" in raw_error.lower():
            fixes.append({
                "action": f"IndexError in {source_project}",
                "suggestion": "Add bounds checking: if len(list) > idx: before accessing list[idx]",
                "type": "bounds-check",
            })
        elif "filenotfounderror" in raw_error.lower() or "no such file" in raw_error.lower():
            fixes.append({
                "action": f"Missing file in {source_project}",
                "suggestion": "Create the missing file/directory or verify the path. Check if it should be generated.",
                "type": "missing-file",
            })
        else:
            fixes.append({
                "action": f"Code bug in {source_project}",
                "suggestion": "Review the traceback, add error handling, and write a regression test",
                "type": "code-review",
            })

    else:  # unknown
        fixes.append({
            "action": f"Unclassified error in {source_project}",
            "suggestion": "Manual investigation needed. Check full logs for context.",
            "type": "manual-review",
        })

    return fixes


# ── Registry management ────────────────────────────────────────────────────

def load_registry():
    """Load the fix registry from JSON."""
    default = {"fixes": [], "avoid_patterns": []}
    if not REGISTRY_PATH.exists():
        return default
    try:
        with open(REGISTRY_PATH) as f:
            data = json.load(f)
            if isinstance(data, dict):
                data.setdefault("fixes", [])
                data.setdefault("avoid_patterns", [])
                return data
    except (json.JSONDecodeError, ValueError):
        pass
    return default


def save_registry(registry):
    """Save the fix registry to JSON."""
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2, default=str)


def is_avoided(fingerprint, fix_type, registry):
    """Check if this error/fix pattern has been marked as 'avoid'."""
    for entry in registry.get("avoid_patterns", []):
        if entry.get("fingerprint") == fingerprint and entry.get("fix_type") == fix_type:
            return True
    return False


def find_prior_attempt(fingerprint, fix_type, registry):
    """Find prior fix attempt for this error pattern."""
    for entry in registry.get("fixes", []):
        if entry.get("fingerprint") == fingerprint and entry.get("fix_type") == fix_type:
            return entry
    return None


def record_proposal(fingerprint, fix_type, source_project, error_class, raw_error, suggestion, registry):
    """Record a fix proposal in the registry (first occurrence = proposal only)."""
    # Check if already proposed
    for entry in registry["fixes"]:
        if entry.get("fingerprint") == fingerprint and entry.get("fix_type") == fix_type:
            entry["occurrences"] = entry.get("occurrences", 0) + 1
            entry["last_seen"] = datetime.now(timezone.utc).isoformat()
            return registry

    registry["fixes"].append({
        "fingerprint": fingerprint,
        "fix_type": fix_type,
        "source_project": source_project,
        "error_class": error_class,
        "error_snippet": raw_error[:200],
        "suggestion": suggestion,
        "occurrences": 1,
        "first_seen": datetime.now(timezone.utc).isoformat(),
        "last_seen": datetime.now(timezone.utc).isoformat(),
        "status": "proposed",  # proposed, applied_success, applied_failed, avoided
        "applied_at": None,
        "outcome": None,
    })
    return registry


# ── Learned fixes ──────────────────────────────────────────────────────────

def promote_to_learned(fix_entry):
    """If a fix succeeded 2+ times, save as a reusable skill snippet."""
    fix_type = fix_entry["fix_type"]
    filename = LEARNED_DIR / f"{fix_type}.json"

    learned = {
        "fix_type": fix_type,
        "fingerprint": fix_entry["fingerprint"],
        "error_class": fix_entry["error_class"],
        "suggestion": fix_entry["suggestion"],
        "success_count": 1,
        "first_learned": datetime.now(timezone.utc).isoformat(),
    }

    if filename.exists():
        try:
            with open(filename) as f:
                existing = json.load(f)
                existing["success_count"] = existing.get("success_count", 0) + 1
                learned = existing
        except (json.JSONDecodeError, ValueError):
            pass

    with open(filename, "w") as f:
        json.dump(learned, f, indent=2)
    return filename


def check_learned_promotions(registry):
    """Check registry for entries that should be promoted to learned fixes."""
    new_promotions = 0
    for entry in registry.get("fixes", []):
        if entry.get("status") == "applied_success" and entry.get("outcome") == "success":
            success_count = sum(
                1 for e in registry["fixes"]
                if e.get("fix_type") == entry["fix_type"]
                and e.get("status") == "applied_success"
                and e.get("outcome") == "success"
            )
            if success_count >= 2 and not (LEARNED_DIR / f"{entry['fix_type']}.json").exists():
                promote_to_learned(entry)
                new_promotions += 1
                break  # One per run
    return new_promotions


def count_learned_fixes():
    """Count existing learned fix files."""
    if not LEARNED_DIR.exists():
        return 0
    return len(list(LEARNED_DIR.glob("*.json")))


def record_failed_fix(fingerprint, fix_type, registry):
    """Mark a fix as 'avoid' so it's never proposed again."""
    registry.setdefault("avoid_patterns", [])
    # Check if already avoided
    for entry in registry["avoid_patterns"]:
        if entry.get("fingerprint") == fingerprint and entry.get("fix_type") == fix_type:
            return registry

    registry["avoid_patterns"].append({
        "fingerprint": fingerprint,
        "fix_type": fix_type,
        "marked_at": datetime.now(timezone.utc).isoformat(),
    })
    # Also mark the fix entry as avoided
    for entry in registry.get("fixes", []):
        if entry.get("fingerprint") == fingerprint and entry.get("fix_type") == fix_type:
            entry["status"] = "avoided"
    return registry


# ── Main scanner ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Self-Heal Scanner — Proactive error detection + self-improvement agent"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--hours", type=int, default=48,
                        help="Time window in hours for log scanning (default: 48)")
    parser.add_argument("--no-registry-check", action="store_true",
                        help="Skip registry check (treat all errors as new)")
    args = parser.parse_args()

    verbose = args.verbose
    hours_back = args.hours

    # ── Stage 1: Discover and read log sources ─────────────────────────
    if verbose:
        print(f"🔍 Scanning log sources (last {hours_back}h)...")

    sources = discover_log_sources()
    all_errors = []

    for src in sources:
        content = read_source(src, hours_back)
        if not content:
            continue

        errors = extract_errors_from_text(content, src["project"])
        for err in errors:
            err["error_class"] = classify_error(err["line"])
            err["fingerprint"] = normalize_error(err["line"])
        all_errors.extend(errors)

        if verbose and errors:
            print(f"  📄 {src['project']:12s} → {len(errors)} errors from {Path(src['path']).name}")

    if verbose:
        print(f"\n📊 Total raw errors extracted: {len(all_errors)}")

    # ── Stage 4: Detect repeated errors (2+ in window) ─────────────────
    if not all_errors:
        from task_finish import success
        print(f"🔧 Self-Heal Scan — {TODAY}")
        print("Errors found: 0 | Repeated: 0 | Fixable: 0")
        success("All clear. No errors detected.")
        sys.exit(0)

    # Group by fingerprint
    by_fingerprint = defaultdict(list)
    for err in all_errors:
        by_fingerprint[err["fingerprint"]].append(err)

    # Filter: 2+ occurrences = repeated
    repeated = {
        fp: errs for fp, errs in by_fingerprint.items() if len(errs) >= 2
    }

    # ── Stage 4: Classify and propose fixes ────────────────────────────
    registry = load_registry() if not args.no_registry_check else {"fixes": [], "avoid_patterns": []}
    prior_learned = count_learned_fixes()
    proposals_made = 0
    avoided_count = 0
    new_learned_promotions = 0
    report_lines = []
    errors_total = len(all_errors)
    errors_repeated = len(repeated)
    errors_fixable = 0

    for fingerprint, errs in sorted(repeated.items(), key=lambda x: -len(x[1])):
        count = len(errs)
        first = errs[0]
        source_project = first["source"]
        error_class = first["error_class"]
        raw_line = first["line"][:300]

        if verbose:
            print(f"\n🔎 [{source_project}] {error_class.upper()} — {count}x")
            print(f"   fingerprint: {fingerprint}")
            print(f"   raw: {raw_line}")

        # Propose fixes
        fix_suggestions = propose_fix(source_project, error_class, fingerprint, raw_line)
        if not fix_suggestions:
            continue

        for fix in fix_suggestions:
            fix_type = fix["type"]

            # Check if this fix pattern is on the avoid list
            if is_avoided(fingerprint, fix_type, registry):
                avoided_count += 1
                if verbose:
                    print(f"   ⛔ SKIP (avoided): {fix['action']}")
                continue

            # Check prior attempts
            prior = find_prior_attempt(fingerprint, fix_type, registry)
            prior_label = ""
            if prior:
                status = prior.get("status", "unknown")
                occs = prior.get("occurrences", 0)
                if status == "applied_success":
                    prior_label = f" (previously fixed, {occs}x)"
                elif status == "applied_failed":
                    prior_label = f" (fix attempted but failed)"
                else:
                    prior_label = f" (proposed {occs}x, not yet applied)"

            # Record the proposal
            registry = record_proposal(
                fingerprint, fix_type, source_project, error_class,
                raw_line, fix["suggestion"], registry
            )

            # Build report line
            proposals_made += 1
            errors_fixable += 1

            report_lines.append(
                f"\n⚠️ [{source_project.upper()}] {first['line'][:60]}... — {count} occurrences in {hours_back}h\n"
                f"   Fix: {fix['action']}\n"
                f"   Detail: {fix['suggestion']}\n"
                f"   Registry: {prior_label or 'first occurrence, no prior fix attempts'}"
            )

            if verbose:
                print(f"   💡 FIX: {fix['action']}")
                print(f"      → {fix['suggestion']}")
                print(f"      Registry: {prior_label or 'first occurrence'}")

    # ── Stage 5: Self-improvement — promote learned fixes ──────────────
    total_learned = prior_learned
    if not args.no_registry_check:
        new_learned_promotions = check_learned_promotions(registry)
        save_registry(registry)
        total_learned = count_learned_fixes()

        if new_learned_promotions > 0:
            report_lines.append(f"\n📚 Learned fixes: {new_learned_promotions} new, {total_learned} total in registry")

    # ── Output compact report ──────────────────────────────────────────
    print(f"\n🔧 Self-Heal Scan — {TODAY}")
    print(f"Errors found: {errors_total} | Repeated: {errors_repeated} | Fixable: {errors_fixable}")

    if avoided_count > 0:
        print(f"⛔ Avoided patterns: {avoided_count} (previously failed, not re-proposing)")

    if report_lines:
        for line in report_lines:
            print(line)
    else:
        if errors_total > 0:
            print("ℹ️  Errors found but none repeated — nothing to fix")

    # Structured outcome logging
    from task_finish import success, partial_success
    if errors_fixable == 0 and avoided_count == 0:
        success(f"Heal scan: {errors_total} total, 0 fixable, {avoided_count} avoided, {total_learned} learned")
    else:
        partial_success(
            done=[f"Scanned {errors_total} errors, {errors_repeated} repeated patterns"],
            failed=([f"{errors_fixable} fixable errors need attention"] if errors_fixable > 0 else [])
                   + ([f"{avoided_count} patterns previously avoided"] if avoided_count > 0 else []),
        )

    if new_learned_promotions > 0:
        print(f"\n📚 New learned fix pattern saved to {LEARNED_DIR}/")
        print(f"   Total learned fixes: {total_learned}")

    if verbose:
        print(f"\n💾 Registry saved to {REGISTRY_PATH}")
        print(f"   Registry entries: {len(registry.get('fixes', []))} fixes, "
              f"{len(registry.get('avoid_patterns', []))} avoided")

    # Exit 0 even with errors — this is a scanner, not an enforcer
    sys.exit(0)


if __name__ == "__main__":
    main()
