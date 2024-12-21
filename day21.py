from collections import deque
from functools import lru_cache
from itertools import pairwise
from pathlib import Path


TEST_INPUT = """029A
980A
179A
456A
379A"""

N_PAD = {
    "0": [("2", "^"), ("A", ">")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")],
    "3": [("2", "<"), ("6", "^"), ("A", "v")],
    "4": [("1", "v"), ("5", ">"), ("7", "^")],
    "5": [("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")],
    "6": [("3", "v"), ("5", "<"), ("9", "^")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("7", "<"), ("9", ">")],
    "9": [("6", "v"), ("8", "<")],
    "A": [("0", "<"), ("3", "^")],
}
D_PAD = {
    "^": [("A", ">"), ("v", "v")],
    "<": [("v", ">")],
    "v": [("<", "<"), ("^", "^"), (">", ">")],
    ">": [("v", "<"), ("A", "^")],
    "A": [("^", "<"), (">", "v")],
}
keypads = [N_PAD, D_PAD]


def bfs(a: str, b: str, keypad: dict[str, list[tuple[str, str]]]) -> list[str]:
    q = deque([(a, [])])
    seen = {a}
    shortest = None
    result = []
    while q:
        current_button, path = q.popleft()
        if current_button == b:
            if shortest is None:
                shortest = len(path)
            if len(path) == shortest:
                result.append("".join(path + ["A"]))
            continue
        if shortest and len(path) >= shortest:
            continue
        for neighbor, direction in keypad[current_button]:
            seen.add(neighbor)
            q.append((neighbor, path + [direction]))
    return result


@lru_cache(maxsize=None)
def dfs(code: str, number_of_robots: int, keypad_index: int=0) -> int:
    keypad = keypads[keypad_index]
    result = 0
    code = "A" + code
    for a, b in pairwise(code):
        paths = bfs(a, b, keypad)
        if number_of_robots == 0:
            result += min(len(path) for path in paths)
        else:
            result += min(dfs(path, number_of_robots - 1, 1) for path in paths)
    return result


def part_one(puzzle: str) -> int:
    codes = puzzle.splitlines()
    score = 0
    for code in codes:
        result = dfs(code, 2)
        score += result * int(code[:-1])
    return score


def part_two(puzzle: str) -> int:
    return sum(dfs(code, 25) * int(code[:-1]) for code in puzzle.splitlines())

def main():
    assert (part_one_result := part_one(TEST_INPUT)) == 126384, part_one_result
    puzzle = Path('day21.txt').read_text()
    print(part_one(puzzle))
    print(part_two(puzzle))

if __name__ == '__main__':
    main()