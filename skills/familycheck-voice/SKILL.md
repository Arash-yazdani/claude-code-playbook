---
name: familycheck-voice
description: Use whenever working on the FamilyCheck voice / phone-call layer: the medication or consent voice assistant, the call sign-off / closing, system prompts, the log_result tool, emergency/911 routing, caregiver callback relay, early-hangup webhook fallback, or the CRISP / SIGNOFF eval suites. Loads the hard-won lessons so we don't re-derive them or re-break fixed behavior.
---

<!-- Sanitized for publication: assistant IDs, persona and test-contact names,
     phone numbers, host names and local paths removed. -->

# FamilyCheck voice / conversation work

**Before changing anything in the voice layer, read the full lessons doc:**
`docs/voice-conversation-lessons.md` in the FamilyCheck repo.

That doc is the source of truth. This skill is the quick reference and guardrails so
you don't repeat past mistakes. **If anything here conflicts with the doc, the doc
wins, and update the doc.**

## Always do first
1. `python3 -m scripts.vapi_dump_prompts`: see the live config before touching it.
2. `python3 -m scripts.vapi_verify_prompts`: confirm live matches source of truth.

## The two assistants
- **Medication** and **Consent** assistants, IDs in config (`VAPI_ASSISTANT_ID`, `VAPI_CONSENT_ASSISTANT_ID`).
- Defined in **code**, not the vendor dashboard. Edit `scripts/vapi_update_voice_flow.py` and PATCH; never edit in the vendor web UI (the next PATCH overwrites it).

## Hard guardrails (each cost call cycles to learn)
- **Single system-owned closing.** The model goes **tool-only** on the final turn; the application speaks the goodbye via the `log_result` `request-complete` message. `endCallMessage` is empty on the medication assistant. Don't re-add a model-spoken goodbye or a third closing.
- **Keep the conditional `request-complete`** (two messages: `status=="emergency"` → 911 line; default → generic closing). This makes the 911 line deterministic even on a tool-only turn. **Never collapse them into one.**
- **`{{variables}}` do NOT substitute in tool messages**, only in the system prompt and `firstMessage`. Closings are generic (no patient name). Don't template them.
- **The model goes tool-only about half the time on the final turn.** That is why the closing must be system-owned, not model-spoken.
- **Caregiver alerts fire only for `confirmed` / `denied` / `concern`.** To guarantee the caregiver is notified (for example a callback request), route through `status="concern"`.
- **Early hang-up is safe:** if the model never emits `log_result`, the `end-of-call-report` fallback in `app/routes/webhooks.py` recovers the outcome from the transcript. Don't change the webhook response shape.
- **The persona name drifts.** Keep it pinned in the prompt; re-verify after edits.
- **Pronunciation is fixed via a TTS pronunciation dictionary plus per-call STT keyterms.** Read `docs/pronunciation-sop.md` before touching it: IPA-only aliases (sounds-like spellings get misread), never the vendor's provider-resource PATCH (cross-tenant bug), the dictionary must be re-attached on every voice PATCH, and TTS verdicts come from a live-call ear only, never transcripts.
- **Run `scripts/sync_vapi_config.py` after any deploy or URL change.** A stale tunnel once silently dropped every webhook POST.

## Evals
- **CRISP** and **SIGNOFF** suites, judged by an LLM via mock conversations.
- `tool_turn(..., allow_tool_only=True)` → a tool-only final turn passes (SIGNOFF). `allow_tool_only=False` → enforces a spoken closing (CRISP dead-air check).
- ⚠️ **These two suites have OPPOSITE final-turn expectations.** After the sign-off de-dup the model correctly goes tool-only; don't chase CRISP final-turn "dead-air" failures.
- Evals catch **model behavior** only. **Audio-level** closing redundancy is provable **only by a real call.**
- Bar: ≥80% overall and per category.

## Deploy and verify a voice change
1. Edit `scripts/vapi_update_voice_flow.py` (and eval scripts if behavior changed); `py_compile` and dry-run.
2. PR → `main`; on the production host `git pull --ff-only`, rebuild the app container, restart the proxy.
3. PATCH: `python3 -m scripts.vapi_update_voice_flow`.
4. `vapi_verify_prompts` (expect exit 0), then re-run the relevant eval suite.
5. **Place a live test call** (it rings a real phone, so get explicit per-call confirmation):
   `python3 -m scripts.dispatch_manual_call` against the designated test number. This is the only way to verify the closing sounds like one clean goodbye.

## Script cheat sheet
| Script | Purpose |
|--------|---------|
| `vapi_dump_prompts` | read-only dump of live config |
| `vapi_verify_prompts` | diff live vs source of truth |
| `vapi_update_voice_flow` | **source of truth** + PATCH assistants |
| `sync_vapi_config` | re-point webhook URL after deploy |
| `vapi_create_eval_suite` | CRISP |
| `vapi_create_signoff_suite` | SIGNOFF |
| `vapi_eval_report` | shareable markdown report |
| `dispatch_manual_call` | interactive live test call |
