#include <stdint.h>

uint32_t isolate_lowest_zero(uint32_t x) {
    for (int i = 0; i < 32; i++) {
        if (!(x & (1u << i))) {
            return 1u << i;
        }
    }
    return 0;
}
