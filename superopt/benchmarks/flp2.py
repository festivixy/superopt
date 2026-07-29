from __future__ import annotations


def flp2(x: int, width: int) -> int:
    x &= (1 << width) - 1
    for i in range(width - 1, -1, -1):
        if x & (1 << i):
            return 1 << i
    return 0
