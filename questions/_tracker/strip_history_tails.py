#!/usr/bin/env python3
"""Strip padding tails from correct answers in L08 History files.

Mechanical, safe cleanup of the "in maths and everyday calculations..." /
"across many regions over many years..." / trailing " in" tails appended
by the upstream generation pass.

Only modifies the `correct` field; distractors are left for manual rewrite.
"""
import json
import os
import re
import sys

ROOT = "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"

# Compound tail patterns to strip
TAIL_PATTERNS = [
    re.compile(r"\s+in\s+maths\s+and\s+everyday.*$", re.IGNORECASE),
    re.compile(r"\s+across\s+many\s+(problem\s+types|regions|societies|countries|years).*$", re.IGNORECASE),
    re.compile(r"\s+in\s+maths\s+and\s+.*$", re.IGNORECASE),
]
# Trailing " in" / " in " (orphan preposition after strip)
TRAILING_IN_RE = re.compile(r"\s+in\.?\s*$")


def clean(s: str) -> str:
    if not s:
        return s
    out = s
    for pat in TAIL_PATTERNS:
        out = pat.sub("", out)
    out = TRAILING_IN_RE.sub("", out)
    out = re.sub(r"\s+", " ", out).strip()
    out = out.rstrip(",;: ")
    return out


def process_file(path: str) -> int:
    if path.endswith(".skeleton.json"):
        return 0
    d = json.loads(open(path).read())
    changes = 0
    for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
        for v in d.get(L, []):
            if v.get("type") != "mc":
                continue
            old = v.get("correct") or ""
            new = clean(old)
            if new != old:
                v["correct"] = new
                changes += 1
    if changes:
        with open(path, "w") as f:
            json.dump(d, f, indent=2)
    return changes


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "questions/level-08/History")
    files = sorted(
        os.path.join(target_dir, f)
        for f in os.listdir(target_dir)
        if f.endswith(".json") and not f.endswith(".skeleton.json")
    )
    total = 0
    for p in files:
        n = process_file(p)
        if n:
            print(f"{n:4d}  {os.path.relpath(p, ROOT)}")
            total += n
    print(f"\nTotal: {total} correct-answer cleanups in {len(files)} files")


if __name__ == "__main__":
    main()
