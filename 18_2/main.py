
from typing import List, Tuple, Union


N, S, E, W = "U", "D", "R", "L"
NW, NE, SW, SE = "NW", "NE", "SW", "SE"
DIRS_TO_CONN = {
    (N, W): NW, (W, N): NW,
    (N, E): NE, (E, N): NE, 
    (S, W): SW, (W, S): SW, 
    (S, E): SE, (E, S): SE,
}
REVERSE_DIR = { N: S, S: N, E: W, W: E }
DIR_FROM_COLOR = { "0": E, "1": S, "2": W, "3": N }
Direction = Union[N, S, E, W]
Pos = Tuple[int, int]


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def poly_area(vertices: List[Tuple[float, float]]) -> float:
    segments = list(zip(vertices, vertices[1:] + [vertices[0]]))
    return 0.5 * abs(sum([x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments]))


def move(pos: Pos, direction: Direction, length: int) -> Pos:
    if direction == N:
        return pos[0], pos[1] - length
    elif direction == S:
        return pos[0], pos[1] + length
    elif direction == W:
        return pos[0] - length, pos[1]
    else: # direction == E
        return pos[0] + length, pos[1]


def tile_outlines(tiles: List[Tuple[str, Tuple[int, int]]]) \
        -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:

    def dir_of(tile: str, is_horizontal: bool) -> str:
        if tile == NE:
            return E if is_horizontal else N
        elif tile == NW:
            return W if is_horizontal else N
        elif tile == SE:
            return E if is_horizontal else S
        elif tile == SW:
            return W if is_horizontal else S

    vertices = [(t, p) for t, p in tiles if t in [NE, NW, SW, SE]]
    vertices_loop = vertices + [vertices[0]]

    right_outline, left_outline = [], []
    for (t1, p1), (_, p2) in zip(vertices_loop[:-1], vertices_loop[1:]):
        is_horizontal = p1[1] == p2[1]
        direction = REVERSE_DIR[dir_of(t1, not is_horizontal)]

        if t1 == SE:
            e1 = (p1[0] + 0.5, p1[1] + 0.5)
            e2 = (p1[0] - 0.5, p1[1] - 0.5)
            right_outline.append(e1 if direction == N else e2)
            left_outline.append(e2 if direction == N else e1)
        elif t1 == SW:
            e1 = (p1[0] + 0.5, p1[1] - 0.5)
            e2 = (p1[0] - 0.5, p1[1] + 0.5)
            right_outline.append(e1 if direction == N else e2)
            left_outline.append(e2 if direction == N else e1)
        elif t1 == NE:
            e1 = (p1[0] - 0.5, p1[1] + 0.5)
            e2 = (p1[0] + 0.5, p1[1] - 0.5)
            right_outline.append(e1 if direction == S else e2)
            left_outline.append(e2 if direction == S else e1)
        else: # t1 == NW
            e1 = (p1[0] - 0.5, p1[1] - 0.5)
            e2 = (p1[0] + 0.5, p1[1] + 0.5)
            right_outline.append(e1 if direction == S else e2)
            left_outline.append(e2 if direction == S else e1)

    return right_outline, left_outline


def main():
    lines = read_lines()
    lines = [l for l in lines if l != ""]
    draw_instrs = [line.split(" ") for line in lines]
    draw_instrs = [(DIR_FROM_COLOR[c[-2]], int(c[2:-2], 16)) for _, _, c in draw_instrs]
    edges = [(0, 0)]
    pos = (0, 0)
    for direction, length in draw_instrs:
        pos = move(pos, direction, length)
        edges.append(pos)
    conn = [draw_instrs[-1][0]] + [d for d, _ in draw_instrs]
    conn = [DIRS_TO_CONN[(d1, REVERSE_DIR[d2])] for d1, d2 in zip(conn[:-1], conn[1:])]
    tiles = list(zip(conn, edges))
    right_outline, left_outline = tile_outlines(tiles)
    print("area is", int(max(poly_area(right_outline), poly_area(left_outline))))


if __name__ == "__main__":
    main()
