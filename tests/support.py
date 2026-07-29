from __future__ import annotations

from itertools import combinations_with_replacement

from superopt.cegis import Library, synthesize
from superopt.equiv import Counterexample, equivalent
from superopt.interp import execute
from superopt.ir import InputRef, Op, Program


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
) -> None:
    first, second = probes
    assert execute(spec, first) != execute(spec, second)
    for index in range(n_inputs):
        passthrough = Program(spec.width, (), InputRef(index))
        assert isinstance(equivalent(passthrough, spec), Counterexample)
    for library in libraries_up_to(max_ops):
        assert synthesize(spec, library, seed=0) is None, library.ops
