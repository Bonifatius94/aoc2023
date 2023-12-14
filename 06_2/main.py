from typing import List


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
    time = int(lines[0].split(":")[1].replace(" ", ""))
    distance = int(lines[1].split(":")[1].replace(" ", ""))
    print("options count is", options_count(time, distance))


if __name__ == "__main__":
    main()
