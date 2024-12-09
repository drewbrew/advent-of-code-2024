"""Day 9: remember defrag?"""

from pathlib import Path
from typing import Sequence

TEST_INPUT = """2333133121414131402"""


def checksum(disk_layout: Sequence[int | None]) -> int:
    return sum(
        value * index for (index, value) in enumerate(disk_layout) if value is not None
    )


def rearrange_individual_blocks(disk_layout: Sequence[int | None]) -> list[int | None]:
    result = [None for _ in range(len(disk_layout))]
    pull_from = len(disk_layout) - 1
    indexes_seen = set()
    for index, item in enumerate(disk_layout):
        if index in indexes_seen:
            continue
        indexes_seen.add(index)
        if item is not None:
            result[index] = item
        else:
            while disk_layout[pull_from] is None:
                indexes_seen.add(pull_from)
                pull_from -= 1
                if pull_from <= index:
                    break
            if pull_from <= index:
                return checksum(result)
            result[index] = disk_layout[pull_from]
            disk_layout[pull_from] = None
            indexes_seen.add(pull_from)
    return checksum(result)


def lowest_contiguous_free_space_index(
    interim_layout: Sequence[int | None], blocks_needed: int, stop_at: int
) -> int | None:
    for index, value in enumerate(interim_layout):
        if index >= stop_at:
            return None
        if value is not None:
            continue
        if interim_layout[index : index + blocks_needed] == [None] * blocks_needed:
            return index
    return None


def rearrange_whole_files(disk_layout: Sequence[int | None]) -> list[int | None]:
    max_id = max(i for i in disk_layout if i is not None)
    for file_id in range(max_id, 0, -1):
        start = disk_layout.index(file_id)
        index = start
        blocks_needed = 0
        try:
            while disk_layout[index] == file_id:
                blocks_needed += 1
                index += 1
        except IndexError:
            if file_id != max_id:
                # this is expected to hit for the very first file
                raise
        if (
            new_start := lowest_contiguous_free_space_index(
                disk_layout,
                blocks_needed,
                stop_at=start,
            )
        ) is not None and new_start < start:
            for offset in range(blocks_needed):
                dest_index = new_start + offset
                source_index = start + offset
                assert disk_layout[dest_index] is None, (
                    file_id,
                    blocks_needed,
                    new_start,
                    dest_index,
                    source_index,
                    disk_layout[dest_index],
                    disk_layout,
                )
                assert disk_layout[source_index] == file_id
                disk_layout[dest_index] = file_id
                disk_layout[source_index] = None
    return checksum(disk_layout)


def part_one(puzzle: str) -> int:
    disk_layout = []
    for index, char in enumerate(puzzle):
        value = int(char)
        is_free_space = bool(index % 2)
        file_number = index // 2
        if is_free_space:
            disk_layout += [None] * value
        else:
            disk_layout += [file_number] * value
    return rearrange_individual_blocks(disk_layout)


def part_two(puzzle: str) -> int:
    disk_layout = []
    for index, char in enumerate(puzzle):
        value = int(char)
        is_free_space = bool(index % 2)
        file_number = index // 2
        if is_free_space:
            disk_layout += [None] * value
        else:
            disk_layout += [file_number] * value
    return rearrange_whole_files(disk_layout)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 1928, part_one_result
    puzzle = Path("day09.txt").read_text().replace("\n", "")
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 2858, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()
