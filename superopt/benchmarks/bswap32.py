from __future__ import annotations


def bswap32(x: int, width: int) -> int:
    x &= (1 << width) - 1
    n_bytes = width // 8
    out = 0
    for i in range(n_bytes):
        byte = (x >> (8 * i)) & 0xFF
        out |= byte << (8 * (n_bytes - 1 - i))
    return out
