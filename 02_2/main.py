from typing import List, Dict


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def is_valid_count(color: str, count: int) -> bool:
    if color == "red":
        return count <= 12
    elif color == "green":
        return count <= 13
    elif color == "blue":
        return count <= 14
    else:
        raise ValueError("unknown color!")


def power_of_game(log: str) -> int:
    log = log.split(":")[1].strip()
    subgames = [sg.strip() for sg in log.split(";")]

    min_counts = { "red": 0, "blue": 0, "green": 0 }
    for sg in subgames:
        cubes = [c.strip() for c in sg.split(",")]
        for c in cubes:
            parts = c.split(" ")
            count, color = int(parts[0]), parts[1]
            min_counts[color] = max(min_counts[color], count)

    return min_counts["red"] * min_counts["blue"] * min_counts["green"]


def main():
    lines = read_lines()
    res = sum([power_of_game(l) for l in lines])
    print("sum of game powers is", res)


if __name__ == "__main__":
    main()
