#include <stdint.h>

uint32_t avg_floor(uint32_t x, uint32_t y) {
    return (uint32_t)(((uint64_t)x + y) >> 1);
}
