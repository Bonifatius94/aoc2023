from typing import List, Tuple, Dict, Set, Any


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def group_by_key(pairs: List[Tuple[Any, Any]]) -> Dict[Any, Set[Any]]:
    res: Dict[Any, Set[Any]] = {}
    for k, v in pairs:
        if k in res:
            res[k].add(v)
        else:
            res[k] = set([v])
    return res


def is_adjacent(digit_pos: Tuple[int, int], symbol_pos: Tuple[int, int]) -> bool:
    (d_x, d_y), (s_x, s_y) = digit_pos, symbol_pos
    return abs(d_x - s_x) <= 1 and abs(d_y - s_y) <= 1


def find_adjacent_positions(lines: List[str]) -> Dict[int, Set[Tuple[int, int]]]:
    width = len(lines[0])
    digit_pos = [(col, row) for row, line in enumerate(lines)
                 for col, c in enumerate(line) if c.isdigit()]
    symbol_pos = [(col, row) for row, line in enumerate(lines)
                  for col, c in enumerate(line) if c == "*"]
    adj_pairs = [(d, s) for d in digit_pos for s in symbol_pos if is_adjacent(d, s)]
    return group_by_key([(s[0] + s[1] * width, d) for d, s in adj_pairs])


def find_digit_bounds(lines: List[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    char_pairs = lambda line: zip([None] + [c for c in line], [c for c in line] + [None])

    start_pos = [(col, row)
                 for row, line in enumerate(lines)
                 for col, (c1, c2) in enumerate(char_pairs(line))
                 if (c1 is None and c2.isdigit()) or (c1 is not None and c2 is not None \
                                                      and not c1.isdigit() and c2.isdigit())]

    end_pos = [(col, row)
               for row, line in enumerate(lines)
               for col, (c1, c2) in enumerate(char_pairs(line))
               if (c2 is None and c1.isdigit()) or (c1 is not None and c2 is not None \
                                                    and c1.isdigit() and not c2.isdigit())]

    return start_pos, end_pos


def main():
    lines = read_lines()
    adj_pos = find_adjacent_positions(lines)
    start_pos, end_pos = find_digit_bounds(lines)

    numbers = [int(lines[p1[1]][p1[0]:p2[0]]) for p1, p2 in zip(start_pos, end_pos)]

    numbers_adj_to_gear = group_by_key([
        (g_id, numbers[i])
        for i, (s, e) in enumerate(zip(start_pos, end_pos))
        for g_id in adj_pos for p in adj_pos[g_id]
        if p[1] == s[1] and s[0] <= p[0] < e[0]
    ])
    rel_gears = [numbers_adj_to_gear[g_id]
                 for g_id in numbers_adj_to_gear
                 if len(numbers_adj_to_gear[g_id]) == 2]
    gear_ratios = [r1 * r2 for r1, r2 in rel_gears]

    print("sum of gear ratios is", sum(gear_ratios))


if __name__ == "__main__":
    main()
