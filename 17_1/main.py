from typing import List, Tuple, Union, Dict
from prio_queue import PriorityQueue
import numpy as np

N, S, E, W = "N", "S", "E", "W"
ALL_DIRS = [N, E, S, W]
REVERSE_DIRS = { N: S, S: N, E: W, W: E }
Direction = Union[N, E, S, W]
Pos = Tuple[int, int]
Node = Tuple[Pos, Direction]
Edge = Tuple[Node, Node, int]
Neighbors = Dict[Node, List[Tuple[Node, int]]]


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def border_dist(pos: Pos, d: Direction, height: int, width: int, max_steps: int) -> int:
    x, y = pos
    if d == N:
        return min(y, max_steps)
    elif d == S:
        return min(height - y - 1, 3)
    elif d == W:
        return min(x, max_steps)
    else: # d == E
        return min(width - x - 1, 3)


def move(pos: Pos, direction: str, length: int) -> Pos:
    if direction == N:
        return pos[0], pos[1] - length
    elif direction == S:
        return pos[0], pos[1] + length
    elif direction == W:
        return pos[0] - length, pos[1]
    else: # direction == E
        return pos[0] + length, pos[1]


def outgoing_edges(heat_loss_map: List[List[int]], node: Node) -> List[Edge]:
    ((x, y), d) = node
    width, height = len(heat_loss_map[0]), len(heat_loss_map)
    steps = border_dist((x, y), d, height, width, 3)
    weight = 0
    turn_dirs = (E, W) if d in [N, S] else (N, S)
    for l in range(1, steps+1):
        new_pos = move((x, y), d, l)
        weight += heat_loss_map[new_pos[1]][new_pos[0]]
        yield (((x, y), d), (new_pos, turn_dirs[0]), weight)
        yield (((x, y), d), (new_pos, turn_dirs[1]), weight)


def build_graph(heat_loss_map: List[List[int]]) -> List[Edge]:
    width, height = len(heat_loss_map[0]), len(heat_loss_map)
    for x in range(width):
        for y in range(height):
            for d in ALL_DIRS:
                for e in outgoing_edges(heat_loss_map, ((x, y), d)):
                    yield e


def neighbors_of_graph(graph: List[Edge]) -> Tuple[Neighbors, Neighbors]:
    incoming, outgoing = dict(), dict()
    for n1, n2, d in graph:
        if n1 in outgoing:
            outgoing[n1].append((n2, d))
        else:
            outgoing[n1] = [(n2, d)]
        if n2 in incoming:
            incoming[n2].append((n1, d))
        else:
            incoming[n2] = [(n1, d)]
    return incoming, outgoing


def optimal_path(
        heat_loss_map: List[List[int]],
        start: Node, goals: List[Node]) -> int:

    incoming, outgoing = neighbors_of_graph(build_graph(heat_loss_map))
    all_nodes = list(set(list(incoming.keys()) + list(outgoing.keys())))
    nodes_by_id = dict([(i, n) for i, n in enumerate(all_nodes)])
    ids_by_node = dict([(nodes_by_id[i], i) for i in nodes_by_id])
    distances = np.full((len(nodes_by_id)), np.inf)

    start_id = ids_by_node[start]
    visited = set()
    nodes_to_visit = PriorityQueue([(d, i) for i, d in enumerate(distances)])
    nodes_to_visit.update_elem(start_id, (0, start_id))
    distances[start_id] = 0

    while nodes_to_visit:
        prio, node_id = nodes_to_visit.pop()
        visited.add(node_id)
        print(f"\rvisiting {node_id} with prio {prio}, progress: {len(visited)} / {len(outgoing)}         ", end="")
        adj_nodes = [(ids_by_node[n2], d) for n2, d in outgoing[nodes_by_id[node_id]]] \
            if nodes_by_id[node_id] in outgoing else []
        for adj_node, distance in adj_nodes:
            if adj_node not in visited:
                new_dist = distances[node_id] + distance
                if new_dist < distances[adj_node]:
                    distances[adj_node] = new_dist
                    nodes_to_visit.update_elem(adj_node, (new_dist, adj_node))
    print()

    return int(min([distances[ids_by_node[n]] for n in goals]))


def main():
    lines = read_lines()
    lines = [l for l in lines if l != ""]
    heat_loss_map = [[int(c) for c in line] for line in lines]

    width, height = len(heat_loss_map[0]), len(heat_loss_map)
    goals = [((width-1, height-1), d) for d in ALL_DIRS]
    heat_loss = optimal_path(heat_loss_map, ((0, 0), E), goals)
    print("minimal heat loss is", heat_loss)


if __name__ == "__main__":
    main()
