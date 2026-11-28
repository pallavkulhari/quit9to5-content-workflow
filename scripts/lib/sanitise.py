#!/usr/bin/env python3
"""Sanitise a text file copied from the box before it lands in the portable repo.

Usage:
  python3 sanitise.py SRC DEST [--drop-topics quora,reddit] [--rewrite-links playbook|example]

What it does (in this order):
  1. Rewrites box-specific absolute paths to environment-variable placeholders
     ($Q9_ROOT, $Q9_REELS_DIR, $Q9_SKILLS_DIR, $NODE_BIN, $AGY_BIN, ...).
  2. Replaces account pointers with placeholders: Drive / Google file IDs,
     Buffer-style 24-hex IDs, 64-hex hashes, ElevenLabs-style 20-char IDs,
     UUIDs, GA4 measurement IDs.
  3. Replaces real email addresses with you@example.com and phone numbers with <PHONE>.
  4. Replaces manuscript line references with "manuscript.md (private, not included)".
  5. Optionally drops lines and whole sections about out-of-scope channels.
  6. Optionally rewrites relative links so they resolve inside the repo.

It never adds content. It is deterministic, so re-running on the same input
produces the same output (the sync job relies on that for idempotence).
"""
import re
import sys
import argparse

PATHS = [
    (r"/home/box/\.local/node-v[0-9.]+-linux-x64/bin", "$NODE_BIN"),
    (r"(~|/home/box)/\.local/bin/agy", "$AGY_BIN"),
    (r"/home/box/agent-data/workflows", "$Q9_SKILLS_DIR"),
    (r"/workspace/launch/manuscript\.md", "manuscript.md (private, not included)"),
    (r"/workspace/api-costs/ledger\.csv", "$PAID_CALL_LEDGER"),
    (r"/workspace/quit9to5/motion/reels", "$Q9_REELS_DIR"),
    (r"/workspace/quit9to5", "$Q9_ROOT"),
    (r"/workspace/launch", "$Q9_LAUNCH_DIR"),
    (r"/workspace", "$WORKSPACE"),
    (r"/home/box", "$HOME"),
]

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(\+91[\s-]?\d{5}[\s-]?\d{5}|\b[6-9]\d{9}\b)")
UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
HEX64 = re.compile(r"\b[0-9a-f]{64}\b")
HEX24 = re.compile(r"\b[0-9a-f]{24}\b")
GA4 = re.compile(r"\bG-[A-Z0-9]{8,12}\b")
DRIVE_URL_ID = re.compile(r"(id=|/d/|/folders/)([A-Za-z0-9_-]{20,})")
DRIVE_ID = re.compile(r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{24,43}(?![A-Za-z0-9_-])")
ID20 = re.compile(r"(?<![A-Za-z0-9_/-])[A-Za-z0-9]{20}(?![A-Za-z0-9_-])")
MS_LINES_PAREN = re.compile(r"\(\s*manuscript(\.md)?\s*~?\s*lines?\s*[\d][\d\s,–-]*\)", re.I)
MS_LINES = re.compile(r"manuscript(\.md)?\s*~?\s*lines?\s*[\d][\d,–-]*", re.I)


def mixed(tok):
    return any(c.isupper() for c in tok) and any(c.islower() for c in tok) and any(c.isdigit() for c in tok)


def scrub(text):
    for pat, rep in PATHS:
        text = re.sub(pat, rep, text)
    text = UUID.sub("<UUID>", text)
    text = HEX64.sub("<sha256>", text)
    text = HEX24.sub("<BUFFER_ID>", text)
    text = GA4.sub("<GA4_MEASUREMENT_ID>", text)
    text = DRIVE_URL_ID.sub(lambda m: m.group(1) + "<DRIVE_FILE_ID>", text)
    text = DRIVE_ID.sub(lambda m: "<DRIVE_FILE_ID>" if mixed(m.group(0)) or "_" in m.group(0) else m.group(0), text)
    text = ID20.sub(lambda m: "<ELEVENLABS_ID>" if mixed(m.group(0)) else m.group(0), text)
    text = EMAIL.sub(lambda m: m.group(0) if m.group(0).endswith("example.com") else "you@example.com", text)
    text = PHONE.sub("<PHONE>", text)
    text = MS_LINES_PAREN.sub("(manuscript.md, private, not included)", text)
    text = MS_LINES.sub("manuscript.md (private, not included)", text)
    text = re.sub(r"manuscript\.md \(private, not included\) \(private, not included\)", "manuscript.md (private, not included)", text)
    text = re.sub(r"\(private, not included\) +([).,;])", r"(private, not included)\1", text)
    # Any other line-number pointer into the manuscript on a line that names it
    fixed = []
    for line in text.split("\n"):
        if "manuscript" in line.lower():
            line = re.sub(r"\s*\(\s*~?\s*lines?\s+\d+(\s*[–-]\s*\d+)?\s*\)", "", line)
            line = re.sub(r",?\s*~?\s*lines?\s+\d+(\s*[–-]\s*\d+)?", "", line)
        fixed.append(line)
    return "\n".join(fixed)


def drop_topics(text, topics):
    if not topics:
        return text
    rx = re.compile(r"\b(" + "|".join(map(re.escape, topics)) + r")\b", re.I)
    out, skip_level = [], None
    for line in text.split("\n"):
        h = re.match(r"^(#{1,6})\s", line)
        if h:
            level = len(h.group(1))
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and rx.search(line):
                skip_level = level
                continue
        if skip_level is not None:
            continue
        if rx.search(line):
            continue
        out.append(line)
    return "\n".join(out)


LINKS = {
    "playbook": [
        (r"\[`SCRIPTS\.md`\]\(\./SCRIPTS\.md\)", "`SCRIPTS.md` (older S2/S3 drafts on the box, not included because they quote the manuscript)"),
        (r"\(\./reels/004_runway/", "(../examples/004_runway/"),
        (r"\(\./reels/005_toxic_hike/", "(../examples/005_toxic_hike/"),
        (r"`reels/003_loans/SCRIPT\.md`", "`reels/003_loans/SCRIPT.md` on the box (not included)"),
    ],
    "example": [
        (r"`\.\./COMMON_REEL_BRIEF\.md`", "`../../playbooks/COMMON_REEL_BRIEF.md`"),
        (r"\.\./COMMON_REEL_BRIEF\.md", "../../playbooks/COMMON_REEL_BRIEF.md"),
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dest")
    ap.add_argument("--drop-topics", default="")
    ap.add_argument("--rewrite-links", choices=sorted(LINKS), default=None)
    ap.add_argument("--header", default="", help="optional line(s) prepended after the first heading")
    a = ap.parse_args()
    text = open(a.src, encoding="utf-8").read()
    text = drop_topics(text, [t for t in a.drop_topics.split(",") if t])
    if a.rewrite_links:
        for pat, rep in LINKS[a.rewrite_links]:
            text = re.sub(pat, rep, text)
    text = scrub(text)
    if a.header:
        lines = text.split("\n")
        idx = 1 if lines and lines[0].startswith("#") else 0
        if lines and lines[0] == "---":  # YAML front matter: insert after it
            idx = lines.index("---", 1) + 1
        lines[idx:idx] = ["", a.header.replace("\\n", "\n"), ""]
        text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    open(a.dest, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    sys.exit(main())
