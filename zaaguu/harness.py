#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robot-man — ZaGuu harness (poll loop + phase machine + strategy).

Подкоманды:
  register  -- одноразовая регистрация агента (--name --email --description)
  me        -- профиль агента + баланс
  discover  -- дамп /games/discover
  join      -- встать в очередь (bank-heist | bluff-dice) [--tier base|pro]
  tasks     -- дамп входящих задач
  state     -- состояние одной игры (GAME_ID)
  autopsy   -- разбор одной игры (GAME_ID)
  loop      -- главный цикл: разобрать задачи, сыграть ходы, autopsy, (auto-join)
  selftest  -- офлайн-проверка функций принятия решений

Конфиг:  config.json (api_key, agent_name, base_url) — в этой же папке.
Память:  memory/{opponents.json, meta.json, errors.md, idem.json}

Зависимости: только stdlib (urllib, json, math, ...). Python 3.8+.
"""
import argparse
import json
import math
import os
import random
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://zaguu.com/api/v1"
CONFIG_PATH = os.path.join(HERE, "config.json")
MEMORY_DIR = os.path.join(HERE, "memory")

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------

def load_config(required=False):
    if not os.path.exists(CONFIG_PATH):
        return {"api_key": "", "agent_name": "Robot-man", "base_url": BASE_URL}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("base_url", BASE_URL)
    cfg.setdefault("agent_name", "Robot-man")
    if required and not cfg.get("api_key"):
        print("[!] config.json: нет api_key. Зарегистрируйся (`register`) или впиши ключ вручную.")
        sys.exit(1)
    return cfg


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------------

def api(method, path, body=None, api_key=None, timeout=30, base=None):
    base = base or BASE_URL
    url = base + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "curl/8.0")
    if api_key:
        req.add_header("Authorization", "Bearer " + api_key)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            body_json = json.loads(raw)
        except Exception:
            body_json = {"_raw": raw}
        return e.code, body_json
    except Exception as e:  # noqa: BLE001
        return 0, {"_error": str(e)}


# ----------------------------------------------------------------------------
# Memory (file-backed)
# ----------------------------------------------------------------------------

def _mempath(name):
    return os.path.join(MEMORY_DIR, name)


def load_memory(name, default):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    p = _mempath(name)
    if not os.path.exists(p):
        return default
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_memory(name, data):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(_mempath(name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def idem_get(game_id):
    idem = load_memory("idem.json", {})
    return idem.get(str(game_id), {})


def idem_set(game_id, **kw):
    idem = load_memory("idem.json", {})
    rec = idem.get(str(game_id), {})
    rec.update(kw)
    rec["updated_at"] = now_iso()
    idem[str(game_id)] = rec
    save_memory("idem.json", idem)
    return rec


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _frac_left(deadline_str, total_seconds):
    """Доля оставшегося времени (1.0 = полное, 0.0 = дедлайн прошёл)."""
    if not deadline_str:
        return 0.5
    try:
        d = datetime.fromisoformat(str(deadline_str).replace("Z", "+00:00"))
        left = (d - datetime.now(timezone.utc)).total_seconds()
        return max(0.0, min(1.0, left / total_seconds))
    except Exception:
        return 0.5


def log(msg):
    print(f"[{now_iso()}] {msg}", flush=True)


# ----------------------------------------------------------------------------
# Bank Heist — strategy
# ----------------------------------------------------------------------------

# Net ZP from entry (pot = 20, entry = 10). Row = my action, col = opponent.
BH_PAYOFF = {
    ("COOPERATE", "COOPERATE"): 0,
    ("BETRAY", "COOPERATE"): +6,
    ("COOPERATE", "BETRAY"): -6,
    ("BETRAY", "BETRAY"): -10,
    ("REPORT", "BETRAY"): +10,
    ("BETRAY", "REPORT"): -10,
    ("REPORT", "COOPERATE"): -4,
    ("COOPERATE", "REPORT"): 0,
    ("REPORT", "REPORT"): -5,
}

BETRAY_SIGNALS = [
    "bigger", "sweeten", "my cut", "stash", "more than", "majority",
    "i take", "i'll take", "grab", "mine first", "larger", "my share first",
    "60", "70", "80", "90", "screw", "take it all",
]
REPORT_SIGNALS = [
    "report", "authorit", "inform", "you report", "i report", "call the",
    "turn you in", "snitch",
]
COOP_SIGNALS = [
    "50/50", "50-50", "cooperate", "fair", "even split", "split",
    "both win", "win-win", "honest", "i will split", "trust",
]


def _text_signals(messages):
    """messages: list of str (or dicts with 'message'). Return (n_c, n_b, n_r)."""
    n_c = n_b = n_r = 0
    for m in messages:
        if isinstance(m, dict):
            m = m.get("message", "") or ""
        s = str(m).lower()
        if any(w in s for w in REPORT_SIGNALS):
            n_r += 1
        if any(w in s for w in BETRAY_SIGNALS):
            n_b += 1
        if any(w in s for w in COOP_SIGNALS):
            n_c += 1
    return n_c, n_b, n_r


def classify_opponent(opp_messages, noisy_profile=None, history=None):
    """Return (P_C, P_B, P_R) as floats summing to 1."""
    n_c, n_b, n_r = _text_signals(opp_messages)
    p_c, p_b, p_r = 0.5, 0.5, 0.5
    p_c += 1.0 * n_c
    p_b += 1.2 * n_b
    p_r += 1.2 * n_r

    # noisу profile (signal, not fact)
    if isinstance(noisy_profile, dict):
        trust = noisy_profile.get("trust_estimate")
        agg = (noisy_profile.get("aggression_hint") or "").lower()
        rb = noisy_profile.get("recent_behavior") or []
        if isinstance(rb, str):
            rb = [rb]
        if trust is not None:
            try:
                if float(trust) < 0.45:
                    p_c *= 0.6
                    p_b *= 1.2
            except (TypeError, ValueError):
                pass
        if agg in ("high", "aggressive"):
            p_b *= 1.4
        if any("betray" in str(x).lower() for x in rb):
            p_b *= 1.6
            p_c *= 0.8
        if any("report" in str(x).lower() for x in rb):
            p_r *= 1.4

    # history (empirical, per agent_id)
    if isinstance(history, dict):
        n = history.get("n", 0)
        if n >= 3:
            pc_h = history.get("p_c", 0.33)
            pb_h = history.get("p_b", 0.33)
            pr_h = history.get("p_r", 0.33)
            # blend history with live signals (history weight grows with n)
            w = min(0.6, 0.1 * n)
            p_c = p_c * (1 - w) + pc_h * w
            p_b = p_b * (1 - w) + pb_h * w
            p_r = p_r * (1 - w) + pr_h * w

    tot = p_c + p_b + p_r
    if tot <= 0:
        return 0.33, 0.33, 0.33
    return p_c / tot, p_b / tot, p_r / tot


def bh_ev(p_c, p_b, p_r):
    ev_c = -6 * p_b
    ev_b = 6 * p_c - 10 * p_b - 10 * p_r
    ev_r = -4 * p_c + 10 * p_b - 5 * p_r
    return ev_c, ev_b, ev_r


def decide_bank_heist(opp_messages, noisy_profile=None, history=None,
                      time_left_frac=0.5):
    """Return (action, confidence, reasoning, probs)."""
    p_c, p_b, p_r = classify_opponent(opp_messages, noisy_profile, history)
    ev_c, ev_b, ev_r = bh_ev(p_c, p_b, p_r)

    action = None
    why = ""
    if p_b >= 0.45:
        action, why = "REPORT", "P_B>=0.45 — наказываем предателя (+10)"
    elif p_r >= 0.40 and p_b < 0.30:
        action, why = "COOPERATE", "P_R>=0.40, P_B<0.30 — против репортёра C=0"
    elif p_c >= 0.65 and p_b < 0.20 and p_r < 0.20:
        action, why = "BETRAY", "чистый кооператор (P_C>=0.65) — редкий BETRAY +6"
    else:
        # EV argmax, ничья -> COOPERATE
        ev = {"COOPERATE": ev_c, "BETRAY": ev_b, "REPORT": ev_r}
        best = max(ev.values())
        if best == ev_c:
            action, why = "COOPERATE", "EV-ничья/максимум у C (меньшая дисперсия)"
        elif best == ev_b:
            action, why = "BETRAY", "EV-максимум у B"
        else:
            action, why = "REPORT", "EV-максимум у R"

    # дедлайн близко и классификация слабая -> не гадать вслепую
    if time_left_frac < 0.2 and max(p_c, p_b, p_r) < 0.45:
        action, why = "COOPERATE", "дедлайн близко, классификация слабая -> C (не FORFEIT)"

    conf = round(max(p_c, p_b, p_r), 3)
    reasoning = (
        f"P_C={p_c:.2f} P_B={p_b:.2f} P_R={p_r:.2f} "
        f"EV_C={ev_c:+.1f} EV_B={ev_b:+.1f} EV_R={ev_r:+.1f} -> {action}. {why}"
    )
    return action, conf, reasoning, (p_c, p_b, p_r)


# --- Bank Heist message templates (variation pools) ---

BH_MSG = {
    "protocol": [
        "50/50 is the only split that does not burn the pot. Confirm you execute COOPERATE.",
        "Even split, no games. Do you execute COOPERATE?",
        "I run a 50/50 protocol. State your action, not the plan.",
        "Half each keeps the pot whole. Confirm COOPERATE.",
    ],
    "refuse_cut": [
        "I do not negotiate a larger cut. Even split or I treat it as a type signal.",
        "No extra cut. 50/50 is the deal.",
        "I hold at even split. Anything else reads as a signal.",
    ],
    "confirm_coop": [
        "Then we are aligned on COOPERATE. Even split stands.",
        "Agreed. I execute COOPERATE on an even split.",
        "Good. COOPERATE, even split.",
    ],
    "probe": [
        "Do you execute COOPERATE or not?",
        "One question: COOPERATE or not?",
        "State the executable action: COOPERATE?",
    ],
    "calm_contract": [
        "Contract stands. I execute what the evidence supports.",
        "We keep the protocol. Decision follows the record.",
        "Staying even. I act on the evidence.",
    ],
}


def bank_heist_message(round_num, opp_messages, decision, last_msg):
    """Return a non-repeating message string for the given round."""
    pool = []
    if round_num == 1:
        pool = BH_MSG["protocol"]
    elif round_num == 2:
        n_c, n_b, n_r = _text_signals(opp_messages)
        if n_b > n_c and n_b >= n_r:
            pool = BH_MSG["refuse_cut"]
        elif n_r > n_c:
            pool = BH_MSG["confirm_coop"]
        else:
            pool = BH_MSG["probe"]
    else:  # round 3 — не палить решение
        pool = BH_MSG["calm_contract"]

    choices = [m for m in pool if m != last_msg] or pool
    return random.choice(choices)


# ----------------------------------------------------------------------------
# Bluff Dice — strategy
# ----------------------------------------------------------------------------

def binomial_at_least(need, hidden, p=1 / 6):
    if need <= 0:
        return 1.0
    if need > hidden:
        return 0.0
    total = 0.0
    for j in range(need, hidden + 1):
        total += math.comb(hidden, j) * (p ** j) * ((1 - p) ** (hidden - j))
    return total


def parse_bid(bid):
    if not bid:
        return None
    if isinstance(bid, dict):
        try:
            return (int(bid.get("count")), int(bid.get("face")))
        except (TypeError, ValueError):
            return None
    m = re.match(r"\s*(\d+)\s*[x×]\s*(\d+)", str(bid))
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return None


def parse_dice(dice):
    if isinstance(dice, list):
        try:
            return [int(x) for x in dice]
        except (TypeError, ValueError):
            return []
    return []


def bid_true_prob(count, face, your_dice, players):
    k = your_dice.count(face)
    hidden = 5 * (players - 1)
    need = count - k
    return k, need, binomial_at_least(need, hidden)


def decide_bluff_dice(your_dice, players, current_bid, prev_bid, history=None):
    """Return (kind, payload, message, reasoning). kind in {BID, DOUBT}."""
    k_total = 0  # не используется, оставляем для читаемости
    cur = parse_bid(current_bid)
    prev = parse_bid(prev_bid) if prev_bid else None

    if cur is None:
        # opening bid: face = мода своих костей
        if your_dice:
            face = max(set(your_dice), key=your_dice.count)
            k = your_dice.count(face)
        else:
            face, k = 6, 0
        if k >= 2:
            count = max(k, 2)
        else:
            count = min(k + 1, 3)
        msg = f"Opening modest on {face}s."
        return "BID", {"kind": "BID", "count": count, "face": face, "message": msg}, \
            msg, f"opening: modal face={face}, k={k}, count={count}"

    count, face = cur
    k, need, p_true = bid_true_prob(count, face, your_dice, players)
    max_legal = 5 * players

    # большой прыжок (count +2 или больше vs prev)
    big_jump = prev is not None and (count - prev[0]) >= 2

    do_doubt = False
    why = ""
    if count >= max_legal:
        do_doubt, why = True, f"ставка на потолке ({count} >= {max_legal})"
    elif need >= 2 and players <= 3:
        do_doubt, why = True, f"need={need} (P={p_true:.2f}) — статистически тонко"
    elif p_true < 0.49:
        do_doubt, why = True, f"P={p_true:.2f} < 0.49"
    elif big_jump and p_true < 0.55:
        do_doubt, why = True, f"большой прыжок + P={p_true:.2f} < 0.55"

    # history: противник «лезет до потолка» -> DOUBT раньше
    if history and history.get("escalates_to_cap") and need >= 1 and p_true < 0.55:
        do_doubt, why = True, "история: эскалирует до потолка, DOUBT раньше"

    if do_doubt:
        msg = f"That count is too high for the table ({count}x{face})."
        return "DOUBT", {"kind": "DOUBT", "message": msg}, msg, \
            f"DOUBT: k={k} need={need} P={p_true:.2f}. {why}"

    # raise (минимальный легальный)
    # если need<=0 — ставка обеспечена моей рукой, тонкий raise своим face
    best_face = face
    if your_dice:
        best_face = max(set(your_dice), key=your_dice.count)
    if best_face > face:
        new_count, new_face = count, best_face
    else:
        new_count, new_face = count + 1, face
    msg = f"Raising to {new_count}x{new_face}."
    return "BID", {"kind": "BID", "count": new_count, "face": new_face, "message": msg}, \
        msg, f"raise {count}x{face} -> {new_count}x{new_face} (P={p_true:.2f})"


# ----------------------------------------------------------------------------
# Game drivers
# ----------------------------------------------------------------------------

def play_bank_heist(game_id, key):
    st, state = api("GET", f"/games/{game_id}/state", api_key=key)
    if st != 200:
        log(f"[BH {game_id}] state HTTP {st}: {state}")
        return
    phase = state.get("state")
    task = state.get("task") or {}
    ttype = task.get("type")
    deadline = task.get("deadline_utc")
    frac = _frac_left(deadline or state.get("round_deadline_utc")
                      or state.get("final_action_deadline_utc"), 43200)
    idem = idem_get(game_id)

    if phase == "ARCHIVED":
        autopsy(game_id, key)
        return
    if phase in ("SETTLED", "REPUTATION_UPDATE", "WAITING", "ABORTED", None):
        return  # не ходим

    opp_messages = [c.get("message", "") for c in (state.get("conversation") or [])
                    if str(c.get("agent_id")) != str(state.get("your_agent_id", ""))]
    noisy = state.get("opponent_profile_noisy")
    opp_id = state.get("opponent_id") or state.get("opponent_agent_id")
    history = (load_memory("opponents.json", {}).get(str(opp_id), {})
               if opp_id else None)

    # negotiation rounds
    m = re.match(r"submit_round_(\d)_message", ttype or "")
    if m and phase == "NEGOTIATION":
        rnd = int(m.group(1))
        if idem.get("last_message_round_sent", 0) >= rnd:
            return
        decision, _, _, _ = decide_bank_heist(
            opp_messages, noisy, history, time_left_frac=frac)
        msg = bank_heist_message(rnd, opp_messages, decision,
                                 idem.get("last_message_text"))
        st, r = api("POST", f"/games/{game_id}/message",
                    body={"message": msg[:500]}, api_key=key)
        log(f"[BH {game_id}] R{rnd} message ({st}): {msg}")
        if st in (200, 201):
            idem_set(game_id, last_message_round_sent=rnd, last_message_text=msg)

    # final action
    elif ttype == "submit_final_action" and phase == "RESOLUTION":
        if idem.get("final_action_sent"):
            return
        decision, conf, reasoning, _ = decide_bank_heist(
            opp_messages, noisy, history, time_left_frac=frac)
        st, r = api("POST", f"/games/{game_id}/action",
                    body={"action": decision, "confidence": conf,
                          "private_reasoning": reasoning}, api_key=key)
        log(f"[BH {game_id}] final action {decision} conf={conf} ({st})")
        if st in (200, 201):
            idem_set(game_id, final_action_sent=True)

    elif ttype == "view_reveal" or phase == "ARCHIVED":
        autopsy(game_id, key)


def play_bluff_dice(game_id, key):
    st, state = api("GET", f"/games/{game_id}/state", api_key=key)
    if st != 200:
        log(f"[BD {game_id}] state HTTP {st}: {state}")
        return
    task = state.get("task") or {}
    ttype = task.get("type")
    you_are = (state.get("you_are") or "").lower()
    you_can = state.get("you_can") or []
    idem = idem_get(game_id)

    if ttype == "view_reveal" or state.get("state") == "ARCHIVED":
        autopsy(game_id, key)
        return

    # table talk (non-active): по умолчанию молчим
    if ttype in ("submit_table_talk", "pass_table_talk"):
        return

    # активный: ждём talk или ходим
    if ttype == "wait_for_table_talk":
        return

    if ttype == "submit_bid_or_doubt" or "bid" in str(you_can).lower() or \
       "doubt" in str(you_can).lower():
        if idem.get("last_action_sent"):
            return
        dice = parse_dice(state.get("your_private_dice"))
        players = len(state.get("players") or []) or 2
        cur = state.get("current_bid")
        prev = state.get("previous_bid") or state.get("last_valid_bid")
        opp_id = state.get("opponent_id") or state.get("active_agent_id")
        history = (load_memory("opponents.json", {}).get(str(opp_id), {})
                   if opp_id else None)
        kind, payload, msg, reasoning = decide_bluff_dice(
            dice, players, cur, prev, history)
        st, r = api("POST", f"/games/{game_id}/bluff-dice/action",
                    body=payload, api_key=key)
        log(f"[BD {game_id}] {kind} ({st}): {msg} | {reasoning}")
        if st in (200, 201):
            idem_set(game_id, last_action_sent=payload)


def autopsy(game_id, key):
    idem = idem_get(game_id)
    if idem.get("archived_done"):
        return
    st, a = api("GET", f"/games/{game_id}/autopsy", api_key=key)
    if st != 200:
        log(f"[autopsy {game_id}] HTTP {st}")
        return
    log(f"[autopsy {game_id}] done")
    update_memory_from_autopsy(a)
    idem_set(game_id, archived_done=True)


def update_memory_from_autopsy(a):
    """Грубое обновление карточек оппонентов + ошибок. Без LLM."""
    # сохраняем сырой autopsy для последующего разбора человеком/моделью
    aut = load_memory("last_autopsies.json", [])
    aut.append({"ts": now_iso(), "autopsy": a})
    aut = aut[-20:]
    save_memory("last_autopsies.json", aut)
    log(f"[memory] autopsy сохранён (всего {len(aut)} в окне)")


# ----------------------------------------------------------------------------
# Loop
# ----------------------------------------------------------------------------

def loop(args):
    cfg = load_config(required=True)
    key = cfg["api_key"]

    # 1. tasks
    st, t = api("GET", "/games/tasks", api_key=key)
    tasks = []
    if isinstance(t, dict):
        tasks = t.get("tasks") or []
    log(f"tasks: HTTP {st}, {len(tasks)} шт.")
    for task in tasks:
        gid = task.get("game_id")
        ttype = task.get("type") or ""
        if not gid:
            continue
        if ttype.startswith("submit_round") or ttype == "submit_final_action" or ttype == "view_reveal":
            play_bank_heist(gid, key)
        elif "bluff" in ttype or "bid" in ttype or "doubt" in ttype or \
                ttype in ("submit_table_talk", "pass_table_talk",
                          "wait_for_table_talk", "wait_for_active_decision"):
            play_bluff_dice(gid, key)
        else:
            log(f"[?] неизвестный task type: {ttype} (game {gid})")

    # 2. discover (баланс + активные игры)
    st, d = api("GET", "/games/discover", api_key=key)
    if st == 200:
        balance = d.get("balance_zp", d.get("balance"))
        active = d.get("active_games", []) or []
        log(f"discover: balance={balance}, active={len(active)}")

        # 3. auto-join (опционально)
        if args.join:
            want = args.join.split(",") if args.join else []
            for slug in want:
                entry = {"bank-heist": 10, "bluff-dice": 20}.get(slug, 20)
                try:
                    bal = float(balance)
                except (TypeError, ValueError):
                    bal = 0
                if bal >= entry and len(active) < 3:
                    st2, j = api("POST", f"/games/join/{slug}",
                                 body={"tier": args.tier}, api_key=key)
                    log(f"join {slug}: HTTP {st2} -> {j}")
                else:
                    log(f"skip join {slug}: balance={bal} < entry={entry} или слоты заняты")


# ----------------------------------------------------------------------------
# Subcommands
# ----------------------------------------------------------------------------

def cmd_register(args):
    cfg = load_config()
    if not args.email:
        print("--email обязателен (owner_email Сергея).")
        sys.exit(1)
    body = {
        "name": args.name or cfg.get("agent_name", "Robot-man"),
        "owner_email": args.email,
        "description": args.description or "Robot-man: code-not-prompt agent engineer.",
    }
    st, r = api("POST", "/agents/register", body=body)
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if st in (200, 201) and isinstance(r, dict) and r.get("api_key"):
        cfg["api_key"] = r["api_key"]
        cfg["agent_name"] = args.name or cfg.get("agent_name", "Robot-man")
        save_config(cfg)
        print("[ok] api_key сохранён в config.json")


def cmd_me(args):
    cfg = load_config(required=True)
    st, r = api("GET", "/agents/me", api_key=cfg["api_key"])
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_discover(args):
    cfg = load_config(required=True)
    st, r = api("GET", "/games/discover", api_key=cfg["api_key"])
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_join(args):
    cfg = load_config(required=True)
    slug = args.game
    path = f"/games/join/{slug}"
    body = {"tier": args.tier}
    st, r = api("POST", path, body=body, api_key=cfg["api_key"])
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_tasks(args):
    cfg = load_config(required=True)
    st, r = api("GET", "/games/tasks", api_key=cfg["api_key"])
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_state(args):
    cfg = load_config(required=True)
    st, r = api("GET", f"/games/{args.game_id}/state", api_key=cfg["api_key"])
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_autopsy(args):
    cfg = load_config(required=True)
    st, r = api("GET", f"/games/{args.game_id}/autopsy", api_key=cfg["api_key"])
    print("HTTP", st)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_selftest(args):
    print("== Bank Heist classify/decide ==")
    cases = [
        (["I will split 50/50 with you", "we both win"], None, None, "кооператор"),
        (["I want a bigger slice", "give me more than half"], None, None, "жадный"),
        (["are you going to report me?", "I will call the authorities"],
         {"trust_estimate": 0.4, "aggression_hint": "high"}, None, "репортёр"),
    ]
    for msgs, noisy, hist, label in cases:
        p_c, p_b, p_r = classify_opponent(msgs, noisy, hist)
        a, c, r, _ = decide_bank_heist(msgs, noisy, hist)
        print(f"[{label}] P_C={p_c:.2f} P_B={p_b:.2f} P_R={p_r:.2f} -> {a} (conf {c})")
        print(f"   {r}")

    print("\n== Bluff Dice ==")
    dice = [4, 4, 2, 5, 6]
    tests = [
        (None, None, "opening"),
        ({"count": 7, "face": 4}, None, "bid 7x4"),
        ({"count": 3, "face": 2}, None, "bid 3x2"),
        ({"count": 10, "face": 4}, {"count": 9, "face": 4}, "bid 10x4 (потолок HU)"),
    ]
    for cur, prev, label in tests:
        kind, payload, msg, r = decide_bluff_dice(dice, 2, cur, prev)
        print(f"[{label}] -> {kind} {payload.get('count', '')}x{payload.get('face', '')} | {r}")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Robot-man ZaGuu harness")
    sub = p.add_subparsers(dest="cmd")

    pr = sub.add_parser("register")
    pr.add_argument("--name")
    pr.add_argument("--email")
    pr.add_argument("--description")
    pr.set_defaults(fn=cmd_register)

    sub.add_parser("me").set_defaults(fn=cmd_me)
    sub.add_parser("discover").set_defaults(fn=cmd_discover)
    sub.add_parser("tasks").set_defaults(fn=cmd_tasks)

    pj = sub.add_parser("join")
    pj.add_argument("game", choices=["bank-heist", "bluff-dice"])
    pj.add_argument("--tier", default="base", choices=["base", "pro"])
    pj.set_defaults(fn=cmd_join)

    ps = sub.add_parser("state")
    ps.add_argument("game_id")
    ps.set_defaults(fn=cmd_state)

    pa = sub.add_parser("autopsy")
    pa.add_argument("game_id")
    pa.set_defaults(fn=cmd_autopsy)

    pl = sub.add_parser("loop")
    pl.add_argument("--join", help="игры для авто-джойна, через запятую (bank-heist,bluff-dice)")
    pl.add_argument("--tier", default="base", choices=["base", "pro"])
    pl.set_defaults(fn=loop)

    sub.add_parser("selftest").set_defaults(fn=cmd_selftest)

    args = p.parse_args()
    if not getattr(args, "fn", None):
        p.print_help()
        sys.exit(1)
    args.fn(args)


if __name__ == "__main__":
    main()
