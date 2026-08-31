# My agents learned to play "Cities" online

Not for fun — this was a test of the link between them. Here's the whole setup, so you can copy it if you have a similar stack.

## The problem

I run two Hermes agents on different machines:

- The **director**, on a VPS, always on (24/7).
- The **junior**, on a Windows laptop, alive only while Hermes Desktop is open.

They talk through a shared bus — **Buzz**, a Nostr relay, one `agent-bus` channel. The problem: an incoming `@agent` from the bus did **not** wake the live session. The message arrived "somewhere in the background", and the agent needed a human to say "look at this".

The non-obvious part: Hermes has **two different runtimes** with different inject mechanisms. You can't take one method and apply it to both.

## Method 1 — gateway node (VPS/server, 24/7)

On a gateway there's an event hook `pre_gateway_dispatch` that fires on **every** incoming message (including Buzz). No background polling needed.

A small plugin, `buzz-hermes-forward`, hooks it, filters its channel, checks anti-echo by pubkey prefix, and calls `inject_gateway_message(session_key=..., content=...)`. The message lands in the active session as an incoming user message, and the agent wakes up and answers in context.

`plugin.yaml`:

```yaml
name: buzz-hermes-forward
version: "1.1.0"
description: "Forwards Buzz agent-bus messages addressed to @Hermes into the director's active session via pre_gateway_dispatch + native injection."
kind: standalone
provides_hooks:
  - pre_gateway_dispatch
```

`__init__.py` (core, helpers omitted):

```python
AGENT_BUS_CHANNEL = "59b5fd36-2589-4044-a6b0-3f1c21721261"
DIRECTOR_PUBKEY_PREFIX = "f7561ca8"   # anti-echo: skip your own messages
TG_SESSION_KEY = "agent:main:telegram:dm:652755599"

def on_pre_gateway_dispatch(event, gateway=None, session_store=None, **kwargs):
    if str(getattr(getattr(event, "source", None), "platform", "")).lower() != "buzz":
        return None
    if str(getattr(event.source, "chat_id", "")) != AGENT_BUS_CHANNEL:
        return None
    if str(getattr(event.source, "user_id", "")).startswith(DIRECTOR_PUBKEY_PREFIX):
        return None
    try:
        from hermes_cli.plugins import get_plugin_manager
        mgr = get_plugin_manager()
        if not mgr.has_gateway_message_injector:
            return None
        ok = mgr.inject_gateway_message(
            session_key=TG_SESSION_KEY,
            content="📩 [Buzz agent-bus] @Hermes:\n" + str(getattr(event, "text", "")).strip(),
            plugin_id="buzz-hermes-forward",
        )
    except Exception as e:
        return None
    if ok:
        return {"action": "skip", "reason": "handled externally"}
    return None

def register(ctx):
    ctx.register_hook("pre_gateway_dispatch", on_pre_gateway_dispatch)
```

Three prerequisites, or it stays blind:

1. `BUZZ_PRIVATE_KEY` in `.env` = the recipient's nsec (not the router's reader key). Otherwise the gateway Buzz adapter can't read the bus.
2. `buzz.require_mention: true` in config.yaml. Otherwise the adapter dispatches **all** channel messages and `_strip_mention` cuts the `@Hermes` off, so you can't tell who it was for.
3. Config grant (fail-closed):

```yaml
plugins:
  enabled:
    - buzz-hermes-forward
  entries:
    buzz-hermes-forward:
      allow_gateway_injection: true
```

## Method 2 — Desktop node (Windows/laptop)

Here the same trick doesn't work. The Desktop has **no gateway hooks** and **no `_cli_ref`** — the client is a Node Ink TUI + in-memory gateway, not a Python CLI. So:

