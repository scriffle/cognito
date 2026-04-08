#!/usr/bin/env python3
"""
Generates structural skeleton JSON files for all curriculum codes.
All type/variant/bloomsLevel fields pre-filled. Content fields set to null.

Reads: cd_explanations.json, area-code-mapping.json
Writes: questions/level-XX/Subject/CODE.skeleton.json

Usage:
    python generate-skeletons.py                    # All codes
    python generate-skeletons.py --code VC2S2U01    # Single code
    python generate-skeletons.py --level 2          # All codes at one level
    python generate-skeletons.py --dry-run           # Count only, no files
"""

import json
import os
import re
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

BLOOMS_TYPE_COUNTS = {
    2: {"tf": 12, "mc": 12, "cloze": 2},
    3: {"tf": 8, "mc": 12, "cloze": 6},
    4: {"tf": 2, "mc": 12, "cloze": 12},
    5: {"tf": 0, "mc": 14, "cloze": 12},
}

LEVEL_AGE_BAND = {
    1: "5-6", 2: "7-8", 3: "7-8", 4: "9-10", 5: "9-10",
    6: "11-12", 7: "11-12", 8: "13-14", 9: "13-14", 10: "15-16",
}

AGE_BAND_MC_DISTRACTORS = {
    "5-6": 2, "7-8": 2, "9-10": 2, "11-12": 2, "13-14": 3, "15-16": 3,
}


def tf_skeleton(variant, blooms_level):
    return {
        "type": "tf",
        "variant": variant,
        "bloomsLevel": blooms_level,
        "question": None,
        "correct": None,
        "correctExplanation": None,
        "distractors": [
            {"answer": None, "explanation": None}
        ],
    }


def mc_skeleton(variant, blooms_level, distractor_count):
    return {
        "type": "mc",
        "variant": variant,
        "bloomsLevel": blooms_level,
        "question": None,
        "correct": None,
        "correctExplanation": None,
        "distractors": [
            {"answer": None, "explanation": None}
            for _ in range(distractor_count)
        ],
    }


def cloze_skeleton(variant, blooms_level):
    """Default 2-blank scaffold. AI may add blanks 3-4 if needed."""
    return {
        "type": "cloze",
        "variant": variant,
        "bloomsLevel": blooms_level,
        "sentence": None,
        "blanks": [
            {
                "id": "1",
                "correct": None,
                "correctExplanation": None,
                "distractors": [
                    {"answer": None, "explanation": None, "misconceptionSource": None},
                    {"answer": None, "explanation": None, "misconceptionSource": None},
                ],
            },
            {
                "id": "2",
                "correct": None,
                "correctExplanation": None,
                "distractors": [
                    {"answer": None, "explanation": None, "misconceptionSource": None},
                    {"answer": None, "explanation": None, "misconceptionSource": None},
                ],
            },
        ],
        "scoring": None,
    }


def build_blooms_array(blooms_level, mc_distractor_count):
    counts = BLOOMS_TYPE_COUNTS[blooms_level]
    items = []
    variant = 1

    for _ in range(counts["tf"]):
        items.append(tf_skeleton(variant, blooms_level))
        variant += 1
    for _ in range(counts["mc"]):
        items.append(mc_skeleton(variant, blooms_level, mc_distractor_count))
        variant += 1
    for _ in range(counts["cloze"]):
        items.append(cloze_skeleton(variant, blooms_level))
        variant += 1

    return items


def parse_level_from_code(code):
    match = re.match(r"^VC2[A-Z]+?(\d+)", code)
    if not match:
        return None
    return int(match.group(1))


def find_area(code, areas):
    """Match code to area, longest prefix first."""
    for prefix in sorted(areas.keys(), key=len, reverse=True):
        if code.startswith("VC2" + prefix):
            return prefix, areas[prefix]
    return None, None


def build_skeleton(code, level, area_label, age_band, key_knowledge, mc_distractor_count):
    return {
        "_meta": {
            "code": code,
            "level": level,
            "area": area_label,
            "ageBand": age_band,
            "keyKnowledge": key_knowledge,
            "generatedAt": None,
            "specVersions": {
                "mcq_rules": "1.0",
                "tf_rules": "1.0",
                "cloze_spec": "2.1",
                "addendum": "1.2",
            },
        },
        "_source": {
            "w": key_knowledge,
            "y": None,  # Populated below
            "eg": None,  # Populated below
        },
        "toLevel2": build_blooms_array(2, mc_distractor_count),
        "toLevel3": build_blooms_array(3, mc_distractor_count),
        "toLevel4": build_blooms_array(4, mc_distractor_count),
        "toLevel5": build_blooms_array(5, mc_distractor_count),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate skeleton JSON files for curriculum codes")
    parser.add_argument("--code", help="Generate for a single code")
    parser.add_argument("--level", type=int, help="Generate for all codes at this year level")
    parser.add_argument("--dry-run", action="store_true", help="Count only, don't write files")
    args = parser.parse_args()

    # Load data
    with open(BASE_DIR / "cd_explanations.json") as f:
        cd = json.load(f)

    with open(BASE_DIR / "questions" / "_tracker" / "area-code-mapping.json") as f:
        mapping = json.load(f)

    areas = mapping["areas"]

    # Excluded prefixes (not generating questions for these)
    excludes = mapping.get("_excludes", [])
    exclude_prefixes = ["VC2EAL"]  # EAL codes match 'E' (English) otherwise

    # Filter codes
    codes = list(cd.keys())
    codes = [c for c in codes if not any(c.startswith(ep) for ep in exclude_prefixes)]
    if args.code:
        codes = [args.code]
    elif args.level:
        codes = [c for c in codes if parse_level_from_code(c) == args.level]

    generated = 0
    skipped = 0

    for code in sorted(codes):
        level = parse_level_from_code(code)
        if level is None or level not in LEVEL_AGE_BAND:
            skipped += 1
            continue

        age_band = LEVEL_AGE_BAND[level]
        mc_distractor_count = AGE_BAND_MC_DISTRACTORS[age_band]

        prefix, area_data = find_area(code, areas)
        if not area_data:
            skipped += 1
            continue

        entry = cd[code]
        key_knowledge = entry.get("w", "")

        skeleton = build_skeleton(code, level, area_data["label"], age_band, key_knowledge, mc_distractor_count)

        # Embed source material for the AI to use
        skeleton["_source"]["y"] = entry.get("y", [])
        skeleton["_source"]["eg"] = entry.get("eg", [])

        if args.dry_run:
            generated += 1
            continue

        # Write file
        level_str = f"level-{level:02d}"
        folder = area_data["folderName"]
        out_dir = BASE_DIR / "questions" / level_str / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{code}.skeleton.json"

        with open(out_path, "w") as f:
            json.dump(skeleton, f, indent=2)

        generated += 1

    print(f"Generated: {generated} skeletons")
    if skipped:
        print(f"Skipped: {skipped} codes (no level/area match)")
    if not args.dry_run:
        print(f"Output: questions/level-XX/Subject/CODE.skeleton.json")

    # Summary by level
    level_counts = {}
    for code in sorted(codes):
        level = parse_level_from_code(code)
        if level and level in LEVEL_AGE_BAND:
            level_counts[level] = level_counts.get(level, 0) + 1
    for level in sorted(level_counts.keys()):
        print(f"  Year {level}: {level_counts[level]} codes")


if __name__ == "__main__":
    main()
