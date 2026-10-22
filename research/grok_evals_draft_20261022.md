I'll read the draft, the facts file, and the relevant rules so I can score it against the checklist.I'll count the post body and scan it against each rule, including the first-line ALL-CAPS check.Checking local posting rules so the checklist matches the house standard.**Verdict: PASS-WITH-FIXES** (2527 chars; voice/hook/length hold; local sale lines and one overclaim)

1. Voice: first-person I/my. No “my bot” / “the agent” as self. **PASS**
2. Hook, first line literal: `Drafts keep passing. Nothing stops a deploy. A line in a checklist doesn't block code — an exit code does.` Mixed case, no ALL-CAPS words. **PASS**
3. Audience: the 3-file suite, 0/2/3, yaml thresholds, env-gated OTel travel. `kupi` / `F4` / `buzz-send` do not. **SHOULD**
4. Value: copyable tomorrow — suite layout, rc contract, gold set + live block, OTel that cannot change rc. **PASS**
5. Facts vs `evals-facts-20261020.md`: 11 gates, 225-line stdlib+PyYAML runner, sha256 verdict JSON, 0/2/3 + stdout signal, kind agent/service, post-gate 7/7 and rc=2 before X, kupi 0.96 / 27/671/78 → 1.0 after F4, Langfuse deferred, EVALS_OTLP_ENDPOINT off-by-default, metric name, buzz-send 5-path self-test — match. Gaps below. **MUST**
6. Format: 2527 ≤ 4000. **PASS**
7. Tone: report body is calm. Sale/штамп lines listed. **MUST**
8. Anti-попа (sale): industry claim, “not trust…”, philosophy reprise, closer. **MUST**

**MUST**
1. Drop or rewrite para 3 (`This is where the industry landed…` + `The pattern is the same whether…`). Not in the fact-base. Sale. Keep only what I run.
2. Line 5: `before anything deploys` fights the buzz-send limit. Use `before a gated deploy runs`.
3. Cut `Not trust, not a self-report — rc` → `The deploy script blocks on rc.`
4. Cut the reprise `Same philosophy as my last post… mechanics instead of trust. Exit codes instead of a checklist line.` Duplicate slogan.
5. Cut `Building in public. 🤖` (штамп + emoji). End on the 225-line limit.

**SHOULD**
6. Hook is present-tense agitation (`Nothing stops a deploy`) against “I run 11 gates.” Open on the contract: `I block deploys on eval rc: 0=PASS, 2=FAIL, 3=CONFIG.`
7. One gloss or drop: `kupi` = shop deploy; `F4` = open fail class; `buzz-send` = handshake with no eval suite. Keep 27/671/78.
8. OTel sentence: add `:4318` and dashboard `Evals-Gates`. Facts list both ports and that name. Optional: collector contrib 0.163.1.

**NICE**
9. `11 eval gates… report-gate, verdict-gate…` → `11 eval gates, including…` so five names are not the full set.
10. `tiny eval suite` → `eval suite`.
