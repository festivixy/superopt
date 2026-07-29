from __future__ import annotations


def rotl5(x: int, width: int) -> int:
    mask = (1 << width) - 1
    x &= mask
    return ((x << 5) | (x >> (width - 5))) & mask
