#include <stdint.h>

uint32_t flp2(uint32_t x) {
    for (int i = 31; i >= 0; i--) {
        if (x & (1u << i)) {
            return 1u << i;
        }
    }
    return 0;
}
