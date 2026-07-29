#include <stdint.h>

uint32_t bswap32(uint32_t x) {
    uint32_t out = 0;
    for (int i = 0; i < 4; i++) {
        uint32_t byte = (x >> (8 * i)) & 0xFFu;
        out |= byte << (8 * (3 - i));
    }
    return out;
}
