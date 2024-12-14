from pathlib import Path

from PIL import Image

TEST_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

TEST_WIDTH = 11
TEST_HEIGHT = 7

REAL_WIDTH = 101
REAL_HEIGHT = 103


def parse_input(puzzle: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    result = []
    for line in puzzle.splitlines():
        p_info, v_info = line.split()
        position = tuple(int(i) for i in p_info[2:].split(","))
        velocity = tuple(int(i) for i in v_info[2:].split(","))
        result.append((position, velocity))
    return result


def move_robot(
    position: tuple[int, int],
    bearing: tuple[int, int],
    width: int,
    height: int,
    turns: int = 100,
) -> tuple[int, int]:
    x, y = position
    dx, dy = bearing
    final_x = (x + (dx * turns)) % width
    final_y = (y + (dy * turns)) % height
    return final_x, final_y


def part_one(puzzle: str, turns: int = 100) -> int:
    robots = parse_input(puzzle)
    width = TEST_WIDTH if puzzle == TEST_INPUT else REAL_WIDTH
    height = TEST_HEIGHT if puzzle == TEST_INPUT else REAL_HEIGHT
    positions_by_quadrant = {"nw": 0, "sw": 0, "ne": 0, "se": 0}
    mid_x = width // 2
    mid_y = height // 2
    for robot in robots:
        position, bearing = robot
        final_x, final_y = move_robot(
            position=position,
            bearing=bearing,
            width=width,
            height=height,
            turns=turns,
        )
        if final_x == mid_x or final_y == mid_y:
            if puzzle == TEST_INPUT:
                print(f"robot starting at {position} ends in a midpoint")
        elif final_x > mid_x:
            # in the eastern half
            if final_y > mid_y:
                positions_by_quadrant["se"] += 1
            else:
                positions_by_quadrant["ne"] += 1
        else:
            # western half
            if final_y > mid_y:
                positions_by_quadrant["sw"] += 1
            else:
                positions_by_quadrant["nw"] += 1
    return (
        positions_by_quadrant["ne"]
        * positions_by_quadrant["sw"]
        * positions_by_quadrant["nw"]
        * positions_by_quadrant["se"]
    )


def part_two(puzzle: str, turns: int = 10000) -> None:
    robots = parse_input(puzzle)
    # use 1-based because we're rendering the state at the start of the next turn
    for turn in range(1, turns + 1):
        filename = f"day14_{turn:0>8}.png"
        # new transparent image
        image = Image.new("RGBA", (REAL_WIDTH, REAL_HEIGHT), (255, 255, 255, 0))
        new_robots = []
        pixels_to_draw: set[tuple[int, int]] = set()
        for position, bearing in robots:
            new_position = move_robot(position, bearing, REAL_WIDTH, REAL_HEIGHT, 1)
            pixels_to_draw.add(new_position)
            new_robots.append((new_position, bearing))
        for pixel in pixels_to_draw:
            image.putpixel(pixel, (0, 128, 0, 255))  # merry xmas
        image.save(filename)
        print(f"saved to {filename}", end="\r")
        robots = new_robots


def main():
    assert move_robot((2, 4), (2, -3), TEST_WIDTH, TEST_HEIGHT, turns=1) == (
        4,
        1,
    ), move_robot((2, 4), (2, -3), TEST_WIDTH, TEST_HEIGHT, 1)
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 12, part_one_result
    puzzle = Path("day14.txt").read_text()
    print(part_one(puzzle))
    part_two(puzzle)
    print("")


if __name__ == "__main__":
    main()
