"""
Robot-man MCP Server — exposes content pipeline tools via Model Context Protocol.

Tools:
  - status: check all cron jobs + content queue
  - analytics: weekly follower/engagement report
  - next_post: preview next scheduled content
  
Run: python3 robotman_mcp.py
"""

import json
import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path

ROBOT_MAN_DIR = Path(__file__).parent


# === Handlers ===

def handle_status():
    """Check all cron jobs and content queue state."""
    cron_out = Path.home() / ".hermes" / "cron" / "output"
    
    lines = ["# Robot-man Status", f"Time: {datetime.now().isoformat()}", ""]
    
    # Check cron output files
    if cron_out.exists():
        for job_dir in sorted(cron_out.iterdir()):
            if not job_dir.is_dir():
                continue
            latest = max(job_dir.glob("*.md"), default=None, key=lambda p: p.stat().st_mtime)
            if latest:
                age = datetime.now().timestamp() - latest.stat().st_mtime
                name = latest.stem
                lines.append(f"- {job_dir.name[:8]}: {name} ({age/3600:.1f}h ago)")
    
    # Content queue
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
        ["python3", "analytics.py", "--summary"],
        capture_output=True, text=True, timeout=60,
        cwd=str(ROBOT_MAN_DIR)
    )
    return result.stdout or result.stderr or "No analytics data"


def handle_next_post():
    """Preview the next scheduled post."""
    queue_file = ROBOT_MAN_DIR / ".content_queue.json"
    if not queue_file.exists():
        return "No content queue found. Run `xurl search` to populate."
    
    queue = json.loads(queue_file.read_text())
    ready = [item for item in queue if item.get("status") == "ready"]
    
    if not ready:
        return "No ready posts in queue."
    
    post = ready[0]
    return json.dumps(post, indent=2, ensure_ascii=False)


TOOLS = {
    "status": handle_status,
    "analytics": handle_analytics,
    "next_post": handle_next_post,
}


# === MCP Server ===

def main():
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool
    
    server = Server("robotman-mcp")
    
    @server.list_tools()
    async def list_tools():
        return [
            Tool(name="status", description="Check Robot-man cron jobs and content queue state", inputSchema={"type": "object", "properties": {}}),
            Tool(name="analytics", description="Get weekly follower and engagement analytics", inputSchema={"type": "object", "properties": {}}),
            Tool(name="next_post", description="Preview next scheduled content post", inputSchema={"type": "object", "properties": {}}),
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        from mcp.types import TextContent
        if name not in TOOLS:
            return [TextContent(type="text", text=f"Unknown tool: {name}. Available: {', '.join(TOOLS)}")]
        try:
            result = TOOLS[name]()
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    import asyncio
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
