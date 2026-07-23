from __future__ import annotations

from itertools import combinations_with_replacement

from superopt.cegis import Library, synthesize
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


def _libraries_by_cost(max_cost: int) -> list[tuple[Op, ...]]:
    combos: list[tuple[Op, ...]] = []
    for size in range(1, max_cost + 1):
        for combo in combinations_with_replacement(tuple(Op), size):
            if sum(WEIGHTS[op] for op in combo) <= max_cost:
                combos.append(combo)
    combos.sort(key=lambda combo: (sum(WEIGHTS[op] for op in combo), len(combo), combo))
    return combos


def synthesize_min_cost(
    spec: Program, *, max_cost: int, seed: int = 0
) -> Program | None:
    for ops in _libraries_by_cost(max_cost):
        library = Library(ops=ops, n_constants=2 * len(ops))
        result = synthesize(spec, library, seed=seed)
        if result is not None:
            return result
    return None
