from pathlib import Path

# to move from A to 0:
# keypad 1 needs <A
# which means keypad 2 needs to feed in those inputs
# < becomes v<<A and A becomes >>^A
# then we need to feed each of those inputs in to that robot
# v<<A becomes <vA<AA>>^A

# A to 1
# keypad 1 needs <^<A

# A to 2

FIRST_LEVEL_MOVES = {
    ("A", "0"): "<A",
    ("A", "1"): "<^<A",
    ("A", "2"): "<^A",
    ("A", "3"): "^A",
    ("A", "4"): "<^<^A",
    ("A", "5"): "<^^A",
    ("A", "6"): "^^A",
    ("A", "7"): "^^^<<A",
    ("A", "8"): "^^^<A",
    ("A", "9"): "^^^A",
    ("0", "1"): "^<A",
    ("0", "2"): "^A",
    ("0", "3"): "^>A",
    ("0", "4"): "^^<A",
    ("0", "5"): "^^A",
    ("0", "6"): "^^>A",
    ("0", "7"): "^^^<A",
    ("0", "8"): "^^^A",
    ("0", "9"): "^^^>A",
    ("1", "2"): ">A",
    ("1", "3"): ">>A",
    ("1", "4"): "^A",
    ("1", "5"): "^>A",
    ("1", "6"): "^>>A",
    ("1", "7"): "^^A",
    ("1", "8"): "^^>A",
    ("1", "9"): "^^>>A",
    ("2", "3"): ">A",
    ("2", "4"): "^<A",
    ("2", "5"): "^A",
    ("2", "6"): "^>A",
    ("2", "7"): "^^<A",
    ("2", "8"): "^^A",
    ("2", "9"): "^^>A",
    ("3", "4"): "<<^A",
    ("3", "5"): "<^A",
    ("3", "6"): "^A",
    ("3", "7"): "<<^^A",
    ("3", "8"): "<^^A",
    ("3", "9"): "^^A",
    ("4", "5"): ">A",
    ("4", "6"): ">>A",
    ("4", "7"): "^A",
    ("4", "8"): ">^A",
    ("4", "9"): ">>^A",
    ("5", "6"): ">A",
    ("5", "7"): "<^A",
    ("5", "8"): "^A",
    ("5", "9"): "^>A",
    ("6", "7"): "^<<A",
    ("6", "8"): "^<A",
    ("6", "9"): "^A",  # nice
    ("7", "8"): ">A",
    ("7", "9"): ">>A",
    ("8", "9"): ">^",
}
for (start, end), path in list(FIRST_LEVEL_MOVES.items()):
    new_path = []
    for char in path:
        match (char):
            case "A":
                next_char = "A"
            case ">":
                next_char = "<"
            case "<":
                next_char = ">"
            case "^":
                next_char = "v"
            case "v":
                next_char = "^"
            case _:
                raise ValueError(f"invalid path {path}")
        new_path.append(next_char)
    FIRST_LEVEL_MOVES[end, start] = "".join(new_path)

for button in "1234567890A":
    FIRST_LEVEL_MOVES[button, button] = "A"


# now we know what button pressses we need on the robot hitting the keypad
# next, convert those into pushes on that robot's keypad
# we'll always be starting on 'A', so this is a bit easier
# the reason for this is that we'll be working sequence by sequence, meaning
# that each time we deal with one of these, we'll either be at the start or
# have just pressed the A to push a button on the keypad
SECOND_LEVEL_MOVES = {"A": "A", "^": "<A", "<": "v<<A", "v": "v<A", ">": "vA"}

# now we have the third-level moves, i.e. what you the human press
# it's actually the same sequence again?
THIRD_LEVEL_MOVES = SECOND_LEVEL_MOVES


TEST_INPUT = """029A
980A
179A
456A
379A"""


def convert_move(start: str, end: str):
    first_level_input = FIRST_LEVEL_MOVES[start, end]
    second_level_input = "".join(SECOND_LEVEL_MOVES[char] for char in first_level_input)
    return "".join(THIRD_LEVEL_MOVES[char] for char in second_level_input)


def part_one(puzzle: str) -> int:
    keypad_robot_pos = "A"
    score = 0
    for code in puzzle.splitlines():
        assert code.endswith("A")
        my_cost = int(code[:-1])
        raw_input = []
        for digit in code:
            raw_input.append(convert_move(keypad_robot_pos, digit))
            keypad_robot_pos = digit
        score += my_cost * len("".join(raw_input))
        if puzzle == TEST_INPUT:
            print(
                f'{code} produced length {len("".join(raw_input))}, score {my_cost}, new total {score}'
            )
    return score


def main():
    assert (push := convert_move("A", "0")) == "<vA<AA>>^A", push
    assert (answer := part_one("029A")) == 68 * 29, answer
    assert (answer := part_one(TEST_INPUT) == 126384), answer
    puzzle = Path("day21.txt").read_text()
    print(part_one(puzzle))


if __name__ == "__main__":
    main()
