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


def run_puzzle(puzzle: str) -> tuple[int, int]:
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
    p1_total = 0
    p2_total = 0
    for x, y in zeroes:
        for x1, y1 in nines:
            paths = list(networkx.all_simple_paths(grid, (x, y), (x1, y1)))
            # if puzzle == TEST_INPUT:
            #     print(f"found {len(paths)} path(s) from {x}, {y} to {x1}, {y1}")
            p2_total += len(paths)
            p1_total += bool(paths)
    return p1_total, p2_total


def main():
    part_one_result, part_two_result = run_puzzle(TEST_INPUT)
    assert part_one_result == 36, part_one_result
    assert part_two_result == 81, part_one_result
    puzzle = Path("day10.txt").read_text()
    print("\n".join(str(i) for i in run_puzzle(puzzle)))


if __name__ == "__main__":
    main()
