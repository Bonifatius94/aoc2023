from typing import List, Dict


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def is_true(cond: str, rating: Dict[str, int]) -> bool:
    if "<" in cond:
        var, cmp = cond.split("<")
        return rating[var] < int(cmp)
    else: # ">" in cond
        var, cmp = cond.split(">")
        return rating[var] > int(cmp)


def is_part_accepted(workflows, rating) -> bool:
    label = "in"
    while True:
        if label == "R":
            return False
        if label == "A":
            return True
        workflow = workflows[label]
        for rule in workflow:
            if ":" in rule:
                cond, next_label = rule.split(":")
                if is_true(cond, rating):
                    label = next_label
                    break
            else:
                label = rule


def main():
    lines = read_lines()
    splitter = lines.index("")
    workflows = dict([(l[:l.index("{")], l[l.index("{")+1:l.index("}")].split(",")) for l in lines[:splitter]])
    part_ratings = [[int(p[p.index("=")+1:]) for p in r[1:-1].split(",")] for r in lines[splitter+1:]]
    part_ratings = [{ "x": x, "m": m, "a": a, "s": s } for x, m, a, s in part_ratings]

    accepted_parts = [p for p in part_ratings if is_part_accepted(workflows, p)]
    score = sum([p["x"] + p["m"] + p["a"] + p["s"] for p in accepted_parts])
    print("score is", score)


if __name__ == "__main__":
    main()
