# Claude Code Playbook

This repository is Arash Yazdani's working setup for Claude Code: the skills, hooks, instruction files, memory, subagent panels, scheduled agents and eval gates they run daily, sanitized for publication. It is written for teams adopting Claude Code beyond chat: platform leads, enablement owners and power users who need a repeatable operating model rather than prompt tips.

Every example here was used on real work (a voice-AI product, consulting deliverables, job-search operations, a personal knowledge vault). Names, identifiers, paths, credentials and private figures were removed. Where something was cut, the file says so.

## Operating model

- **Instructions are code.** `CLAUDE.md` holds rules with a date, a reason and a failing example. A rule without the failure it prevents gets ignored or misapplied.
- **Skills carry the lessons a model cannot re-derive.** Each skill states its trigger, names the source-of-truth document it defers to, and lists the guardrails that each cost a cycle to learn.
- **Hooks enforce what instructions only request.** Anything that must never happen (secrets reaching the transcript) is a `PreToolUse` hook with a self-test, not a sentence in a prompt.
- **No deliverable ships on the author's own review.** A panel of independent subagents, each with a ground-truth brief and a fixed output format, gates every client-facing document.
- **Mechanical checks run before judges.** Recompute every derived number, re-derive every summary count, grep for banned strings. Judges spend attention on what scripts cannot catch.
- **Scheduled agents have narrow, non-destructive permissions.** Draft, never send. Report, never fix. Add and link, never delete.
- **Memory is an index of standing rulings.** One line per ruling, pointing to a file with the date, the reason and the scope. Superseded rulings are marked, not deleted.
- **Cheap models get a validation gate.** A local classifier is used only for questions that passed an AUC and precision threshold on labeled real data; everything else goes to rules or to Claude.

## Contents

| Folder | What it shows | Practice it maps to |
|---|---|---|
| [`patterns/`](patterns/) | Five short pattern notes, each with the failure it prevents | Claude Code foundations; power-user playbooks |
| [`skills/`](skills/) | Six production skills: domain guardrails, eval procedure, compliance, deliverable pipeline, classifier routing, live-call reference | Skill authoring; builder workshops |
| [`hooks/`](hooks/) | A `PreToolUse` hook that blocks `.env` reads, with a built-in self-test | Security guardrails for agentic coding |
| [`scheduled-tasks/`](scheduled-tasks/) | Three unattended agent prompts: inbox drafts, nightly knowledge-base consolidation, vendor status polling | Agent operations; AI enablement |

## Proposed adoption plan

A five-day plan for a team adopting these patterns. It has not been run as written; each step reuses a component that has.

| Day | Work | Output |
|---|---|---|
| 1 | Write a team `CLAUDE.md` from [`patterns/claude-md-design.md`](patterns/claude-md-design.md). Start with 5 to 10 rules, each with a reason and a bad example from your own repos. | Checked-in `CLAUDE.md` |
| 2 | Install a secrets hook modeled on [`hooks/block-env-read.py`](hooks/block-env-read.py). Extend its self-test with your own paths before enabling. | Hook in `.claude/settings.json`, self-test passing |
| 3 | Pick the one subsystem where Claude keeps re-breaking fixed behavior. Write a skill for it in the shape of [`skills/familycheck-voice`](skills/familycheck-voice/SKILL.md): source-of-truth doc, first commands, hard guardrails. | First team skill |
| 4 | Pick one recurring deliverable (design doc, report, release note). Add a judge panel per [`patterns/eval-gates-and-judge-panels.md`](patterns/eval-gates-and-judge-panels.md). Run it on the last three shipped examples to calibrate. | Gate with known catch rate |
| 5 | Move one recurring chore to a scheduled agent per [`patterns/scheduled-agents.md`](patterns/scheduled-agents.md), with read or draft permissions only. Review a week of outputs before widening scope. | One unattended agent |

Measure the week by defects caught before shipping and by repeat corrections avoided, not by prompt count.

## Conventions

- Paths are generic (`~/projects/...`, `docs/...`). Replace them with your own.
- Dates in rules are kept. A dated rule tells a reader whether it predates or follows a given incident.
- Skills under `skills/` keep their `SKILL.md` only. Supporting scripts and reference files referenced in a skill are not included unless noted.

## License

MIT. See [LICENSE](LICENSE).
