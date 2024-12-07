from itertools import product
from operator import mul, add
from pathlib import Path

TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def part_one(puzzle: str) -> int:
    total = 0
    operators = [mul, add]
    for line in puzzle.splitlines():
        result, operands = line.split(": ")
        result = int(result)
        operands = [int(i) for i in operands.split()]
        for operations in product(operators, repeat=len(operands) - 1):
            running_total = 0
            for index, operator in enumerate(operations):
                if index:
                    running_total = operator(running_total, operands[index + 1])
                else:
                    running_total = operator(operands[0], operands[1])
                if running_total > result:
                    break
            if running_total == result:
                total += result
                # don't try other options for this line
                break
    return total


def part_two(puzzle: str) -> int:
    total = 0
    operators = [mul, add, concat]
    for line in puzzle.splitlines():
        result, operands = line.split(": ")
        result = int(result)
        operands = [int(i) for i in operands.split()]
        for operations in product(operators, repeat=len(operands) - 1):
            running_total = 0
            for index, operator in enumerate(operations):
                if index:
                    running_total = operator(running_total, operands[index + 1])
                else:
                    running_total = operator(operands[0], operands[1])
                if running_total > result:
                    break
            if running_total == result:
                total += result
                # don't try other options for this line
                break
    return total


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 3749, part_one_result
    puzzle = Path("day07.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 11387, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
