from pathlib import Path

TEST_INPUT = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


class CPU:
    def __init__(self, puzzle: str):
        registers, instructions = puzzle.split("\n\n")
        self.program = [
            int(i) for i in instructions.replace("Program: ", "").split(",")
        ]
        self.instruction_pointer = 0
        self.registers = {"A": 0, "B": 0, "C": 0}
        for line in registers.splitlines():
            reg_def, value = line.split(": ")
            reg_name = reg_def[-1]
            assert reg_name in self.registers, reg_name
            self.registers[reg_name] = int(value)
        self.outputs: list[int] = []

    def convert_operand(self, operand: int) -> int:
        if operand in range(4):
            return operand
        if operand == 4:
            return self.registers["A"]
        if operand == 5:
            return self.registers["B"]
        if operand == 6:
            return self.registers["C"]
        raise ValueError(f"Unknown operand {operand}")

    def adv(self, operand: int) -> None:
        self.registers["A"] = self.registers["A"] // (
            2 ** self.convert_operand(operand=operand)
        )

    def bxl(self, operand: int) -> None:
        self.registers["B"] = self.registers["B"] ^ operand

    def bst(self, operand: int) -> None:
        self.registers["B"] = self.convert_operand(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.registers["A"] == 0:
            return
        self.instruction_pointer = operand - 2

    def bxc(self, operand: int) -> None:
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def out(self, operand: int) -> None:
        self.outputs.append(self.convert_operand(operand) % 8)

    def bdv(self, operand: int) -> None:
        self.registers["B"] = self.registers["A"] // (
            2 ** self.convert_operand(operand=operand)
        )

    def cdv(self, operand: int) -> None:
        self.registers["C"] = self.registers["A"] // (
            2 ** self.convert_operand(operand=operand)
        )

    def run(self) -> list[int]:
        while True:
            try:
                instruction = self.program[self.instruction_pointer]
                operand = self.program[self.instruction_pointer + 1]
            except IndexError:
                return self.outputs
            match instruction:
                case 0:
                    self.adv(operand)
                case 1:
                    self.bxl(operand)
                case 2:
                    self.bst(operand)
                case 3:
                    self.jnz(operand)
                case 4:
                    self.bxc(operand)
                case 5:
                    self.out(operand)
                case 6:
                    self.bdv(operand)
                case 7:
                    self.cdv(operand)
            self.instruction_pointer += 2

    def disassemble(self) -> list[str]:
        output = []
        for instruction_pointer in range(0, len(self.program), 2):
            instruction = self.program[instruction_pointer]
            operand = self.program[instruction_pointer + 1]
            match instruction, operand:
                case (0, x):
                    # adv
                    if x not in range(4):
                        x = chr(ord('A') + (x - 4))
                    output.append(f'A = A // (2 ** {x})')
                case (1, x):
                    # bxl
                    output.append(f'B = B ^ {x}')
                case (2, x):
                    # bst
                    if x not in range(4):
                        x = chr(ord('A') + (x - 4))
                    output.append(f'B = {x} % 8')
                case (3, x):
                    # jnz
                    output.append(f'if A != 0: ip = {x}')
                case (4, _):
                    # bxc
                    output.append('B ^= C')
                case (5, x):
                    # out
                    output.append(f'self.outputs.append({x} % 8)')
                case (6, x):
                    # bdv
                    if x not in range(4):
                        x = chr(ord('A') + (x - 4))
                    output.append(f'B = A // (2 ** {x})')
                case (7, x):
                    # cdv
                    if x not in range(4):
                        x = chr(ord('A') + (x - 4))
                    output.append(f'C = A // (2 ** {x})')
                case _:
                    raise ValueError(f"Unknown function {instruction}")
        return output


def part_one(puzzle: str) -> str:
    cpu = CPU(puzzle=puzzle)
    print("---")
    # HOW I SOLVED THIS:
    # disassemble the instructions to make it somewhat easier to read
    # looking at the loop, only A gets carried over from round to round
    # and the last 3 bits determine the output for that round
    print("\n".join(cpu.disassemble()))
    return cpu.run()


def part_two(puzzle: str) -> int:
    cpu = CPU(puzzle)
    candidates = []
    output_length = len(cpu.program)
    # work from the right backwards, starting with a value of 0
    values_to_check = [(1, 0)]
    # I would use a heapq but adding to the loop is good enough for this case
    for depth, initial_a in values_to_check:
        for a in range(initial_a, initial_a + 8):  # vary the lower 3 bits
            # reset the CPU
            cpu.instruction_pointer = 0
            cpu.outputs = []
            cpu.registers["A"] = a
            # and run it. Do the last N digits match?
            if cpu.run() == cpu.program[-depth:]:
                # yay we found the right last digit(s)
                # multiply a by 8 and see if that gives us the next digit from the right
                values_to_check += [(depth + 1, a * 8)]
                if depth == output_length:
                    # yay we got the whole program out
                    candidates.append(a)
    return min(candidates)


def main():
    # If register C contains 9, the program 2,6 would set register B to 1.
    setup = """Register A: 0
Register B: 0
Register C: 9

Program: 2,6"""
    cpu = CPU(setup)
    cpu.run()
    assert cpu.registers == {"A": 0, "B": 1, "C": 9}, cpu.registers
    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2
    setup = """Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4"""
    cpu = CPU(setup)
    outputs = cpu.run()
    assert outputs == [0, 1, 2], outputs
    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    setup = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    cpu = CPU(setup)
    outputs = cpu.run()
    assert cpu.registers["A"] == 0, cpu.registers
    assert outputs == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0], outputs
    # If register B contains 29, the program 1,7 would set register B to 26.
    setup = """Register A: 0
Register B: 29
Register C: 0

Program: 1,7"""
    cpu = CPU(setup)
    cpu.run()
    assert cpu.registers == {"A": 0, "B": 26, "C": 0}, cpu.registers
    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    setup = """Register A: 0
Register B: 2024
Register C: 43690

Program: 4,0"""
    cpu = CPU(setup)
    cpu.run()
    assert cpu.registers == {"A": 0, "B": 44354, "C": 43690}, cpu.registers

    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0], part_one_result
    puzzle = Path("day17.txt").read_text()
    print(",".join(str(i) for i in part_one(puzzle)))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
