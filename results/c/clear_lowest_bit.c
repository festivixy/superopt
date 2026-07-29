#include <stdint.h>

uint32_t clear_lowest_bit(uint32_t x) {
    for (int i = 0; i < 32; i++) {
        if (x & (1u << i)) {
            return x ^ (1u << i);
        }
    }
    return 0;
}
