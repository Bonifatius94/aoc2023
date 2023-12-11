from typing import List, Tuple, Set


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def parse_card(line: str) -> Tuple[Set[int], Set[int]]:
    line = line.split(":")[1].strip()
    parts = line.split("|")
    win_ids = set([int(i) for i in parts[0].split(" ") if i.isdigit()])
    own_ids = set([int(i) for i in parts[1].split(" ") if i.isdigit()])
    return win_ids, own_ids


def main():
    lines = read_lines()
    cards = [parse_card(l) for l in lines]
    num_matches = [len(set.intersection(win_ids, own_ids))
                   for win_ids, own_ids in cards]
    scores = [0 if n == 0 else 1 << (n-1) for n in num_matches]
    print("sum of card scores is", sum(scores))


if __name__ == "__main__":
    main()
