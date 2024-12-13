from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np

A_COST = 3
B_COST = 1
MAX_PRESSES = 100


TEST_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


@dataclass
class ClawGame:
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int

    @classmethod
    def from_str(cls, puzzle: str, is_part_two: bool = False) -> Self:
        lines = puzzle.splitlines()
        kwargs = {}
        for line in lines:
            if line.startswith("Button "):
                button_info, coords = line.split(": ")
                button = button_info[-1].casefold()
                x_movement, y_movement = coords.split(", ")
                if x_movement[1] == "+":
                    kwargs[f"{button}_x"] = int(x_movement[2:])
                else:
                    kwargs[f"{button}_x"] = int(x_movement[1:])
                if y_movement[1] == "+":
                    kwargs[f"{button}_y"] = int(y_movement[2:])
                else:
                    kwargs[f"{button}_y"] = int(y_movement[1:])
            elif line.startswith("Prize:"):
                prize_info = line.split(": ")[1]
                x_prize, y_prize = prize_info.split(", ")
                kwargs["prize_x"] = int(x_prize[2:]) + (10000000000000 * is_part_two)
                kwargs["prize_y"] = int(y_prize[2:]) + (10000000000000 * is_part_two)
            else:
                raise ValueError(f"unknown line {line}")
        assert set(kwargs) == {"a_x", "b_x", "a_y", "b_y", "prize_x", "prize_y"}, kwargs
        return cls(**kwargs)


def parse_input(puzzle: str, is_part_two: bool = False) -> list[ClawGame]:
    return [ClawGame.from_str(group, is_part_two) for group in puzzle.split("\n\n")]


def part_one(puzzle: str, is_part_two: bool = False) -> int:
    total = 0
    for game in parse_input(puzzle, is_part_two=is_part_two):
        a = np.array([[game.a_x, game.b_x], [game.a_y, game.b_y]]).astype(int)
        b = np.array([game.prize_x, game.prize_y]).astype(int)
        s = np.linalg.solve(a, b)

        if np.all(np.abs(s - np.round(s)) < 1e-3):
            if not is_part_two:
                assert s[0] <= MAX_PRESSES and s[1] <= MAX_PRESSES
            total += int(s[0] * A_COST + s[1] * B_COST)
    return total


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 480, part_one_result
    puzzle = Path("day13.txt").read_text()
    print(part_one(puzzle))
    print(part_one(puzzle, True))


if __name__ == "__main__":
    main()
