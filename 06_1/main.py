from typing import List
from functools import reduce


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def options_count(time: int, distance: int) -> int:
    count = 0
    for t_hold in range(0, time+1):
        d = (time - t_hold) * t_hold
        if d >= distance:
            count += 1
    return count


def main():
    lines = read_lines()
    print(lines[0].split(":")[1].strip().split(" "))
    times = [int(t.strip()) for t in lines[0].split(":")[1].strip().split(" ") if t != ""]
    distances = [int(d.strip()) for d in lines[1].split(":")[1].strip().split(" ") if d != ""]
    counts = [options_count(t, d) for t, d in zip(times, distances)]
    print("option products are", reduce(lambda x, y: x * y, counts))


if __name__ == "__main__":
    main()
