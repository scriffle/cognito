#!/usr/bin/env python3
"""
Stage 1 Structural Validation for VC2 Assessment Question Files.

Validates a single question JSON file against:
- JSON Schema (question-schema.json)
- Age-band word limits
- TF FALSE balance (55-65%)
- Option count and length rules
- Cloze blank validation
- Variant uniqueness (>40% content word overlap = flag)

Usage:
    python validate.py <path-to-question-file.json>
    python validate.py --batch <directory>
    python validate.py --batch questions/level-02/Science/
"""

import json
import sys
import os
import re
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# --- Configuration ---

SPEC_DIR = Path(__file__).parent.parent.parent / "Question Specifications"
SCHEMA_PATH = SPEC_DIR / "question-schema.json"

AGE_BAND_PARAMS = {
    "7-8": {
        "tf_max_words": 12,
        "mc_stem_max_words": 15,
        "mc_option_max_words": 5,
        "mc_option_count": 3,
        "mc_distractor_count": 2,
        "cloze_options_per_blank": 3,
        "fk_max": 3.0,
    },
    "9-10": {
        "tf_max_words": 18,
        "mc_stem_max_words": 35,
        "mc_option_max_words": 12,
        "mc_option_count": 3,
        "mc_distractor_count": 2,
        "cloze_options_per_blank": 3,
        "fk_max": 5.0,
    },
    "11-12": {
        "tf_max_words": 22,
        "mc_stem_max_words": 55,
        "mc_option_max_words": 20,
        "mc_option_count": 3,
        "mc_distractor_count": 2,
        "cloze_options_per_blank": 3,
        "fk_max": 7.0,
    },
    "13-14": {
        "tf_max_words": 28,
        "mc_stem_max_words": 80,
        "mc_option_max_words": 30,
        "mc_option_count": 4,
        "mc_distractor_count": 3,
        "cloze_options_per_blank": 3,
        "fk_max": 9.0,
    },
    "15-16": {
        "tf_max_words": 35,
        "mc_stem_max_words": 130,
        "mc_option_max_words": 40,
        "mc_option_count": 4,
        "mc_distractor_count": 3,
        "cloze_options_per_blank": 3,
        "fk_max": 11.0,
    },
}

BLOOMS_TYPE_COUNTS = {
    2: {"tf": 12, "mc": 12, "cloze": 2},
    3: {"tf": 8, "mc": 12, "cloze": 6},
    4: {"tf": 2, "mc": 12, "cloze": 12},
    5: {"tf": 0, "mc": 14, "cloze": 12},
}

FUNCTION_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "above", "below", "between", "under",
    "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
    "neither", "each", "every", "all", "any", "few", "more", "most",
    "other", "some", "such", "no", "only", "own", "same", "than",
    "too", "very", "just", "also", "that", "this", "these", "those",
    "it", "its", "he", "she", "they", "them", "their", "we", "us",
    "our", "you", "your", "i", "me", "my", "who", "which", "what",
    "when", "where", "how", "if", "then", "there", "here",
}

NEGATION_WORDS = {"not", "no", "never", "neither", "nor", "cannot", "none", "nothing", "nowhere"}

ABSOLUTE_WORDS = {"always", "never", "all", "none", "every", "only", "no", "nothing", "completely", "entirely"}


# --- Helpers ---

def word_count(text: str) -> int:
    """Count words, excluding blank placeholders."""
    cleaned = re.sub(r"\{\{blank:\w+\}\}", "", text)
    return len(cleaned.split())


def content_words(text: str) -> set:
    """Extract content words (non-function words) from text."""
    cleaned = re.sub(r"\{\{blank:\w+\}\}", "", text).lower()
    words = re.findall(r"[a-z']+", cleaned)
    return {w for w in words if w not in FUNCTION_WORDS}


def has_negation(text: str) -> bool:
    """Check if text contains negation words."""
    words = set(text.lower().split())
    return bool(words & NEGATION_WORDS)


def has_contraction(text: str) -> bool:
    """Check for common contractions."""
    contractions = [
        "doesn't", "don't", "didn't", "isn't", "aren't", "wasn't", "weren't",
        "won't", "wouldn't", "shouldn't", "couldn't", "can't", "hasn't",
        "haven't", "hadn't", "it's", "they're", "we're", "you're", "he's",
        "she's", "that's", "there's", "here's", "who's", "what's",
    ]
    text_lower = text.lower()
    return any(c in text_lower for c in contractions)


