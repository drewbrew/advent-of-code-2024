from itertools import combinations
from pathlib import Path

import networkx


TEST_INPUT = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def parse_input(puzzle: str) -> networkx.Graph:
    graph = networkx.Graph()
    for line in puzzle.splitlines():
        a, b = line.split("-")
        graph.add_edge(a, b)
    return graph


def part_one(puzzle: str) -> int:
    graph = parse_input(puzzle)
    candidates = set()
    for computer in graph.nodes:
        if computer.startswith("t"):
            neighbors = list(networkx.all_neighbors(graph, computer))
            for a, b in combinations(neighbors, 2):
                if graph.has_edge(a, b):
                    if puzzle == TEST_INPUT:
                        print(f"{computer}-{a}-{b}")
                    candidates.add(tuple(sorted([a, b, computer])))
    return len(candidates)


def part_two(puzzle: str) -> str:
    graph = parse_input(puzzle)
    best_result = 0
    best_connection = []
    nodes: list[str] = list(graph.nodes)
    for a, b in combinations(nodes, 2):
        if not graph.has_edge(a, b):
            continue
        common = list(networkx.common_neighbors(graph, a, b))
        if (neighbor_count := len(common)) > best_result - 2:
            nodes = [a, b] + common
            for u, v in combinations(nodes, 2):
                if not graph.has_edge(u, v):
                    break
            else:
                best_result = neighbor_count + 2  # need to count the original
                best_connection = sorted([a, b] + common)
                if puzzle == TEST_INPUT:
                    print(f"new leader: {best_connection}")
    return ",".join(best_connection)


def main():
    assert (part_one_result := part_one(TEST_INPUT)) == 7, part_one_result
    puzzle = Path("day23.txt").read_text()
    print(part_one(puzzle))
    assert (part_two_result := part_two(TEST_INPUT)) == "co,de,ka,ta", part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
