from __future__ import annotations


def turn_off_trailing_ones(x: int, width: int) -> int:
    x &= (1 << width) - 1
    i = 0
    while i < width and x & (1 << i):
        x ^= 1 << i
        i += 1
    return x
