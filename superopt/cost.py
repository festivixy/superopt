from __future__ import annotations

from superopt.ir import Op, Program

WEIGHTS: dict[Op, int] = {
    Op.ADD: 1,
    Op.SUB: 1,
    Op.MUL: 3,
    Op.AND: 1,
    Op.OR: 1,
    Op.XOR: 1,
    Op.NOT: 1,
    Op.NEG: 1,
    Op.SHL: 1,
    Op.LSHR: 1,
    Op.ASHR: 1,
}


def program_cost(program: Program) -> int:
    return sum(WEIGHTS[instruction.op] for instruction in program.instructions)
