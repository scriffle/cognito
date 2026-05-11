#!/usr/bin/env python3
"""Generate quality-pass log: files & MC items needing distractor rewrites.
- Items with 'in maths and...' or other padder remnant filler
- Items where stripping left parity issues
"""
import json
import os
import time

ROOT = "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"

# Patterns that indicate distractors got generic padding (not real content)
PADDING_MARKERS = [
    "in maths and everyday calculations",
    "in maths and",
    "across many problem types",
    "across many regions over many years",
    "across many societies",
    "in any country at any stage",
]

records = []
for root, dirs, fs in os.walk(os.path.join(ROOT, "questions")):
    if "/_" in root:
        continue
    for f in sorted(fs):
        if not f.endswith(".json") or f.endswith(".skeleton.json"):
            continue
        path = os.path.join(root, f)
        try:
            d = json.loads(open(path).read())
        except Exception:
            continue
        items = []
        for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
            for idx, v in enumerate(d.get(L, [])):
                if v.get("type") != "mc":
                    continue
                strs = [v.get("correct") or ""] + [x.get("answer") or "" for x in v.get("distractors", [])]
                bad = [s for s in strs if any(m in s for m in PADDING_MARKERS)]
                if bad:
                    items.append({
                        "level_key": L,
                        "slot_index": idx,
                        "variant": v.get("variant"),
                        "question": v.get("question", ""),
                        "correct": v.get("correct", ""),
                        "distractors": [x.get("answer", "") for x in v.get("distractors", [])],
                        "n_padded": len(bad),
                    })
        if items:
            records.append({
                "path": os.path.relpath(path, ROOT),
                "n_items_needing_rewrite": len(items),
                "items": items,
            })

# Sort by count descending (worst first)
records.sort(key=lambda r: r["n_items_needing_rewrite"], reverse=True)

out = {
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "total_files": len(records),
    "total_mc_items": sum(r["n_items_needing_rewrite"] for r in records),
    "purpose": "MC items with distractors containing generic padding filler — need natural-content rewrites",
    "files": records,
}

out_path = os.path.join(ROOT, "questions/_tracker/quality_pass_log.json")
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print(f"Quality log → {out_path}")
print(f"Files needing rewrite: {len(records)}")
print(f"MC items needing rewrite: {sum(r['n_items_needing_rewrite'] for r in records)}")
print()
# Top 20 worst offenders
print("Top files by item count:")
for r in records[:20]:
    print(f"  {r['n_items_needing_rewrite']:3d}  {r['path']}")
