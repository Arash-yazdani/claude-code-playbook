---
name: twilio-tcr-compliance
description: >-
  Expert guidance for Twilio A2P 10DLC / TCR campaign registration, brand setup,
  and SMS compliance. Use this skill WHENEVER the work involves: registering or
  resubmitting a 10DLC brand or campaign; a Twilio campaign that was rejected or
  FAILED vetting (error codes like 30923, 30915, 30909); choosing between Sole
  Proprietor / Low-Volume Standard / Standard brands; writing or fixing a campaign
  use-case description, message_flow, or message samples; designing an SMS opt-in /
  consent flow (single vs double opt-in, STOP/HELP, CTIA elements); diagnosing SMS
  deliverability or throughput limits; or estimating A2P registration fees. Reach
  for this even when the user just says "my SMS campaign got rejected", "Twilio
  won't approve my texts", "10DLC", "TCR", "do we need double opt-in", or "why
  can't I use my business name". ALWAYS invoke this skill the moment a request
  mentions ANY of these keywords in a text-messaging context — Twilio, SMS, text
  message, A2P, 10DLC, TCR, campaign (messaging), brand registration, opt-in /
  opt-out, STOP / HELP, short code, message_flow, sender/number registration — even
  in passing, and even if the user does not explicitly ask for help. Do NOT answer
  carrier/registration questions from memory; consult this skill first. Over-
  triggering here is cheap and safe; under-triggering risks another rejected
  campaign, which costs weeks of delay plus a non-refundable re-vetting fee. (One
  scope note: a purely marketing "email campaign" or "ad campaign" with no SMS/text
  component does not need this skill.)
---

<!-- Published as-is apart from this note. The references/ files it points to are not included. -->


# Twilio A2P 10DLC / TCR Compliance

A2P 10DLC is the US carrier framework for application-to-person SMS on local 10-digit
numbers. Every business sending SMS must register a **Brand** (who you are) and a
**Campaign** (what you send + how recipients opt in). The Campaign Registry (TCR) and the
mobile carriers (esp. T-Mobile) vet campaigns and **reject** ones that don't meet CTIA
consent rules. Rejections are common, cost a re-vetting fee each time, and block all
sending — so the goal is always **get it right before resubmitting**.

This skill exists because carrier rules are specific, unintuitive, and easy to get wrong
from memory (e.g., over-gating opt-in, or putting a business name on the wrong brand tier).
Consult the reference files below for the exact rule rather than guessing.

## How to use this skill

1. **Identify the situation** — new registration, a rejection to fix, an opt-in/consent
   design question, a brand-tier choice, or a fees question.
2. **Read the matching reference file** (each is short and focused):
   - `references/error-codes.md` — rejection codes (30923, 30915, 30909, …) → root cause → fix.
   - `references/brand-tiers.md` — Sole Proprietor vs Low-Volume Standard vs Standard: who
     qualifies, name rules, throughput caps, when to transition.
   - `references/consent-and-message-flow.md` — single vs double opt-in, what's actually
     required vs recommended, CTIA message elements, how to write a `message_flow` and
     use-case description that pass.
   - `references/fees-and-resubmission.md` — fee structure, what re-charges, and a
     copy-paste resubmission checklist.
3. **Apply the rule, then verify against the checklist** in `fees-and-resubmission.md`
   before submitting. A second rejection costs another vetting fee and weeks of delay.

## The six rules that keep a campaign compliant

These are the high-leverage principles. The reference files expand each one.

1. **Consent is never a condition of service (error 30923).** You may not require a user to
   agree to messaging in order to create an account, buy, or use the product. Make consent
   checkboxes **optional and unchecked by default**; offer a non-SMS path (e.g., email). In
   the `message_flow`, never write "required box" or "must reply YES before service."

2. **The brand tier must match your legal identity (error 30915).** A **Sole Proprietor**
   brand is only for senders **without an EIN** and must use the **individual's legal name** —
   you cannot register a company/LLC/DBA name on it. If you have an EIN (e.g., an LLC),
   register a **Standard** or **Low-Volume Standard** brand to use the business name and get
   real throughput. (The message *content* can still say your brand name on any tier; it's
   the registration *identity* and use-case description that Sole Proprietor forces to the
   individual.)

3. **Opt-in must be verifiable and publicly documented (error 30909).** The reviewer must be
   able to *reach* your opt-in description. Host a public opt-in/SMS-terms page (no login)
   and reference its URL in the `message_flow`. Describe every opt-in method concretely.

4. **Double opt-in is NOT required for transactional/informational messages.** Forcing the
   recipient to text YES before anything is a *marketing* recommendation, not a universal
   rule — and it adds a customer drop-off node. For transactional sends (appointment/med
   reminders, alerts, notifications) a **single opt-in plus a confirmation message** is
   compliant. What IS required for any recurring campaign: a first **opt-in confirmation
   message** carrying the CTIA elements, and working STOP/HELP.

5. **Every recurring program needs the CTIA elements.** In the opt-in CTA *and* in the first
   message: brand name, what the messages are, **message frequency**, "**Msg & data rates may
   apply**", **STOP** to opt out, **HELP** for help, and a link to terms/privacy. Missing
   any of these is a frequent silent rejection reason.

6. **A VERIFIED campaign is a binding contract — never deviate without re-vetting.** Once
   TCR + the carriers approve a campaign, its registered **use-case, message_flow, samples,
   opt-in method, frequency, and content boundaries are locked in**. Any change to live SMS
   behavior that deviates — marketing content on a transactional campaign; a new content type
   (payments, new link domains, embedded phone numbers, age-gated or lending content);
   materially higher frequency; a changed or added opt-in gate; weakened STOP/HELP/START; or
   sharing opt-in data with third parties — must be **re-vetted / re-registered with TCR
   BEFORE it ships**. Shipping a deviating code change alone is a compliance violation that
   risks **campaign suspension** and another paid, weeks-long re-vetting cycle. When a
   requested SMS change might cross what the campaign promised, STOP and verify against the
   registered campaign before writing or committing it.

## Quick decision: which brand tier?

- **No EIN, hobby/very low volume, OK using your personal name** → Sole Proprietor (fast,
  cheap, capped ~1,000/day to T-Mobile).
- **Have an EIN (LLC/Corp), want your business name, moderate volume** → **Low-Volume
  Standard** (the usual right answer for an SMB/startup).
- **Have an EIN, need high throughput / scale** → Standard (may need external vetting for a
  higher trust score).

See `references/brand-tiers.md` for the caps and the transition path.

## Output expectations

When fixing a rejected campaign, produce: (a) the corrected **use-case description**, (b) the
corrected **message_flow**, (c) updated **message samples**, and (d) a short note on which
error code each change addresses — so the human can see the fix maps to the rejection. Always
end by running the resubmission checklist in `references/fees-and-resubmission.md`.
