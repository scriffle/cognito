#!/usr/bin/env python3
"""Recompute every level manifest's completed/validated counts and statuses
to match the actual files on disk. Idempotent.

For each subject in a level's manifest:
- Scan the matching folder for .json files (excluding .skeleton.json)
- Any code whose .json file exists -> status "validated"
- Any code whose .json file does NOT exist -> status "pending"
- Recompute `completed` and `validated` totals
"""
import json
import os

ROOT = "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"


def update(level: str) -> tuple[int, int]:
    mpath = os.path.join(ROOT, f"questions/_tracker/level-{level}-manifest.json")
    if not os.path.exists(mpath):
        return 0, 0
    m = json.loads(open(mpath).read())
    subjects = m.get("subjects", {})
    total_validated = 0
    total_completed = 0
    for sub_key, sub in subjects.items():
        folder = sub.get("folderName")
        if not folder:
            continue
        sub_dir = os.path.join(ROOT, f"questions/level-{level}", folder)
        built = set()
        if os.path.isdir(sub_dir):
            for f in os.listdir(sub_dir):
                if f.endswith(".json") and not f.endswith(".skeleton.json"):
                    built.add(f[:-5])  # strip .json
        codes = sub.get("codes", {})
        v = 0
        for code, entry in codes.items():
            if code in built:
                entry["status"] = "validated"
                v += 1
            else:
                entry["status"] = "pending"
        sub["validated"] = v
        sub["completed"] = v  # treating completed == validated for present purposes
        total_validated += v
        total_completed += v
    # Update timestamp at top level if present
    from datetime import datetime, timezone
    m["_generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(mpath, "w") as f:
        json.dump(m, f, indent=2)
    return total_completed, total_validated


def main():
    for L in ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10"):
        c, v = update(L)
        print(f"level-{L}: completed={c} validated={v}")


if __name__ == "__main__":
    main()
