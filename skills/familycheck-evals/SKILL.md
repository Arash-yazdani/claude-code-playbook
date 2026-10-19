---
name: familycheck-evals
description: Use whenever working on FamilyCheck evaluation: running or changing the CRISP-53 / SIGNOFF-10 suites, the LLM judges, the human-vs-judge agreement study (kappa / Gwet's AC1), the ASR-vs-model attribution pilot, WER or keyterm work, annotation queues, or any eval report or judge rubric. Loads the measurement traps that have already produced wrong numbers, so we don't publish another one.
---

<!-- Sanitized for publication: host names, container names and local paths removed. -->

# FamilyCheck evaluation work

**Before changing anything, read the source-of-truth docs** in the FamilyCheck repo `docs/`:
`monitoring-sop.md` (signals and baselines) · `asr-vs-model-separation.md`
(the data-vs-model story) · `voice-conversation-lessons.md` §9 (eval harness) ·
`evals/langsmith/online-evaluators.md` (**the judge rubric; this file wins over
the LangSmith UI**).

Those docs are the source of truth. This skill is the quick reference and
guardrails. **If anything here conflicts with a doc, the doc wins, and update
the doc.**

## Always do first
1. `python3 -m scripts.vapi_verify_prompts`: confirm live config matches source of truth before measuring anything.
2. `python3 -m pytest tests/test_crisp_suite.py -q`: the eval harness's own invariants (metadata regex recovery, name truncation, category counts).

## Numbers that are routinely misread
- ⚠️ **"~9%" is the transcriber's share of LATENCY, not accuracy.** There is **no WER anywhere** in this repo for either transcriber. Quoting it as accuracy is the fastest way to be publicly wrong.
- ⚠️ **The two transcriber latency profiles are NOT a before/after.** Different metric, tooling and window, and confounded by five other changes.
- ⚠️ **CRISP's old "~51% baseline" was a stale-rubric artifact**, not model quality. Current CRISP-53 baseline is **84% scenario-pass / 94% turn-pass**; it ranged **84-86% across four runs of identical code** at temperature 0.85, so report a median across repeats and never read a single-scenario delta as signal.
- ⚠️ **`tool-only` is the IDEAL final-turn shape** since the sign-off de-dup. A "dead air" finding now means `shape == "broken"` (no content AND no tool), a real defect.

## Hard guardrails (each cost a cycle to learn)
- **Never run the CRISP suite without `--delete-existing`.** Every run otherwise adds 53 more evals; the list endpoints are un-paginated and silently truncate. Verified live: the account held 109 evals while `limit=100` was in use, so the suite was already scoring a partial set.
- **Human feedback keys MUST be prefixed `human_*`.** Feedback IDs are `uuid5(f"...:{trace_id}:{key}")`; same run plus same key gives the same ID, so an unprefixed human label **overwrites the judge's**, destroying the exact datum an agreement study measures.
- **Kappa collapses at skewed marginals.** At ~95% agreement with a ~95% pass rate, Cohen's κ can go *negative* while agreement is excellent (verified fixture: a=51, b=1, c=1, d=0 ⇒ p_o 0.962, κ −0.019, AC1 0.961, same table). **Report Gwet's AC1 as primary, always print the 2×2 cell counts, and never report κ without its undefined-replicate count.**
- **Never sample a validation study from the `prod-review` queue.** Its automation rule fires only on failing scores, so the queue is a 100%-failure stratum by construction, with no true-negative cell.
- **Never route eval data through the production logging helper.** Its session name is hardcoded to the production projects; that is the one way to pollute production dashboards and trip the disclosure/sign-off alerts. Uploading as a dataset-backed experiment keeps eval runs invisible to online rules; don't break that isolation.
- **The judge is never told about transcription noise**, so ASR error is silently priced into every production score. Changing that (a new `transcript_intelligible` key) **changes the judge**: cut a version and do not pool scores across the cutover.
- **Offline suites contain no transcriber.** Any CRISP/SIGNOFF failure is a model/prompt failure by construction. Never attribute one to ASR.
- **Transcripts cannot judge TTS.** The transcriber folds some phonemes together; only a human ear on a live call (or the recording) is a valid pronunciation verdict. Pass = green on **two consecutive** calls.

## Which knob for which symptom
| Symptom | Layer | Knob |
|---|---|---|
| Assistant **speaks** a name/med wrong | TTS | pronunciation dictionary (IPA only; sounds-like aliases are banned) |
| Transcript wrong for what the **patient** said | STT | per-call `keyterm` list (the current STT model uses `keyterm`, **not** legacy `keywords`) |
| Transcript wrong for what the **assistant** said | STT of our own output | none available on the current TTS vendor |
| Redaction misses a mis-transcribed name | eval hygiene | `KNOWN_TRANSCRIPT_VARIANTS`: append only when **observed**, never speculatively |

## Run the CRISP-53 suite
```
# copy the worktree into the app container; never deploy an unmerged branch to prod
python3 -m scripts.vapi_create_eval_suite --delete-existing --run
python3 -m scripts.vapi_eval_report -o evals/<date>-crisp-53-report.md
```
About 4 minutes and $1.60 per run. Smoke a slice first with `--crisp X --filter NAME`.

## Run the agreement study
```
python3 -m scripts.agreement_study --selftest              # kappa/AC1 vs hand-computed fixtures
python3 -m scripts.agreement_study build --check           # blinding assertion -> READY
python3 -m scripts.agreement_study --suffix vN build       # dataset + annotation queue
python3 -m scripts.agreement_study --suffix vN populate --rebuild   # <-- --rebuild IS REQUIRED
python3 -m scripts.set_agreement_rubric                    # <-- rubric does NOT survive a rebuild
python3 -m scripts.verify_annotation_readiness             # <-- must print READY 53/53
#   ... annotate, THEN run the judge (blinding = sequencing) ...
python3 -m scripts.agreement_study --suffix vN export -o evals/agreement/pairs-vN.csv
python3 -m scripts.agreement_study --suffix vN stats  -i evals/agreement/pairs-vN.csv
```
Label **before** judging. That ordering is the blinding guarantee.

⚠️ The three marked lines were missing from this block at first, and each omission cost a cycle:
- **`populate` without `--rebuild`** leaves the queue serving the PREVIOUS build's transcripts. A corrected dataset sat behind 53 stale runs for a full round because every dataset-level check passed.
- **`set_agreement_rubric`** must re-run after every `build`; a queue with no rubric looks fine until the annotator opens it.
- **`verify_annotation_readiness`** printing `READY` is the definition of ready. Skipping it is how partial conversations reached a human twice.

⚠️ **`--suffix` is the instrument version.** Bump it whenever the RUBRIC changes. A new rubric is a new instrument, and its agreement must never be pooled with the old one.

## Script cheat sheet
| Script | Purpose |
|---|---|
| `vapi_create_eval_suite.py` | CRISP-53 suite + shared judge harness/rubrics |
| `vapi_create_signoff_suite.py` | SIGNOFF-10 (imports the harness above) |
| `vapi_eval_report.py` | markdown scorecard |
| `crisp_judge_offline.py` | reads the rubric from `online-evaluators.md` at runtime; scores arbitrary transcripts |
| `agreement_study.py` | blinded substrate, export, κ / AC1 / bootstrap CI |
| `asr_attribution_pilot.py` | raw-vs-corrected transcript study (n=8 pilot) |
| `eval_suite_runner.py` | scheduled weekly SIGNOFF / monthly CRISP |

*If you change the judge rubric, edit `evals/langsmith/online-evaluators.md`
first, then the UI, and re-baseline before comparing anything across the change.*
