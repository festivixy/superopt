#include <stdint.h>

uint32_t smear_lowest_bit(uint32_t x) {
    if (x == 0) {
        return 0xFFFFFFFFu;
    }
    for (int i = 0; i < 32; i++) {
        if (x & (1u << i)) {
            return x | ((1u << i) - 1);
        }
    }
    return 0xFFFFFFFFu;
}
