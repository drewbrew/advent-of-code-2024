from collections import deque, defaultdict
from pathlib import Path


EXAMPLE_INPUT = 123

EXAMPLE_RESULTS = [
    15887950,
    16495136,
    527345,
    704524,
    1553684,
    12683156,
    11100544,
    12249484,
    7753432,
    5908254,
]

TEST_INPUT = """1
10
100
2024"""

PART_TWO_TEST_INPUT = """1
2
3
2024"""


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(value: int) -> int:
    return value % 16777216


def calculate_price(secret: int) -> int:
    value = secret * 64
    secret = prune(mix(secret, value))
    value = secret // 32
    secret = prune(mix(secret, value))
    value = secret * 2048
    secret = prune(mix(secret, value))
    return secret


def part_one(puzzle: str, turns: int = 2000) -> int:
    result = 0
    for line in puzzle.splitlines():
        secret = int(line)
        for _ in range(turns):
            secret = calculate_price(secret)
        result += secret
    return result


def part_two(puzzle: str) -> int:
    result: dict[tuple[int, int, int, int], int] = defaultdict(int)
    for line in puzzle.splitlines():
        consecutives: dict[tuple[int, int], int] = {}
        secret = int(line)
        ones = int(line) % 10
        my_changes = deque(maxlen=4)
        for turn in range(2000):
            next_secret = calculate_price(secret)
            next_ones = next_secret % 10
            my_changes.append(next_ones - ones)
            if turn > 3 and tuple(my_changes) not in consecutives:
                consecutives[tuple(my_changes)] = next_ones
            secret = next_secret
            ones = next_ones
        for changes, bananas in consecutives.items():
            result[changes] += bananas
    return max(result.values())


def main():
    test_pairs = [EXAMPLE_INPUT] + EXAMPLE_RESULTS
    for secret, result in zip(test_pairs[:-1], test_pairs[1:]):
        assert (calculated := calculate_price(secret)) == result, (
            secret,
            result,
            calculated,
        )
    assert (part_one_result := part_one(TEST_INPUT)) == 37327623, part_one_result
    puzzle = Path("day22.txt").read_text()
    print(part_one(puzzle=puzzle))
    assert (part_two_result := part_two(PART_TWO_TEST_INPUT)) == 23, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()
