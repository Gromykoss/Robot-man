#!/usr/bin/env python3
"""robot-man post-gate scorer (kind: agent) — флотовый стандарт eval-gates, 20.10.2026.

Детерминированный структурный скорер кандидата на публикацию @RobotsTJ500.
Правила канона (AGENTS.md 05.09): English only, URL в теле запрещён, хэштеги = 0
по умолчанию (если в dataset-строке allow_hashtags=true — бриф явно разрешает),
ALL-CAPS хуки запрещены. Пост читает ОДНУ строку dataset.jsonl:
  {"text": "...", "mode": "post"|"reply", "allow_hashtags": false}
metrics.json: бинарные метрики, 1.0 = все строки соблюдены (агрегат по датасету).
"""
import json
import re
from pathlib import Path

CYRILLIC = re.compile(r"[\u0400-\u04FF]")
URL = re.compile(r"https?://|www\.|t\.co/", re.IGNORECASE)
ALLCAPS = re.compile(r"\b[A-Z]{5,}\b")  # ALL-CAPS прогон ≥5 букв (акронимы 2-4 букв разрешены)


def check_line(line: dict) -> dict:
    text = line.get("text", "")
    # 21.10 spec-drift fix: длина по mode — post = note_tweet до 4000 (канон),
    # reply = 500. Раньше жёсткий 500 блокировал все длинные посты.
    max_len = 4000 if line.get("mode", "post") == "post" else 500
    return {
        "cyrillic_free": 0.0 if CYRILLIC.search(text) else 1.0,
        "url_free": 0.0 if URL.search(text) else 1.0,
        "hashtags_canonical": 1.0 if (line.get("allow_hashtags", False) or "#" not in text) else 0.0,
        "caps_ok": 0.0 if ALLCAPS.search(text[:160]) else 1.0,
        "length_ok": 1.0 if 10 <= len(text) <= max_len else 0.0,
    }


rows = [json.loads(l) for l in Path("dataset.jsonl").read_text().splitlines() if l.strip()]
if not rows:
    metrics = {m: 0.0 for m in ("cyrillic_free", "url_free", "hashtags_canonical", "caps_ok", "length_ok")}
else:
    per_line = [check_line(r) for r in rows]
    metrics = {m: min(float(d[m]) for d in per_line)
               for m in ("cyrillic_free", "url_free", "hashtags_canonical", "caps_ok", "length_ok")}
Path("metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(metrics, ensure_ascii=False))
