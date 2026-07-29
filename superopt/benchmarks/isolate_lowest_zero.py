from __future__ import annotations


def isolate_lowest_zero(x: int, width: int) -> int:
    x &= (1 << width) - 1
    for i in range(width):
        if not x & (1 << i):
            return 1 << i
    return 0
