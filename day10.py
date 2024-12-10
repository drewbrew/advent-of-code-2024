from pathlib import Path

import networkx

TEST_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def part_one(puzzle: str) -> int:
    grid = networkx.DiGraph()
    zeroes: set[tuple[int, int]] = set()
    nines: set[tuple[int, int]] = set()
    ints = [[int(char) for char in line.strip()] for line in puzzle.splitlines()]
    for y, line in enumerate(ints):
        for x, value in enumerate(line):
            if value == 0:
                zeroes.add((x, y))
            elif value == 9:
                nines.add((x, y))
            for x1, y1 in [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                if x1 < 0 or y1 < 0:
                    continue
                try:
                    if ints[y1][x1] - value == 1:
                        grid.add_edge((x, y), (x1, y1))
                except IndexError:
                    pass
    total = 0
    for x, y in zeroes:
        for x1, y1 in nines:
            try:
                networkx.shortest_path(grid, (x, y), (x1, y1))
            except networkx.exception.NetworkXNoPath:
                pass
            else:
                # if puzzle == TEST_INPUT:
                #     print(f"found a path from {x}, {y} to {x1}, {y1}")
                total += 1
    return total


def part_two(puzzle: str) -> int:
    grid = networkx.DiGraph()
    zeroes: set[tuple[int, int]] = set()
    nines: set[tuple[int, int]] = set()
    ints = [[int(char) for char in line.strip()] for line in puzzle.splitlines()]
    for y, line in enumerate(ints):
        for x, value in enumerate(line):
            if value == 0:
                zeroes.add((x, y))
            elif value == 9:
                nines.add((x, y))
            for x1, y1 in [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                if x1 < 0 or y1 < 0:
                    continue
                try:
                    if ints[y1][x1] - value == 1:
                        grid.add_edge((x, y), (x1, y1))
                except IndexError:
                    pass
    total = 0
    for x, y in zeroes:
        for x1, y1 in nines:
            paths = list(networkx.all_simple_paths(grid, (x, y), (x1, y1)))
            # if puzzle == TEST_INPUT:
            #     print(f"found {len(paths)} path(s) from {x}, {y} to {x1}, {y1}")
            total += len(paths)
    return total


def main():
    test_result = part_one(TEST_INPUT)
    assert test_result == 36, test_result
    puzzle = Path("day10.txt").read_text()
    print(part_one(puzzle))
    test_result = part_two(TEST_INPUT)
    assert test_result == 81, test_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
