#include <stdint.h>

uint32_t sign(uint32_t x) {
    if (x == 0) {
        return 0;
    }
    if (x & 0x80000000u) {
        return 0xFFFFFFFFu;
    }
    return 1;
}
