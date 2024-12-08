from pathlib import Path

TEST_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def display_grid_with_antinodes(
    grid: dict[str, list[tuple[int, int]]], antinodes: set[tuple[int, int]]
):

    max_y = max(y for _, y in antinodes)
    max_x = max(x for x, _ in antinodes)
    base_displays: dict[tuple[int, int], str] = {}
    for char, nodes in grid.items():
        max_x = max(max_x, max(x for x, _ in nodes))
        max_y = max(max_y, max(y for _, y in nodes))
        for node in nodes:
            base_displays[node] = char
    for y in range(max_y + 1):
        print("")
        for x in range(max_x + 1):
            print(
                base_displays.get((x, y), "#" if (x, y) in antinodes else "."),
                end="",
            )
    print("")


def parse_input(puzzle: str) -> tuple[int, int, dict[str, list[tuple[int, int]]]]:
    grid: dict[str, list[tuple[int, int]]] = {}
    max_y = 0
    max_x = 0
    for y, line in enumerate(puzzle.splitlines()):
        if y > max_y:
            max_y = y
        for x, char in enumerate(line):
            if x > max_x:
                max_x = x
            if char not in "#.":
                try:
                    grid[char].append((x, y))
                except KeyError:
                    grid[char] = [(x, y)]
    return max_x, max_y, grid


def part_one(puzzle: str) -> int:
    max_x, max_y, grid = parse_input(puzzle)
    ok_x = range(max_x + 1)
    ok_y = range(max_y + 1)
    antinodes: set[tuple[int, int]] = set()
    for char, nodes in grid.items():
        for index, (x, y) in enumerate(nodes):
            other_nodes = nodes[index + 1 :]
            for xa, ya in other_nodes:
                dx = xa - x
                dy = ya - y
                xb = x + dx * 2
                yb = y + dy * 2
                xc = xa - dx * 2
                yc = ya - dy * 2
                if xb in ok_x and yb in ok_y:
                    if puzzle == TEST_INPUT:
                        print(
                            f"created antinode for {char} from ({x}, {y}) and ({xa}, {ya}) at {xb}, {yb}"
                        )
                    antinodes.add((xb, yb))
                if xc in ok_x and yc in ok_y:
                    if puzzle == TEST_INPUT:
                        print(
                            f"created antinode for {char} from ({x}, {y}) and ({xa}, {ya}) at {xc}, {yc}"
                        )
                    antinodes.add((xc, yc))
    if puzzle == TEST_INPUT:
        print(antinodes)
        display_grid_with_antinodes(grid, antinodes)
    return len(antinodes)


def part_two(puzzle: str) -> int:
    max_x, max_y, grid = parse_input(puzzle)
    ok_x = range(max_x + 1)
    ok_y = range(max_y + 1)
    antinodes: set[tuple[int, int]] = set()
    for char, nodes in grid.items():
        for index, (x, y) in enumerate(nodes):
            other_nodes = nodes[index + 1 :]
            for xa, ya in other_nodes:
                dx = xa - x
                dy = ya - y
                xb = x + dx
                yb = y + dy
                xc = xa - dx
                yc = ya - dy
                while True:
                    if xb in ok_x and yb in ok_y:
                        if puzzle == TEST_INPUT:
                            print(
                                f"created antinode for {char} from ({x}, {y}) and ({xa}, {ya}) at {xb}, {yb}"
                            )
                        antinodes.add((xb, yb))
                    if xc in ok_x and yc in ok_y:
                        if puzzle == TEST_INPUT:
                            print(
                                f"created antinode for {char} from ({x}, {y}) and ({xa}, {ya}) at {xc}, {yc}"
                            )
                        antinodes.add((xc, yc))
                    xb += dx
                    yb += dy
                    xc -= dx
                    yc -= dy
                    if (
                        xb not in ok_x
                        and yb not in ok_y
                        and xc not in ok_x
                        and yc not in ok_y
                    ):
                        break
    if puzzle == TEST_INPUT:
        print(antinodes)
        display_grid_with_antinodes(grid, antinodes)
    return len(antinodes)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 14, part_one_result
    puzzle = Path("day08.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 34, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