# --- Validators ---

class ValidationResult:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: list[dict] = []
        self.warnings: list[dict] = []

    def error(self, location: str, rule: str, message: str):
        self.errors.append({"location": location, "rule": rule, "message": message})

    def warning(self, location: str, rule: str, message: str):
        self.warnings.append({"location": location, "rule": rule, "message": message})

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def summary(self) -> dict:
        return {
            "filepath": self.filepath,
            "passed": self.passed,
            "errorCount": len(self.errors),
            "warningCount": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_meta(data: dict, result: ValidationResult):
    """Validate _meta block."""
    meta = data.get("_meta")
    if not meta:
        result.error("_meta", "REQUIRED", "_meta block is missing")
        return None

    required = ["code", "level", "area", "ageBand", "keyKnowledge", "generatedAt", "specVersions"]
    for field in required:
        if field not in meta:
            result.error(f"_meta.{field}", "REQUIRED", f"Missing required field: {field}")

    age_band = meta.get("ageBand")
    if age_band and age_band not in AGE_BAND_PARAMS:
        result.error("_meta.ageBand", "ENUM", f"Invalid ageBand: {age_band}")

    level = meta.get("level")
    if level and level not in [2, 4, 6, 8, 10]:
        result.error("_meta.level", "ENUM", f"Invalid level: {level}")

    return meta


def validate_array_structure(data: dict, result: ValidationResult):
    """Validate that toLevel2-5 arrays exist with 26 items each."""
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key)
        if arr is None:
            result.error(key, "REQUIRED", f"Missing {key} array")
            continue
        if not isinstance(arr, list):
            result.error(key, "TYPE", f"{key} must be an array")
            continue
        if len(arr) != 26:
            result.error(key, "COUNT", f"{key} has {len(arr)} items, expected 26")


def validate_type_counts(data: dict, result: ValidationResult):
    """Validate question type distribution within each Bloom's level."""
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])
        if not isinstance(arr, list):
            continue

        counts = Counter(q.get("type") for q in arr if isinstance(q, dict))
        expected = BLOOMS_TYPE_COUNTS[blooms]

        for qtype, expected_count in expected.items():
            actual = counts.get(qtype, 0)
            if actual != expected_count:
                result.error(
                    key,
                    "TYPE_COUNT",
                    f"{key}: expected {expected_count} {qtype}, got {actual}",
                )


def validate_tf_question(q: dict, age_band: str, location: str, result: ValidationResult):
    """Validate a single TF question."""
    params = AGE_BAND_PARAMS.get(age_band, {})
    statement = q.get("question", "")
    max_words = params.get("tf_max_words", 35)

    # Word count
    wc = word_count(statement)
    if wc > max_words:
        result.error(location, "TF_WORD_COUNT", f"TF statement is {wc} words, max {max_words}")

    # Negation check (prohibited for ages 7-8 and 9-10)
    if age_band in ("7-8", "9-10") and has_negation(statement):
        result.error(location, "TF_NEGATION", f"Negation prohibited at age band {age_band}")

    # Contraction check
    if has_contraction(statement):
        result.error(location, "TF_CONTRACTION", "Contractions not permitted in stems")

    # Single proposition check (basic: flag compound conjunctions)
    compound_markers = [" and ", " but ", " or ", " because ", " therefore ", " however "]
    for marker in compound_markers:
        if marker in statement.lower():
            result.warning(location, "TF_COMPOUND", f"Possible compound statement (contains '{marker.strip()}')")

    # Correct value
    if q.get("correct") not in ("True", "False"):
        result.error(location, "TF_CORRECT", f"correct must be 'True' or 'False', got '{q.get('correct')}'")

    # Distractors
    distractors = q.get("distractors", [])
    if len(distractors) != 1:
        result.error(location, "TF_DISTRACTOR_COUNT", f"TF must have exactly 1 distractor, got {len(distractors)}")

    # Explanation
    if not q.get("correctExplanation"):
        result.error(location, "TF_EXPLANATION", "Missing correctExplanation")


