# Eval gates and judge panels

No client-facing deliverable ships on the author's own review. A panel of independent subagents, each briefed with the ground truth and a fixed output format, judges the draft; the author applies findings by consensus and discloses what changed.

**Failure this prevents:** credibility errors that pass every string-level check. In one recorded case a package passed its build gate and was delivered, then a four-judge panel run afterward found: an unsigned letter, a regulated-industry term of art used nine times for an adjacent capability, a claimed clinical reviewer who did not exist, and the same engagement described at two levels of accuracy in two documents. Each fix took minutes. Any one, found by the reader, ended the conversation.

## Order of gates

1. **Mechanical checks** (scripts, before any judge). Recompute every derived figure from its inputs. Re-derive every summary count from the exhibit it summarizes. Check every chart bar width against its label. Check every figure that appears twice for agreement. Grep for banned strings. On one market study these found 5 of 10 matrix summary counts wrong and 3 charts contradicting their own labels.
2. **Judge panel** (parallel subagents).
3. **Apply findings, re-run mechanical checks, re-run the panel.** Edits introduce defects: one remediation pass changed a headline figure without propagating it to six downstream mentions. Budget two judge cycles.
4. **Brand or format gate** (script that returns PASS/FAIL and blocks the send).
5. **Disclose** to the requester what the judges found and what changed.

## Building the panel

**Four seats, each catching a failure class the others miss.** Example seats for a document aimed at a hiring or buying committee:

| Seat | Failure class it catches |
|---|---|
| Decision owner | Leveling; whether the document survives against the competing alternatives |
| Domain authority (licensed practitioner in the reader's field) | Terminology overreach: words that are terms of art in that field and casual English elsewhere |
| First-pass screener (15 to 40 seconds per document) | Structure and skim path; disclosures that work in conversation and fail in writing |
| Peer bar-raiser (does the same job at a competitor) | Negative transfer: judgment formed in a context whose economics invert in the target context |

Run all seats in one message so they execute in parallel. Use the strongest available model for judges.

**Every judge gets a ground-truth brief.** State what is true, including the unflattering facts: real user counts, what has never been done, the limits of the strongest evidence. Instruct: "Use this only to detect overreach. Do not reward claims that are not on the page." A judge without ground truth praises the overclaims.

**Every judge gets a fixed output format.** Required sections for every seat:

- `VERDICT` and `SCORE /10`
- `OVERREACH CHECK`: each claim implying more than the brief supports, quoted, with what a hostile reader concludes
- `FIRST 15-20 SECONDS`: what the reader notices, in order
- `WHAT WOULD MOVE THIS ONE POINT`: sentence-level edits only

End each prompt with "Produce exactly this output and nothing else" and an explicit instruction to be adversarial.

## Synthesis rules

- Unanimous: apply.
- Three of four: apply, unless the evidence record forbids it.
- One seat: weigh it. A stylistic preference is not a defect; a factual catch from the domain authority is.
- **Never apply an edit that makes a claim less true.** Judges optimize for persuasion. The evidence record outranks every judge.

## Pre-checks that recur across panels

Check these before running the panel so it spends attention on new problems:

- Do not use the target industry's term of art for an adjacent thing. A pilot is not a deployment; review is not certification.
- State the boundary of the work in the first paragraph.
- State the small number instead of hiding it.
- Give sample size and interval for any rate. 84% at n=53 has a 95% interval of roughly 72% to 91%.
- Name why a method was chosen ("Gwet's AC1 rather than Cohen's kappa, which degenerates at these marginals").
- Two documents describing the same work must use the same claim in the same words.

## Model evals follow the same discipline

For model behavior (see [`skills/familycheck-evals`](../skills/familycheck-evals/SKILL.md)):

- Report a median across repeated runs; one run at temperature 0.85 varied 84% to 86% on identical code.
- Version the instrument. A rubric change is a new instrument; never pool scores across it.
- Report Gwet's AC1 alongside Cohen's kappa and print the 2x2 cells. At 95% agreement and a 95% pass rate kappa can go negative.
- Never sample a validation set from a queue that only contains failures.
- Label before judging when measuring human-judge agreement; the ordering is the blinding.
