#!/usr/bin/env python3
"""
MC question extraction and merge tooling for the regeneration phase.

Three modes:

1. STRIP mode: Given a question file, back it up, replace MC questions with
   null slots (preserving type/variant/bloomsLevel), and write a "brief" file
   containing _meta, the original skeleton's _source block, and the existing
   TF/cloze questions for variant-diversity reference.

   python extract-mc-for-regen.py strip <path-to-CODE.json>

   Outputs:
   - <CODE>.pre-mc-regen.json  (backup of the original)
   - <CODE>.mc-stripped.json   (working file with null MC slots)
   - <CODE>.mc-brief.json      (generation brief)

2. MERGE mode: Given the path to the original file and a file containing newly
   generated MC questions, slot the new questions into the null positions and
   re-validate. If valid, replace the original. If not, leave the backup.

   python extract-mc-for-regen.py merge <path-to-CODE.json> <path-to-new-mc.json>

3. REGEN-DISTRACTORS mode: Given a question file, extract all MC questions with
   their stems and correct answers preserved, but null out ONLY the distractor
   answer text. The brief includes the correct answer and its word count so new
   distractors can be written to match complexity and length.

   python extract-mc-for-regen.py regen-distractors <path-to-CODE.json>

   Outputs:
   - <CODE>.pre-distractor-regen.json  (backup)
   - <CODE>.distractor-brief.json       (generation brief with stems + correct answers)
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

VALIDATE_SCRIPT = Path(__file__).parent.parent / "_validation" / "validate.py"


def find_skeleton(json_path: Path) -> Optional[Path]:
    """Find the matching skeleton file for a generated question file."""
    skel = json_path.with_suffix(".skeleton.json").with_name(json_path.stem + ".skeleton.json")
    if skel.exists():
        return skel
    return None


def strip_mc(json_path: Path):
    """Strip MC questions from a file, preserving slot metadata."""
    if not json_path.exists():
        print(f"ERROR: {json_path} does not exist")
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    # Backup
    backup_path = json_path.with_name(json_path.stem + ".pre-mc-regen.json")
    if backup_path.exists():
        print(f"WARNING: backup already exists at {backup_path} — will not overwrite")
        sys.exit(1)
    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Backup written: {backup_path}")

    # Build stripped version: replace MC questions with null-content slots
    stripped = json.loads(json.dumps(data))  # deep copy
    stripped_count = 0
    preserved_tf_cloze = []

    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = stripped.get(key, [])
        for i, q in enumerate(arr):
            if not isinstance(q, dict):
                continue
            if q.get("type") == "mc":
                # Replace content fields with null but keep structural fields
                arr[i] = {
                    "type": "mc",
                    "variant": q.get("variant"),
                    "bloomsLevel": q.get("bloomsLevel"),
                    "question": None,
                    "correct": None,
                    "correctExplanation": None,
                    "distractors": [
                        {"answer": None, "explanation": None}
                        for _ in q.get("distractors", [])
                    ],
                }
                stripped_count += 1
            else:
                # Preserve TF/cloze for diversity reference
                preserved_tf_cloze.append({
                    "level": key,
                    "type": q.get("type"),
                    "variant": q.get("variant"),
                    "text": q.get("question") or q.get("sentence", ""),
                })

    stripped_path = json_path.with_name(json_path.stem + ".mc-stripped.json")
    with open(stripped_path, "w") as f:
        json.dump(stripped, f, indent=2, ensure_ascii=False)
    print(f"Stripped file written: {stripped_path} ({stripped_count} MC slots nulled)")

    # Build brief
    brief = {
        "_meta": data.get("_meta", {}),
        "instructions": (
            "Generate replacement MC questions for the null slots in the stripped file. "
            "Follow the master generation prompt. Pay particular attention to MC RULE 4: "
            "options must be within ±20% word count and ±30% character count of each other, "
            "and the correct answer must be the longest option in no more than 1/n of cases "
            "across the file. New MC questions must also stay >40% diverse in content words "
            "from the existing TF/cloze questions listed below."
        ),
        "existing_tf_cloze_for_diversity_reference": preserved_tf_cloze,
    }

    # Try to attach _source from skeleton
    skeleton = find_skeleton(json_path)
    if skeleton:
        with open(skeleton) as f:
            skel_data = json.load(f)
        brief["_source"] = skel_data.get("_source", {})
        print(f"Attached _source from skeleton: {skeleton}")
    else:
        print("WARNING: no skeleton found; brief will not include _source")

    brief_path = json_path.with_name(json_path.stem + ".mc-brief.json")
    with open(brief_path, "w") as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)
    print(f"Brief written: {brief_path}")


def merge_mc(original_path: Path, new_mc_path: Path):
    """Merge newly generated MC questions into the original file."""
    if not original_path.exists():
        print(f"ERROR: {original_path} does not exist")
        sys.exit(1)
    if not new_mc_path.exists():
        print(f"ERROR: {new_mc_path} does not exist")
        sys.exit(1)

    with open(original_path) as f:
        original = json.load(f)
    with open(new_mc_path) as f:
        new_mc_file = json.load(f)

    # Build a lookup of new MC questions by (bloomsLevel, variant)
    new_by_key = {}
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        for q in new_mc_file.get(key, []):
            if isinstance(q, dict) and q.get("type") == "mc":
                new_by_key[(blooms, q.get("variant"))] = q

    # Merge into original
    merged = json.loads(json.dumps(original))
    merged_count = 0
    missing = []
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = merged.get(key, [])
        for i, q in enumerate(arr):
            if isinstance(q, dict) and q.get("type") == "mc":
                lookup = new_by_key.get((blooms, q.get("variant")))
                if lookup is None:
                    missing.append(f"{key} v{q.get('variant')}")
                    continue
                arr[i] = lookup
                merged_count += 1

    if missing:
        print(f"ERROR: missing {len(missing)} MC replacements: {missing[:5]}{'...' if len(missing)>5 else ''}")
        sys.exit(1)

    # Write to a temp path first, validate, then commit
    temp_path = original_path.with_name(original_path.stem + ".merged-temp.json")
    with open(temp_path, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"Merged file written to temp: {temp_path} ({merged_count} MC questions merged)")

    # Validate
    print(f"Running validator...")
    proc = subprocess.run(
        ["python3", str(VALIDATE_SCRIPT), str(temp_path)],
        capture_output=True,
        text=True,
    )
    print(proc.stdout)
    if proc.returncode != 0:
        print(f"VALIDATION FAILED — temp file kept at {temp_path} for inspection")
        print(f"Original is unchanged. Backup is at {original_path.with_name(original_path.stem + '.pre-mc-regen.json')}")
        sys.exit(1)

    # Commit
    with open(original_path, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    os.remove(temp_path)
    print(f"OK — merged file committed to {original_path}")
    print(f"Backup remains at {original_path.with_name(original_path.stem + '.pre-mc-regen.json')}")


def regen_distractors(json_path: Path):
    """Extract MC questions for distractor-only regeneration.

    Preserves stems and correct answers. Nulls out distractor answer text only,
    keeping distractor count and structure. The brief includes the correct answer
    word count so new distractors can be written to match.
    """
    if not json_path.exists():
        print(f"ERROR: {json_path} does not exist")
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    # Backup
    backup_path = json_path.with_name(json_path.stem + ".pre-distractor-regen.json")
    if backup_path.exists():
        print(f"WARNING: backup already exists at {backup_path} — will not overwrite")
        sys.exit(1)
    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Backup written: {backup_path}")

    # Build brief: for each MC question, include stem + correct answer + correct word count,
    # and null out distractor answers (keep explanation structure for misconception targeting)
    brief_questions = []
    mc_count = 0

    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        level_questions = []
        for q in data.get(key, []):
            if not isinstance(q, dict) or q.get("type") != "mc":
                continue
            mc_count += 1
            correct_text = q.get("correct", "")
            correct_words = len(correct_text.split())
            correct_chars = len(correct_text)

            # Build distractor slots: null the answer text, keep explanation as guidance
            distractor_slots = []
            for d in q.get("distractors", []):
                distractor_slots.append({
                    "answer": None,  # TO BE REGENERATED
                    "explanation": d.get("explanation", ""),  # keep as misconception guidance
                    "original_answer": d.get("answer", ""),  # reference for what was there
                    "original_word_count": len(d.get("answer", "").split()),
                })

            level_questions.append({
                "type": "mc",
                "variant": q.get("variant"),
                "bloomsLevel": q.get("bloomsLevel"),
                "question": q.get("question"),  # PRESERVED
                "correct": correct_text,  # PRESERVED
                "correct_word_count": correct_words,
                "correct_char_count": correct_chars,
                "correctExplanation": q.get("correctExplanation"),  # PRESERVED
                "target_distractor_words": f"{max(correct_words - 3, 5)}-{correct_words + 3}",
                "distractors": distractor_slots,
            })
        if level_questions:
            brief_questions.append({"bloomsLevel": blooms, "key": key, "questions": level_questions})

    brief = {
        "_meta": data.get("_meta", {}),
        "instructions": (
            "DISTRACTOR-ONLY REGENERATION. For each MC question below, the stem, correct answer, "
            "and correctExplanation are FINAL — do not change them. Replace each distractor's "
            "null 'answer' field with a new distractor that:\n"
            "  1. Matches the correct answer's word count (see target_distractor_words range)\n"
            "  2. Uses the same level of specific detail and domain terminology\n"
            "  3. Sounds like a confident, substantive claim — not a vague shortcut\n"
            "  4. Is wrong for ONE identifiable reason (see the existing 'explanation' for the "
            "     misconception to target)\n"
            "  5. Directly addresses the question being asked\n\n"
            "The 'original_answer' field shows what was there before — use it as a reference for "
            "the misconception being targeted, but write a NEW answer at the correct length.\n\n"
            "Return the complete question file structure (toLevel2 through toLevel5) with all "
            "questions — TF and cloze questions must be included unchanged from the original file."
        ),
        "mc_questions_to_fix": brief_questions,
        "total_mc_questions": mc_count,
    }

    # Attach _source from skeleton if available
    skeleton = find_skeleton(json_path)
    if skeleton:
        with open(skeleton) as f:
            skel_data = json.load(f)
        brief["_source"] = skel_data.get("_source", {})
        print(f"Attached _source from skeleton: {skeleton}")

    brief_path = json_path.with_name(json_path.stem + ".distractor-brief.json")
    with open(brief_path, "w") as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)
    print(f"Distractor brief written: {brief_path} ({mc_count} MC questions)")
    print(f"\nNext steps:")
    print(f"  1. Generate new distractors using the brief")
    print(f"  2. Merge back: python {sys.argv[0]} merge {json_path} <new-file>")


def main():
    parser = argparse.ArgumentParser(description="MC extraction and merge tooling for regeneration")
    sub = parser.add_subparsers(dest="cmd", required=True)

    strip_p = sub.add_parser("strip", help="Strip MC questions and produce regen brief")
    strip_p.add_argument("path", help="Path to the question JSON file")

    merge_p = sub.add_parser("merge", help="Merge newly generated MC questions back into the original file")
    merge_p.add_argument("original", help="Path to the original question JSON file")
    merge_p.add_argument("new_mc", help="Path to the file containing newly generated MC questions")

    regen_d = sub.add_parser("regen-distractors", help="Extract MC for distractor-only regeneration (keeps stems + correct answers)")
    regen_d.add_argument("path", help="Path to the question JSON file")

    args = parser.parse_args()

    if args.cmd == "strip":
        strip_mc(Path(args.path))
    elif args.cmd == "merge":
        merge_mc(Path(args.original), Path(args.new_mc))
    elif args.cmd == "regen-distractors":
        regen_distractors(Path(args.path))


if __name__ == "__main__":
    main()
