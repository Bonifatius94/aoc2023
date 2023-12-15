from typing import List, Tuple, Set


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def galaxy_positions(map_data: List[str]) -> List[Tuple[int, int]]:
    return [(col, row)
            for row, line in enumerate(map_data)
            for col, c in enumerate(line)
            if c == "#"]


def manhattan_distance(
        p1: Tuple[int, int], p2: Tuple[int, int],
        empty_rows: Set[int], empty_cols: Set[int]) -> int:
    x_diff, y_diff = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    for row in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
        if row in empty_rows:
            y_diff += 1_000_000 - 1
    for col in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
        if col in empty_cols:
            x_diff += 1_000_000 - 1
    return x_diff + y_diff


def main():
    map_data = [l for l in read_lines() if l != ""]
    galaxy_pos = galaxy_positions(map_data)

    width, height = len(map_data[0]), len(map_data)
    empty_rows = set(range(height)).difference(set([p[1] for p in galaxy_pos]))
    empty_cols = set(range(width)).difference(set([p[0] for p in galaxy_pos]))

    total_dist = 0
    for i in range(len(galaxy_pos)):
        for j in range(i):
            p1, p2 = galaxy_pos[i], galaxy_pos[j]
            total_dist += manhattan_distance(p1, p2, empty_rows, empty_cols)

    print("sum of galaxy distances is", total_dist)



if __name__ == "__main__":
    main()
