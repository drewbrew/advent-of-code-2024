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
            func_table = {
                0: self.adv,
                1: self.bxl,
                2: self.bst,
                3: self.jnz,
                4: self.bxc,
                5: self.out,
                6: self.bdv,
                7: self.cdv,
            }
            func_table[instruction](operand)
            self.instruction_pointer += 2


def part_one(puzzle: str) -> str:
    cpu = CPU(puzzle=puzzle)
    return cpu.run()


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


if __name__ == "__main__":
    main()
