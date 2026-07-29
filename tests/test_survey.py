from __future__ import annotations

import pytest

from superopt.benchmarks.avg_ceil import avg_ceil
from superopt.benchmarks.avg_floor import avg_floor
from superopt.benchmarks.bswap32 import bswap32
from superopt.benchmarks.clear_lowest_bit import clear_lowest_bit
from superopt.benchmarks.flp2 import flp2
from superopt.benchmarks.isolate_lowest_zero import isolate_lowest_zero
from superopt.benchmarks.rotl5 import rotl5
from superopt.benchmarks.sign import sign
from superopt.benchmarks.smear_lowest_bit import smear_lowest_bit
from superopt.benchmarks.turn_off_trailing_ones import turn_off_trailing_ones
from superopt.cegis import Library, synthesize
from superopt.equiv import Equivalent, equivalent
from superopt.fuzz import fuzz
from superopt.interp import execute
from superopt.ir import Const, InputRef, Instruction, Op, Operand, Program, ResultRef
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
    result = synthesize(spec, Library(ops=(Op.SUB, Op.AND), n_constants=1), seed=0)
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
    result = synthesize(spec, Library(ops=(Op.SUB, Op.OR), n_constants=1), seed=0)
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
    result = synthesize(spec, Library(ops=(Op.ADD, Op.AND), n_constants=1), seed=0)
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


def _sign_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.ASHR, (InputRef(0), Const(width - 1))),
            Instruction(Op.NEG, (InputRef(0),)),
            Instruction(Op.LSHR, (ResultRef(1), Const(width - 1))),
            Instruction(Op.OR, (ResultRef(0), ResultRef(2))),
        ),
        ResultRef(3),
    )


def test_sign_spec_matches_benchmark():
    spec = _sign_spec(8)
    for x in range(256):
        assert execute(spec, (x,)) == sign(x, 8)
    spec32 = _sign_spec(32)
    assert fuzz(spec32, sign, trials=20_000, seed=1) is None


def test_sign_synthesizes():
    spec = _sign_spec(32)
    result = synthesize(
        spec, Library(ops=(Op.ASHR, Op.NEG, Op.LSHR, Op.OR), n_constants=2), seed=0
    )
    assert result is not None
    assert len(result.instructions) == 4
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, sign, trials=20_000, seed=1) is None




def _avg_floor_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.AND, (InputRef(0), InputRef(1))),
            Instruction(Op.XOR, (InputRef(0), InputRef(1))),
            Instruction(Op.LSHR, (ResultRef(1), Const(1))),
            Instruction(Op.ADD, (ResultRef(0), ResultRef(2))),
        ),
        ResultRef(3),
    )


def test_avg_floor_spec_matches_benchmark():
    spec = _avg_floor_spec(8)
    for x in range(256):
        for y in range(256):
            assert execute(spec, (x, y)) == avg_floor(x, y, 8)
    spec32 = _avg_floor_spec(32)
    assert fuzz(spec32, avg_floor, trials=20_000, seed=1) is None


def test_avg_floor_synthesizes():
    spec = _avg_floor_spec(32)
    result = synthesize(
        spec, Library(ops=(Op.AND, Op.XOR, Op.LSHR, Op.ADD), n_constants=1), seed=0
    )
    assert result is not None
    assert len(result.instructions) == 4
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, avg_floor, trials=20_000, seed=1) is None




def _avg_ceil_spec(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.OR, (InputRef(0), InputRef(1))),
            Instruction(Op.XOR, (InputRef(0), InputRef(1))),
            Instruction(Op.LSHR, (ResultRef(1), Const(1))),
            Instruction(Op.SUB, (ResultRef(0), ResultRef(2))),
        ),
        ResultRef(3),
    )


def test_avg_ceil_spec_matches_benchmark():
    spec = _avg_ceil_spec(8)
    for x in range(256):
        for y in range(256):
            assert execute(spec, (x, y)) == avg_ceil(x, y, 8)
    spec32 = _avg_ceil_spec(32)
    assert fuzz(spec32, avg_ceil, trials=20_000, seed=1) is None


