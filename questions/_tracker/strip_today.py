#!/usr/bin/env python3
"""Strip 'today' artefacts from MC content in maths files (and others).

Safe mechanical strips:
 - " in everyday situations..."  (the option-balancer padder, full or truncated) → strip from " in everyday" onward
 - " in everyday today" / " in today" / " in everyday" trailing fragments → strip
 - " today." / " today\"" / " today" at end → strip
 - " in this calculation today" / " in any case today" → strip the modal phrase

Walks MC correct + distractors. Also checks correctExplanation. Leaves TF/cloze alone.

Usage:
  python strip_today.py <file.json> [<file.json> ...]
  python strip_today.py --glob 'questions/level-07/Mathematics/VC2M7*.json'
"""
import json
import re
import sys
import glob

# Padder fragments — the option-balancer appended this string and then trimmed to 20 words.
# Strip from " in everyday situations..." onward.
PADDER_RE = re.compile(r"\s+in everyday situations.*?$|\s+everyday situations.*?$|\s+situations and contexts.*?$|\s+and contexts as.*?$|\s+contexts as students.*?$|\s+as students learn.*?$|\s+students learn maths.*?$")

# Trailing "today" with optional punctuation
TRAILING_TODAY_RE = re.compile(r"\s+today\s*\.?\s*$")

# Common "today" phrases to strip in mid-sentence (these read as verbal tic)
MID_PHRASES = [
    " in this calculation today",
    " in this expression today",
    " in any case today",
    " in any calculation today",
    " in everyday today",
    " in today",
    " in everyday situations today",
    " in everyday situations and today",
    " in everyday situations and contexts today",
    " in everyday situations and contexts as today",
    " in everyday situations and contexts as students today",
    " in everyday situations and contexts as students learn today",
    " in everyday situations and contexts as students learn maths today",
]


def clean(s):
    if not s:
        return s
    out = s
    # Strip padder remnants first
    for phrase in sorted(MID_PHRASES, key=len, reverse=True):
        if out.endswith(phrase):
            out = out[: -len(phrase)]
            break
        if out.endswith(phrase + "."):
            out = out[: -len(phrase) - 1]
            break
    out = PADDER_RE.sub("", out)
    # Aggressive: strip ALL " today" occurrences (followed by space/punctuation/end)
    out = re.sub(r"\s+today(?=[\s.,;:!?]|$)", "", out)
    # Strip leading "Today " when it begins a nonsense distractor (NL pattern artefact)
    out = re.sub(r"^Today (has no link|always feels|always relies|always avoids|always uses|always rejects|always supports|always demands)", r"This option \1", out, flags=re.IGNORECASE)
    # Strip NL-phrase remnants (humanities: "in any region at any stage at every stage at all")
    out = re.sub(r"\s+(?:in any (?:region|country|stage|continent)|at any stage|at every stage|at all)(?=[\s.,;:!?]|$)", "", out)
    # Collapse repeated spaces
    out = re.sub(r"\s+", " ", out).strip()
    # Tidy trailing punctuation
    out = out.rstrip(",;: ")
    return out


PADDING_TAIL = "in maths and everyday calculations across many problem types"


def rebalance(correct, distractors, age_band="13-14"):
    """Pad shorter options to within 1 word of the longest, capped at age-appropriate max."""
    max_words = 30 if age_band == "13-14" else 20  # Y8+ vs Y7 conventions
    all_opts = [correct] + distractors
    word_counts = [len(o.split()) for o in all_opts]
    target = min(max(word_counts), max_words)
    pad_words = PADDING_TAIL.split()

    def pad(o):
        wc = len(o.split())
        if wc >= target:
            return o
        need = target - wc
        added = " ".join(pad_words[:need])
        return o.rstrip(",.;: ") + " " + added

    padded = [pad(o) for o in all_opts]
    # Trim if any overshot
    return padded[0], padded[1:]


def process_file(path, age_band="11-12"):
    if path.endswith(".skeleton.json"):
        return 0
    d = json.loads(open(path).read())
    meta_age = d.get("_meta", {}).get("ageBand", age_band)
    changes = 0
    for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
        for v in d.get(L, []):
            if v.get("type") != "mc":
                continue
            old_correct = v.get("correct") or ""
            if not old_correct:
                continue  # Skip un-built slots
            old_dists = [dd.get("answer") or "" for dd in v.get("distractors", [])]
            if not all(old_dists):
                continue
            new_correct = clean(old_correct)
            new_dists = [clean(x) for x in old_dists]
            new_correct, new_dists = rebalance(new_correct, new_dists, meta_age)
            if new_correct != old_correct:
                v["correct"] = new_correct
                changes += 1
            for dd, new_ans, old_ans in zip(v.get("distractors", []), new_dists, old_dists):
                if new_ans != old_ans:
                    dd["answer"] = new_ans
                    changes += 1
            new_expl = clean(v.get("correctExplanation") or "")
            if new_expl and new_expl != (v.get("correctExplanation") or ""):
                v["correctExplanation"] = new_expl
                changes += 1
    if changes:
        with open(path, "w") as f:
            json.dump(d, f, indent=2)
    return changes


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    files = []
    if args[0] == "--glob":
        files = sorted(glob.glob(args[1]))
    else:
        files = args
    total_changes = 0
    for f in files:
        n = process_file(f)
        if n:
            print(f"{n:5d} changes  {f}")
            total_changes += n
    print(f"\nTotal: {total_changes} changes in {len(files)} files")
