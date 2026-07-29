#include <stdint.h>

uint32_t turn_off_trailing_ones(uint32_t x) {
    int i = 0;
    while (i < 32 && (x & (1u << i))) {
        x ^= 1u << i;
        i++;
    }
    return x;
}
