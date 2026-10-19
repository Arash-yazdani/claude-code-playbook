---
name: familycheck-evals
description: Use whenever working on FamilyCheck evaluation: the CRISP scenario suites, the LLM judge, the human-vs-judge agreement study (Gwet's AC1 / Cohen's kappa), or any eval report or judge rubric. Loads the measurement traps that produce wrong numbers, so none get published.
---

<!-- Published as a structural example. FamilyCheck's source is private; this copy keeps only
     what the public case study (github.com/Arash-yazdani/familycheck-engineering) and the
     open-source crisp-eval harness state. Script names, internal baselines, tooling and
     run commands are removed. -->

# FamilyCheck evaluation work

**Before changing anything, read the source-of-truth docs** in the product repo: the monitoring
SOP, the eval harness notes, and the judge rubric file. **The rubric file wins over any UI copy of
the rubric.** If anything here conflicts with a doc, the doc wins, and update the doc.

## Always do first
1. Confirm the live configuration matches source of truth before measuring anything.
2. Run the eval harness's own unit tests.

## Numbers that are routinely misread
- ⚠️ **A saturated suite is not a correct agent.** The first 10-scenario suite went from 71% to 100%;
  the 50-scenario adversarial suite then scored 56% scenario-pass. Report the harder suite.
- ⚠️ **Turn-pass and scenario-pass are different numbers.** 83% → 87% turn-pass was 56% → 66%
  scenario-pass on the same runs. Always label which one is quoted.
- ⚠️ **Judge-vs-human agreement is an upper bound.** AC1 0.958 / 0.843 / 1.000 across three
  dimensions, from a single rater who built the system, on synthetic transcripts. State that with
  the number.

## Hard guardrails
- **Report Gwet's AC1 as primary and print the 2×2 cells.** At high agreement and a high pass rate,
  Cohen's kappa goes negative on the same table. This happened on real data here; AC1 was
  pre-registered as primary for that reason.
- **Check the both-fail cell.** When it is empty, the study validates the judge's pass behavior and
  says almost nothing about its fail behavior. Say so.
- **Report the direction of disagreement.** 7 of 9 disagreements were the judge passing a call the
  human failed. A lenient judge inflates every downstream score.
- **Name the judge family.** The deployed judge is same-family (GPT-4o grading GPT-4.1). That is the
  reason the agreement study exists; never present judge scores without it.
- **Label before judging.** Human labels are collected blind, before judge scores are visible.
- **A rubric change is a new instrument.** Version it and never pool scores across the change.
- **Safety keys are deterministic.** PII leak (held at 0%) and escalation recall (held at 100%) are
  checked by code, not by the LLM judge.
- **Cost changes go through the suite.** A cheaper model was A/B tested and rejected because it lost
  the keyword reliability the safety rubric depends on. Without the eval the saving would have
  looked free.

## Reference
The method (CRISP taxonomy, turn-pass vs scenario-pass, deterministic safety keys, judge-vs-human
agreement statistics) is open source: github.com/Arash-yazdani/crisp-eval.