def validate_mc_question(q: dict, age_band: str, location: str, result: ValidationResult):
    """Validate a single MC question."""
    params = AGE_BAND_PARAMS.get(age_band, {})
    stem = q.get("question", "")
    max_stem = params.get("mc_stem_max_words", 80)
    max_option = params.get("mc_option_max_words", 30)
    expected_distractors = params.get("mc_distractor_count", 2)

    # Stem word count
    wc = word_count(stem)
    if wc > max_stem:
        result.error(location, "MC_STEM_WORDS", f"MC stem is {wc} words, max {max_stem}")

    # Contraction check
    if has_contraction(stem):
        result.error(location, "MC_CONTRACTION", "Contractions not permitted in stems")

    # Negation check (prohibited for ages 7-8 and 9-10)
    if age_band in ("7-8", "9-10") and has_negation(stem):
        result.error(location, "MC_NEGATION", f"Negation prohibited in stems at age band {age_band}")

    # Correct answer
    correct = q.get("correct", "")
    if not correct:
        result.error(location, "MC_CORRECT", "Missing correct answer")
    elif word_count(correct) > max_option:
        result.error(location, "MC_OPTION_WORDS", f"Correct option is {word_count(correct)} words, max {max_option}")

    # Distractors
    distractors = q.get("distractors", [])
    if len(distractors) != expected_distractors:
        result.error(
            location,
            "MC_DISTRACTOR_COUNT",
            f"Expected {expected_distractors} distractors, got {len(distractors)}",
        )

    # Option length check
    all_options = [correct] + [d.get("answer", "") for d in distractors]
    option_wcs = [word_count(o) for o in all_options if o]
    for i, owc in enumerate(option_wcs):
        if owc > max_option:
            result.error(location, "MC_OPTION_WORDS", f"Option {i+1} is {owc} words, max {max_option}")

    # Option length parity by word count (±20%)
    if option_wcs:
        mean_wc = sum(option_wcs) / len(option_wcs)
        if mean_wc > 0:
            for i, owc in enumerate(option_wcs):
                if owc > mean_wc * 1.2 + 1:  # +1 for rounding tolerance on short options
                    result.error(
                        location,
                        "MC_OPTION_PARITY",
                        f"Option {i+1} ({owc} words) is >20% longer than mean ({mean_wc:.1f})",
                    )

    # Option length parity by character count (±30%)
    option_ccs = [len(o) for o in all_options if o]
    if option_ccs:
        mean_cc = sum(option_ccs) / len(option_ccs)
        if mean_cc > 0:
            for i, occ in enumerate(option_ccs):
                if occ > mean_cc * 1.3 + 5:  # +5 for tolerance on short options
                    result.error(
                        location,
                        "MC_OPTION_CHAR_PARITY",
                        f"Option {i+1} ({occ} chars) is >30% longer than mean ({mean_cc:.1f})",
                    )

    # Explanation
    if not q.get("correctExplanation"):
        result.error(location, "MC_EXPLANATION", "Missing correctExplanation")

    # Distractor explanations
    for i, d in enumerate(distractors):
        if not d.get("explanation"):
            result.error(location, "MC_DISTRACTOR_EXPLANATION", f"Distractor {i+1} missing explanation")


def validate_cloze_question(q: dict, age_band: str, location: str, result: ValidationResult):
    """Validate a single cloze question."""
    sentence = q.get("sentence", "")
    blanks = q.get("blanks", [])

    # Check blank count
    if len(blanks) < 2:
        result.error(location, "CLOZE_BLANK_COUNT", f"Cloze must have at least 2 blanks, got {len(blanks)}")
    if len(blanks) > 4:
        result.error(location, "CLOZE_BLANK_COUNT", f"Cloze must have at most 4 blanks, got {len(blanks)}")

    # Check placeholders match blanks
    placeholders = set(re.findall(r"\{\{blank:(\w+)\}\}", sentence))
    blank_ids = {b.get("id", "") for b in blanks}
    if placeholders != blank_ids:
        result.error(
            location,
            "CLOZE_BLANK_MISMATCH",
            f"Placeholder IDs {placeholders} do not match blank IDs {blank_ids}",
        )

    # Scoring field
    if q.get("scoring") not in ("all", "partial"):
        result.error(location, "CLOZE_SCORING", f"scoring must be 'all' or 'partial', got '{q.get('scoring')}'")

    # Validate each blank
    for i, blank in enumerate(blanks):
        blank_loc = f"{location}.blanks[{i}]"

        if not blank.get("id"):
            result.error(blank_loc, "CLOZE_BLANK_ID", "Missing blank id")
        if not blank.get("correct"):
            result.error(blank_loc, "CLOZE_BLANK_CORRECT", "Missing correct answer")
        if not blank.get("correctExplanation"):
            result.error(blank_loc, "CLOZE_BLANK_EXPLANATION", "Missing correctExplanation")

        distractors = blank.get("distractors", [])
        if len(distractors) != 2:
            result.error(
                blank_loc,
                "CLOZE_DISTRACTOR_COUNT",
                f"Each blank must have exactly 2 distractors, got {len(distractors)}",
            )

        for j, d in enumerate(distractors):
            d_loc = f"{blank_loc}.distractors[{j}]"
            if not d.get("answer"):
                result.error(d_loc, "CLOZE_DISTRACTOR_ANSWER", "Missing distractor answer")
            if not d.get("explanation"):
                result.error(d_loc, "CLOZE_DISTRACTOR_EXPLANATION", "Missing distractor explanation")
            if d.get("misconceptionSource") not in ("documented", "teacher-reported", "inferred"):
                result.error(
                    d_loc,
                    "CLOZE_MISCONCEPTION_SOURCE",
                    f"misconceptionSource must be documented/teacher-reported/inferred, got '{d.get('misconceptionSource')}'",
                )


