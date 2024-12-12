from math import sqrt
from collections import Counter, defaultdict
from pathlib import Path

import networkx

TEST_INPUT = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def price(points: list[tuple[int, int]]) -> float:
    per = 0
    point_set = set(points)
    for x, y in point_set:
        point_perimeter = 4
        for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if neighbor in point_set:
                point_perimeter -= 1
        per += point_perimeter
    return per * len(points)


def part_one(puzzle: str) -> int:
    grid = puzzle.splitlines()
    graph = networkx.Graph()
    polygons: list[tuple[str, list[tuple[int, int]]]] = []
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            current_char = char
            for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if x1 >= 0 and y1 >= 0:
                    try:
                        char2 = grid[y1][x1]
                    except IndexError:
                        continue
                    if char2 != current_char:
                        continue
                    graph.add_edge((x1, y1), (x, y))
    max_y = len(grid)
    max_x = len(grid[0])
    nodes_seen = set()
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in nodes_seen:
                continue
            nodes_seen.add((x, y))
            try:
                polygon = networkx.descendants(graph, (x, y)) | {(x, y)}
            except networkx.exception.NetworkXError as exc:
                if "is not in the graph" not in str(exc):
                    raise
                polygon = {(x, y)}
            nodes_seen |= polygon
            polygons.append((grid[y][x], sorted(polygon)))
    prices = defaultdict(int)
    for char, polygon in polygons:
        prices[char] += price(polygon)
    total = sum(prices.values())
    return total


def sides(points: set[tuple[int, int]], x: int, y: int) -> int:
    result = 0
    # Outer corners
    result += (x - 1, y) not in points and (x, y - 1) not in points
    result += (x + 1, y) not in points and (x, y - 1) not in points
    result += (x - 1, y) not in points and (x, y + 1) not in points
    result += (x + 1, y) not in points and (x, y + 1) not in points
    # Inner corners
    result += (
        (x - 1, y) in points and (x, y - 1) in points and (x - 1, y - 1) not in points
    )
    result += (
        (x + 1, y) in points and (x, y - 1) in points and (x + 1, y - 1) not in points
    )
    result += (
        (x - 1, y) in points and (x, y + 1) in points and (x - 1, y + 1) not in points
    )
    result += (
        (x + 1, y) in points and (x, y + 1) in points and (x + 1, y + 1) not in points
    )
    return result


def part_two(puzzle: str) -> int:
    grid = puzzle.splitlines()
    graph = networkx.Graph()
    polygons: list[tuple[str, list[tuple[int, int]]]] = []
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            current_char = char
            for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if x1 >= 0 and y1 >= 0:
                    try:
                        char2 = grid[y1][x1]
                    except IndexError:
                        continue
                    if char2 != current_char:
                        continue
                    graph.add_edge((x1, y1), (x, y))
    max_y = len(grid)
    max_x = len(grid[0])
    nodes_seen = set()
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in nodes_seen:
                continue
            nodes_seen.add((x, y))
            try:
                polygon = networkx.descendants(graph, (x, y)) | {(x, y)}
            except networkx.exception.NetworkXError as exc:
                if "is not in the graph" not in str(exc):
                    raise
                polygon = {(x, y)}
            nodes_seen |= polygon
            polygons.append((grid[y][x], sorted(polygon)))
    prices = defaultdict(int)
    for char, polygon in polygons:
        p_sides = sum(sides(polygon, x, y) for x, y in polygon) * len(polygon)
        prices[char] += p_sides
    total = sum(prices.values())
    return total


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 1930, part_one_result
    puzzle = Path("day12.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 1206, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()
