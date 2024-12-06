from pathlib import Path

TEST_IHPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


# returns grid, position, bearing, max_x, min_y
def parse_input(puzzle: str) -> tuple[set[complex], complex, complex, int, int]:
    grid = set()
    max_x = 0
    max_y = 0
    for y, line in enumerate(puzzle.splitlines()):
        if y > max_y:
            max_y = y
        for x, char in enumerate(line):
            if x > max_x:
                max_x = x
            if char == "#":
                grid.add(x - 1j * y)
            elif char == "^":
                # up
                bearing = 1j
                position = x - 1j * y
            elif char == ">":
                bearing = 1j
                position = x - 1j * y
            elif char == "<":
                bearing = -1 + 0j
                position = x - 1j * y
            elif char == "v":
                bearing = -1j
                position = x - 1j * y
    return grid, position, bearing, max_x, -max_y


def turn_right(bearing: complex) -> complex:
    return bearing * -1j


def part_one(
    puzzle: str, added_obstacle: complex | None = None
) -> tuple[int, set[complex]]:
    grid, position, bearing, max_x, min_y = parse_input(puzzle)
    if added_obstacle:
        grid.add(added_obstacle)
    min_x = max_y = 0
    ok_x = range(min_x, max_x + 1)
    ok_y = range(min_y, max_y + 1)
    positions_seen: set[tuple[complex, complex]] = set()
    while int(position.real) in ok_x and int(position.imag) in ok_y:
        # is there something in front of us?
        while position + bearing in grid:
            # note in part 2 there can be corners, so we need to check multiple turns in a row
            bearing = turn_right(bearing)
        if (position, bearing) in positions_seen:
            raise InfiniteLoopError()
        positions_seen.add((position, bearing))
        position += bearing
    locations = set(pos for pos, _ in positions_seen)
    return len(locations), locations


def part_two(puzzle: str, places_visited_in_part_one: set[complex]) -> int:
    _, position, _, _, _ = parse_input(puzzle)
    candidates = set()
    for candidate in places_visited_in_part_one:
        if candidate == position:
            continue
        try:
            part_one(puzzle, candidate)
        except InfiniteLoopError:
            candidates.add(candidate)
    # if puzzle == TEST_IHPUT:
    #     print(candidates)
    return len(candidates)


def main():
    assert turn_right(1j) == 1 + 0j
    assert turn_right(1 + 0j) == -1j
    assert turn_right(-1j) == -1 + 0j
    assert turn_right(-1 + 0j) == 1j
    part_one_test_result, paths_seen_test = part_one(TEST_IHPUT)
    assert part_one_test_result == 41, part_one_test_result
    real_input = Path("day06.txt").read_text()
    part_one_answer, paths_seen = part_one(real_input)
    print(part_one_answer)
    part_two_test_result = part_two(TEST_IHPUT, paths_seen_test)
    assert part_two_test_result == 6, part_two_test_result
    print(part_two(real_input, paths_seen))


class InfiniteLoopError(Exception):
    pass


if __name__ == "__main__":
    main()
