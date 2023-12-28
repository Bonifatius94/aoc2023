from typing import List, Tuple, Dict
from tqdm import tqdm
from prio_queue import PriorityQueue

Bitboard = List[List[bool]]
Map = List[List[str]]
Pos = Tuple[int, int]
Edge = Tuple[Pos, Pos, int]
Graph = List[Edge]
Distances = Dict[Pos, float]


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def is_in_bounds(p: Pos, width: int, height: int) -> bool:
    return 0 <= p[0] < width and 0 <= p[1] < height


def is_plot(p: Pos, map_data: Map) -> bool:
    return map_data[p[1]][p[0]] in [".", "S"]


def adj_pos(pos: Pos, map_data: Map) -> List[Pos]:
    (x, y), width, height = pos, len(map_data[0]), len(map_data)
    left, right, top, bot = (x-1, y), (x+1, y), (x, y-1), (x, y+1)
    for adj in [left, right, top, bot]:
        if is_in_bounds(adj, width, height) and is_plot(adj, map_data):
            yield adj


def build_graph(map_data: Map) -> Graph:
    width, height = len(map_data[0]), len(map_data)
    for x in range(width):
        for y in range(height):
            p1 = x, y
            if is_plot(p1, map_data):
                for p2 in adj_pos(p1, map_data):
                    yield (p1, p2, 1)


def dijkstra_dists(graph: Graph, start: Pos) -> Distances:
    nodes = set([p1 for p1, p2, d in graph] + [p2 for p1, p2, d in graph])
    distances = dict([(n, float("inf")) for n in nodes])
    distances[start] = 0
    visited = set()
    nodes_to_visit = PriorityQueue([(distances[n], n) for n in nodes])
    
    def neighbors(node: Pos) -> List[Tuple[Pos, int]]:
        for p1, p2, d in graph:
            if p1 == node:
                yield p2, d

    for i in tqdm(range(len(nodes))):
        _, node = nodes_to_visit.pop()
        visited.add(node)
        for neighbor, edge_dist in neighbors(node):
            if neighbor not in visited:
                new_dist = distances[node] + edge_dist
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    nodes_to_visit.update_elem(neighbor, (new_dist, neighbor))

    return distances


def main():
    lines = read_lines()
    map_data = [[c for c in line] for line in lines]
    start_pos = [(x, y) for y, line in enumerate(lines)
                 for x, c in enumerate(line) if c == "S"][0]

    graph = list(build_graph(map_data))
    print(len(graph))
    distances = dijkstra_dists(graph, start_pos)

    reachable = [p for p in distances if distances[p] % 2 == 0 and distances[p] <= 64]
    print("amount of reachable plots is", len(reachable))


if __name__ == "__main__":
    main()
