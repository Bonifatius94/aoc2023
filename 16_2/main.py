from typing import List, Tuple
from tqdm import tqdm


N, S, E, W = "N", "S", "E", "W"
MOVE_SLASH =  { N: W, S: E, W: N, E: S }
MOVE_BSLASH = { N: E, S: W, W: S, E: N }


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def move(pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    if direction == N:
        return pos[0], pos[1] - 1
    elif direction == S:
        return pos[0], pos[1] + 1
    elif direction == W:
        return pos[0] - 1, pos[1]
    else: # direction == E
        return pos[0] + 1, pos[1]


def follow_beam(
        map_data: List[List[str]],
        pos: Tuple[int, int],
        direction: str,
        visited_splitters: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    width, height = len(map_data[0]), len(map_data)
    while 0 <= pos[0] < width and 0 <= pos[1] < height:
        x, y = pos
        tile = map_data[y][x]
        yield pos
        if tile == "." \
                or (tile == "|" and direction in [S, N]) \
                or (tile == "-" and direction in [W, E]):
            pos = move(pos, direction)
        elif tile in ["/", "\\"]:
            mapping = MOVE_SLASH if tile == "\\" else MOVE_BSLASH
            direction = mapping[direction]
            pos = move(pos, direction)
        else: # tile in ["|", "-"]:
            if (x, y) in visited_splitters:
                return
            visited_splitters.append((x, y))
            ortho_dirs = [S, N] if tile == "|" else [E, W]
            for d in ortho_dirs:
                for p in follow_beam(map_data, pos, d, visited_splitters):
                    yield p
            return


def main():
    lines = read_lines()
    map_data = [[c for c in line] for line in lines if line != ""]
    tile_pos = [(x, y) for y in range(len(lines)) for x in range(len(lines[0]))]
    start_configs = \
        [(p, N) for p in tile_pos if p[1] == len(lines) - 1] + \
        [(p, S) for p in tile_pos if p[1] == 0] + \
        [(p, E) for p in tile_pos if p[0] == 0] + \
        [(p, W) for p in tile_pos if p[0] == len(lines[0]) - 1]
    energized_pos = max([len(set(follow_beam(map_data, s, d, []))) for s, d in start_configs])
    print("energized tiles", energized_pos)


if __name__ == "__main__":
    main()
