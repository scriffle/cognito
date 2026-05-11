#!/usr/bin/env python3
"""Audit every question .json file for 'today' in MC distractors (and correct).
Sorted by modification time (most recent first).
Outputs a JSON log: today_audit.json
"""
import json
import os
import time

ROOT = "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"
QROOT = os.path.join(ROOT, "questions")

records = []

for level in sorted(os.listdir(QROOT)):
    if not level.startswith("level-"):
        continue
    lvl_dir = os.path.join(QROOT, level)
    for subj in sorted(os.listdir(lvl_dir)):
        sd = os.path.join(lvl_dir, subj)
        if not os.path.isdir(sd):
            continue
        for f in sorted(os.listdir(sd)):
            if not f.endswith(".json") or f.endswith(".skeleton.json"):
                continue
            path = os.path.join(sd, f)
            try:
                d = json.loads(open(path).read())
            except Exception:
                continue
            mtime = os.path.getmtime(path)
            file_hits = []
            for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
                arr = d.get(L, [])
                for idx, v in enumerate(arr):
                    if v.get("type") != "mc":
                        continue
                    correct = v.get("correct", "")
                    distractors = [x.get("answer", "") for x in v.get("distractors", [])]
                    correct_has = " today" in correct or "today" in correct.split()
                    dist_has = [(" today" in dd or "today" in dd.split()) for dd in distractors]
                    if any(dist_has) or correct_has:
                        file_hits.append({
                            "level_key": L,
                            "slot_index": idx,
                            "variant": v.get("variant"),
                            "question": v.get("question", ""),
                            "correct": correct,
                            "correct_has_today": bool(correct_has),
                            "distractors": distractors,
                            "distractor_has_today": dist_has,
                        })
            if file_hits:
                records.append({
                    "path": os.path.relpath(path, ROOT),
                    "mtime": mtime,
                    "mtime_iso": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)),
                    "n_mc_with_today": len(file_hits),
                    "items": file_hits,
                })

# Sort by mtime descending
records.sort(key=lambda r: r["mtime"], reverse=True)

out = {
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "total_files": len(records),
    "total_mc_items": sum(r["n_mc_with_today"] for r in records),
    "files": records,
}

out_path = os.path.join(ROOT, "questions/_tracker/today_audit.json")
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

# Print summary by file
print(f"AUDIT SUMMARY  — wrote {out_path}")
print(f"Files affected: {len(records)}")
print(f"Total MC items with today: {sum(r['n_mc_with_today'] for r in records)}")
print()
print(f"{'mtime':<22} {'count':>5}  file")
print("-" * 80)
for r in records[:60]:
    print(f"{r['mtime_iso']:<22} {r['n_mc_with_today']:>5}  {r['path']}")
if len(records) > 60:
    print(f"... and {len(records) - 60} more files")