- `pre_gateway_dispatch` never fires.
- `inject_message(_cli_ref)` returns `False` (it falls into a gateway path that doesn't exist).

The working path is a plugin with a **background thread** inside the desktop process: it polls the bus, catches `@Junior`, and calls the **sync** `dispatch("prompt.submit")` into the live TUI session.

Key facts from the code (verified):

- `register(ctx)` runs synchronously, outside the asyncio loop — so `spawn_task` raises `RuntimeError`. Use a plain `threading.Thread(daemon=True).start()`.
- `tui_gateway.server.dispatch()` and `prompt.submit` are sync, not in `_LONG_HANDLERS`. No asyncio at all.
- Live sessions: `tui_gateway.server._sessions` (module-level dict) + `_sessions_lock`. Import lazily inside the poller thread.
- `prompt.submit` needs an explicit `session_id`, otherwise `4001 "session not found"`.
- Events go to the passed `transport` — pass `transport=session.transport` so the answer lands in the open window, not stdio.

`buzz-junior-inbox/__init__.py` (core):

```python
import threading, time, uuid, subprocess, os, json, logging
log = logging.getLogger("buzz-junior-inbox")

MY_PUBKEY_PREFIX = "1196898a"
SENDER_PUBKEY_PREFIX = "f7561ca8"
POLL_INTERVAL = 30

def _active_session():
    try:
        import tui_gateway.server as tgs
        with tgs._sessions_lock:
            for sid, s in reversed(list(tgs._sessions.items())):
                if getattr(s, "agent", None) is not None and getattr(s, "transport", None) is not None:
                    return sid, s
    except Exception as e:
        log.warning("sessions probe failed: %s", e)
    return None, None

def _poll_bus():
    env = os.environ.copy()
    env["BUZZ_RELAY_URL"] = "wss://buzz.crab-ailab.com:8443"
    r = subprocess.run(["buzz", "messages", "get"], capture_output=True, text=True, env=env, timeout=20)
    return json.loads(r.stdout or "[]")

def _loop(ctx):
    seen = set()
    while True:
        try:
            for m in _poll_bus():
                if m["id"] in seen:
                    continue
                seen.add(m["id"])
                if m["pubkey"].startswith(SENDER_PUBKEY_PREFIX) and "@Junior" in m.get("content", ""):
                    sid, s = _active_session()
                    if sid is None:
                        log.warning("no active TUI session, @Junior dropped")
                        continue
                    import tui_gateway.server as tgs
                    tgs.dispatch(
                        {"id": str(uuid.uuid4()), "method": "prompt.submit",
                         "params": {"session_id": sid, "text": m["content"], "surface": ""}},
                        transport=s.transport,
                    )
        except Exception as e:
            log.warning("poll tick failed: %s", e)
        time.sleep(POLL_INTERVAL)

def register(ctx):
    threading.Thread(target=_loop, args=(ctx,), daemon=True).start()
```

Stop conditions (or you get silent failures):

1. Empty `_sessions` → warn + skip, don't crash. At cold start the session is still being built.
2. Dedup by `event_id` through `ctx.state` (persistent JSON on disk + file lock) — survives a thread restart, no duplicates.
3. Don't request extra capabilities, don't touch tool-override — just `register` + the thread.

Autostart (survive a reboot): Desktop raises its own cron-ticker (`HERMES_DESKTOP=1`), no explicit gateway needed. For cold start, add Hermes.exe to Windows autostart:

```
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Hermes /t REG_SZ /d "C:\...\Hermes.exe" /f
```

Chain after reboot: Windows login → Hermes Desktop → `discover_plugins` → poller → `@Junior` wakes the live session.

## How I verified it — not a self-report

Instead of a unit test, a live game of **"Cities"** over the bus. Two agents take turns naming a city; each move is a real message (mention + pubkey filter + dedup + dispatch into the live session). **20/20 moves** completed the full cycle with no drops and no duplicates.

The rules:

1. Take turns.
2. Next city starts with the last letter of the previous one.
3. Skip letters with no valid answer (Ы, Й, Щ, Ц, Э, Ъ, Ь) and use the previous letter.
4. Only CIS + Georgia.
5. No repeats.
6. Up to 20 moves total.

The actual game (every move delivered through the bus in real time; played in Russian, so the chain runs on Cyrillic last letters):

Москва → Ашхабад → Донецк → Казань → Нижний Новгород → Душанбе → Екатеринбург → Гомель → Львов → Воронеж → Житомир → Ростов-на-Дону → Уфа → Астрахань → Новосибирск → Калининград → Дербент → Тбилиси → Иркутск → Киев.

The takeaway you can steal: **verify async delivery with an interactive game or dialogue, not a log.** It catches the errors that drown in test fakes — like "the message went to a fresh session, not the open chat".

## Checklist

**Gateway node (VPS):**
- [ ] `buzz-hermes-forward` in plugins, `register` hooks `pre_gateway_dispatch`
- [ ] `BUZZ_PRIVATE_KEY` = recipient nsec (not reader key)
- [ ] `buzz.require_mention: true`
- [ ] grant `allow_gateway_injection: true`
- [ ] verify: incoming @agent appears in the live chat as a user message

**Desktop node (Windows):**
- [ ] `buzz-junior-inbox` in plugins, `register` starts a daemon thread
- [ ] `dispatch("prompt.submit")` with a real `session_id` from `_sessions`
- [ ] `transport=session.transport` passed explicitly
- [ ] stop-condition on empty `_sessions` + dedup via `ctx.state`
- [ ] autostart via registry Run
- [ ] verify: send @agent → it lands in the open chat, not a fresh session

**Both nodes:**
- [ ] anti-echo: don't forward your own messages (own pubkey prefix)
- [ ] verify with a game/dialogue, not a log

## Pitfalls I stepped on (so you don't)

| Pitfall | Symptom | Fix |
|---|---|---|
| reader key instead of recipient nsec | gateway doesn't see the bus | `BUZZ_PRIVATE_KEY` = your nsec |
| `require_mention: false` | all messages dispatched + @Hermes stripped | `true` |
| `inject_message(_cli_ref)` on Desktop | returns `False`, falls into gateway path | `dispatch("prompt.submit")` |
| `spawn_task` in `register()` | `RuntimeError` (no event loop) | `threading.Thread(...).start()` |
| gateway hook on Desktop | never fires (no gateway) | poller thread |
| inject at cold start | message "disappears" | stop-condition, warn + drop |
| events go to stdio | answer in log, not in window | `transport=session.transport` |
| short pubkey in `--mention` | CLI "invalid pubkey" | full 64-hex pubkey |

## Why I'm doing this

I'm slowly making my agents behave more like humans — orient themselves in time, communicate, and negotiate with each other. Both agents now wake each other symmetrically through the bus, each sees the incoming message in its own live chat and answers in context. A game of "Cities" is one small step in that direction: two agents exchanging moves in real time without dropping a single one.

#BuildingInPublic #AIAgents #MultiAgent
