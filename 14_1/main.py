from typing import List


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def tilt_north(map_data: List[List[str]]):
    width, height = len(map_data[0]), len(map_data)
    rocks_advanced = 1
    while rocks_advanced:
        rocks_advanced = 0
        for y in range(1, height):
            for x in range(width):
                if map_data[y][x] == "O" and map_data[y-1][x] == ".":
                    map_data[y][x] = "."
                    map_data[y-1][x] = "O"
                    rocks_advanced += 1


def rocks_weight(map_data: List[List[str]]) -> int:
    height = len(map_data)
    total_weight = 0
    for row, row_factor in zip(map_data, reversed(range(1, height+1))):
        row_weight = sum([1 for r in row if r == "O"])
        total_weight += row_weight * row_factor
    return total_weight


def main():
    lines = read_lines()
    map_data = [[c for c in l] for l in lines if l != ""]
    tilt_north(map_data)
    print("weight is", rocks_weight(map_data))


if __name__ == "__main__":
    main()
