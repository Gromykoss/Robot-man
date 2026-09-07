# AgentMail smoke — 2026-09-03

**Key:** inbox-scoped (`auth.me.scope_type=inbox`), path `data/secrets/agentmail.env` + `~/.hermes/credentials/agentmail.env`  
**Inbox:** `robot-man@agentmail.to`  
**Org/pod:** `07200354-cbe0-415d-b506-6ce38fe8276f`

## Results

| Step | Result |
|------|--------|
| auth.me | OK — scope=inbox, inbox_id=robot-man@agentmail.to |
| inboxes.list/get | OK — 1 inbox |
| messages.list | OK |
| messages.get (welcome) | OK — text body present |
| messages.send (self loopback) | OK — message_id SES, thread_id issued |
| messages.reply (to welcome) | OK — same thread_id as welcome |
| threads.list | OK — sees welcome thread (sent-only smoke thread may lag/filter) |

## Notes

- Key prefix `am_us_inbox_*` confirmed inbox-scoped (cannot create extra org inboxes with this key alone).
- Self-send appeared as `labels: [sent]`, not as separate `received` (loopback not mirrored as inbound).
- Welcome from `admin@agentmail.to` is real inbound `received+unread`.
- External deliverability to Sergey human mailbox: **not tested yet** (need recipient email).
- Custom domain: N/A on free.