def validate_tf_balance(data: dict, result: ValidationResult):
    """Check TF FALSE balance is 55-65% per Bloom's level."""
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])
        tf_items = [q for q in arr if isinstance(q, dict) and q.get("type") == "tf"]

        if not tf_items:
            continue

        false_count = sum(1 for q in tf_items if q.get("correct") == "False")
        total = len(tf_items)

        # With fewer than 4 TF items, the 55-65% range cannot be hit precisely.
        # Apply a relaxed rule: at least 1 FALSE when total ≤ 3.
        if total <= 3:
            if false_count == 0:
                result.error(key, "TF_BALANCE", f"No FALSE items among {total} TF questions (need at least 1)")
            continue

        pct = false_count / total * 100

        if pct < 55:
            result.error(key, "TF_BALANCE", f"FALSE is {pct:.0f}%, minimum 55% (got {false_count}/{total})")
        elif pct > 65:
            result.error(key, "TF_BALANCE", f"FALSE is {pct:.0f}%, maximum 65% (got {false_count}/{total})")


def validate_mc_correct_position_balance(data: dict, age_band: str, result: ValidationResult):
    """Check that the correct answer is not systematically the longest across the file."""
    params = AGE_BAND_PARAMS.get(age_band, {})
    option_count = params.get("mc_option_count", 3)

    # Threshold: chance level for n options is 1/n. Allow small headroom.
    # 3 options: chance ~33%, threshold 40%. 4 options: chance ~25%, threshold 30%.
    if option_count == 3:
        threshold_pct = 40
    elif option_count == 4:
        threshold_pct = 30
    else:
        threshold_pct = 40  # fallback

    total_mc = 0
    longest_count = 0
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])
        for q in arr:
            if not isinstance(q, dict) or q.get("type") != "mc":
                continue
            correct = q.get("correct", "")
            distractors = q.get("distractors", [])
            if not correct or not distractors:
                continue
            total_mc += 1
            correct_wc = word_count(correct)
            distractor_wcs = [word_count(d.get("answer", "")) for d in distractors]
            max_distractor_wc = max(distractor_wcs) if distractor_wcs else 0
            # Count only STRICTLY longest — ties are not exploitable
            if correct_wc > max_distractor_wc:
                longest_count += 1

    if total_mc == 0:
        return

    pct = longest_count / total_mc * 100
    if pct > threshold_pct:
        result.error(
            "file",
            "MC_SYSTEMATIC_LENGTH_BIAS",
            f"Correct answer is the longest in {longest_count}/{total_mc} MC questions "
            f"({pct:.0f}%); maximum is {threshold_pct}% for {option_count}-option questions",
        )


