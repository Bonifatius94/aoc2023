from typing import List, Tuple
from shapely.geometry import Polygon


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


def all_tiles(map_data: List[str]) -> List[Tuple[str, Tuple[int, int]]]:
    start_pos = next(iter(
        [(col, row) for row, line in enumerate(map_data)
         for col, c in enumerate(line) if c == "S"]
    ))
    assert map_data[start_pos[1]][start_pos[0]] == "S"

    direction = EAST
    pos = move(start_pos, direction)

    res = []
    while True:
        x, y = pos
        tile = map_data[y][x]
        res.append((tile, pos))
        direction = TILE_MAP[(tile, direction)]
        pos = move(pos, direction)
        if pos == start_pos:
            break
    res.append(("S", start_pos))
    return res


def poly_area(tiles: List[Tuple[str, Tuple[int, int]]]) -> int:

    def dir_of(tile: str, is_horizontal: bool) -> str:
        if tile == NE:
            return EAST if is_horizontal else NORTH
        elif tile == NW:
            return WEST if is_horizontal else NORTH
        elif tile == SE:
            return EAST if is_horizontal else SOUTH
        elif tile == SW:
            return WEST if is_horizontal else SOUTH

    def reverse_dir(direction: str) -> str:
        if direction == NORTH:
            return SOUTH
        elif direction == SOUTH:
            return NORTH
        elif direction == WEST:
            return EAST
        else: # direction == EAST
            return WEST

    vertices = [(t, p) for t, p in tiles if t in [NE, NW, SW, SE]]
    vertices_loop = vertices + [vertices[0]]

    right_outline, left_outline = [], []
    for (t1, p1), (_, p2) in zip(vertices_loop[:-1], vertices_loop[1:]):
        is_horizontal = p1[1] == p2[1]
        direction = reverse_dir(dir_of(t1, not is_horizontal))

        if t1 == SE:
            e1 = (p1[0] + 0.5, p1[1] + 0.5)
            e2 = (p1[0] - 0.5, p1[1] - 0.5)
            right_outline.append(e1 if direction == NORTH else e2)
            left_outline.append(e2 if direction == NORTH else e1)
        elif t1 == SW:
            e1 = (p1[0] + 0.5, p1[1] - 0.5)
            e2 = (p1[0] - 0.5, p1[1] + 0.5)
            right_outline.append(e1 if direction == NORTH else e2)
            left_outline.append(e2 if direction == NORTH else e1)
        elif t1 == NE:
            e1 = (p1[0] - 0.5, p1[1] + 0.5)
            e2 = (p1[0] + 0.5, p1[1] - 0.5)
            right_outline.append(e1 if direction == SOUTH else e2)
            left_outline.append(e2 if direction == SOUTH else e1)
        else: # t1 == NW
            e1 = (p1[0] - 0.5, p1[1] - 0.5)
            e2 = (p1[0] + 0.5, p1[1] + 0.5)
            right_outline.append(e1 if direction == SOUTH else e2)
            left_outline.append(e2 if direction == SOUTH else e1)

    # TODO: implement own polygon area calculation
    p1, p2 = Polygon(right_outline), Polygon(left_outline)
    return int(min(p1.area, p2.area))


def main():
    map_data = [l for l in read_lines() if l != ""]
    tiles = all_tiles(map_data)
    print("area is", poly_area(tiles))


if __name__ == "__main__":
    main()
