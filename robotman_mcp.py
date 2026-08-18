"""
Robot-man MCP Server — exposes content pipeline tools via Model Context Protocol.

Tools:
  - status: check all cron jobs + content queue
  - analytics: weekly follower/engagement report
  - next_post: preview next scheduled content

Run: python3 robotman_mcp.py
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROBOT_MAN_DIR = Path(__file__).parent

mcp = FastMCP("robotman-mcp")


# === Handlers ===

def handle_status():
    """Check all cron jobs and content queue state."""
    cron_out = Path.home() / ".hermes" / "cron" / "output"

    lines = ["# Robot-man Status", f"Time: {datetime.now().isoformat()}", ""]

    if cron_out.exists():
        for job_dir in sorted(cron_out.iterdir()):
            if not job_dir.is_dir():
                continue
            latest = max(job_dir.glob("*.md"), default=None, key=lambda p: p.stat().st_mtime)
            if latest:
                age = datetime.now().timestamp() - latest.stat().st_mtime
                name = latest.stem
                lines.append(f"- {job_dir.name[:8]}: {name} ({age/3600:.1f}h ago)")

    queue_file = ROBOT_MAN_DIR / ".content_queue.json"
    if queue_file.exists():
        queue = json.loads(queue_file.read_text())
        lines.append(f"\n## Content Queue ({len(queue)} items)")
        for item in queue[-5:]:
            lines.append(f"- [{item.get('status','?')}] {item.get('title','untitled')}")
    else:
        lines.append("\n## Content Queue: empty (no .content_queue.json)")

    return "\n".join(lines)


def handle_analytics():
    """Run analytics script and return summary."""
    result = subprocess.run(
        ["python3", "scripts/analytics_loop.py", "--days", "7"],
        capture_output=True, text=True, timeout=90,
        cwd=str(ROBOT_MAN_DIR)
    )
    return result.stdout or result.stderr or "No analytics data"


def handle_next_post():
    """Preview the next scheduled post."""
    queue_file = ROBOT_MAN_DIR / ".content_queue.json"
    if not queue_file.exists():
        return "No content queue found."

    queue = json.loads(queue_file.read_text())
    ready = [item for item in queue if item.get("status") == "ready"]

    if not ready:
        return "No ready posts in queue."

    return json.dumps(ready[0], indent=2, ensure_ascii=False)


# === MCP tools ===

@mcp.tool()
def status() -> str:
    """Check Robot-man cron jobs and content queue state."""
    return handle_status()


@mcp.tool()
def analytics() -> str:
    """Get weekly follower and engagement analytics."""
    return handle_analytics()


@mcp.tool()
def next_post() -> str:
    """Preview next scheduled content post."""
    return handle_next_post()


# === Main ===

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
