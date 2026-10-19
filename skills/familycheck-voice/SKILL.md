---
name: familycheck-voice
description: Use whenever working on the FamilyCheck voice / phone-call layer: the check-in or consent voice assistant, outcome classification, the emergency path, caregiver alerts, or the call evaluation suites. Loads the standing guardrails so fixed behavior is not re-broken.
---

<!-- Published as a structural example. FamilyCheck's source is private; this copy keeps only
     what the public case study (github.com/Arash-yazdani/familycheck-engineering) states.
     Script names, assistant configuration, prompt mechanics and internal numbers are removed. -->

# FamilyCheck voice / conversation work

**Before changing anything in the voice layer, read the lessons doc** in the product repo
(`docs/<voice-lessons>.md`).

That doc is the source of truth. This skill is the quick reference and guardrails. **If anything
here conflicts with the doc, the doc wins, and update the doc.**

## Always do first
1. Dump the live assistant configuration (read-only) before touching it.
2. Diff live configuration against the source of truth in the repo. Assistants are defined in code;
   a change made only in a vendor dashboard is overwritten by the next deploy.

## Hard guardrails
- **Six outcome states:** `confirmed · deferred · denied · concern · unclear · no-answer`.
  `unclear` is the abstain path and routes to a human. Never remove it or map it to the nearest
  confident label.
- **The emergency path is deterministic.** It does not depend on the model choosing to say the
  right words. It was added after a live call exposed the gap; do not regress it to model-spoken text.
- **Consent is a separate assistant with its own definition of correct**: was consent freely given,
  and recorded faithfully per channel. Calls and texts are asked and tagged separately; a patient
  who declines texts is never texted, enforced at one chokepoint, not at each send site.
- **Recorded voice consent is the opt-in.** Do not reintroduce a "reply YES" activation gate; carriers
  reject consent as a condition of service.
- **The assistant never discloses phone numbers, account identifiers or internal IDs.** This is a
  test assertion, not only prompt text. Keep it in the suite.
- **Traces are PII-redacted before they leave the system.** Patient data does not go to an
  observability tool.
- **Every safety property is bound to a check that blocks a release.** A guardrail without a failing
  check is a wish.

## Evals
- Scenario suites follow the CRISP taxonomy (Common, Realistic, Invalid/malicious, Specific/edge,
  Performance); report turn-pass and scenario-pass separately.
- Evals measure model behavior. Audio-level behavior (how the closing sounds, pronunciation) is
  verified only on a live call.

## Deploy and verify a voice change
1. Edit the source-of-truth configuration in the repo; compile and dry-run.
2. Merge, deploy, push the configuration to the voice platform.
3. Re-run the live-vs-source diff (expect no differences), then the relevant eval suite.
4. **Place a live test call only with explicit per-call confirmation.** It rings a real phone.
