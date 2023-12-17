from typing import List


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def find_symmetry(rows: List[str]) -> int:
    height = len(rows)
    for middle in range(1, height):
        offset = min(middle, height - middle)
        matches = 0
        for i in range(offset):
            if rows[middle-i-1] == rows[middle+i]:
                matches += 1
        if matches == offset:
            return middle
    return 0


def main():
    lines = read_lines()
    bounds = [-1] + [i for i, l in enumerate(lines) if l == ""] + [len(lines)]
    maps_as_rows = [lines[i+1:j] for i, j in zip(bounds[:-1], bounds[1:])]
    maps_as_cols = [["".join([map[y][x] for y in range(len(map))])
                     for x in range(len(map[0]))] for map in maps_as_rows]
    h_count = [find_symmetry(m) for m in maps_as_rows]
    v_count = [find_symmetry(m) for m in maps_as_cols]
    print("sum of counts is", sum(h_count) * 100 + sum(v_count))


if __name__ == "__main__":
    main()