def test_avg_ceil_synthesizes():
    spec = _avg_ceil_spec(32)
    result = synthesize(
        spec, Library(ops=(Op.OR, Op.XOR, Op.LSHR, Op.SUB), n_constants=1), seed=0
    )
    assert result is not None
    assert len(result.instructions) == 4
    assert isinstance(equivalent(result, spec), Equivalent)
    assert fuzz(result, avg_ceil, trials=20_000, seed=1) is None


def _flp2_spec(width: int) -> Program:
    instructions: list[Instruction] = []
    current: Operand = InputRef(0)
    shift = 1
    index = 0
    while shift < width:
        instructions.append(Instruction(Op.LSHR, (current, Const(shift))))
        instructions.append(Instruction(Op.OR, (current, ResultRef(index))))
        current = ResultRef(index + 1)
        index += 2
        shift *= 2
    instructions.append(Instruction(Op.LSHR, (current, Const(1))))
    instructions.append(Instruction(Op.SUB, (current, ResultRef(index))))
    return Program(width, tuple(instructions), ResultRef(index + 1))


def test_flp2_upper_bound_verified():
    for width in (8, 16):
        spec = _flp2_spec(width)
        for x in range(1 << width):
            assert execute(spec, (x,)) == flp2(x, width)
    spec32 = _flp2_spec(32)
    assert len(spec32.instructions) == 12
    assert fuzz(spec32, flp2, trials=20_000, seed=1) is None


def _bswap_spec(width: int) -> Program:
    if width == 16:
        return Program(
            16,
            (
                Instruction(Op.SHL, (InputRef(0), Const(8))),
                Instruction(Op.LSHR, (InputRef(0), Const(8))),
                Instruction(Op.OR, (ResultRef(0), ResultRef(1))),
            ),
            ResultRef(2),
        )
    return Program(
        32,
        (
            Instruction(Op.SHL, (InputRef(0), Const(24))),
            Instruction(Op.AND, (InputRef(0), Const(0xFF00))),
            Instruction(Op.SHL, (ResultRef(1), Const(8))),
            Instruction(Op.LSHR, (InputRef(0), Const(8))),
            Instruction(Op.AND, (ResultRef(3), Const(0xFF00))),
            Instruction(Op.LSHR, (InputRef(0), Const(24))),
            Instruction(Op.OR, (ResultRef(0), ResultRef(2))),
            Instruction(Op.OR, (ResultRef(6), ResultRef(4))),
            Instruction(Op.OR, (ResultRef(7), ResultRef(5))),
        ),
        ResultRef(8),
    )


def test_bswap32_upper_bound_verified():
    spec16 = _bswap_spec(16)
    for x in range(1 << 16):
        assert execute(spec16, (x,)) == bswap32(x, 16)
    spec32 = _bswap_spec(32)
    assert len(spec32.instructions) == 9
    assert fuzz(spec32, bswap32, trials=20_000, seed=1) is None


def _folklore_min_trick(width: int) -> Program:
    return Program(
        width,
        (
            Instruction(Op.SUB, (InputRef(0), InputRef(1))),
            Instruction(Op.ASHR, (ResultRef(0), Const(width - 1))),
            Instruction(Op.AND, (ResultRef(0), ResultRef(1))),
            Instruction(Op.ADD, (InputRef(1), ResultRef(2))),
        ),
        ResultRef(3),
    )


def _signed_min(x: int, y: int, width: int) -> int:
    mask = (1 << width) - 1
    half = 1 << (width - 1)
    sx = (x & mask) - (1 << width) if (x & mask) & half else x & mask
    sy = (y & mask) - (1 << width) if (y & mask) & half else y & mask
    return min(sx, sy) & mask


def test_folklore_min_trick_is_wrong():
    trick = _folklore_min_trick(32)
    divergence = fuzz(trick, _signed_min, trials=100_000, seed=1)
    assert divergence is not None
    x, y = divergence.inputs
    assert execute(trick, (x, y)) != _signed_min(x, y, 32)
    int_min = 1 << 31
    assert execute(trick, (int_min, 1)) == 1
    assert _signed_min(int_min, 1, 32) == int_min


