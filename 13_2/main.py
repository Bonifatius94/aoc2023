from typing import List, Tuple, Set


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def find_symmetry(rows: List[str]) -> Set[int]:
    height = len(rows)
    symms = set()
    for middle in range(1, height):
        offset = min(middle, height - middle)
        matches = 0
        for i in range(offset):
            if rows[middle-i-1] == rows[middle+i]:
                matches += 1
        if matches == offset:
            symms.add(middle)
    return symms


def is_symm_affected(height: int, affected_row: int, middle: int) -> bool:
    offset = min(middle, height - middle)
    min_row = middle - offset - 2
    max_row = middle + offset - 1
    return min_row <= affected_row <= max_row


def cols_of_map(map: List[str]) -> List[str]:
    width, height = len(map[0]), len(map)
    return [[map[y][x] for y in range(height)] for x in range(width)]


def invert_at(map: List[str], p: Tuple[int, int]):
    c = map[p[1]][p[0]]
    map[p[1]][p[0]] = "." if c == "#" else "#"


def fix_smudge(map: List[str]) -> int:
    width, height = len(map[0]), len(map)
    map_as_rows = [[c for c in line] for line in map]
    map_as_cols = cols_of_map(map)

    h_symm = find_symmetry(map_as_rows)
    v_symm = find_symmetry(map_as_cols)

    for x in range(width):
        for y in range(height):
            invert_at(map_as_rows, (x, y))
            invert_at(map_as_cols, (y, x))

            new_h_symm = find_symmetry(map_as_rows)
            new_v_symm = find_symmetry(map_as_cols)
            if new_h_symm and set.difference(new_h_symm, h_symm):
                new_symm = set.difference(new_h_symm, h_symm).pop()
                return new_symm * 100
            if new_v_symm and set.difference(new_v_symm, v_symm):
                new_symm = set.difference(new_v_symm, v_symm).pop()
                return new_symm

            invert_at(map_as_rows, (x, y))
            invert_at(map_as_cols, (y, x))

    raise ValueError("no new symmetry found")


def main():
    lines = read_lines()
    bounds = [-1] + [i for i, l in enumerate(lines) if l == ""] + [len(lines)]
    maps_as_rows = [lines[i+1:j] for i, j in zip(bounds[:-1], bounds[1:])]
    count = [fix_smudge(m) for m in maps_as_rows]
    print("sum of counts is", sum(count))


if __name__ == "__main__":
    main()
