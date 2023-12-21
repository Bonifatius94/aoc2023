from typing import List
from tqdm import tqdm


DAMAGED = "#"
OPERATIONAL = "."
WILDCARD = "?"


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def is_possible_arrangement(pattern: str, backup_log: List[int]) -> bool:
    # TODO: reimplement this with bitwise ops
    offset = 0
    for count in backup_log:
        while offset < len(pattern) and pattern[offset] == OPERATIONAL:
            offset += 1

        if offset < len(pattern) and len(pattern[offset:]) < count:
            return False

        if not all([s == DAMAGED for s in pattern[offset:offset+count]]):
            return False

        offset += count
        if not (offset >= len(pattern) or pattern[offset] == OPERATIONAL):
            return False

    while offset < len(pattern) and pattern[offset] == OPERATIONAL:
        offset += 1

    return offset == len(pattern)


def permute_no_duplicates(
        pattern: List[str], wildcard_pos: List[int],
        num_damaged_wildcards: int, offset: int=0) -> List[str]:

    remaining_wildcards = len(wildcard_pos) - offset
    if num_damaged_wildcards == 0:
        for pos in wildcard_pos[offset:]:
            pattern[pos] = OPERATIONAL
        yield pattern
    elif remaining_wildcards == num_damaged_wildcards:
        for pos in wildcard_pos[offset:]:
            pattern[pos] = DAMAGED
        yield pattern
    elif remaining_wildcards > num_damaged_wildcards:
        if offset == len(wildcard_pos) - 1:
            for s in [OPERATIONAL, DAMAGED]:
                pattern[wildcard_pos[offset]] = s
                yield pattern
        else:
            for s in [OPERATIONAL, DAMAGED]:
                pattern[wildcard_pos[offset]] = s
                remaining_damaged = num_damaged_wildcards - (1 if s == DAMAGED else 0)
                perms = permute_no_duplicates(
                    pattern, wildcard_pos, remaining_damaged, offset+1)
                for p in perms:
                    yield p


def possible_arrangements(pattern: str, backup_log: List[int]) -> int:
    pattern = [s for s in pattern]
    wildcard_pos = [i for i, s in enumerate(pattern) if s == WILDCARD]
    num_det_damaged = sum([1 for s in pattern if s == DAMAGED])
    num_damaged_wildcards = sum(backup_log) - num_det_damaged

    count = 0
    for pattern_to_test in permute_no_duplicates(
            pattern, wildcard_pos, num_damaged_wildcards):
        if is_possible_arrangement(pattern_to_test, backup_log):
            count += 1

    return count


def main():
    # lines = read_lines()
    lines = [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1",
    ]
    spring_records = [
        (l[:l.index(" ")], [int(c) for c in l[l.index(" ")+1:].split(",")])
        for l in lines if l != ""
    ]
    spring_records = [("?".join([p for _ in range(5)]), b * 5) for p, b in spring_records]
    # print(spring_records[0])
    # print(max([sum([1 for s in p if s == WILDCARD]) for p, b in spring_records]))

    poss_arr = [possible_arrangements(p, b) for p, b in tqdm(spring_records)]
    print("sum of possible arrangements", sum(poss_arr))


if __name__ == "__main__":
    main()
