from __future__ import annotations

from superopt.cost import WEIGHTS, _libraries_by_cost, program_cost
from superopt.ir import Const, InputRef, Instruction, Op, Program, ResultRef


def test_every_op_has_a_weight():
    assert set(WEIGHTS) == set(Op)
    assert all(weight >= 1 for weight in WEIGHTS.values())
    assert WEIGHTS[Op.MUL] == 3


def test_program_cost_sums_weights_and_consts_are_free():
    mul9 = Program(32, (Instruction(Op.MUL, (InputRef(0), Const(9))),), ResultRef(0))
    shift_add = Program(
        32,
        (
            Instruction(Op.SHL, (InputRef(0), Const(3))),
            Instruction(Op.ADD, (ResultRef(0), InputRef(0))),
        ),
        ResultRef(1),
    )
    assert program_cost(mul9) == 3
    assert program_cost(shift_add) == 2
    assert program_cost(Program(32, (), InputRef(0))) == 0


def test_libraries_by_cost_ordering_and_bounds():
    libs = _libraries_by_cost(3)
    weights = [sum(WEIGHTS[op] for op in combo) for combo in libs]
    assert weights == sorted(weights)
    assert all(weight <= 3 for weight in weights)
    assert len(set(libs)) == len(libs)
    assert (Op.MUL,) in libs
