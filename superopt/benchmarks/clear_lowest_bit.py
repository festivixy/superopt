from __future__ import annotations


def clear_lowest_bit(x: int, width: int) -> int:
    x &= (1 << width) - 1
    for i in range(width):
        if x & (1 << i):
            return x ^ (1 << i)
    return 0
