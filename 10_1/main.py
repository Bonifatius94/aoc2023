from typing import List, Tuple
from math import ceil


NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"
DIRS = [NORTH, SOUTH, EAST, WEST]
NS, EW, NE, NW, SW, SE = "|", "-", "L", "J", "7", "F"
TILES = [NS, EW, NE, NW, SW, SE]
TILE_MAP = {
    (NS, SOUTH): SOUTH,
    (NS, NORTH): NORTH,
    (EW, WEST): WEST,
    (EW, EAST): EAST,
    (NE, SOUTH): EAST,
    (NE, WEST): NORTH,
    (NW, SOUTH): WEST,
    (NW, EAST): NORTH,
    (SW, NORTH): WEST,
    (SW, EAST): SOUTH,
    (SE, NORTH): EAST,
    (SE, WEST): SOUTH,
}


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def find_initial_dirs(map_data: List[str], pos: Tuple[int, int]) -> List[str]:
    x, y = pos
    dirs = []
    if map_data[y][x-1] in [EW, SW, NW]:
        dirs.append(WEST)
    if map_data[y][x+1] in [EW, SE, NE]:
        dirs.append(EAST)
    if map_data[y-1][x] in [NS, NE, NW]:
        dirs.append(NORTH)
    if map_data[y+1][x] in [NS, SE, SW]:
        dirs.append(SOUTH)
    return dirs


def move(pos: Tuple[int, int], dir: str) -> Tuple[int, int]:
    x, y = pos
    if dir == NORTH:
        return x, y - 1
    elif dir == SOUTH:
        return x, y + 1
    elif dir == EAST:
        return x + 1, y
    else: # dir == WEST
        return x - 1, y


def find_distance(map_data: List[str]):
    start_pos = next(iter(
        [(col, row) for row, line in enumerate(map_data)
         for col, c in enumerate(line) if c == "S"]
    ))
    assert map_data[start_pos[1]][start_pos[0]] == "S"

    direction = find_initial_dirs(map_data, start_pos)
    pos = move(start_pos, direction)

    steps = 1
    while True:
        x, y = pos
        tile = map_data[y][x]
        direction = TILE_MAP[(tile, direction)]
        pos = move(pos, direction)
        steps += 1
        if pos == start_pos:
            break

    return int(ceil(steps / 2))


def main():
    map_data = [l for l in read_lines() if l != ""]
    print("distance is", find_distance(map_data))


if __name__ == "__main__":
    main()
