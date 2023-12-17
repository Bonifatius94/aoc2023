from typing import List, Tuple, Optional
from math import floor


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


def tilt_south(map_data: List[List[str]]):
    width, height = len(map_data[0]), len(map_data)
    rocks_advanced = 1
    while rocks_advanced:
        rocks_advanced = 0
        for y in reversed(range(0, height - 1)):
            for x in range(width):
                if map_data[y][x] == "O" and map_data[y+1][x] == ".":
                    map_data[y][x] = "."
                    map_data[y+1][x] = "O"
                    rocks_advanced += 1


def tilt_west(map_data: List[List[str]]):
    width, height = len(map_data[0]), len(map_data)
    rocks_advanced = 1
    while rocks_advanced:
        rocks_advanced = 0
        for x in range(1, width):
            for y in range(height):
                if map_data[y][x] == "O" and map_data[y][x-1] == ".":
                    map_data[y][x] = "."
                    map_data[y][x-1] = "O"
                    rocks_advanced += 1


def tilt_east(map_data: List[List[str]]):
    width, height = len(map_data[0]), len(map_data)
    rocks_advanced = 1
    while rocks_advanced:
        rocks_advanced = 0
        for x in reversed(range(0, width-1)):
            for y in range(height):
                if map_data[y][x] == "O" and map_data[y][x+1] == ".":
                    map_data[y][x] = "."
                    map_data[y][x+1] = "O"
                    rocks_advanced += 1


def turn_around(map_data: List[List[str]]):
    tilt_north(map_data)
    tilt_west(map_data)
    tilt_south(map_data)
    tilt_east(map_data)


def rocks_weight(map_data: List[List[str]]) -> int:
    height = len(map_data)
    total_weight = 0
    for row, row_factor in zip(map_data, reversed(range(1, height+1))):
        row_weight = sum([1 for r in row if r == "O"])
        total_weight += row_weight * row_factor
    return total_weight


def find_cycle(weights: List[int]) -> Optional[Tuple[int, List[int]]]:
    for offset in range(3, floor(len(weights) / 2)):
        i = len(weights) - offset
        j = len(weights) - 2*offset
        if weights[i:] == weights[j:i]:
            return j, weights[j:i]
    return None


def main():
    lines = read_lines()
    map_data = [[c for c in l] for l in lines if l != ""]

    weights = []
    while True:
        turn_around(map_data)
        weights.append(rocks_weight(map_data))
        cycle = find_cycle(weights)
        if cycle:
            offset, cycle_weights = cycle
            i = (1_000_000_000 - offset - 1) % len(cycle_weights)
            print("weight after 1_000_000_000 cycles is", cycle_weights[i])
            break


if __name__ == "__main__":
    main()
