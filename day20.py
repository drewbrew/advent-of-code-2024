from pathlib import Path

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


def display_grid(graph: networkx.Graph, start: tuple[int, int], end: tuple[int, int]):
    nodes = sorted(graph.nodes)
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
) -> tuple[networkx.Graph, tuple[int, int], tuple[int, int]]:
    graph = networkx.Graph()
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
            for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if x1 >= 0 and y1 >= 0:
                    try:
                        if lines[y1][x1] != "#":
                            graph.add_edge((x, y), (x1, y1))
                    except IndexError:
                        continue
    return graph, start, end


def run_race(
    graph: networkx.Graph, start: tuple[int, int], end: tuple[int, int]
) -> int:
    x_start, y_start = start
    x_end, y_end = end
    score = networkx.shortest_path_length(graph, (x_start, y_start), (x_end, y_end))

    return score


def manhattan_circle(x: int, y: int, radius: int):
    s = set()
    for i in range(radius + 1):
        x1, y1 = (i, radius - i)
        s |= {(x1, y1), (-x1, -y1), (x1, -y1), (-x1, y1)}
    for d in s:
        yield tuple(x + y for x, y in zip((x, y), d))


def cheat_within_circle(
    position: tuple[int, int],
    threshold: int,
    path: dict[tuple[int, int], int],
    start_index: int,
    radius: int,
) -> bool:
    try:
        return path[position] - start_index - radius >= threshold
    except KeyError:
        return False


def part_one(puzzle: str, threshold: int = 100) -> int:
    graph, start, end = parse_input(puzzle)
    display_grid(graph, start, end)
    base_result = run_race(graph, start, end)
    if puzzle == TEST_INPUT:
        assert base_result == 84, base_result
    raw_path = networkx.shortest_path(graph, start, end)
    path = {point: index for index, point in enumerate(raw_path)}
    saves_enough = 0
    radius = 2
    for index, (x, y) in enumerate(raw_path):
        for position in manhattan_circle(x, y, radius):
            if cheat_within_circle(position, threshold, path, index, radius):
                saves_enough += 1
    return saves_enough


def part_two(puzzle: str, threshold: int = 100) -> int:
    graph, start, end = parse_input(puzzle)
    base_result = run_race(graph, start, end)
    if puzzle == TEST_INPUT:
        assert base_result == 84, base_result
    raw_path = networkx.shortest_path(graph, start, end)
    path = {point: index for index, point in enumerate(raw_path)}
    saves_enough = 0
    max_radius = 20
    for index, (x, y) in enumerate(raw_path):
        for radius in range(2, max_radius + 1):
            for position in manhattan_circle(x, y, radius):
                if cheat_within_circle(position, threshold, path, index, radius):
                    saves_enough += 1
    return saves_enough


def main():
    part_one_result = part_one(TEST_INPUT, 1)
    # check that we get all results from the test input
    assert part_one_result == 14 + 14 + 2 + 4 + 2 + 3 + 5, part_one_result
    # assert part_two_result == 45, part_two_result
    puzzle = Path("day20.txt").read_text()
    part_one_real_result = part_one(puzzle)
    print(f"{part_one_real_result}")
    part_two_result = part_two(TEST_INPUT, 50)
    assert (
        part_two_result
        == 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
    ), (
        part_two_result,
        32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3,
    )
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
