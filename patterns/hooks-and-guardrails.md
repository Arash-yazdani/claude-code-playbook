# Hooks and guardrails

Anything that must never happen is enforced by a hook, not requested in an instruction. Instructions shape behavior on average; a `PreToolUse` hook that returns `deny` blocks every instance, and its reason string tells the model what to do instead.

**Failure this prevents:** secrets entering the transcript. AI tools were able to read a production `.env` during routine debugging, and every key on that host had to be rotated. An instruction saying "do not read .env" was already in place.

## The `.env` hook

[`hooks/block-env-read.py`](../hooks/block-env-read.py) inspects every Bash command before it runs and denies:

- any reference to a `.env` file (`.env`, `.env.local`, `.env.bak-*`, remote `host:.env`), except `.env.example` / `.sample` / `.template` / `.dist`
- commands that print environment values indirectly: `docker compose config`, `docker inspect` without a narrow format, `printenv`, bare `env`, `/proc/*/environ`
- recursive `grep`, which reads `.env` files along the way; `rg` without `--hidden` is allowed because it skips dotfiles

Registration in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [{ "type": "command",
                    "command": "/usr/bin/python3 \"$HOME/.claude/hooks/block-env-read.py\"",
                    "timeout": 10 }] }
    ]
  }
}
```

## Hook design rules

- **Ship a self-test with the hook.** `block-env-read.py --test` runs 20 commands that must be blocked and 16 that must be allowed. Run it after every edit. The allow list matters as much as the block list: a hook that blocks `process.env` in source code or `docker compose ps` gets disabled by frustrated users.
- **State the threat model in the docstring.** This hook catches accidental reads by a cooperative model. It does not stop deliberate obfuscation. Saying so prevents false confidence.
- **The deny reason is an instruction.** "Do not work around this. Ask the user to run the command in their own terminal." gives the model a next step instead of a retry loop.
- **Decide fail-open or fail-closed explicitly** and comment it. This hook fails open on a malformed payload because the harness always sends valid JSON; a hook guarding a destructive action should fail closed.
- **Keep secrets on the host that uses them.** Remote checks read credentials and call the API on the server, and return only the result (see [`scheduled-tasks/vendor-status-poll`](../scheduled-tasks/vendor-status-poll/SKILL.md)).

## Guardrails that live in skills

Not every rule needs a hook. Guardrails that depend on judgment live in the skill for that domain, written as a hard rule with the incident that produced it:

- "Never edit the assistant in the vendor web UI; the next deploy overwrites it. Edit the source file and deploy." (voice skill)
- "Place a live test call only with explicit per-call confirmation; it rings a real phone." (voice skill)
- "A verified SMS campaign is a binding contract. Any change to live message behavior that deviates from it is re-vetted before it ships." (compliance skill)
- "Never route eval data through the production logging path." (eval skill)
