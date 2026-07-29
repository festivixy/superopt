from __future__ import annotations


def smear_lowest_bit(x: int, width: int) -> int:
    mask = (1 << width) - 1
    x &= mask
    if x == 0:
        return mask
    for i in range(width):
        if x & (1 << i):
            return x | ((1 << i) - 1)
    return mask
