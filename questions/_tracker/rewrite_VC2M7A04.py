#!/usr/bin/env python3
"""Manual distractor rewrite for VC2M7A04.json — graphs and variable relationships."""
import json

PATH = "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum/questions/level-07/Mathematics/VC2M7A04.json"

REWRITES = {
    "What does a line going up to the right show?": [
        "A decreasing relationship where y falls as x rises",
        "No relationship at all between the two variables shown",
    ],
    "What does a line going down to the right show?": [
        "An increasing relationship where y rises as x rises",
        "No relationship at all between the two variables shown",
    ],
    "What does the point (3, 5) mean?": [
        "At x equals 5 and y equals 3 on the Cartesian plane",
        "At the very centre of the Cartesian plane where axes meet",
    ],
    "What does a horizontal line on a graph show?": [
        "That y changes very fast as x changes across the graph",
        "That x stays constant as y changes across the graph",
    ],
    "Can real-world data appear on graphs?": [
        "No, only invented data appears on graphs in school textbooks",
        "Only data from textbooks appears on graphs we draw at school",
    ],
    "Why is the Cartesian plane used for graphing?": [
        "It uses three perpendicular axes to plot every single value",
        "It uses just one axis to plot pairs of values together",
    ],
    "Why is the order in (x, y) important?": [
        "x and y can be in any order without changing the point at all",
        "y comes first and x comes second whenever we plot any point",
    ],
    "Why does an increasing relationship slope upward?": [
        "As x increases, y stays the same height on the line we draw",
        "As x decreases, y increases on the line because of the inverse pattern",
    ],
    "Why does a horizontal line mean y is constant?": [
        "x does not change as y changes on the line, so the line is vertical instead",
        "Both x and y change rapidly along the line, creating a steep slope upward",
    ],
    "Why is time usually on the x-axis?": [
        "Time is always the dependent variable on every graph we draw",
        "Time always appears on the y-axis whenever we draw a graph",
    ],
    "Why does a scatter plot show many points?": [
        "Each point shows the average of every observation we made",
        "Each point shows only the highest single observation in the data",
    ],
    "Why is plotting (3, 5) different from plotting (5, 3)?": [
        "The two points are at the same place on the Cartesian plane",
        "Order does not matter at all when we plot two points on a graph",
    ],
    "Why are axes usually labelled with units?": [
        "Labels are decorative and have no function on the graph itself",
        "Labels confuse the reader of the graph and should be avoided",
    ],
    "Why is a graph more useful than a long list of numbers?": [
        "Lists always show patterns better than graphs in every situation",
        "Graphs always hide the underlying patterns in any set of numbers",
    ],
    "Which best explains using graphs to investigate variables?": [
        "Graphs only display data with no analysis or pattern finding",
        "Graphs cannot show two variables together on the same plane",
    ],
    "Why is order in (x, y) important?": [
        "x and y can be in any order without changing the point at all",
        "y comes first and x comes second whenever we plot any point",
    ],
    "Why is a graph more useful than a long list?": [
        "Lists always show patterns better than graphs in every situation",
        "Graphs always hide the underlying patterns in any set of numbers",
    ],
    "Evaluate: how do graphs investigate real-world relationships?": [
        "Graphs only display data with no analysis or pattern finding",
        "Graphs cannot show two variables together on the same plane",
    ],
    "Justify: why are graphs useful for trends?": [
        "They hide the data from the reader of the graph",
        "They convert data into long text descriptions of the values",
    ],
    "Evaluate: how do increasing relationships look on graphs?": [
        "Lines fall to the right as x increases on the graph",
        "Lines stay completely flat regardless of x values plotted",
    ],
    "Justify: why does a horizontal line mean y is constant?": [
        "x does not change as y changes on the line, making it vertical",
        "Both x and y change rapidly along the line, creating a steep slope",
    ],
    "Critique: a risk of expecting real data to fit a perfect line is what?": [
        "Real measurements always fit a perfect line on every kind of graph",
        "Real data never has any scatter in any practical situation we meet",
    ],
    "Evaluate: how do scatter plots help with real data?": [
        "They show only the average of every value in the dataset",
        "They hide the spread of values from the reader of the graph",
    ],
    "Justify: why are linear graphs important?": [
        "Linear graphs never appear in real-world data at any time",
        "Linear graphs only appear in textbooks and never in real measurements",
    ],
    "Assess: when does labelling axes most help?": [
        "When labels are decorative and unused on the graph itself",
        "When labels confuse the reader of the graph at every step",
    ],
    "Critique: a risk of skipping graph analysis is what?": [
        "Lists always show patterns better than graphs in every case",
        "Skipping analysis improves understanding of the data shown",
    ],
    "Evaluate: how do First Nations seasonal calendars show variable relationships?": [
        "They never show any relationships between events on Country",
        "They only show one season at a time without connections between them",
    ],
    "Justify: why is a graph more useful than a long list?": [
        "Lists always show patterns better than graphs in every situation",
        "Graphs always hide the underlying patterns in any set of numbers",
    ],
}


def main():
    d = json.loads(open(PATH).read())
    n = 0
    missing = set()
    for L in ("toLevel2", "toLevel3", "toLevel4", "toLevel5"):
        for v in d.get(L, []):
            if v.get("type") != "mc":
                continue
            q = v.get("question", "").strip()
            if q in REWRITES:
                new_dists = REWRITES[q]
                if len(new_dists) == len(v.get("distractors", [])):
                    for dd, new_ans in zip(v["distractors"], new_dists):
                        dd["answer"] = new_ans
                    n += 1
            else:
                strs = [v.get("correct") or ""] + [x.get("answer") or "" for x in v.get("distractors", [])]
                if any("in maths and" in s or "across many problem types" in s for s in strs):
                    missing.add(q)
    with open(PATH, "w") as f:
        json.dump(d, f, indent=2)
    print(f"Replaced distractors in {n} MC items")
    for q in sorted(missing):
        print(f"  MISS: {q}")


if __name__ == "__main__":
    main()
