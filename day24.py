from pathlib import Path

SMALL_INPUT = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

TEST_INPUT = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


def part_one(puzzle: str) -> int:
    presets, conditionals = puzzle.split("\n\n")
    nodes: dict[str, int] = {}
    for line in presets.splitlines():
        node, value = line.split(": ")
        nodes[node] = int(value)

    nodes_set_this_round = True
    while nodes_set_this_round:
        nodes_set_this_round = False
        for line in conditionals.splitlines():
            expr = line.split()
            node1 = expr[0]
            node2 = expr[2]
            dest = expr[4]

            if (
                dest not in nodes
                and (a := nodes.get(node1)) is not None
                and (b := nodes.get(node2)) is not None
            ):
                # we can go ahead and resolve it
                match (expr[1]):
                    case "AND":
                        nodes[dest] = a & b
                    case "OR":
                        nodes[dest] = a | b
                    case "XOR":
                        nodes[dest] = a ^ b
                    case _:
                        raise ValueError(f"Unknown expr {line}")
                nodes_set_this_round = True
    z_nodes = sorted(
        ((key, val) for (key, val) in nodes.items() if key.startswith("z")),
        reverse=True,
    )
    # print(z_nodes)
    result = int("".join(str(val) for (_, val) in z_nodes), 2)
    return result


def part_two(puzzle: str) -> str:
    operations = []
    highest_z = "z00"
    presets, conditionals = puzzle.split("\n\n")
    nodes: dict[str, int] = {}
    for line in presets.splitlines():
        node, value = line.split(": ")
        nodes[node] = int(value)

    for line in conditionals.splitlines():
        node1, op, node2, _, dest = line.split()
        operations.append((node1, op, node2, dest))
        if dest[0] == "z" and int(dest[1:]) > int(highest_z[1:]):
            highest_z = dest

    wrong = set()
    for node1, op, node2, dest in operations:
        if dest[0] == "z" and op != "XOR" and dest != highest_z:
            # z nodes must always be xors!
            wrong.add(dest)
        if (
            op == "XOR"
            and dest[0] not in ["x", "y", "z"]
            and node1[0] not in ["x", "y", "z"]
            and node2[0] not in ["x", "y", "z"]
        ):
            # no XORs between intermediate nodes
            wrong.add(dest)
        if op == "AND" and "x00" not in [node1, node2]:
            # we have an and gate that's not using the LSB of the input.
            # does its output get fed into something
            # other than an OR?
            for sub_node1, subop, sub_node2, _ in operations:
                if (dest == sub_node1 or dest == sub_node2) and subop != "OR":
                    wrong.add(dest)
        if op == "XOR":
            # we have an xor gate. does its output get fed into an OR?
            for sub_node1, subop, sub_node2, _ in operations:
                if (dest == sub_node1 or dest == sub_node2) and subop == "OR":
                    wrong.add(dest)

    return ",".join(sorted(wrong))


def main():
    assert (part_one_result := part_one(SMALL_INPUT)) == 4, part_one_result
    assert (part_one_result := part_one(TEST_INPUT)) == 2024, part_one_result
    puzzle = Path("day24.txt").read_text()
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
