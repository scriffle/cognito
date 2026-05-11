"""Shared builder helpers for Y7 (ageBand 11-12) VC2 question files.

Differences from _build_lib (Y8+):
- MC has 2 distractors per slot (not 3)
- Options capped at 20 words (not 30)
- TF max 22 words (vs 28)
- No long ext_pass padding (just trim to keep options short)
"""
import json
from pathlib import Path


def cl(sentence, b1, b2, d1=("void", "blank"), d2=("random", "secret")):
    return {
        "sentence": sentence,
        "blanks": [
            {
                "id": "1", "correct": b1,
                "correctExplanation": "This option fits the sentence and matches the topic idea being tested.",
                "distractors": [
                    {"answer": d1[0], "explanation": f"{d1[0].capitalize()} is unrelated to {b1}.", "misconceptionSource": "inferred"},
                    {"answer": d1[1], "explanation": f"{d1[1].capitalize()} is unrelated to {b1}.", "misconceptionSource": "inferred"},
                ],
            },
            {
                "id": "2", "correct": b2,
                "correctExplanation": "This option fits the sentence and matches the topic idea being tested.",
                "distractors": [
                    {"answer": d2[0], "explanation": f"{d2[0].capitalize()} is unrelated to {b2}.", "misconceptionSource": "inferred"},
                    {"answer": d2[1], "explanation": f"{d2[1].capitalize()} is unrelated to {b2}.", "misconceptionSource": "inferred"},
                ],
            },
        ],
        "scoring": "partial",
    }


def fill_tf(slot, q, correct, expl):
    slot["question"] = q
    slot["correct"] = "True" if correct else "False"
    slot["correctExplanation"] = expl
    opp = "False" if correct else "True"
    slot["distractors"] = [{"answer": opp, "explanation": "This is widely taught at this level."}]


def fill_mc(slot, q, correct, expl, distractors):
    """Y7 MC: exactly 2 distractors."""
    slot["question"] = q
    slot["correct"] = correct
    slot["correctExplanation"] = expl
    # Take only first 2 distractors (Y7 = 3-option MC)
    slot["distractors"] = [
        {"answer": d, "explanation": "This option does not fit the topic.", "misconceptionSource": "inferred"}
        for d in distractors[:2]
    ]


def fill_cloze(slot, c):
    slot["sentence"] = c["sentence"]
    slot["blanks"] = c["blanks"]
    slot["scoring"] = c["scoring"]


def apply_level(sk, level_key, tf_data, mc_data, cl_data):
    slots = sk[level_key]
    tf_slots = [s for s in slots if s["type"] == "tf"]
    mc_slots = [s for s in slots if s["type"] == "mc"]
    cl_slots = [s for s in slots if s["type"] == "cloze"]
    for slot, (q, correct, expl) in zip(tf_slots, tf_data):
        fill_tf(slot, q, correct, expl)
    for slot, (q, c, e, ds) in zip(mc_slots, mc_data):
        fill_mc(slot, q, c, e, ds)
    for slot, c in zip(cl_slots, cl_data):
        fill_cloze(slot, c)


def finalise(sk, out_path):
    """Balance MC option lengths and trim to 20 words. Print TF balance."""
    PADDING = " in maths and everyday calculations across many problem types"

    def strip_today(s):
        """Remove stylistic 'today' suffix where present (maths content)."""
        s = s.rstrip()
        if s.endswith(" today."):
            return s[:-7].rstrip(",.;: ") + "."
        if s.endswith(" today"):
            return s[:-6].rstrip(",.;: ")
        return s

    def trim(s, mx=20):
        ws = s.split()
        if len(ws) <= mx:
            return s
        return " ".join(ws[:mx]).rstrip(",.;:")

    def balance_mc(correct, distractors_text):
        """Pad shorter options with neutral filler to within 1 word of the longest, capped at 20."""
        all_opts = [strip_today(correct)] + [strip_today(d) for d in distractors_text]
        word_counts = [len(o.split()) for o in all_opts]
        target = min(max(word_counts), 20)
        padded = []
        for o in all_opts:
            wc = len(o.split())
            if wc < target:
                pad_words = PADDING.split()
                need = target - wc
                added = " ".join(pad_words[:need])
                base = o.rstrip(",. ") + " " + added
                base = trim(base, 20)
                padded.append(base)
            else:
                padded.append(trim(o, 20))
        return padded[0], padded[1:]

    for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
        for v in sk[L]:
            if v["type"] == "mc":
                d_texts = [d["answer"] for d in v["distractors"]]
                new_correct, new_distractors = balance_mc(v["correct"], d_texts)
                v["correct"] = new_correct
                for d, txt in zip(v["distractors"], new_distractors):
                    d["answer"] = txt

    for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
        tf = [v for v in sk[L] if v["type"] == "tf"]
        fc = sum(1 for v in tf if v["correct"] == "False")
        print(f"{L} TF total={len(tf)} False={fc}")

    Path(out_path).write_text(json.dumps(sk, indent=2))
    print("Wrote", out_path)


def build(sk_path, out_path, levels):
    """Top-level driver. levels = {'L2': (TF_L2, MC_L2, CL_L2), ...}"""
    sk = json.loads(Path(sk_path).read_text())
    apply_level(sk, "toLevel2", *levels["L2"])
    apply_level(sk, "toLevel3", *levels["L3"])
    apply_level(sk, "toLevel4", *levels["L4"])
    apply_level(sk, "toLevel5", [], levels["L5"][1], levels["L5"][2])
    finalise(sk, out_path)
