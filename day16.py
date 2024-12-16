from itertools import permutations
from pathlib import Path

import networkx

TEST_INPUT = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


def display_grid(graph: networkx.DiGraph, start: tuple[int, int], end: tuple[int, int]):
    nodes = sorted((x, y) for (x, y, _, _) in graph.nodes)
    min_x, min_y = nodes[0]
    max_x, max_y = nodes[-1]
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
                graph.add_edge((x, y, dx1, dy1), (x, y, dx2, dy2), cost=1000)
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


def path_score(path: list[tuple[int, int]], bearing: tuple[int, int] = (1, 0)):
    score = 0
    for space, next_space in zip(path[:-1], path[1:]):
        x1, y1 = space
        x2, y2 = next_space
        dx = x2 - x1
        dy = y2 - y1
        if (dx, dy) != bearing:
            # had to turn
            score += 1000
            bearing = (dx, dy)
        score += 1
    return score


def cost(start: tuple[int, int, int, int], end: tuple[int, int, int, int], attrs):
    return attrs["cost"]


def part_one(puzzle: str) -> int:
    graph, start, end = parse_input(puzzle)
    display_grid(graph, start, end)
    x_start, y_start = start
    x_end, y_end = end
    best_score = 10000000000000000000000000000
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        try:
            score = networkx.shortest_path_length(
                graph, (x_start, y_start, 1, 0), (x_end, y_end, dx, dy), weight=cost
            )
        except (networkx.exception.NodeNotFound, networkx.exception.NetworkXNoPath):
            print(f"no way to enter the end using direction {dx}, {dy}")
        else:
            if score < best_score:
                print("new winner", score)
            best_score = score
    return best_score


def part_two(puzzle: str, part_one_result: int) -> int:
    graph, start, end = parse_input(puzzle)
    x_start, y_start = start
    x_end, y_end = end
    best_direction = None
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        try:
            score = networkx.shortest_path_length(
                graph, (x_start, y_start, 1, 0), (x_end, y_end, dx, dy), weight=cost
            )
        except (networkx.exception.NodeNotFound, networkx.exception.NetworkXNoPath):
            print(f"no way to enter the end using direction {dx}, {dy}")
        else:
            if score == part_one_result:
                best_direction = dx, dy
    nodes = set()
    dx, dy = best_direction
    for path in networkx.all_shortest_paths(
        graph, (x_start, y_start, 1, 0), (x_end, y_end, dx, dy), weight=cost
    ):
        nodes |= {(x, y) for (x, y, _, _) in path}
    return len(nodes)


def main():
    assert (
        path_score(
            [
                (1, 13),
                (1, 12),
                (1, 11),
                (1, 10),
                (1, 9),
                (2, 9),
                (3, 9),
                (3, 8),
                (3, 7),
                (4, 7),
                (5, 7),
                (6, 7),
                (7, 7),
                (8, 7),
                (9, 7),
                (10, 7),
                (11, 7),
                (11, 8),
                (11, 9),
                (11, 10),
                (11, 11),
                (11, 12),
                (11, 13),
                (12, 13),
                (13, 13),
                (13, 12),
                (13, 11),
                (13, 10),
                (13, 9),
                (13, 8),
                (13, 7),
                (13, 6),
                (13, 5),
                (13, 4),
                (13, 3),
                (13, 2),
                (13, 1),
            ]
        )
        == 7036
    )
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 7036, part_one_result
    puzzle = Path("day16.txt").read_text()
    part_one_real_result = part_one(puzzle)
    print(part_one_real_result)
    part_two_result = part_two(TEST_INPUT, part_one_result)
    assert part_two_result == 45, part_two_result
    print(part_two(puzzle, part_one_real_result))


if __name__ == "__main__":
    main()
