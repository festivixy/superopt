from __future__ import annotations

import pytest

from superopt.benchmarks.clear_lowest_bit import clear_lowest_bit
from superopt.benchmarks.isolate_lowest_zero import isolate_lowest_zero
from superopt.benchmarks.rotl5 import rotl5
from superopt.benchmarks.smear_lowest_bit import smear_lowest_bit
from superopt.benchmarks.turn_off_trailing_ones import turn_off_trailing_ones
from superopt.cegis import Library, synthesize
from superopt.equiv import Equivalent, equivalent
from superopt.fuzz import fuzz
from superopt.interp import execute
from superopt.ir import Const, InputRef, Instruction, Op, Program, ResultRef
from tests.support import assert_floor


def _clear_lowest_bit_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.SUB, (InputRef(0), Const(1))),
            Instruction(Op.AND, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


def test_clear_lowest_bit_spec_matches_benchmark():
    spec = _clear_lowest_bit_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == clear_lowest_bit(x, 8)
    spec32 = _clear_lowest_bit_spec(32)
    assert fuzz(spec32, clear_lowest_bit, trials=20_000, seed=1) is None


def test_clear_lowest_bit_synthesizes():
    spec = _clear_lowest_bit_spec(32)
    result = synthesize(spec, Library(ops=(Op.SUB, Op.AND), n_constants=2), seed=0)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, clear_lowest_bit, trials=20_000, seed=1) is None


def test_clear_lowest_bit_proven_at_2():
    assert_floor(_clear_lowest_bit_spec(32), 1, 1, ((1,), (3,)))


def _smear_lowest_bit_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.SUB, (InputRef(0), Const(1))),
            Instruction(Op.OR, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


def test_smear_lowest_bit_spec_matches_benchmark():
    spec = _smear_lowest_bit_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == smear_lowest_bit(x, 8)
    spec32 = _smear_lowest_bit_spec(32)
    assert fuzz(spec32, smear_lowest_bit, trials=20_000, seed=1) is None


def test_smear_lowest_bit_synthesizes():
    spec = _smear_lowest_bit_spec(32)
    result = synthesize(spec, Library(ops=(Op.SUB, Op.OR), n_constants=2), seed=0)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, smear_lowest_bit, trials=20_000, seed=1) is None


def test_smear_lowest_bit_proven_at_2():
    assert_floor(_smear_lowest_bit_spec(32), 1, 1, ((1,), (2,)))


def _turn_off_trailing_ones_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.ADD, (InputRef(0), Const(1))),
            Instruction(Op.AND, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


def test_turn_off_trailing_ones_spec_matches_benchmark():
    spec = _turn_off_trailing_ones_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == turn_off_trailing_ones(x, 8)
    spec32 = _turn_off_trailing_ones_spec(32)
    assert fuzz(spec32, turn_off_trailing_ones, trials=20_000, seed=1) is None


def test_turn_off_trailing_ones_synthesizes():
    spec = _turn_off_trailing_ones_spec(32)
    result = synthesize(spec, Library(ops=(Op.ADD, Op.AND), n_constants=2), seed=0)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, turn_off_trailing_ones, trials=20_000, seed=1) is None


def test_turn_off_trailing_ones_proven_at_2():
    assert_floor(_turn_off_trailing_ones_spec(32), 1, 1, ((1,), (2,)))


def _isolate_lowest_zero_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.NOT, (InputRef(0),)),
            Instruction(Op.ADD, (InputRef(0), Const(1))),
            Instruction(Op.AND, (ResultRef(0), ResultRef(1))),
        ),
        ResultRef(2),
    )


def test_isolate_lowest_zero_spec_matches_benchmark():
    spec = _isolate_lowest_zero_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == isolate_lowest_zero(x, 8)
    spec32 = _isolate_lowest_zero_spec(32)
    assert fuzz(spec32, isolate_lowest_zero, trials=20_000, seed=1) is None


def test_isolate_lowest_zero_synthesizes():
    spec = _isolate_lowest_zero_spec(32)
    result = synthesize(
        spec, Library(ops=(Op.NOT, Op.ADD, Op.AND), n_constants=1), seed=0
    )
    assert result is not None
    assert len(result.instructions) == 3
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, isolate_lowest_zero, trials=20_000, seed=1) is None


@pytest.mark.slow
def test_isolate_lowest_zero_proven_at_3():
    assert_floor(_isolate_lowest_zero_spec(32), 2, 1, ((0,), (1,)))


def _rotl5_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.SHL, (InputRef(0), Const(5))),
            Instruction(Op.LSHR, (InputRef(0), Const(width - 5))),
            Instruction(Op.OR, (ResultRef(0), ResultRef(1))),
        ),
        ResultRef(2),
    )


def test_rotl5_spec_matches_benchmark():
    spec = _rotl5_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == rotl5(x, 8)
    spec32 = _rotl5_spec(32)
    assert fuzz(spec32, rotl5, trials=20_000, seed=1) is None


def test_rotl5_synthesizes():
    spec = _rotl5_spec(32)
    result = synthesize(
        spec, Library(ops=(Op.SHL, Op.LSHR, Op.OR), n_constants=2), seed=0
    )
    assert result is not None
    assert len(result.instructions) == 3
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, rotl5, trials=20_000, seed=1) is None


@pytest.mark.slow
def test_rotl5_proven_at_3():
    assert_floor(_rotl5_spec(32), 2, 1, ((1,), (2,)))
