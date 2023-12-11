from typing import List
import numpy as np


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def first_digit(line: str, rev: bool=False) -> int:
    long_digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    if rev:
        long_digits = ["".join(reversed(d)) for d in long_digits]
    long_digits_int = dict(zip(long_digits, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

    long_matches = [line.index(t) if t in line else len(line) for t in long_digits]
    long_digit_id = np.min(long_matches)
    token = long_digits[np.argmin(long_matches)]

    short_digit_id = len(line)
    for i, c in enumerate(line):
        if c.isdigit():
            short_digit_id = i
            break

    if long_digit_id < short_digit_id:
        return long_digits_int[token]
    else:
        return int(line[short_digit_id])


def last_digit(line: str) -> int:
    return first_digit("".join(reversed(line)), True)


def main():
    lines = read_lines()
    scores = [first_digit(l) * 10 + last_digit(l) for l in lines]
    total = sum(scores)
    print(f"total is {total}")


if __name__ == "__main__":
    main()
