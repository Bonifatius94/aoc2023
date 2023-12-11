from typing import List, Tuple


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def is_adjacent(digit_pos: Tuple[int, int], symbol_pos: Tuple[int, int]) -> bool:
    (d_x, d_y), (s_x, s_y) = digit_pos, symbol_pos
    return abs(d_x - s_x) <= 1 and abs(d_y - s_y) <= 1


def find_adjacent_positions(lines: List[str]) -> List[Tuple[int, int]]:
    digit_pos = [(col, row) for row, line in enumerate(lines)
                 for col, c in enumerate(line) if c.isdigit()]
    symbol_pos = [(col, row) for row, line in enumerate(lines)
                  for col, c in enumerate(line) if not c.isdigit() and c != "."]
    return [d for d in digit_pos if any([is_adjacent(d, s) for s in symbol_pos])]


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
    digit_ids = [i for i, (s, e) in enumerate(zip(start_pos, end_pos)) for p in adj_pos
                 if p[1] == s[1] and s[0] <= p[0] < e[0]]
    adj_numbers = [numbers[i] for i in set(list(digit_ids))]

    print("sum of part numbers is", sum(adj_numbers))


if __name__ == "__main__":
    main()
