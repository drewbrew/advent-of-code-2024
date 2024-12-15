from pathlib import Path


MOVES = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

SMALL_INPUT = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

P2_SMALL_INPUT = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

TEST_INPUT = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


def parse_input(puzzle: str) -> tuple[
    dict[tuple[int, int], str],
    tuple[int, int],
    list[tuple[int, int]],
]:
    raw_grid, raw_moves = puzzle.split("\n\n")
    moves = [MOVES[char] for char in raw_moves if char in MOVES]
    grid = {}
    for y, row in enumerate(raw_grid.splitlines()):
        for x, char in enumerate(row):
            if char == "@":
                robot = (x, y)
            elif char == ".":
                continue
            else:
                grid[x, y] = char
    return grid, robot, moves


def parse_input_p2(puzzle: str) -> tuple[
    dict[tuple[int, int], str],
    tuple[int, int],
    list[tuple[int, int]],
]:
    raw_grid, raw_moves = puzzle.split("\n\n")
    moves = [MOVES[char] for char in raw_moves if char in MOVES]
    grid = {}
    for y, row in enumerate(raw_grid.splitlines()):
        for x, char in enumerate(row):
            if char == "@":
                robot = (2 * x, y)
            elif char == ".":
                continue
            else:
                if char == "#":
                    grid[2 * x, y] = "#"
                    grid[2 * x + 1, y] = "#"
                else:
                    assert char == "O"
                    grid[2 * x, y] = "["
                    grid[2 * x + 1, y] = "]"
    return grid, robot, moves


def make_move(
    grid: dict[tuple[int, int]],
    robot_position: tuple[int, int],
    next_move: tuple[int, int],
) -> tuple[int, int]:
    """Move the robot and any boxes adjacent to it in the given direction as long as it is possible"""
    x, y = robot_position
    dx, dy = next_move
    next_char = grid.get((x + dx, y + dy))
    if next_char is None:
        # yay empty space
        return x + dx, y + dy
    if next_char == "#":
        # wall, do nothing
        return x, y
    if dy == 0:
        if dx == -1:
            return move_left(grid, robot_position, False), y
        return move_right(grid, robot_position, False), y
    if dy == -1:
        return x, move_up(grid, robot_position, False)
    return x, move_down(grid, robot_position, False)


def move_left(
    grid: dict[tuple[int, int], str],
    robot: tuple[int, int],
    dry_run: bool = False,
) -> int:
    x, y = robot
    next_left = grid.get((x - 1, y))
    if next_left is None:
        # yay
        return x - 1
    if next_left == "#":
        # boo
        return x
    if next_left == "O":
        # it's a block
        pretend_move = move_left(grid, (x - 1, y), dry_run=True)
        if pretend_move == x - 1:
            # can't move
            return x
        if not dry_run:
            move_left(grid, (x - 1, y), False)
            del grid[x - 1, y]
            grid[x - 2, y] = "O"
        return x - 1
    if next_left == "]":
        # it's a big block
        # look past that block and pretend the robot is there
        pretend_move = move_left(grid, (x - 2, y), dry_run=True)
        if pretend_move == x - 2:
            # can't move
            return x
        if not dry_run:
            move_left(grid, (x - 2, y), False)
            # move the box
            del grid[x - 2, y]
            del grid[x - 1, y]
            grid[x - 3, y] = "["
            grid[x - 2, y] = "]"
        return x - 1
    raise ValueError("this should never happen")


def move_right(
    grid: dict[tuple[int, int], str],
    robot: tuple[int, int],
    dry_run: bool = False,
) -> int:
    x, y = robot
    next_right = grid.get((x + 1, y))
    if next_right is None:
        # yay
        return x + 1
    if next_right == "#":
        # boo
        return x
    if next_right == "O":
        # it's a block
        pretend_move = move_right(grid, (x + 1, y), dry_run=True)
        if pretend_move == x + 1:
            # can't move
            return x
        if not dry_run:
            move_right(grid, (x + 1, y), False)
            del grid[x + 1, y]
            grid[x + 2, y] = "O"
        return x + 1
    if next_right == "[":
        # look two more right and pretend the robot is there
        pretend_move = move_right(grid, (x + 2, y), dry_run=True)
        if pretend_move == x + 2:
            # can't move
            return x
        if not dry_run:
            move_right(grid, (x + 2, y), False)
            # move the box
            del grid[x + 2, y]
            del grid[x + 1, y]
            grid[x + 2, y] = "["
            grid[x + 3, y] = "]"
        return x + 1
    raise ValueError("this should never happen")


