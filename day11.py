from collections import Counter, defaultdict
from pathlib import Path

TEST_INPUT = """125 17"""


def replace_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    if (length := len(str(stone))) % 2 == 0:

        left = str(stone)[: length // 2]
        right = str(stone)[length // 2 :]
        return [int(left), int(right)]
    return [stone * 2024]


def part_one(puzzle: str, turns: int = 25) -> int:
    stones = Counter(int(i) for i in puzzle.split())
    stone_map: dict[str, list[int]] = {}
    for turn in range(turns):
        new_stones = defaultdict(int)
        for stone, count in stones.items():
            try:
                replacements = stone_map[stone]
            except KeyError:
                stone_map[stone] = replace_stone(stone)
                replacements = stone_map[stone]
            for replacement in replacements:
                new_stones[replacement] += count
        stones = new_stones
        if turns > 25:
            print(turn, sum(stones.values()))
    if puzzle == TEST_INPUT and turns < 10:
        print(stones)
    return sum(stones.values())


def main():
    assert part_one("0 1 10 99 999", 1) == 7
    expected_results = [(1, 3), (2, 4), (3, 5), (4, 9), (5, 13), (6, 22), (25, 55312)]
    for turns, result in expected_results:
        test_result = part_one(TEST_INPUT, turns)
        assert test_result == result, (turns, result, test_result)
    puzzle = Path("day11.txt").read_text()
    print(part_one(puzzle))
    print(part_one(puzzle, 75))


if __name__ == "__main__":
    main()
