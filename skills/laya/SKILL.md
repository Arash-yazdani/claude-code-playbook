---
name: laya
description: Routes classification work to Laya, a free local classifier, only where it passed testing, and tests new task types before trusting them. Use whenever a task screens or sorts many items into fixed buckets or yes/no answers (job postings, leads, tickets, emails, records), when the user says "use Laya" or "can Laya do this", or asks whether a sorting task could be automated cheaply. Also use when a new task type is proposed for Laya, to run the validation workflow.
---

<!-- Sanitized for publication: local paths generalized. Laya is the open-source
     @receptron/laya package (MIT), a ModernBERT encoder with a decision head run on CPU. -->

# Laya

Laya is a local classifier. It costs nothing to run and keeps data on the machine, but on real data it beat neither keyword rules nor Claude on most tasks. Its value is narrow, so this skill decides *whether* to use it before using it.

## Decide first
1. **Rules first.** If keywords, sender domains, regex, dates or labels answer the question, use them. They won on every tested task.
2. **Laya only through a validated question.** Open the registry `validated.json`. Use only entries with `status: "validated"`, called by name. If the task matches a `rejected` entry, say so and don't use Laya.
3. **Claude for everything else**, including combining several facts into a decision.

Never use Laya for money, legal, compliance, medical or patient decisions, for writing text, or for more than 20 options.

## Status as of 2026-10-16
| Question | Result | Use |
|---|---|---|
| `job_product`: is this a product job? | AUC 0.94 | Fallback for job titles with no lane keyword |
| `job_senior`: senior/principal/staff/lead? | AUC 0.865 | Fallback only; title keywords scored 98% |
| Inbox triage | 27-46% vs 51% baseline | Rejected |
| Job type, 5-way | 54% | Rejected |
| Account management / customer success | AUC 0.72 | Rejected |
| AI-search "first recommendation" | AUC 0.60 | Rejected |
| Calendar "call to prep for" | AUC 0.59 vs keyword rule 97% | Rejected |

## Use it
- **Job postings:** `jobscreen --laya` (stdin: JSON array of `{ref, title, company, summary}`). Keywords decide; Laya checks only keyword-less titles.
- **Other validated questions:** MCP `laya_decide` (one item) or `laya_decide_batch` (many), questions given by registry name. Or the CLI `laya-ask`.
- Act on the `verdict`: `yes` / `no`; send `unsure` to Claude. Report the question's tested AUC and precision, not raw probabilities.
- Keep each item under 512 tokens; longer input is rejected.

## Validate a new task type
1. Phrase one single-fact yes/no question. Questions that pack in several rules failed.
2. Build 30+ labeled examples from real data (`[{"state": ..., "y": 0|1}]`), with both classes present. Record who labeled them.
3. Run `node scripts/validate.mjs labeled.json "question"`.
4. Measure the keyword/rule baseline on the same set.
5. Add the result to `validated.json`: `validated` only if AUC is at least 0.9, both bands reach 90% precision, and it beats or adds to the rule; otherwise `rejected` with the reason. Report the numbers either way.
