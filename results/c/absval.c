#include <stdint.h>

uint32_t absval(uint32_t x) {
    if (x & 0x80000000u) {
        return -x;
    }
    return x;
}
