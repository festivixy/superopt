#include <stdint.h>

uint32_t popcount(uint32_t x) {
    uint32_t count = 0;
    for (int i = 0; i < 32; i++) {
        count += (x >> i) & 1u;
    }
    return count;
}
