from pathlib import Path

import networkx

TEST_INPUT = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def part_one(puzzle: str, turns: int = 1024) -> int:
    max_x = max_y = 6 if puzzle == TEST_INPUT else 70
    grid = networkx.Graph()
    corrupted_blocks = set()
    for line in puzzle.splitlines()[:turns]:
        x, y = line.split(",")
        corrupted_blocks.add((int(x), int(y)))

    if puzzle == TEST_INPUT:
        assert (4, 2) in corrupted_blocks, corrupted_blocks
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in corrupted_blocks:
                continue
            for x1, y1 in [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                if (
                    0 <= x1 <= max_x
                    and 0 <= y1 <= max_y
                    and (x1, y1) not in corrupted_blocks
                ):
                    grid.add_edge((x, y), (x1, y1))
    return networkx.shortest_path_length(grid, (0, 0), (max_x, max_y))


def part_two(puzzle: str) -> str:
    lines = puzzle.splitlines()
    start = 0
    end = len(lines)

    while True:
        # do a rough bisecting search
        turns = (end - start) // 2 + start
        try:
            part_one(puzzle, turns=turns)
        except networkx.exception.NetworkXNoPath:
            # didn't make it. that means the end of the search region is here
            end = turns
            if end == start:
                raise ValueError("This should never happen")
        else:
            # did make it. that means start of the search region is here
            start = turns
            if start + 1 == end:
                return lines[turns]


def main():
    part_one_result = part_one(TEST_INPUT, 12)
    assert part_one_result == 22, part_one_result
    puzzle = Path("day18.txt").read_text()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == "6,1", part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
