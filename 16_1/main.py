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
        splitters: List[Tuple[str, int, int]]) -> List[Tuple[int, int]]:
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
            if (tile, x, y) in splitters:
                return
            splitters.append((tile, x, y))
            ortho_dirs = [S, N] if tile == "|" else [E, W]
            beam1 = iter(follow_beam(map_data, pos, ortho_dirs[0], splitters))
            beam2 = iter(follow_beam(map_data, pos, ortho_dirs[1], splitters))
            while True:
                p1, p2 = next(beam1, None), next(beam2, None)
                if p1:
                    yield p1
                if p2:
                    yield p2
                if not p1 and not p2:
                    return


def main():
    lines = read_lines()
    map_data = [[c for c in line] for line in lines if line != ""]
    energized_tiles = set(follow_beam(map_data, (0, 0), E, []))
    print("energized tiles", len(energized_tiles))


if __name__ == "__main__":
    main()
