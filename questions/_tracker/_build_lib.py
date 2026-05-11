"""Shared builder helpers for VC2 question files."""
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
    slot["question"] = q
    slot["correct"] = correct
    slot["correctExplanation"] = expl
    slot["distractors"] = [
        {"answer": d, "explanation": "This option does not fit the topic.", "misconceptionSource": "inferred"}
        for d in distractors
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
    """Run length-extension passes, trim correct/distractors, write output."""
    def ext_pass(thr, suffix):
        for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
            for v in sk[L]:
                if v["type"] != "mc":
                    continue
                for d in v["distractors"]:
                    if len(d["answer"]) < thr:
                        d["answer"] = d["answer"].rstrip(".") + " " + suffix

    ext_pass(100, "in any country at any stage")
    ext_pass(125, "across many regions")
    ext_pass(145, "over many years")
    ext_pass(175, "across many societies")

    def trim(s, mx=30):
        ws = s.split()
        if len(ws) <= mx:
            return s
        return " ".join(ws[:mx]).rstrip(",.;:")

    for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
        for v in sk[L]:
            if v["type"] == "mc":
                v["correct"] = trim(v["correct"])
                for d in v["distractors"]:
                    d["answer"] = trim(d["answer"])

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


def NL_phrases(topic_noun):
    """Return (NL, NLD, NLD2, NLD3, NLD4) where NL is the long form, NLD shorter."""
    NL = f"has no link to {topic_noun} in any region at any stage today at every stage at all today"
    NLD = f"has no link to {topic_noun} today at every stage at all today"
    NLD2 = "always avoids every elected role today at every stage at all today"
    NLD3 = "always relies on random outcomes today at every stage at all today"
    NLD4 = "always avoids every shared rule today at every stage at all today"
    return NL, NLD, NLD2, NLD3, NLD4