def validate_variant_uniqueness(data: dict, result: ValidationResult):
    """Check that no two variants share >40% content words."""
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])

        # Extract text per question
        texts = []
        for q in arr:
            if not isinstance(q, dict):
                continue
            qtype = q.get("type")
            if qtype == "tf":
                texts.append((q.get("variant", "?"), content_words(q.get("question", ""))))
            elif qtype == "mc":
                texts.append((q.get("variant", "?"), content_words(q.get("question", ""))))
            elif qtype == "cloze":
                texts.append((q.get("variant", "?"), content_words(q.get("sentence", ""))))

        # Pairwise comparison (only within same type for meaningful comparison)
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                v1, words1 = texts[i]
                v2, words2 = texts[j]
                if not words1 or not words2:
                    continue
                union = words1 | words2
                intersection = words1 & words2
                if union and len(intersection) / len(union) > 0.4:
                    result.warning(
                        key,
                        "VARIANT_SIMILARITY",
                        f"Variants {v1} and {v2} share >{40}% content words ({len(intersection)}/{len(union)})",
                    )


def validate_variant_numbers(data: dict, result: ValidationResult):
    """Check variant numbers are 1-26 and sequential."""
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])
        variants = sorted(q.get("variant", 0) for q in arr if isinstance(q, dict))
        expected = list(range(1, 27))
        if variants != expected:
            result.error(key, "VARIANT_SEQUENCE", f"Variants should be 1-26, got {variants}")


def validate_blooms_levels(data: dict, result: ValidationResult):
    """Check each question has the correct bloomsLevel."""
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])
        for i, q in enumerate(arr):
            if isinstance(q, dict) and q.get("bloomsLevel") != blooms:
                result.error(
                    f"{key}[{i}]",
                    "BLOOMS_LEVEL",
                    f"bloomsLevel should be {blooms}, got {q.get('bloomsLevel')}",
                )


def validate_file(filepath: str) -> ValidationResult:
    """Run all validations on a single file."""
    result = ValidationResult(filepath)

    # Load JSON
    try:
        with open(filepath) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result.error("file", "JSON_PARSE", f"Invalid JSON: {e}")
        return result
    except FileNotFoundError:
        result.error("file", "NOT_FOUND", f"File not found: {filepath}")
        return result

    # Meta validation
    meta = validate_meta(data, result)
    age_band = meta.get("ageBand", "7-8") if meta else "7-8"

    # Structure
    validate_array_structure(data, result)
    validate_type_counts(data, result)
    validate_variant_numbers(data, result)
    validate_blooms_levels(data, result)

    # Per-question validation
    for blooms in [2, 3, 4, 5]:
        key = f"toLevel{blooms}"
        arr = data.get(key, [])
        if not isinstance(arr, list):
            continue

        for i, q in enumerate(arr):
            if not isinstance(q, dict):
                result.error(f"{key}[{i}]", "TYPE", "Question must be an object")
                continue

            location = f"{key}[{i}] (v{q.get('variant', '?')})"
            qtype = q.get("type")

            if qtype == "tf":
                validate_tf_question(q, age_band, location, result)
            elif qtype == "mc":
                validate_mc_question(q, age_band, location, result)
            elif qtype == "cloze":
                validate_cloze_question(q, age_band, location, result)
            else:
                result.error(location, "UNKNOWN_TYPE", f"Unknown question type: {qtype}")

    # Cross-question checks
    validate_tf_balance(data, result)
    validate_mc_correct_position_balance(data, age_band, result)
    validate_variant_uniqueness(data, result)

    return result


