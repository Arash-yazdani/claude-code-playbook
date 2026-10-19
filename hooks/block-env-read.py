#!/usr/bin/env python3
"""PreToolUse hook (Bash): deny commands that would put .env secrets in the transcript.

AI tools with shell access can read secrets files, so this hook blocks the read
before it runs. It catches accidental reads by a cooperative model,
not deliberate workarounds (obfuscated paths, scripts that print one setting).

Self-test: python3 block-env-read.py --test
"""
import json
import re
import sys

# .env, .env.local, .env.bak-2026..., /opt/x/.env, host:.env (any case: APFS is case-insensitive).
# A word character before the dot (process.env, import.meta.env) means code, not a file.
ENV_FILE = re.compile(r"(?<!\w)\.env(?![a-z0-9])[\w.~-]*", re.I)
TEMPLATE = re.compile(r"\.env\.(example|sample|template|dist)$", re.I)

SEG = r"[^|;&\n]*"  # rest of the current simple command
RULES = [
    (rf"\bdocker[ -]compose\b{SEG}\sconfig(?=[\s'\"]|$)(?!{SEG}(--services|--volumes|--profiles|--images|--networks|--hash|--quiet|\s-q\b))",
     "docker compose config prints every value from .env"),
    (rf"\bdocker\s+(container\s+)?inspect\b(?!{SEG}(\s-f\b|--format))", "docker inspect prints the container's env vars"),
    (r"Config\.Env", "that format prints the container's env vars"),
    (r"\bprintenv\b", "printenv prints env vars"),
    (r"(^|[\s;&|(`'\"])env\s*($|[;&|)`'\"])", "bare env prints env vars"),
    (r"/proc/[^/\s]+/environ", "/proc/*/environ holds a process's env vars"),
    (rf"\b[ef]?grep\b{SEG}\s(-[a-zA-Z]*[rR][a-zA-Z]*|--recursive|--dereference-recursive|--directories=recurse)\b",
     "recursive grep also reads .env files (use the Grep tool or rg)"),
    (rf"\brg\b{SEG}\s(--hidden|-\.|-u{{2,}})(?=\s|$)", "rg with hidden files reads .env files"),
]


def why_blocked(cmd):
    for token in ENV_FILE.findall(cmd):
        if not TEMPLATE.search(token):
            return f"it touches {token}"
    for pattern, why in RULES:
        if re.search(pattern, cmd):
            return why
    return None


def selftest():
    block = [
        "cat .env", "cat ./.env.local", "head -5 .ENV",
        "ssh prod-host 'grep API_KEY /opt/app/.env'",
        "shred -u /opt/app/.env.bak-20260101",
        "scp prod-host:/opt/app/.env /tmp/x",
        "python3 -c \"print(open('.env').read())\"",
        "cat .env.example .env",
        "docker compose config",
        "ssh prod-host 'cd /opt/app && docker compose config'",
        "docker inspect app_container",
        "docker inspect -f '{{json .Config.Env}}' app_container",
        "ssh prod-host 'docker exec app_container env'",
        "env | sort",
        "docker compose exec app printenv API_KEY",
        "cat /proc/1/environ",
        "grep -rn STRIPE .", "grep --recursive KEY /opt/app",
        "rg --hidden SECRET", "rg -uu SECRET",
    ]
    allow = [
        "cat .env.example", "cp .env.example /tmp/example",
        "rg -n 'process.env' frontend/src", "rg -n 'import.meta.env' frontend/src",
        "grep -n settings app/config.py",
        "docker compose ps", "docker compose config --services",
        "docker compose exec app cat app/config.py",
        "docker inspect -f '{{.State.Health.Status}}' app_container",
        "docker volume inspect app_pgdata",
        "/usr/bin/env python3 -m pytest -q", "env FOO=1 python3 x.py",
        "uv venv .venv && source .venv/bin/activate",
        "git grep -n JWT_SECRET",
        "openssl rand -hex 32 | ssh prod-host rotate-secret JWT_SECRET",
        "ls -la",
    ]
    wrong = [c for c in block if not why_blocked(c)] + [c for c in allow if why_blocked(c)]
    for c in wrong:
        print("WRONG:", c, "->", why_blocked(c))
    total = len(block) + len(allow)
    print(f"{total - len(wrong)}/{total} ok ({len(block)} blocked, {len(allow)} allowed)")
    return 1 if wrong else 0


def main():
    if sys.argv[1:] == ["--test"]:
        return selftest()
    try:
        cmd = json.load(sys.stdin)["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        return 0  # ponytail: fails open on a malformed payload; Claude Code always sends a valid one
    why = why_blocked(cmd)
    if why:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Blocked: {why}. .env secrets must never reach the model. "
                "Do not work around this. Ask the user to run the command in their own terminal."),
        }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
