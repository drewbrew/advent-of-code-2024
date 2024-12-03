import re
from pathlib import Path

MUL_REGEX = re.compile(r"mul\((\d\d?\d?),(\d\d?\d?)\)")


TEST_INPUT = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
PART_TWO_TEST_INPUT = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)


def part1(puzzle: str) -> int:
    matches = MUL_REGEX.findall(puzzle)
    total = sum(int(a) * int(b) for a, b in matches)
    return total


def part2(puzzle: str) -> int:
    offsets = []
    start = 0
    stop = puzzle.index("don't()")
    offsets.append((start, stop))
    while True:
        try:
            start = puzzle.index("do()", stop, len(puzzle))
        except ValueError:
            # no more starts, so we are done here
            break
        try:
            stop = puzzle.index("don't()", start, len(puzzle))
        except ValueError:
            # reached the end while enabled
            offsets.append((start, len(puzzle)))
            break
        offsets.append((start, stop))
    stripped = "".join(puzzle[start: stop] for start, stop in offsets)
    return part1(stripped)


def main():
    test_result = part1(puzzle=TEST_INPUT)
    assert test_result == 161, test_result
    real_puzzle = Path("day03.txt").read_text()
    print(part1(real_puzzle))
    test_result = part2(PART_TWO_TEST_INPUT)
    assert test_result == 48, test_result
    print(part2(real_puzzle))


if __name__ == "__main__":
    main()
