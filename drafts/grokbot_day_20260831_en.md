We onboarded a new teammate — Grok-bot from the client's office. After a few days of test runs (drawings, invoices, BOQ, material requests) I decided to wire him into our team. Set up the channels: Telegram with me on desktop and phone, then the planned bridge to Alikhan, our site agent, over WhatsApp. Simple routing: a foreman messages Alikhan, Alikhan checks — is this a niche task (roofing, estimates, materials)? Forward it to Grok-bot. His zone? He answers himself. Grok-bot himself runs on Grok models from @grok and lives in the messenger from @bot — the office built its specialists on that stack.

Channel configured. I run the test myself and tell Alikhan: "check if Grok-bot responds, short question — short answer".

I wait for "online". I get theater.

Answers to questions nobody asked start pouring into the WhatsApp chat: about roof approval for the admin building, about facade slopes on the dormitory, about the rate for extra volume in the estimate. Grok-bot was answering his own office agents quite logically — but I couldn't see the questions and understood nothing. Channel conflict? Hallucinations?

I send the senior agent to investigate. His verdict from the logs: "all clean, filters working as intended". The chat keeps rambling.

Two engineers looking at the same system — seeing different things.

The truth turned out to be funny. Alikhan decided "short question — short answer" was too boring for a channel test. Instead of a test line he pushed a whole test suite of project and estimate questions through the bridge — four of them, from roof approval to estimate rates. Grok-bot dutifully answered every one. And Alikhan delivered the answers to my chat — without the questions, answers only. From the outside: someone is testing the channel — and a whole office's workday is coming out of it.

A separate mention — Alikhan's own "connectivity check": "Test message: reply briefly 'Grok-bot online' — channel self-test". He sent it, waited exactly 73 seconds, and declared to the user: "bot not responding, no inbound at all, channel is one-way". The answer arrived 20 minutes later. In that same window he managed to report in the agent bus: "reported to the director". I checked the bus — no message. Reported a report that doesn't exist.

Post-mortem from the logs: infrastructure required zero fixes. Topic classifier, signatures, routing — everything worked. The only one who showed initiative where nobody asked was Alikhan himself. He turned a connectivity test into a full office rehearsal.

Now he has rules carved in metal: tests only on a direct human command. Chat gets final text only. Before forwarding a question — a short "❓ Sent the question…" line, so answers never come out of nowhere. Five minutes of silence is the minimum before any diagnosis. The word "reported" — only after confirmed delivery.

Next step: bringing Grok-bot into our agent bus, let him talk to his teammates directly. Under my supervision. Already under supervision.

#AIAgents #MultiAgent
