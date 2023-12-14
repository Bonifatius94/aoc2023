from typing import List, Dict, Tuple


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def navigate(instructions: str, rules: Dict[str, Tuple[str, str]]) -> int:
    steps = 0
    node = "AAA"
    while True:
        for instr in instructions:
            left, right = rules[node]
            node = left if instr == "L" else right
            steps += 1
            if node == "ZZZ":
                return steps


def main():
    lines = [l for l in read_lines() if l != ""]
    instructions = lines[0]
    orig_nodes = [l.split("=")[0].strip() for l in lines[1:]]
    dest_nodes = [[n.strip() for n in l[l.index("(")+1:l.index(")")].split(",")] for l in lines[1:]]
    rules = dict(zip(orig_nodes, dest_nodes))
    steps = navigate(instructions, rules)
    print("total navigation steps are", steps)


if __name__ == "__main__":
    main()