def audit_mc_length_bias(directory: str) -> dict:
    """Run only MC length checks across a directory; return summary dict."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for fn in filenames:
            if fn.endswith(".json") and not fn.startswith(".") and ".skeleton." not in fn and ".pre-mc-regen." not in fn and ".mc-brief." not in fn:
                files.append(os.path.join(root, fn))
    files.sort()

    biased_files = []
    file_reports = []

    for fp in files:
        try:
            with open(fp) as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            continue

        meta = data.get("_meta", {})
        age_band = meta.get("ageBand", "13-14")
        params = AGE_BAND_PARAMS.get(age_band, {})
        option_count = params.get("mc_option_count", 4)
        threshold_pct = 50 if option_count == 3 else 40

        total_mc = 0
        longest_count = 0
        outliers = []

        for blooms in [2, 3, 4, 5]:
            key = f"toLevel{blooms}"
            arr = data.get(key, [])
            for q in arr:
                if not isinstance(q, dict) or q.get("type") != "mc":
                    continue
                correct = q.get("correct", "")
                distractors = q.get("distractors", [])
                if not correct or not distractors:
                    continue
                total_mc += 1
                correct_wc = word_count(correct)
                distractor_wcs = [word_count(d.get("answer", "")) for d in distractors]
                max_distractor_wc = max(distractor_wcs) if distractor_wcs else 0
                # Count only STRICTLY longest — ties are not exploitable
                if correct_wc > max_distractor_wc:
                    longest_count += 1

                # Track worst character-length outliers
                correct_cc = len(correct)
                avg_dist_cc = sum(len(d.get("answer", "")) for d in distractors) / len(distractors)
                if avg_dist_cc > 0 and correct_cc > avg_dist_cc * 1.5:
                    pct_longer = (correct_cc / avg_dist_cc - 1) * 100
                    outliers.append({
                        "location": f"{key}[v{q.get('variant','?')}]",
                        "correct_cc": correct_cc,
                        "avg_dist_cc": avg_dist_cc,
                        "pct_longer": pct_longer,
                    })

        if total_mc == 0:
            continue

        pct = longest_count / total_mc * 100
        is_biased = pct > threshold_pct

        report = {
            "file": fp,
            "code": os.path.basename(fp).replace(".json", ""),
            "total_mc": total_mc,
            "longest_count": longest_count,
            "pct": pct,
            "threshold_pct": threshold_pct,
            "option_count": option_count,
            "is_biased": is_biased,
            "outliers": sorted(outliers, key=lambda x: -x["pct_longer"])[:3],
        }
        file_reports.append(report)
        if is_biased:
            biased_files.append(fp)

    return {
        "total_files": len(file_reports),
        "biased_files": biased_files,
        "file_reports": file_reports,
    }


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Validate VC2 assessment question files")
    parser.add_argument("path", help="Path to a JSON file or directory (with --batch or --audit)")
    parser.add_argument("--batch", action="store_true", help="Validate all JSON files in directory")
    parser.add_argument("--audit", action="store_true", help="Run only MC length-bias checks across a directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    if args.audit:
        result = audit_mc_length_bias(args.path)
        biased = result["biased_files"]
        for r in result["file_reports"]:
            if not r["is_biased"]:
                continue
            print(f"{r['code']}: {r['longest_count']}/{r['total_mc']} MC questions have correct=longest ({r['pct']:.0f}%) — SYSTEMATIC BIAS")
            if r["outliers"]:
                print(f"  Worst outliers:")
                for o in r["outliers"]:
                    print(f"    {o['location']}: correct ({o['correct_cc']} chars) vs avg distractor ({o['avg_dist_cc']:.0f} chars) — {o['pct_longer']:.0f}% longer")
            print()

        # Write biased file list
        out_path = Path(__file__).parent / "audit-biased-files.txt"
        with open(out_path, "w") as f:
            for fp in biased:
                f.write(fp + "\n")

        print(f"AUDIT SUMMARY: {len(biased)}/{result['total_files']} files show systematic length bias")
        print(f"Biased file list written to: {out_path}")
        sys.exit(0 if not biased else 1)

    files = []
    if args.batch:
        for root, dirs, filenames in os.walk(args.path):
            for fn in filenames:
                if fn.endswith(".json") and not fn.startswith("."):
                    files.append(os.path.join(root, fn))
        files.sort()
    else:
        files = [args.path]

    if not files:
        print("No files found to validate.")
        sys.exit(1)

    all_results = []
    total_errors = 0
    total_warnings = 0

    for filepath in files:
        result = validate_file(filepath)

        if args.strict:
            total_errors += len(result.errors) + len(result.warnings)
        else:
            total_errors += len(result.errors)
        total_warnings += len(result.warnings)

        all_results.append(result.summary())

        if not args.json:
            status = "PASS" if result.passed else "FAIL"
            print(f"[{status}] {filepath}: {len(result.errors)} errors, {len(result.warnings)} warnings")
            for err in result.errors:
                print(f"  ERROR  {err['location']}: [{err['rule']}] {err['message']}")
            for warn in result.warnings:
                print(f"  WARN   {warn['location']}: [{warn['rule']}] {warn['message']}")

    if args.json:
        output = {
            "validatedAt": datetime.now().isoformat() + "Z",
            "filesValidated": len(files),
            "totalErrors": total_errors,
            "totalWarnings": total_warnings,
            "results": all_results,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n--- Summary ---")
        print(f"Files: {len(files)}")
        print(f"Errors: {total_errors}")
        print(f"Warnings: {total_warnings}")
        passed = sum(1 for r in all_results if r["passed"])
        print(f"Passed: {passed}/{len(files)}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
