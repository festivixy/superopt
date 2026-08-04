from __future__ import annotations

import pytest

from superopt.benchmarks.abs_val import absval
from superopt.benchmarks.clear_lowest_bit import clear_lowest_bit
from superopt.benchmarks.isolate_rmb import isolate_rmb
from superopt.benchmarks.smear_lowest_bit import smear_lowest_bit
from superopt.benchmarks.turn_off_trailing_ones import turn_off_trailing_ones
from superopt.cegis import Library, synthesize
from superopt.equiv import Equivalent, equivalent
from superopt.fuzz import fuzz
from superopt.interp import execute
from superopt.ir import Const, InputRef, Instruction, Op, Program, ResultRef, ShiftMode
from tests.support import assert_floor


def _absval_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.ASHR, (InputRef(0), Const(width - 1))),
            Instruction(Op.NOT, (ResultRef(0),)),
            Instruction(Op.AND, (InputRef(0), ResultRef(1))),
            Instruction(Op.NEG, (InputRef(0),)),
            Instruction(Op.AND, (ResultRef(3), ResultRef(0))),
            Instruction(Op.OR, (ResultRef(2), ResultRef(4))),
        ),
        ResultRef(5),
    )


def _clear_lowest_bit_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.SUB, (InputRef(0), Const(1))),
            Instruction(Op.AND, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


def _smear_lowest_bit_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.SUB, (InputRef(0), Const(1))),
            Instruction(Op.OR, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


def _turn_off_trailing_ones_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.ADD, (InputRef(0), Const(1))),
            Instruction(Op.AND, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


def _isolate_rmb_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.NEG, (InputRef(0),)),
            Instruction(Op.AND, (InputRef(0), ResultRef(0))),
        ),
        ResultRef(1),
    )


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


def test_absval_spec_is_mode_independent():
    spec = _absval_spec(32)
    for x in (0, 1, 5, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF):
        assert execute(spec, (x,)) == execute(spec, (x,), shift_mode=ShiftMode.MASK)


def test_constant_free_absval_exists_only_under_saturate():
    spec = _absval_spec(32)
    library = Library(ops=(Op.ASHR, Op.XOR, Op.SUB), n_constants=0)
    saturate = synthesize(spec, library, seed=0)
    assert saturate is not None
    assert isinstance(equivalent(saturate, spec), Equivalent)
    assert fuzz(saturate, absval, trials=20_000, seed=1) is None
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK) is None


def test_masked_absval_needs_the_constant():
    spec = _absval_spec(32)
    library = Library(ops=(Op.ASHR, Op.XOR, Op.SUB), n_constants=1)
    result = synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK)
    assert result is not None
    assert len(result.instructions) == 3
    assert isinstance(equivalent(result, spec, shift_mode=ShiftMode.MASK), Equivalent)
    assert (
        fuzz(result, absval, trials=20_000, seed=1, shift_mode=ShiftMode.MASK) is None
    )


def test_clear_lowest_bit_floor_holds_under_mask():
    assert_floor(
        _clear_lowest_bit_spec(32), 1, 1, ((1,), (3,)), shift_mode=ShiftMode.MASK
    )


def test_smear_lowest_bit_floor_holds_under_mask():
    assert_floor(
        _smear_lowest_bit_spec(32), 1, 1, ((1,), (2,)), shift_mode=ShiftMode.MASK
    )


def test_turn_off_trailing_ones_floor_holds_under_mask():
    assert_floor(
        _turn_off_trailing_ones_spec(32),
        1,
        1,
        ((1,), (2,)),
        shift_mode=ShiftMode.MASK,
    )


def test_isolate_rmb_floor_holds_under_mask():
    assert_floor(_isolate_rmb_spec(32), 1, 1, ((1,), (2,)), shift_mode=ShiftMode.MASK)


@pytest.mark.slow
def test_absval_floor_holds_under_mask():
    assert_floor(_absval_spec(32), 2, 1, ((0,), (1,)), shift_mode=ShiftMode.MASK)


def test_clear_lowest_bit_synthesizes_under_mask():
    spec = _clear_lowest_bit_spec(32)
    library = Library(ops=(Op.SUB, Op.AND), n_constants=1)
    result = synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec, shift_mode=ShiftMode.MASK), Equivalent)
    assert (
        fuzz(
            result,
            clear_lowest_bit,
            trials=20_000,
            seed=1,
            shift_mode=ShiftMode.MASK,
        )
        is None
    )


def test_smear_lowest_bit_synthesizes_under_mask():
    spec = _smear_lowest_bit_spec(32)
    library = Library(ops=(Op.SUB, Op.OR), n_constants=1)
    result = synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec, shift_mode=ShiftMode.MASK), Equivalent)
    assert (
        fuzz(
            result,
            smear_lowest_bit,
            trials=20_000,
            seed=1,
            shift_mode=ShiftMode.MASK,
        )
        is None
    )


def test_turn_off_trailing_ones_synthesizes_under_mask():
    spec = _turn_off_trailing_ones_spec(32)
    library = Library(ops=(Op.ADD, Op.AND), n_constants=1)
    result = synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec, shift_mode=ShiftMode.MASK), Equivalent)
    assert (
        fuzz(
            result,
            turn_off_trailing_ones,
            trials=20_000,
            seed=1,
            shift_mode=ShiftMode.MASK,
        )
        is None
    )


def test_isolate_rmb_synthesizes_under_mask():
    spec = _isolate_rmb_spec(32)
    library = Library(ops=(Op.NEG, Op.AND))
    result = synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK)
    assert result is not None
    assert len(result.instructions) == 2
    assert isinstance(equivalent(result, spec, shift_mode=ShiftMode.MASK), Equivalent)
    assert (
        fuzz(result, isolate_rmb, trials=20_000, seed=1, shift_mode=ShiftMode.MASK)
        is None
    )


def test_clear_lowest_bit_zero_constant_hunt():
    spec = _clear_lowest_bit_spec(32)
    library = Library(ops=(Op.SUB, Op.AND), n_constants=0)
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.SATURATE) is None
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK) is None


def test_smear_lowest_bit_zero_constant_hunt():
    spec = _smear_lowest_bit_spec(32)
    library = Library(ops=(Op.SUB, Op.OR), n_constants=0)
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.SATURATE) is None
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK) is None


def test_turn_off_trailing_ones_zero_constant_hunt():
    spec = _turn_off_trailing_ones_spec(32)
    library = Library(ops=(Op.ADD, Op.AND), n_constants=0)
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.SATURATE) is None
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK) is None


def test_rotl5_zero_constant_hunt():
    spec = _rotl5_spec(32)
    library = Library(ops=(Op.SHL, Op.LSHR, Op.OR), n_constants=0)
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.SATURATE) is None
    assert synthesize(spec, library, seed=0, shift_mode=ShiftMode.MASK) is None
