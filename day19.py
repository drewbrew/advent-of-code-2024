from functools import lru_cache
from pathlib import Path

TEST_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse_input(puzzle: str) -> tuple[frozenset[str], list[str]]:
    towel_line, combo_liness = puzzle.split("\n\n")
    combos = combo_liness.splitlines()
    towels = frozenset(towel_line.split(", "))
    return towels, combos


@lru_cache(maxsize=None)
def is_possible(
    pattern: str,
    towels: frozenset[str],
) -> bool:
    if pattern in towels:
        return True
    for towel in towels:
        if len(towel) > len(pattern):
            continue
        if pattern.startswith(towel):
            if is_possible(pattern[len(towel) :], towels=towels):
                return True
    return False


@lru_cache(maxsize=None)
def possible_combos(pattern: str, towels: frozenset[str]) -> int:
    options = 0
    if not pattern:
        # at the end. Return 1 since we've made it here
        return 1
    for towel in towels:
        if len(towel) > len(pattern):
            continue
        if pattern.startswith(towel):
            if result := possible_combos(pattern[len(towel) :], towels=towels):
                options += result
    return options


def part_one(puzzle: str) -> int:
    towels, combos = parse_input(puzzle)
    return sum(is_possible(combination, towels=towels) for combination in combos)


def part_two(puzzle: str) -> int:
    towels, combos = parse_input(puzzle)
    return sum(possible_combos(combination, towels=towels) for combination in combos)


def main():
    test_towels = frozenset(TEST_INPUT.split("\n")[0].split(", "))
    assert is_possible("brwrr", test_towels)
    assert is_possible("bggr", test_towels)
    assert is_possible("gbbr", test_towels)
    assert is_possible("rrgbr", test_towels)
    assert not is_possible("ubwu", test_towels)
    assert is_possible("bwurrg", test_towels)
    assert is_possible("brgr", test_towels)
    assert not is_possible("bbrgwb", test_towels)
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 6, part_one_result
    puzzle = Path("day19.txt").read_text()
    print(part_one(puzzle))
    assert (result := possible_combos("gbbr", test_towels)) == 4, result
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 16, part_two_result

    print(part_two(puzzle))


if __name__ == "__main__":
    main()
