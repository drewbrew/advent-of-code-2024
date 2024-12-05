from pathlib import Path

TEST_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse_input(puzzle: str) -> tuple[set[tuple[int, int]], list[list[int]]]:
    prereqs, raw_pages = puzzle.split("\n\n")
    pages = [[int(i) for i in line.split(",")] for line in raw_pages.splitlines()]
    graph = set()
    for line in prereqs.splitlines():
        source, dest = (int(i) for i in line.split("|"))
        graph.add((source, dest))
    return graph, pages


def is_sequence_valid(graph: set[tuple[int, int]], page_list: list[int]) -> bool:
    # print(f"checking {page_list} against {graph}")
    for index, x in enumerate(page_list):
        if not index:
            continue
        for dx in range(index):
            # print(f"checking {x} against {page_list[dx]}")
            if (page_list[dx], x) not in graph:
                # print(f"no path from {x} to {page_list[dx]}")
                return False
    # print("yes valid")
    return True


def find_incorrect_index(graph: set[tuple[int, int]], page_list: list[int]) -> int:
    """Find the first index where rules are broken"""
    for index, x in enumerate(page_list):
        if not index:
            continue
        for dx in range(index):
            if (page_list[dx], x) not in graph:

                return index
    raise ValueError("no incorrect index?")


def part_one(puzzle: str) -> int:
    graph, pages = parse_input(puzzle)
    total = 0
    for page_list in pages:
        if is_sequence_valid(graph, page_list):
            total += page_list[len(page_list) // 2]
            # print(total)
    return total


def part_two(puzzle: str) -> int:
    graph, pages = parse_input(puzzle)
    total = 0
    for page_list in pages:
        while not is_sequence_valid(graph, page_list):
            first_incorrect = find_incorrect_index(graph, page_list)
            # shift it left one and try again
            last = page_list[first_incorrect - 1]
            current = page_list[first_incorrect]
            page_list[first_incorrect - 1] = current
            page_list[first_incorrect] = last
            if is_sequence_valid(graph, page_list):
                total += page_list[len(page_list) // 2]
                break

    return total


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 143, part_one_result
    puzzle = Path("day05.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 123, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
