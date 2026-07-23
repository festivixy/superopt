from __future__ import annotations

from superopt.benchmarks.times_nine import times_nine
from superopt.cegis import Library, synthesize
from superopt.cost import (
    WEIGHTS,
    _libraries_by_cost,
    program_cost,
    synthesize_min_cost,
)
from superopt.equiv import Counterexample, Equivalent, equivalent
from superopt.fuzz import fuzz
from superopt.interp import execute
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


def _times_nine_spec(width: int) -> Program:
    return Program(
        width,
        (Instruction(Op.MUL, (InputRef(0), Const(9))),),
        ResultRef(0),
    )


def test_times_nine_spec_matches_benchmark():
    spec = _times_nine_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == times_nine(x, 8)
    assert fuzz(_times_nine_spec(32), times_nine, trials=20_000, seed=1) is None


def test_length_optimal_times_nine_is_the_multiply():
    spec = _times_nine_spec(32)
    assert execute(spec, (1,)) != execute(spec, (2,))
    identity = Program(32, (), InputRef(0))
    assert isinstance(equivalent(identity, spec), Counterexample)
    for op in Op:
        if op is Op.MUL:
            continue
        assert synthesize(spec, Library(ops=(op,), n_constants=2), seed=0) is None, op
    result = synthesize(spec, Library(ops=(Op.MUL,), n_constants=1), seed=0)
    assert result is not None
    assert len(result.instructions) == 1
    assert program_cost(result) == 3
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, times_nine, trials=20_000, seed=1) is None


def test_cost_optimal_times_nine_is_shift_add():
    spec = _times_nine_spec(32)
    assert execute(spec, (1,)) != execute(spec, (2,))
    identity = Program(32, (), InputRef(0))
    assert isinstance(equivalent(identity, spec), Counterexample)
    result = synthesize_min_cost(spec, max_cost=3, seed=0)
    assert result is not None
    assert len(result.instructions) == 2
    assert program_cost(result) == 2
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, times_nine, trials=20_000, seed=1) is None


def test_the_two_definitions_disagree_on_times_nine():
    spec = _times_nine_spec(32)
    assert execute(spec, (1,)) != execute(spec, (2,))
    identity = Program(32, (), InputRef(0))
    assert isinstance(equivalent(identity, spec), Counterexample)
    by_length = synthesize(spec, Library(ops=(Op.MUL,), n_constants=1), seed=0)
    by_cost = synthesize_min_cost(spec, max_cost=3, seed=0)
    assert by_length is not None
    assert by_cost is not None
    assert isinstance(equivalent(by_length, spec), Equivalent)
    assert isinstance(equivalent(by_cost, spec), Equivalent)
    assert fuzz(by_length, times_nine, trials=20_000, seed=1) is None
    assert fuzz(by_cost, times_nine, trials=20_000, seed=1) is None
    assert len(by_length.instructions) < len(by_cost.instructions)
    assert program_cost(by_cost) < program_cost(by_length)
