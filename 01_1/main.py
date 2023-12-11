from typing import List
import numpy as np


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def first_digit(line: str) -> int:
    for c in line:
        if c.isdigit():
            return int(c)


def last_digit(line: str) -> int:
    return first_digit("".join(reversed(line)))


def main():
    lines = read_lines()
    scores = [first_digit(l) * 10 + last_digit(l) for l in lines]
    total = sum(scores)
    print(f"total is {total}")


if __name__ == "__main__":
    main()
