from itertools import permutations
from pathlib import Path
from typing import TypedDict

import networkx

TEST_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


class CostDict(TypedDict):
    cost: int


def display_grid(graph: networkx.DiGraph, start: tuple[int, int], end: tuple[int, int]):
    nodes = sorted((x, y) for (x, y, _, _) in graph.nodes)
    (min_x, *_, max_x) = sorted(x for (x, _) in nodes)
    (min_y, *_, max_y) = sorted(y for (_, y) in nodes)
    node_set = set(nodes)
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if (x, y) not in node_set:
                print("#", end="")
            else:
                if (x, y) == start:
                    print("S", end="")
                elif (x, y) == end:
                    print("E", end="")
                else:
                    print(".", end="")
        print("")


def parse_input(
    puzzle: str,
) -> tuple[networkx.DiGraph, tuple[int, int], tuple[int, int]]:
    graph = networkx.DiGraph()
    lines = puzzle.splitlines()
    start = ()
    end = ()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)
                # don't add edges leaving this node
                continue
            if char == "#":
                continue
            # add edges representing each possible turn
            for (dx1, dy1), (dx2, dy2) in permutations(
                [(1, 0), (0, 1), (-1, 0), (0, -1)], 2
            ):
                # unlike in day 16, turns are free
                graph.add_edge((x, y, dx1, dy1), (x, y, dx2, dy2), cost=0)
            for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if x1 >= 0 and y1 >= 0:
                    dx = x1 - x
                    dy = y1 - y
                    try:
                        if lines[y1][x1] != "#":
                            graph.add_edge((x, y, dx, dy), (x1, y1, dx, dy), cost=1)
                    except IndexError:
                        continue
    return graph, start, end


def cost(
    start: tuple[int, int, int, int],
    end: tuple[int, int, int, int],
    attrs: CostDict,
) -> int:
    return attrs["cost"]


def run_race(
    graph: networkx.DiGraph, start: tuple[int, int], end: tuple[int, int]
) -> int:
    x_start, y_start = start
    x_end, y_end = end
    best_score = 10000000000000000000000000000
    ways_into_end = [(dx, dy) for (x, y, dx, dy) in graph.nodes if (x, y) == end]
    for dx, dy in ways_into_end:
        try:
            score = networkx.shortest_path_length(
                graph, (x_start, y_start, 1, 0), (x_end, y_end, dx, dy), weight=cost
            )
        except (networkx.exception.NodeNotFound, networkx.exception.NetworkXNoPath):
            pass
        else:
            if score < best_score:
                best_score = score
    return best_score


def get_candidate_walls(
    graph: networkx.DiGraph, start: tuple[int, int], end: tuple[int, int]
) -> set[tuple[int, int]]:
    x_start, y_start = start
    x_end, y_end = end
    ways_into_end = [(dx, dy) for (x, y, dx, dy) in graph.nodes if (x, y) == end]
    nodes_found = set()
    nodes_in_grid = {(x, y) for (x, y, _, _) in graph.nodes}
    (min_x, *_, max_x) = sorted(x for (x, _) in nodes_in_grid)
    (min_y, *_, max_y) = sorted(y for (_, y) in nodes_in_grid)
    for dx, dy in ways_into_end:
        try:
            paths = networkx.shortest_simple_paths(
                graph, (x_start, y_start, 1, 0), (x_end, y_end, dx, dy), weight=cost
            )
        except (networkx.exception.NodeNotFound, networkx.exception.NetworkXNoPath):
            continue
        for path in paths:
            nodes_found |= set((x, y) for (x, y, _, _) in path)
            break
    walls = set()
    for x, y in nodes_found:
        for dx, dy in (
            [(x1, 0) for x1 in range(1, 11)]
            + [(-x1, 0) for x1 in range(1, 11)]
            + [(0, y1) for y1 in range(1, 11)]
            + [(0, -y1) for y1 in range(1, 11)]
        ):
            print(x, y, dx, dy, (x + dx, y + dy) not in nodes_in_grid)
            if (
                (x1 := (x + dx), y1 := (y + dy)) not in nodes_in_grid
                and min_x <= x1 <= max_x
                and min_y <= y1 <= max_y
            ):
                walls.add((x1, y1))
    print(len(walls))
    return walls


def run_puzzle(puzzle: str, threshold: int = 100) -> tuple[int, int]:
    graph, start, end = parse_input(puzzle)
    display_grid(graph, start, end)
    base_result = run_race(graph, start, end)
    if puzzle == TEST_INPUT:
        assert base_result == 84, base_result
    lines = puzzle.splitlines()
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1
    walls = sorted(get_candidate_walls(graph=graph, start=start, end=end))
    saves_enough = 0
    for x, y in walls:
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            x1 = x + dx
            y1 = y + dy
            assert 0 <= x1 <= max_x
            assert 0 <= y1 <= max_y
            if lines[y1][x1] != "#":
                # this is a possible cheat!
                new_graph = graph.copy()
                new_graph.add_edge((x, y, dx, dy), (x1, y1, dx, dy), cost=1)
                # find all ways into the spot
                for dx2, dy2 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    x2 = x - dx
                    y2 = y - dy
                    if (x2, y2) == (x1, y1):
                        continue
                    if lines[y2][x2] != "#":
                        # here's a way in
                        new_graph.add_edge(
                            (x2, y2, dx2, dy2),
                            (x, y, dx2, dy2),
                            cost=1,
                        )
                new_score = run_race(new_graph, start, end)
                print(
                    f"removing {x, y} heading to {x1, y1} returns {new_score}, saving {base_result - new_score}"
                )
                if base_result - new_score >= threshold:
                    saves_enough += 1
    return saves_enough, 0


def main():
    part_one_result, part_two_result = run_puzzle(TEST_INPUT, 1)
    assert part_one_result == 14 + 14 + 2 + 4 + 2 + 3 + 5, part_one_result
    # assert part_two_result == 45, part_two_result
    puzzle = Path("day16.txt").read_text()
    part_one_real_result, part_two_real_result = run_puzzle(puzzle)
    print(f"{part_one_real_result}\n{part_two_real_result}")


if __name__ == "__main__":
    main()
