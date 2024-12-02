from pathlib import Path

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def parse_input(puzzle: str) -> list[list[int]]:
    return [[int(char) for char in line.split()] for line in puzzle.splitlines()]


def is_safe(level: list[int]) -> bool:
    if level not in (sorted(level), sorted(level, reverse=True)):
        return False
    for reading, last in zip(level[1:], level[:-1]):
        if abs(last - reading) not in range(1, 4):
            return False
    return True


def part_one(puzzle: str) -> int:
    readings = parse_input(puzzle=puzzle)
    return sum(is_safe(level) for level in readings)


def part_two(puzzle: str) -> int:
    readings = parse_input(puzzle=puzzle)
    total = 0
    for level in readings:
        if is_safe(level):
            total += 1
            continue
        for index in range(0, len(level) + 1):
            if is_safe(level[:index] + level[index + 1 :]):
                total += 1
                break

    return total


def main():
    test_result = part_one(TEST_INPUT)
    assert test_result == 2, test_result
    real_input = Path("day02.txt").read_text()
    print(part_one(real_input))
    part_two_test = part_two(TEST_INPUT)
    assert part_two_test == 4, part_two_test
    print(part_two(real_input))


if __name__ == "__main__":
    main()
