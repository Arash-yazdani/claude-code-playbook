# CLAUDE.md design

A `CLAUDE.md` rule works when it states the rule, the date it was set, the incident that caused it, and a wrong-versus-right example. Rules written as adjectives ("be concise", "be professional") are applied inconsistently because the model has to guess the boundary.

**Failure this prevents:** the same correction made repeatedly by hand. In one case four separate edits to a client deck were logged as four style preferences. They were four repairs of one defect, and the defect then reappeared in two later documents. A rule that names the defect class stops the recurrence; four preference notes do not.

## Structure

1. **Scope line.** Which outputs the rule covers: chat, documents, commit messages, code comments. Distinguish chat style from document tone; they are different rules.
2. **The rule in one sentence.**
3. **A test the model can run.** Example: "Cover the heading. If the first sentence alone does not answer what the heading asked, rewrite it."
4. **Banned constructions, each with a wrong and a right example.**
5. **Why it exists**, with the date and the incident.
6. **An override clause** for documents that have their own voice authority (a client brand kit, a style guide).

## Example (sanitized excerpt of a global CLAUDE.md)

```markdown
# Response style

Default to terse. Lead with the answer.

- No preamble, no restating my question, no recap of what you just did.
- Findings: the claim, the evidence, the consequence.
- Prefer a table or a short list over paragraphs.

**Expand fully when I ask for it**: reports, plans, walkthroughs, code review.

**Never compress these**, regardless of length:
- Safety, security, compliance, legal, or money implications
- Deploy-order constraints and anything irreversible
- Assumptions you made, and what you deliberately did NOT do
- Test/verification results, including failures, with output

# Document tone

Applies to every document: reports, decks, READMEs, commit messages, emails.

- State the finding. Do not warm up to it or soften it afterward.
- No hype adjectives: robust, seamless, world-class, cutting-edge, transformative.
- Prefer the number to the adjective. "31% contribution margin" over "thin margin".
- Name the mechanism, the instrument, the statute, the model.

# Answer first

Set <date> after a reviewer rejected a slide for this.

The first sentence answers the question asked. Then stop.

Banned constructions:
- A second clause that reverses or puns on the first.
  Wrote: "Two groups pay for this problem. Neither of them is billed for it."
  Should have been: "Administrators and residents."
- "not X. Y." and "X, not Y."
- A kicker appended after the answer is already complete.
- Editorializing about the document itself: "importantly", "notably".
```

## Design notes

- **Separate "default" from "cap".** "Terse by default" without "expand fully when asked" produces truncated reports. Say both.
- **List what is never compressed.** Brevity rules otherwise eat security caveats and failed test output first.
- **Keep the user's own words for the rule's rationale.** A verbatim quote with a date carries more weight with the model than a paraphrase, and it survives later edits.
- **Routing rules belong here too.** Which tool or model handles which class of task (deterministic rules first, a local classifier only for validated questions, Claude for the rest) is a standing instruction, not a per-session decision.
- **Project `CLAUDE.md` / `AGENTS.md` repeats only what the project needs.** Global rules live in `~/.claude/CLAUDE.md`; duplicating them in every repo produces drift.
