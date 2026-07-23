from __future__ import annotations


def times_nine(x: int, width: int) -> int:
    mask = (1 << width) - 1
    x &= mask
    return (x * 9) & mask
