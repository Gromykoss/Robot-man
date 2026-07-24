#!/usr/bin/env python3
"""Knowledge Graph for Robot-man — Anthropic Graph Engineering Playbook.
Extract → Resolve → Assemble → Query → Grounded Answer → Maintain.
No external NLP, no graph DB. Just prompts + schema + NetworkX.
"""
import os, re, json, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path
import networkx as nx

ROBOT_MAN = os.path.expanduser("~/robot-man")
GRAPH_DIR = os.path.join(ROBOT_MAN, "knowledge_graph")
GRAPH_FILE = os.path.join(GRAPH_DIR, "graph.json")
os.makedirs(GRAPH_DIR, exist_ok=True)

# ─── Stage 1: EXTRACT ───────────────────────────────────────
def extract_entities_from_file(filepath: str) -> list[dict]:
    """Extract entities and S-P-O triples from a markdown file.
    In production: DeepSeek API call with Pydantic schema.
    For pilot: regex-based extraction from structured CHRONOLOGY format."""
    triples = []
    with open(filepath) as f:
        content = f.read()
    
    # Extract from CHRONOLOGY format: ## YYYY-MM-DD — title
    for match in re.finditer(r'##\s+(\d{4}-\d{2}-\d{2})\s*[-—]\s*(.+)', content):
        date, title = match.groups()
        entity_id = f"event/{date}/{title[:40].strip()}"
        triples.append({
            "subject": entity_id,
            "predicate": "occurred_on",
            "object": date,
            "source": filepath,
            "confidence": 0.95
        })
        triples.append({
            "subject": entity_id,
            "predicate": "described_as",
            "object": title.strip(),
            "source": filepath,
            "confidence": 0.90
        })
    
    # Extract people/handles
    for handle in re.finditer(r'@(\w+)', content):
        triples.append({
            "subject": f"person/@{handle.group(1)}",
            "predicate": "mentioned_in",
            "object": os.path.basename(filepath),
            "source": filepath,
            "confidence": 0.85
        })
    
    # Extract project references
    for proj in re.finditer(r'\b(robot-man|GULAG|gooolag|Alikhan|RAB9|rab9)\b', content, re.I):
        triples.append({
            "subject": f"project/{proj.group(1).lower()}",
            "predicate": "referenced_in",
            "object": os.path.basename(filepath),
            "source": filepath,
            "confidence": 0.85
        })
    
    # Extract task references (T-XXX)
    for task in re.finditer(r'(T-\d+)', content):
        triples.append({
            "subject": f"task/{task.group(1)}",
            "predicate": "mentioned_in",
            "object": os.path.basename(filepath),
            "source": filepath,
            "confidence": 0.90
        })
    
    return triples

# ─── Stage 2: RESOLVE ────────────────────────────────────────
def resolve_entities(triples: list[dict]) -> list[dict]:
    """Cluster equivalent entities. Pilot: simple normalization."""
    aliases = {
        "project/gooolag": "project/gulag",
        "project/rab9": "project/rab9",
        "project/alikhan": "project/alikhan",
        "project/robot-man": "project/robot-man",
    }
    
    resolved = []
    for t in triples:
        t = dict(t)
        t["subject"] = aliases.get(t["subject"], t["subject"])
        t["object"] = aliases.get(t["object"], t["object"])
        resolved.append(t)
    return resolved

# ─── Stage 3: ASSEMBLE ───────────────────────────────────────
def assemble_graph(triples: list[dict]) -> nx.DiGraph:
    """Build directed graph with typed edges and provenance."""
    G = nx.DiGraph()
    for t in triples:
        s, p, o = t["subject"], t["predicate"], t["object"]
        if not G.has_node(s):
            G.add_node(s, type=s.split("/")[0] if "/" in s else "unknown")
        if not G.has_node(o):
            G.add_node(o, type=o.split("/")[0] if "/" in o else "unknown")
        G.add_edge(s, o, predicate=p, source=t["source"], confidence=t["confidence"])
    return G

# ─── Stage 4: QUERY ──────────────────────────────────────────
def query_graph(G: nx.DiGraph, center: str, hops: int = 2) -> str:
    """Serialize subgraph around center node as triple lines."""
    nodes = {center}
    frontier = {center}
    for _ in range(hops):
        nxt = set()
        for n in frontier:
            if n in G:
                nxt |= set(G.successors(n)) | set(G.predecessors(n))
        frontier = nxt - nodes
        nodes |= frontier
    
    existing = [n for n in nodes if n in G]
    if not existing:
        return f"(no nodes found for '{center}')"
    
    sub = G.subgraph(existing)
    lines = []
    for s, t, data in sub.edges(data=True):
        lines.append(f"({s}) --[{data.get('predicate','?')}]--> ({t}) [src: {Path(data.get('source','?')).name}]")
    return "\n".join(sorted(set(lines)))

def graph_stats(G: nx.DiGraph) -> dict:
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "projects": len([n for n in G.nodes if n.startswith("project/")]),
        "events": len([n for n in G.nodes if n.startswith("event/")]),
        "people": len([n for n in G.nodes if n.startswith("person/")]),
        "tasks": len([n for n in G.nodes if n.startswith("task/")]),
    }

# ─── Main ────────────────────────────────────────────────────
def build_graph():
    """Full pipeline: extract → resolve → assemble → save."""
    all_triples = []
    
    # Extract from CHRONOLOGY
    chron = os.path.join(ROBOT_MAN, "CHRONOLOGY.md")
    if os.path.exists(chron):
        all_triples.extend(extract_entities_from_file(chron))
    
    # Extract from memory
    mem = os.path.expanduser("~/.hermes/profiles/robot-man/memories/MEMORY.md")
    if os.path.exists(mem):
        all_triples.extend(extract_entities_from_file(mem))
    
    # Extract from strategy
    strat = os.path.join(ROBOT_MAN, "STRATEGY.md")
    if os.path.exists(strat):
        all_triples.extend(extract_entities_from_file(strat))
    
    # Resolve
    resolved = resolve_entities(all_triples)
    
    # Assemble
    G = assemble_graph(resolved)
    
    # Save
    data = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "stats": graph_stats(G),
        "nodes": list(G.nodes(data=True)),
        "edges": [
            {"source": s, "target": t, "predicate": d.get("predicate"), 
             "source_file": d.get("source"), "confidence": d.get("confidence")}
            for s, t, d in G.edges(data=True)
        ]
    }
    with open(GRAPH_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Stage 5: MAINTAIN — run checks after each rebuild
    try:
        sys.path.insert(0, GRAPH_DIR)
        import maintenance
        maintenance.run_report()
    except Exception as e:
        print(f"⚠️  Maintenance check failed (non-fatal): {e}", file=sys.stderr)
    
    return G

if __name__ == "__main__":
    G = build_graph()
    stats = graph_stats(G)
    print(f"📊 Knowledge Graph built: {stats['nodes']} nodes, {stats['edges']} edges")
    print(f"   📁 {stats['projects']} projects, 📅 {stats['events']} events, 👤 {stats['people']} people, 📋 {stats['tasks']} tasks")
    print(f"\n🔍 Sample queries:")
    print(f"   project/gulag (1 hop):")
    print(query_graph(G, "project/gulag", hops=1)[:300])
