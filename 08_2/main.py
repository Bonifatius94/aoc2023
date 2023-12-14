from typing import List, Dict, Tuple


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def is_start_node(node: str) -> bool:
    return node.endswith("A")


def is_end_node(node: str) -> bool:
    return node.endswith("Z")


def frequency(
        start_node: str, instructions: str,
        rules: Dict[str, Tuple[str, str]]) -> int:
    node = start_node
    steps = 0
    while True:
        for instr in instructions:
            left, right = rules[node]
            node = left if instr == "L" else right
            steps += 1
            if is_end_node(node):
                return steps


def gcf(a: int, b: int) -> int:
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a


def lcm(a: int, b: int) -> int:
    return (a / gcf(a, b)) * b


def lcm_reduce(items: List[int]) -> int:
    a = items[0]
    for b in items[1:]:
        a = lcm(a, b)
    return a


def main():
    lines = [l for l in read_lines() if l != ""]
    instructions = lines[0]
    orig_nodes = [l[:l.index("=")].strip() for l in lines[1:]]
    dest_nodes = [[n.strip() for n in l[l.index("(")+1:l.index(")")].split(",")] for l in lines[1:]]
    rules = dict(zip(orig_nodes, dest_nodes))

    # info: The input data is arranged such that each start node only reaches
    #       one specific end node. Moreover the amount of steps until reaching
    #       the end node always doubles. So the solution is to compute the LCM
    #       of the steps until the end node is reached first. This is obviously no
    #       general purpose algorithm to solve any input as specified in the task.

    start_nodes = [n for n in orig_nodes if is_start_node(n)]
    freqs = [frequency(n, instructions, rules) for n in start_nodes]
    steps = lcm_reduce(freqs)
    print("steps are", steps)


if __name__ == "__main__":
    main()
