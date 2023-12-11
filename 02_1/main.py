from typing import List


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


def is_game_possible(log: str) -> bool:
    log = log.split(":")[1].strip()
    subgames = [sg.strip() for sg in log.split(";")]

    for sg in subgames:
        cubes = [c.strip() for c in sg.split(",")]
        for c in cubes:
            parts = c.split(" ")
            count, color = int(parts[0]), parts[1]
            if not is_valid_count(color, count):
                return False

    return True


def main():
    lines = read_lines()
    res = sum([i+1 for i, l in enumerate(lines) if is_game_possible(l)])
    print("sum of IDs is", res)


if __name__ == "__main__":
    main()
