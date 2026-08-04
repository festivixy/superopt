from __future__ import annotations

from itertools import combinations_with_replacement

from superopt.cegis import Library, synthesize
from superopt.equiv import Counterexample, equivalent
from superopt.interp import execute
from superopt.ir import InputRef, Op, Program, ShiftMode


def libraries_up_to(max_ops: int) -> list[Library]:
    libraries: list[Library] = []
    for size in range(1, max_ops + 1):
        for combo in combinations_with_replacement(tuple(Op), size):
            libraries.append(Library(ops=combo, n_constants=2 * size))
    return libraries


def assert_floor(
    spec: Program,
    max_ops: int,
    n_inputs: int,
    probes: tuple[tuple[int, ...], tuple[int, ...]],
    *,
    shift_mode: ShiftMode = ShiftMode.SATURATE,
) -> None:
    first, second = probes
    assert execute(spec, first) != execute(spec, second)
    for index in range(n_inputs):
        passthrough = Program(spec.width, (), InputRef(index))
        assert isinstance(
            equivalent(passthrough, spec, shift_mode=shift_mode), Counterexample
        )
    for library in libraries_up_to(max_ops):
        assert (
            synthesize(spec, library, seed=0, shift_mode=shift_mode) is None
        ), library.ops
