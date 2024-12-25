"""Day 25: lock picking"""

from pathlib import Path

TEST_INPUT = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


def parse_input(puzzle: str) -> list[tuple[bool, list[int]]]:
    groups = []
    for group in puzzle.split("\n\n"):
        lines = [list(line) for line in group.splitlines()]
        is_lock = set(lines[0]) == {"#"}
        max_reaches = []
        for x in range(len(lines[0])):
            iter = range(len(lines))
            max_y = 0
            for y in iter:
                if lines[y][x] == ("#" if is_lock else "."):
                    max_y = y
                else:
                    max_reaches.append(max_y)
                    break
        groups.append((is_lock, max_reaches))
    return groups


def is_candidate(lock: list[list[int]], key: list[list[int]]) -> bool:
    return all(lock_length <= key_length for lock_length, key_length in zip(lock, key))


def part_one(puzzle: str) -> int:
    groups = parse_input(puzzle)
    locks = [group for is_lock, group in groups if is_lock]
    keys = [group for is_lock, group in groups if not is_lock]
    candidates = 0
    for lock in locks:
        candidate_keys = [key for key in keys if is_candidate(lock, key)]
        candidates += len(candidate_keys)
    return candidates


def main():
    assert (part_one_result := part_one(TEST_INPUT)) == 3, part_one_result
    puzzle = Path("day25.txt").read_text()
    print(part_one(puzzle))
    # you're on your own for part 2, sorry


if __name__ == "__main__":
    main()
