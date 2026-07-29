from __future__ import annotations


def sign(x: int, width: int) -> int:
    mask = (1 << width) - 1
    x &= mask
    if x == 0:
        return 0
    if x & (1 << (width - 1)):
        return mask
    return 1
