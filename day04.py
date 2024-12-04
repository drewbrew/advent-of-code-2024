from pathlib import Path

TEST_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def find_horizontal(lines: list[str]) -> int:
    return sum(
        line.count('XMAS') + line.count('SAMX') for line in lines
    )


def find_vertical(lines: list[str]) -> int:
    transposed = ["".join(line[y] for line in lines) for y in range(len(lines[0]))]

    return find_horizontal(transposed)


def find_diagonal(lines: list[str]) -> int:
    min_x = 0
    min_y = 0
    max_x = len(lines[0])
    max_y = len(lines)
    ok_x = range(min_x, max_x)
    ok_y = range(min_y, max_y)
    total = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "X":
                for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    if (
                        (d2x := (x + dx)) in ok_x
                        and (d2y := y + dy) in ok_y
                        and lines[d2y][d2x] == "M"
                        and (d3x := (d2x + dx)) in ok_x
                        and (d3y := d2y + dy) in ok_y
                        and lines[d3y][d3x] == "A"
                        and (d4x := d3x + dx) in ok_x
                        and (d4y := d3y + dy) in ok_y
                        and lines[d4y][d4x] == "S"
                    ):
                        total += 1
    return total


def part_one(puzzle: str) -> int:
    grid = puzzle.splitlines()
    return find_horizontal(grid) + find_vertical(grid) + find_diagonal(grid)


def part_two(puzzle: str) -> int:
    lines = puzzle.splitlines()
    min_x = 0
    min_y = 0
    max_x = len(lines[0])
    max_y = len(lines)
    ok_x = range(min_x, max_x)
    ok_y = range(min_y, max_y)
    total = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "A":
                xw = x - 1
                xe = x + 1
                yn = y - 1
                ys = y + 1
                if (
                    xw in ok_x
                    and xe in ok_x
                    and yn in ok_x
                    and ys in ok_y
                    and "".join(
                        (
                            lines[yn][xw],
                            lines[yn][xe],
                            lines[ys][xw],
                            lines[ys][xe],
                        )
                    )
                    in {"MMSS", "SSMM", "MSMS", "SMSM"}
                ):
                    total += 1

    return total


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 18, part_one_result
    puzzle = Path("day04.txt").read_text()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 9, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
