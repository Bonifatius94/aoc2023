from typing import List
from tqdm import tqdm
from functools import lru_cache


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def can_fit_damaged_sequence(pattern: str, num_damaged: int) -> bool:
    return len(pattern) >= num_damaged \
        and all([c in ["#", "?"] for c in pattern[:num_damaged]]) \
        and (len(pattern) == num_damaged or pattern[num_damaged] in [".", "?"])


def potential_damanged_count(pattern: str) -> int:
    return sum([1 for c in pattern if c in ["#", "?"]])


@lru_cache(maxsize=1024)
def possible_arrangements(pattern: str, backup: List[int]) -> int:
    if len(backup) == 0:
        return 0 if "#" in pattern else 1
    elif len(pattern) == 0:
        return 0

    first_damaged = pattern.index("#") if "#" in pattern else len(pattern)
    first_lossy = pattern.index("?") if "?" in pattern else len(pattern)
    if first_damaged < first_lossy:
        offset = first_damaged
        if can_fit_damaged_sequence(pattern[offset:], backup[0]):
            return possible_arrangements(pattern[offset+backup[0]+1:], backup[1:])
        else:
            return 0
    else:
        offset = first_lossy
        if can_fit_damaged_sequence(pattern[offset:], backup[0]):
            count_no_dmg = possible_arrangements(pattern[offset+1:], backup)
            count_dmg = possible_arrangements(pattern[offset+backup[0]+1:], backup[1:])
            return count_no_dmg + count_dmg
        else:
            return possible_arrangements(pattern[offset+1:], backup)


def main():
    lines = read_lines()
    spring_records = [
        (l[:l.index(" ")], [int(c) for c in l[l.index(" ")+1:].split(",")])
        for l in lines if l != ""
    ]
    spring_records = [("?".join([p for _ in range(5)]), b * 5) for p, b in spring_records]
    spring_records = [(p, tuple(b)) for p, b in spring_records]

    poss_arr = [possible_arrangements(p, b) for p, b in spring_records]
    print("sum of possible arrangements", sum(poss_arr))


if __name__ == "__main__":
    main()