def move_up(
    grid: dict[tuple[int, int], str],
    robot: tuple[int, int],
    dry_run: bool = False,
) -> int:
    x, y = robot
    next_up = grid.get((x, y - 1))
    if next_up is None:
        # yay
        return y - 1
    if next_up == "#":
        # boo
        return y
    if next_up == "O":
        # it's a block
        pretend_move = move_up(grid, (x, y - 1), dry_run=True)
        if pretend_move == y - 1:
            # can't move
            return y
        if not dry_run:
            move_up(grid, (x, y - 1), False)
            del grid[x, y - 1]
            grid[x, y - 2] = "O"
        return y - 1
    if next_up == "[":
        # left edge, check both that spot and one to its right
        spaces_to_check = [(x, y - 1), (x + 1, y - 1)]
    else:
        assert next_up == "]"
        spaces_to_check = [(x - 1, y - 1), (x, y - 1)]
    if set(move_up(grid, space, True) for space in spaces_to_check) == {y - 2}:
        # yay we can move
        if not dry_run:
            for (x1, y1), char in zip(spaces_to_check, "[]"):
                move_up(grid, (x1, y1), False)
                del grid[x1, y1]
                grid[x1, y1 - 1] = char
        return y - 1
    return y


def move_down(
    grid: dict[tuple[int, int], str],
    robot: tuple[int, int],
    dry_run: bool = False,
) -> int:
    x, y = robot
    next_down = grid.get((x, y + 1))
    if next_down is None:
        # yay
        return y + 1
    if next_down == "#":
        # boo
        return y
    if next_down == "O":
        # it's a block
        pretend_move = move_down(grid, (x, y + 1), dry_run=True)
        if pretend_move == y + 1:
            # can't move
            return y

        if not dry_run:
            move_down(grid, (x, y + 1), False)
            del grid[x, y + 1]
            grid[x, y + 2] = "O"
        return y + 1
    if next_down == "[":
        # left edge, check both that spot and one to its right
        spaces_to_check = [(x, y + 1), (x + 1, y + 1)]
    else:
        assert next_down == "]"
        spaces_to_check = [(x - 1, y + 1), (x, y + 1)]
    if set(move_down(grid, space, True) for space in spaces_to_check) == {y + 2}:
        # yay we can move
        if not dry_run:
            for (x1, y1), char in zip(spaces_to_check, "[]"):
                move_down(grid, (x1, y1), False)
                del grid[x1, y1]
                grid[x1, y1 + 1] = char
        return y + 1
    return y


def gps_score(grid: dict[tuple[int, int]]) -> int:
    return sum(
        (x + 100 * y) for (x, y), char in grid.items() if char == "O" or char == "["
    )


def part_one(puzzle: str) -> int:
    grid, robot, moves = parse_input(puzzle)
    for move in moves:
        original_length = len(grid)
        robot = make_move(grid, robot, move)
        assert len(grid) == original_length, 'oh no, lost a piece'
    display_grid(grid, robot)
    return gps_score(grid)


def part_two(puzzle: str) -> int:
    grid, robot, moves = parse_input_p2(puzzle)
    for move in moves:
        robot = make_move(grid, robot, move)
    display_grid(grid, robot)
    return gps_score(grid)


def display_grid(grid: dict[tuple[int, int], str], robot: tuple[int, int]):
    min_x = min_y = 0
    max_x, max_y = max(grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) == robot:
                print("@", end="")
            else:
                print(grid.get((x, y), "."), end="")
        print("")


def main():
    small_result = part_one(puzzle=SMALL_INPUT)
    assert small_result == 2028, small_result
    test_result = part_one(puzzle=TEST_INPUT)
    assert test_result == 10092, test_result
    puzzle = Path("day15.txt").read_text()
    print(part_one(puzzle))
    small_result_p2 = part_two(puzzle=P2_SMALL_INPUT)
    assert small_result_p2 == 105 + 207 + 306, small_result_p2
    test_result_p2 = part_two(puzzle=TEST_INPUT)
    assert test_result_p2 == 9021, test_result_p2
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
