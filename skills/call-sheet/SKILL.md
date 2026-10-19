---
name: call-sheet
description: >-
  Builds a live call sheet: a one-page interactive reference kept open during a conversation
  (sticky section chips, keys 1-9 to jump, tick-off points, a clickable stage funnel, phone and dark-mode
  friendly), published as a private Claude artifact. Use whenever the user is preparing for any live
  conversation: interviews, recruiter screens, panel rounds, case interviews, networking calls, client,
  sales or discovery meetings. Trigger on "prep me for my call/interview/meeting with...", "give me
  talking points / an outline / a cheat sheet for the call", "what should I say", "questions to ask
  them", or pasted rough notes for an upcoming call, even if no visual is requested. Skip it for
  written-only work (resumes, emails) and after-the-call work (thank-yous, follow-ups).
---

<!-- Sanitized for publication: personal paths, compensation figures, employer names and
     the origin page name removed. The build script and HTML template are not included. -->

# Call sheet

The user wants a glanceable, clickable sheet for every meeting, phone or video: their own words,
organized into a few sections they can jump between with number keys and tick off as they cover them.
The sheet is a reference for a live conversation, so every line has to be readable in two seconds and
true under follow-up questions.

## Workflow

1. **Pin down the meeting.** Who, which company and role, phone or video, when, and the goal. Pull what
   exists before asking: the user's message and pasted notes; the knowledge base (person note, pipeline
   note, prep notes); the role's folder; the calendar event if a time is mentioned. Ask only for what you
   cannot find, in one question.
2. **Pick the sections** from the recipes below and draft the content in the user's voice (rules below).
3. **Write the sheet JSON** to `call-sheets/<YYYY-MM-DD> <Who>/sheet.json` (schema below).
4. **Build:** `python3 scripts/build_sheet.py <sheet.json> <same folder>/call-sheet.html`.
   It refuses to build on problems (missing or long title, more than 9 sections, unknown block, em-dash)
   and prints what to fix.
5. **Publish** with the Artifact tool. The template already meets the page contract, so do not redesign
   it. For a revision in the same session, republish the same file path to keep the URL; in a later
   session, pass the artifact URL.
6. **Reply** with the link, then two short lists: how to use it (keys, ticks, the funnel if present) and
   **"Added beyond your notes"**, naming every line you wrote that the user did not, so they can check
   they would say it. Record the link in the person's note so the next session updates the same page.

## Voice and truth rules

- **The user's words first.** When they give notes, keep their wording; fix spelling and grammar only.
- **Answer first, then stop.** Each item is one plain sentence or a short bullet, about 20 words at
  most, with real numbers. No scene-setting, no epigrams, no "not X, Y", no callback lines. Q&A cards
  hold a one-sentence answer and one example.
- **Numbers and claims come from the record.** Use the evidence library and approved spoken answers in
  memory. Never put a claim on the sheet that the record does not support; a gap goes on a Q&A card as
  the honest spoken answer.
- **Recruiter calls get a Logistics block** (`kv`): work authorization, expected rate from the logistics
  file, and availability. If the engagement type differs from the stored rate's type, ask before quoting.
- **Compensation, only if asked** on non-recruiter calls: use the line in that meeting's prep notes, or
  the posted range.

## Section recipes

Pick 4 to 7 sections. Order them the way the conversation will run.

| Meeting | Sections |
|---|---|
| Hiring manager or panel interview | Open (who I am, 3-4 facts) · Their problem · My proof (stories with numbers) · Tough questions (`qa`) · Questions I ask · Close (the ask) |
| Recruiter or agency screen | Open · Fit to the req · Logistics (`kv`) · Gaps (`qa`) · Questions · Close |
| Case or problem-solving interview | Open · Frame (`split`) · Diagnose (`stages` + `cards`) · Plan (`steps`) · Pushback (`quote`, `numbered`, `columns`) · Close (`chain`) |
| Client, sales, or discovery call | Goal · Their world · Questions to ask · Proof · Objections (`qa`) · Next step |
| Networking or referral call | Open (the relationship) · My arc · Ask them · Bridge to their world · The asks (`numbered`) · Close |

## Sheet JSON

```json
{"title": "2-5 word name", "subtitle": "Meeting type · who · when", "slug": "unique-id-for-ticks",
 "sections": [{"id": "open", "label": "Open", "heading": "Who I am", "blocks": [ ... ]}]}
```

Block types (text fields accept `<mark>`, `<b>`, `<em>`, `<br>`; use `<mark>` on the 1-3 words that must not be missed):

| type | fields | renders as |
|---|---|---|
| `lead` | `text` | one large line |
| `facts` | `items: [{big, small}]` | credibility tiles |
| `split` | `items: [{eyebrow, text}]`, `verdict?` | side-by-side boxes |
| `stages` | `items: [{id, label, hint}]`, `caption?`, `start_hint?` | clickable funnel; put a `cards` block right after it and give cards `stages: [ids]` to light them |
| `cards` | `items: [{title?, eyebrow?, body?, bullets?, stages?, fork?}]`, `cols?` | tickable cards |
| `steps` | same as cards | tickable timeline (weeks, phases) |
| `numbered` | `items: [text]` | tickable numbered sequence (only for real sequences) |
| `qa` | `items: [{q, a}]` | tickable question and answer cards |
| `columns` | `items: [{title, tone?: "ok"\|"drop", bullets}]` | ownership or comparison columns |
| `kv` | `items: [{k, v}]` | logistics rows |
| `quote`, `note`, `callout` | `text` | their words, a proof line, the one rule to remember |
| `chain` | `items: [text]` | the closing sequence |

## Updating a sheet

The user may come back with "add X" or "change Y". Edit `sheet.json`, rebuild, and republish to the
same URL. Keep the `slug` unchanged so ticks survive.
