#include <stdint.h>

uint32_t rotl5(uint32_t x) {
    return (x << 5) | (x >> 27);
}
