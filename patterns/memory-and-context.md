# Memory and context

Persistent memory is an index of standing rulings: one line per ruling in `MEMORY.md`, each pointing to a file that holds the date, the reason, the scope and the exact wording. Context that is large or changes often (evidence records, product docs) stays in its source document; skills and memory point to it rather than copying it.

**Failure this prevents:** two kinds. First, a correction given once is lost at the next session and has to be repeated. Second, a copied fact goes stale: a skill that duplicated a source document drifts from it, and the model follows the stale copy.

## Memory index format

```markdown
- [Answer first, no epigrams](feedback_answer_first.md) — first sentence answers the question, then stop; no clause that reverses or puns on the first
- [Judge loop mandatory](feedback_judge_loop.md) — four-seat panel before any external document ships; evidence record outranks judges
- [No new spending](feedback_no_new_spending.md) — free or self-hosted only; state any unavoidable cost and stop (set <date>)
- [Old routing rule](feedback_old_rule.md) — SUPERSEDED <date>, history only
```

Rules for the index:

- **One line, under 200 characters, with the operative rule in the line itself.** The model often acts on the index without opening the file.
- **Each file starts with the date set and the reason.** Undated rulings cannot be ordered when two conflict.
- **Supersede, do not delete.** Mark the old entry and link the new one; the history explains why the current rule exists.
- **Prefix by kind** (`feedback_`, `project_`, `user_`) so the index can be scanned by type.

## Source of truth over copies

Every domain skill in this repo opens with the same block:

```markdown
Before changing anything, read the source-of-truth docs: docs/<lessons>.md ...
This skill is the quick reference and guardrails. If anything here conflicts
with a doc, the doc wins, and update the doc.
```

That sentence makes the skill a pointer with guardrails, and assigns the fix for drift to whoever finds it.

## Context loading

- **Retrieval hook on prompt submit.** A `UserPromptSubmit` hook queries the knowledge base and injects matching notes, so relevant prior decisions appear without the user naming them.
- **Progressive loading.** Load identity and current priorities at a short level by default; load full project history only when the task needs it.
- **Subagents for wide reads.** When answering requires reading many files, delegate to a subagent and keep only its conclusion in the main context.
- **Write-back conventions.** Notes written by agents carry frontmatter (`date`, `type`, `ai-first: true`) and a "For future agent" preamble, so the next session can tell agent-written state from human-written notes.
