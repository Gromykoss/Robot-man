#!/usr/bin/env python3
"""Append new radar IDs to radar_seen.json"""

import json
from datetime import date

# Top 15 selected posts - curated for technical relevance
new_ids = [
    # Hermes Agent (4)
    "2077275873330237601",  # @TeksCreate - Hermes overview
    "2076624300489011271",  # @witcheer - v0.18.0+ changelog
    "2078005114644877610",  # @JulianGoldieSEO - parallel tasks
    "2077936049288782304",  # @OnlyTerp - optimization guide
    # Codex CLI (2)
    "2077728951850459343",  # @grok - Codex CLI overview
    "2078040075980734968",  # @okmetom - hybrid Claude+Codex workflow
    # MCP (2)
    "2077807287381430625",  # @iatoskill - MCP overview
    "2078043654040756425",  # @GHak2learn27752 - MCP security
    # AI Agents (2)
    "2076715289769845049",  # @rohit4verse - Meta engineer agentic workflow
    "2076621270771523895",  # @AiCamila_ - self-improving agents course
    # Open Source AI (2)
    "2077292080418713662",  # @TeksCreate - top self-hosted frameworks
    "2077608472146055359",  # @leozc - xAI harness open-sourced
    # Voice Cloning (1)
    "2077173010339906019",  # @ridark_eth - CosyVoice beats ElevenLabs
    # RAG (1)
    "2076849663525945807",  # Pinecone - 7 RAG failure modes
    # Crypto Trading (1)
    "2077778168669471055",  # @DumpOnTrenches - AI Solana memecoin agent
]

with open("radar_seen.json") as f:
    data = json.load(f)

existing = set(data["seen_ids"])
added = [i for i in new_ids if i not in existing]
data["seen_ids"].extend(added)
data["last_scan"] = str(date.today())
data["total_seen"] = len(data["seen_ids"])

with open("radar_seen.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Added {len(added)} new IDs")
print(f"Total seen: {data['total_seen']}")
