from collections import Counter
from pathlib import Path

TEST_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse_input(puzzle: str) -> tuple[list[int], list[int]]:
    list0 = []
    list1 = []
    for line in puzzle.splitlines():
        entries = line.split()
        list0.append(int(entries[0]))
        list1.append(int(entries[1]))
    return list0, list1


def part1(puzzle: str) -> int:
    list0, list1 = parse_input(puzzle)
    list0.sort()
    list1.sort()
    return sum(abs(a - b) for a, b in zip(list0, list1))


def part2(puzzle: str) -> int:
    list0, list1 = parse_input(puzzle)
    counts = Counter(list1)
    return sum(a * counts.get(a, 0) for a in list0)


def main():
    test_result = part1(TEST_INPUT)
    assert test_result == 11, test_result
    real_puzzle = Path("day01.txt").read_text()
    print(part1(real_puzzle))
    test_result = part2(TEST_INPUT)
    assert test_result == 31, test_result
    print(part2(real_puzzle))


if __name__ == "__main__":
    main()
