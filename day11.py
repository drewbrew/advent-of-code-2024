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
    stones = [int(i) for i in puzzle.split()]
    for turn in range(turns):
        new_stones = []
        for stone in stones:
            new_stones += replace_stone(stone)
        stones = new_stones
        if turns > 25:
            print(turn, len(stones))
    if puzzle == TEST_INPUT and turns < 10:
        print(stones)
    return len(stones)


def part_two(puzzle: str, turns: int = 75) -> int:
    stones = [int(i) for i in puzzle.split()]
    while turns > 0:
        zeroes = [index for index, val in enumerate(stones) if val == 0]
        if zeroes and turns > 4:
            last_zero = 0
            next_stones = []
            for index in zeroes:
                # if we get a 0, then we know we'll get:
                # 1
                # 2024
                # 20 24
                # 2 0 2 4
                before = take_single_turn(
                    take_single_turn(
                        take_single_turn(
                            take_single_turn(
                                stones[last_zero:index],
                            )
                        )
                    )
                )
                middle = [2, 0, 2, 4]
                next_stones += before + middle
                last_zero = index
            next_stones += stones[index:]
            turns -= 4
            print(
                f"shortcut! went from {len(stones)} to {len(next_stones)} and turn {turns + 4} to {turns}"
            )
            stones = next_stones
        if turns <= 0:
            break
        stones = take_single_turn(stones)
        turns -= 1
    return len(stones)


def inner(stones: list[int], turns_remaining: int) -> int:
    if turns_remaining == 0:
        return len(stones)
    return sum(
        inner(replace_stone(stone), turns_remaining=turns_remaining - 1)
        for stone in stones
    )


def take_single_turn(stones: list[int]) -> list[int]:
    result = []
    for stone in stones:
        result += replace_stone(stone)
    return result


def main():
    assert part_one("0 1 10 99 999", 1) == 7
    expected_results = [(1, 3), (2, 4), (3, 5), (4, 9), (5, 13), (6, 22), (25, 55312)]
    for turns, result in expected_results:
        test_result = part_one(TEST_INPUT, turns)
        assert test_result == result, (turns, result, test_result)
    puzzle = Path("day11.txt").read_text()
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
