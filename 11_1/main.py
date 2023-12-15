from typing import List, Tuple


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def insert_empty_column(map_data: List[str], col: int):
    for i in range(len(map_data)):
        map_data[i] = map_data[i][:col] + "." + map_data[i][col:]


def insert_empty_row(map_data: List[str], row: int):
    map_data.insert(row, "." * len(map_data[0]))


def galaxy_positions(map_data: List[str]) -> List[Tuple[int, int]]:
    return [(col, row)
            for row, line in enumerate(map_data)
            for col, c in enumerate(line)
            if c == "#"]


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def main():
    map_data = [l for l in read_lines() if l != ""]
    galaxy_pos = galaxy_positions(map_data)

    width, height = len(map_data[0]), len(map_data)
    empty_rows = set(range(height)).difference(set([p[1] for p in galaxy_pos]))
    empty_cols = set(range(width)).difference(set([p[0] for p in galaxy_pos]))
    for row in reversed(sorted(list(empty_rows))):
        insert_empty_row(map_data, row)
    for col in reversed(sorted(list(empty_cols))):
        insert_empty_column(map_data, col)

    scaled_galaxy_pos = galaxy_positions(map_data)
    total_dist = 0
    for i in range(len(scaled_galaxy_pos)):
        for j in range(i):
            p1, p2 = scaled_galaxy_pos[i], scaled_galaxy_pos[j]
            total_dist += manhattan_distance(p1, p2)

    print("sum of galaxy distances is", total_dist)



if __name__ == "__main__":
    main()
