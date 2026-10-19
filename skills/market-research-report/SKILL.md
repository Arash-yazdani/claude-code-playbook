---
name: market-research-report
description: >-
  Market research report pipeline for consulting engagements. Use when building, reviewing, or
  polishing a market research or discovery study. Runs a three-agent adversarial review (CMO, CPO,
  gap research), a three-pass edit cycle (data fixes, content additions, judge), a machine-enforced
  brand gate, and renders a client-ready PDF. Trigger on: "market research", "market report",
  "discovery study", "competitive analysis", or any deliverable that is a written market study.
---

<!-- Sanitized for publication: client and engagement names, brand-kit specifics, logo paths and
     brand copy removed. Reference files (design system, brand rules, judge rubric)
     are not included. -->

# Market research report pipeline

A repeatable workflow for producing client-ready market research reports. Used at Modeo, Arash
Yazdani's AI consulting studio, first on a client engagement in September 2026.

## When to use

Any engagement where the deliverable is a market research report, competitive analysis, or
product-market discovery study. The pipeline assumes the report exists as an HTML file.

## Confidentiality

Engagements operate under NDA unless stated otherwise. Never transmit client concepts, proprietary
data, or unpublished findings to external services. Research agents use generic prompts only. Never
publish the report as a shared artifact unless the client authorizes it.

---

## Phase 0: Report authoring (if starting from scratch)

Read `references/report-design-system.md` for tokens, typography, section structure and components.

- Serif display face, sans body face, monospace for data and numbers
- 15-17 numbered sections, sticky table of contents, stat tiles, bar charts, SWOT cards
- Full light/dark/print palettes via CSS custom properties
- Print stylesheet forces the light palette: `@page { size:Letter; margin:14mm 12mm 16mm }`

---

## Phase 1: Three-agent adversarial review

Launch three agents **in parallel**. Each reviews the full HTML report from a different perspective.
No client IP in the agent prompt.

### Agent 1: CMO review
```
Review this market research report from the perspective of a Chief Marketing Officer.
Score it 1-10 on: narrative clarity, persuasiveness, data presentation, visual design,
client-readiness. List specific issues ranked by severity. Does it tell a clear story?
Is the verdict up front? Would an executive who reads only the first two pages get the
finding? Are the charts honest and labeled? Is the positioning clear?
```

### Agent 2: CPO review
```
Review this market research report from the perspective of a Chief Product Officer.
Score it 1-10 on: analytical rigor, data accuracy, logical consistency, completeness of
competitive analysis, actionability of recommendations. List specific issues ranked by
severity. Are the numbers internally consistent? Do cross-references match? Are
assumptions stated? Is the recommendation supported by the evidence?
```

### Agent 3: Gap research
```
Identify gaps in this market research report. For each gap: what is missing, why it
matters, what data or analysis would fill it, and how hard it is to obtain. Check:
regulatory/compliance risks, international comparables, adjacency analysis, timing
window, platform dependency, buyer persona depth, pricing validation, distribution
channel risks, technology moat durability.
```

Collect all findings before proceeding.

---

## Phase 2: Edit cycle

### Pass 1: Data fixes (correctness)

Cross-reference every number in the report against itself:
- Bar chart values vs. prose claims
- Table figures vs. badges on summary cards
- Date consistency (masthead, footer, section references)
- Cross-section references ("92% gross margin" in one place, "97%" in another)
- Arithmetic in derived figures ("market cap $X less $Y net cash = $Z")

Data errors destroy credibility faster than any other defect.

### Pass 2: Content additions (impact)

Add content where CMO, CPO and gap findings converge. Additions that proved high-value:

1. **Decision brief** after the verdict: a numbered list of what to do before spending anything.
   Zero-cost validation first, paid phases last.
2. **Platform dependency risk** in unit economics: if the recommended route runs on a channel the
   product does not control, state it.
3. **Validation gap flags** on recommended routes: if no potential customer or partner has been
   contacted, say so on the route card.
4. **Methodology note**: what the study is based on (desk research, public filings) and what it is
   not (no primary buyer research, no survey data).

Do not add content that pads, introduces claims without evidence, or hedges the verdict.

### Pass 3: Analysis judge (gating)

Score the report against `references/modern-analysis-judge.md`. A report that fails any Layer 1 gate
is not client-ready and its Layer 2 score is not reported.

Run the judge as a **separate adversarial agent**, not inline. Reviewing your own edits does not work;
every real defect on the first engagement was found by an agent that had not written the text.

**Run the mechanical checks yourself first.** On the first engagement they found five of ten
competitive-matrix summary counts disagreeing with the matrix they summarized, three charts whose bar
widths contradicted their own labels, and an enterprise value that did not reconcile:

```
# Every derived figure recomputed from its stated inputs
# Every summary count re-derived from the exhibit it summarizes
# Every bar width checked against the value it encodes, on a stated scale
# Every figure appearing twice checked for agreement
```

**Re-run the whole judge after remediating.** The first remediation pass changed a headline reference
class without propagating it to six downstream mentions, and introduced a new arithmetic error. Budget
at least two judge cycles.

**When a discrepancy cannot be resolved, flag it in the report.** A figure the reader is warned about
costs less credibility than one silently made to tie.

### Pass 4: Brand gate (gating)

The brand kit is machine-enforced: `python3 brand-gate.py <html> <pdf>`. `FAIL` blocks the send. Run
it on **both** the HTML and the rendered PDF; the HTML catches palette and voice, the PDF catches font
embedding.

Three failures the gate caught:

1. **A requested font is not an embedded font.** A font absent from the rendering machine silently
   falls back to system fonts. Rendered reports use a base64-embedded webfont.
2. **Remote webfonts do not embed.** Chrome's PDF writer emits Type3 glyph procedures for fonts loaded
   over the network. Verify zero Type3 fonts on every render.
3. **`background-clip: text` breaks in print.** Gradient text is screen-only.

Reports that quote third-party dollar figures trip the pricing check. State once in the document that
dollar figures are third-party market data, not the consultancy's pricing.

Also grep for banned strings (em-dashes, deprecated product names) before rendering.

---

## Phase 3: PDF generation

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="<output path>" "<input html path>"
```

The flag is `--no-pdf-header-footer`. `--print-to-pdf-no-header` is silently ignored and leaves the
default headers and footers in the PDF.

Verify page count (25-30 for a full study), no browser chrome in headers or footers, charts and tables
render.

---

## Phase 4: Report what changed

- **Pass 1:** each data fix (old value, new value, location)
- **Pass 2:** each content addition (what, where, why)
- **Passes 3-4:** judge and brand gate results
- **PDF:** page count, file size, output path
