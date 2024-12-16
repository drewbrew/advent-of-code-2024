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


def display_grid(graph: networkx.Graph, start: tuple[int, int], end: tuple[int, int]):
    nodes = sorted(graph.nodes)
    min_x, min_y = nodes[0]
    max_x, max_y = nodes[-1]
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if (x, y) not in graph.nodes:
                print("#", end="")
            else:
                if (x, y) == start:
                    print("S", end="")
                elif (x, y) == end:
                    print("E", end="")
                else:
                    print(".", end="")
        print("")


def parse_input(puzzle: str) -> tuple[networkx.Graph, tuple[int, int], tuple[int, int]]:
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
            if char == "#":
                continue
            for dx, dy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if dx >= 0 and dy >= 0:
                    try:
                        if lines[dy][dx] != "#":
                            graph.add_edge((x, y), (dx, dy))
                    except IndexError:
                        continue
    display_grid(graph, start, end)
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


def part_one(puzzle: str) -> int:
    graph, start, end = parse_input(puzzle)
    paths = networkx.all_simple_paths(graph, start, end)
    paths_found = 0
    best_score = 10000000000000000000000000000
    for path in paths:
        paths_found += 1
        score = path_score(path)
        if score < best_score:
            print(f"found new best {score} after path number {paths_found}!", end="\r")
            best_score = score
    print("")
    return best_score


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
    print(part_one(puzzle))


if __name__ == "__main__":
    main()
