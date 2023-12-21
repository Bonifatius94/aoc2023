from typing import List, Dict, Tuple, Optional
from copy import deepcopy

RatingRange = Dict[str, Tuple[int, int]]
Workflows = Dict[str, str]


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def satisfies_condition(cond: str, rating_range: RatingRange) \
        -> Tuple[Optional[RatingRange], Optional[RatingRange]]:
    if "<" in cond:
        var, cmp = cond.split("<")
        cmp = int(cmp)
        lower, upper = rating_range[var]
        if upper < cmp:
            return rating_range, None
        elif lower < cmp <= upper:
            acc_range = deepcopy(rating_range)
            acc_range[var] = (lower, cmp-1)
            rej_range = deepcopy(rating_range)
            rej_range[var] = (cmp, upper)
            return acc_range, rej_range
        else: # cmp < lower
            return None, rating_range
    else: # ">" in cond
        var, cmp = cond.split(">")
        cmp = int(cmp)
        lower, upper = rating_range[var]
        if cmp < lower:
            return rating_range, None
        elif lower <= cmp < upper:
            acc_range = deepcopy(rating_range)
            acc_range[var] = (cmp+1, upper)
            rej_range = deepcopy(rating_range)
            rej_range[var] = (lower, cmp)
            return acc_range, rej_range
        else: # upper < upper
            return None, rating_range


def satisfies_workflow(workflows: Workflows, label: str, acc_range: RatingRange):
    if label == "A":
        yield acc_range
    elif label == "R":
        pass
    else:
        workflow = workflows[label]
        for rule in workflow[:-1]:
            cond, next_label = rule.split(":")
            acc_range, rej_range = satisfies_condition(cond, acc_range)
            if acc_range:
                for r in satisfies_workflow(workflows, next_label, acc_range):
                    yield r
            if rej_range:
                acc_range = rej_range
            else:
                return
        for r in satisfies_workflow(workflows, workflow[-1], acc_range):
            yield r


def main():
    print(satisfies_condition("a<10", { "a": (0, 10) }))
    print(satisfies_condition("a<10", { "a": (0, 11) }))
    print(satisfies_condition("a<10", { "a": (10, 20) }))
    print(satisfies_condition("a<10", { "a": (11, 20) }))

    print(satisfies_condition("a>10", { "a": (0, 9) }))
    print(satisfies_condition("a>10", { "a": (0, 10) }))
    print(satisfies_condition("a>10", { "a": (0, 12) }))
    print(satisfies_condition("a>10", { "a": (10, 20) }))
    print(satisfies_condition("a>10", { "a": (11, 20) }))
    # exit()

    lines = [
        "px{a<2006:qkq,m>2090:A,rfg}",
        "pv{a>1716:R,A}",
        "lnx{m>1548:A,A}",
        "rfg{s<537:gd,x>2440:R,A}",
        "qs{s>3448:A,lnx}",
        "qkq{x<1416:A,crn}",
        "crn{x>2662:A,R}",
        "in{s<1351:px,qqz}",
        "qqz{s>2770:qs,m<1801:hdj,R}",
        "gd{a>3333:R,R}",
        "hdj{m>838:A,pv}",
        "",
        "{x=787,m=2655,a=1222,s=2876}",
        "{x=1679,m=44,a=2067,s=496}",
        "{x=2036,m=264,a=79,s=2244}",
        "{x=2461,m=1339,a=466,s=291}",
        "{x=2127,m=1623,a=2188,s=1013}",
    ]
    # 167010937327821
    # 167409079868000

    # lines = read_lines()
    splitter = lines.index("")
    workflows = dict([(l[:l.index("{")], l[l.index("{")+1:l.index("}")].split(","))
                      for l in lines[:splitter]])
    full_range = { "x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000) }
    sat_ranges = satisfies_workflow(workflows, "in", full_range)
    num_poss = [(r["x"][1] - r["x"][0]) * (r["m"][1] - r["m"][0]) \
                * (r["a"][1] - r["a"][0]) * (r["s"][1] - r["s"][0]) for r in sat_ranges]
    print("score is", sum(num_poss))


if __name__ == "__main__":
    main()
