#!/usr/bin/env python3
"""Secret / ID / scope scan for the portable repo. Exits 1 if anything real-looking is found.

Usage: python3 secret_scan.py [REPO_ROOT]

Checks every file under REPO_ROOT (skipping .git) for:
  - forbidden files: .env (anything but .env.example), media/binary extensions,
    manuscript.md, part-one-draft.*, source-accounts.md, zip archives
  - credential shapes: OpenAI/Anthropic/xAI/Google/Slack/GitHub/Stripe keys,
    Bearer tokens, private-key blocks, ya29 OAuth tokens
  - account pointers: Buffer-style 24-hex IDs, Drive/Google file IDs,
    ElevenLabs-style 20-char IDs, UUIDs, GA4 IDs, long digit runs (10+)
  - personal data: real email addresses, Indian phone numbers
  - un-parameterised box paths (/workspace/..., /home/box/...)

Known false positives live in scripts/secret-scan-allowlist.txt, one per line:
  <path glob><TAB><python regex matched against the offending text>
Lines starting with # are comments.
"""
import fnmatch
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", ".."))
ALLOW_FILE = os.path.join(ROOT, "scripts", "secret-scan-allowlist.txt")

MEDIA = {".mp4", ".wav", ".mp3", ".mov", ".m4a", ".aac", ".png", ".jpg", ".jpeg", ".webp", ".gif",
         ".pdf", ".docx", ".doc", ".ttf", ".otf", ".woff", ".woff2", ".zip", ".tar", ".gz", ".b64"}
FORBIDDEN_NAMES = {"manuscript.md", "part-one-draft.md", "part-one-draft.docx", "source-accounts.md",
                   "cookies.txt", "credentials.json", "token.json"}

CHECKS = [
    ("openai/anthropic key", r"\bsk-(ant-)?[A-Za-z0-9_-]{16,}"),
    ("xai key", r"\bxai-[A-Za-z0-9]{16,}"),
    ("google api key", r"\bAIza[0-9A-Za-z_-]{30,}"),
    ("google oauth token", r"\bya29\.[0-9A-Za-z_-]{10,}"),
    ("slack token", r"\bxox[baprs]-[0-9A-Za-z-]{10,}"),
    ("github token", r"\b(ghp_[0-9A-Za-z]{20,}|github_pat_[0-9A-Za-z_]{20,})"),
    ("stripe key", r"\bsk_live_[0-9A-Za-z]{10,}"),
    ("elevenlabs key", r"\bsk_[0-9a-f]{40,}"),
    ("bearer token", r"Bearer\s+[A-Za-z0-9._~+/-]{20,}"),
    ("private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("assigned secret", r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+]{16,}"),
    ("24-hex id", r"\b[0-9a-f]{24}\b"),
    ("uuid", r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    ("ga4 id", r"\bG-[A-Z0-9]{8,12}\b"),
    ("drive id", r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{24,43}(?![A-Za-z0-9_-])"),
    ("20-char mixed id", r"(?<![A-Za-z0-9_/-])(?=[A-Za-z0-9]{20}(?![A-Za-z0-9_-]))(?=[A-Za-z0-9]*[A-Z])(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[0-9])[A-Za-z0-9]{20}"),
    ("long digit run", r"\b[0-9]{10,}\b"),
    ("email", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b"),
    ("phone", r"(\+91[\s-]?\d{5}[\s-]?\d{5}|(?<![0-9])[6-9]\d{9}(?![0-9]))"),
    ("box path", r"(/workspace/|/home/box)"),
]
SAFE_EMAIL = re.compile(r"@example\.(com|org)$")


def load_allow():
    rules = []
    if os.path.exists(ALLOW_FILE):
        for ln in open(ALLOW_FILE, encoding="utf-8"):
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"):
                continue
            glob, _, rx = ln.partition("\t")
            rules.append((glob, re.compile(rx)))
    return rules


def allowed(rules, rel, text):
    return any(fnmatch.fnmatch(rel, g) and rx.search(text) for g, rx in rules)


def main():
    rules = load_allow()
    hits, files = [], 0
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in (".git",)]
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, ROOT)
            ext = os.path.splitext(fn)[1].lower()
            if fn == ".env" or (fn.startswith(".env") and fn != ".env.example"):
                hits.append((rel, 0, "forbidden file", fn)); continue
            if ext in MEDIA or fn in FORBIDDEN_NAMES or "node_modules" in rel or ".hyperframes" in rel:
                hits.append((rel, 0, "forbidden file", fn)); continue
            if rel == os.path.join("scripts", "secret-scan-allowlist.txt") or rel == os.path.join("scripts", "lib", "secret_scan.py") or rel == os.path.join("scripts", "lib", "sanitise.py"):
                continue  # these files contain the patterns themselves
            try:
                text = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                hits.append((rel, 0, "binary file", fn)); continue
            files += 1
            for i, line in enumerate(text.split("\n"), 1):
                for name, rx in CHECKS:
                    for m in re.finditer(rx, line):
                        s = m.group(0)
                        if name == "email" and SAFE_EMAIL.search(s):
                            continue
                        if allowed(rules, rel, s) or allowed(rules, rel, line):
                            continue
                        hits.append((rel, i, name, s))
    print(f"secret_scan: {files} text files scanned under {ROOT}")
    if hits:
        for rel, i, name, s in hits:
            print(f"  HIT {rel}:{i} [{name}] {s[:80]}")
        print(f"secret_scan: FAIL ({len(hits)} hit(s)). Fix them, or add a reviewed false positive to scripts/secret-scan-allowlist.txt")
        return 1
    print("secret_scan: PASS (0 unallowlisted hits)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
