from __future__ import annotations


def avg_ceil(x: int, y: int, width: int) -> int:
    mask = (1 << width) - 1
    return ((x & mask) + (y & mask) + 1) >> 1
