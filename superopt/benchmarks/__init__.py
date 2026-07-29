from __future__ import annotations

from superopt.benchmarks.abs_val import absval
from superopt.benchmarks.clear_lowest_bit import clear_lowest_bit
from superopt.benchmarks.isolate_lowest_zero import isolate_lowest_zero
from superopt.benchmarks.isolate_rmb import isolate_rmb
from superopt.benchmarks.popcount import popcount
from superopt.benchmarks.rotl5 import rotl5
from superopt.benchmarks.smear_lowest_bit import smear_lowest_bit
from superopt.benchmarks.times_nine import times_nine
from superopt.benchmarks.turn_off_trailing_ones import turn_off_trailing_ones

__all__ = [
    "absval",
    "clear_lowest_bit",
    "isolate_lowest_zero",
    "isolate_rmb",
    "popcount",
    "rotl5",
    "smear_lowest_bit",
    "times_nine",
    "turn_off_trailing_ones",
]
