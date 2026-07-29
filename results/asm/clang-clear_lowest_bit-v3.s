# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64-v3
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
clear_lowest_bit:
        mov     eax, 1
        test    dil, 1
        jne     .LBB0_33
        mov     eax, 2
        test    dil, 2
        jne     .LBB0_33
        mov     eax, 4
        test    dil, 4
        jne     .LBB0_33
        mov     eax, 8
        test    dil, 8
        jne     .LBB0_33
        mov     eax, 16
        test    dil, 16
        jne     .LBB0_33
        mov     eax, 32
        test    dil, 32
        jne     .LBB0_33
        mov     eax, 64
        test    dil, 64
        jne     .LBB0_33
        mov     eax, 128
        test    dil, dil
        js      .LBB0_33
        mov     eax, 256
        test    edi, 256
        jne     .LBB0_33
        mov     eax, 512
        test    edi, 512
        jne     .LBB0_33
        mov     eax, 1024
        test    edi, 1024
        jne     .LBB0_33
        mov     eax, 2048
        test    edi, 2048
        jne     .LBB0_33
        mov     eax, 4096
        test    edi, 4096
        jne     .LBB0_33
        mov     eax, 8192
        test    edi, 8192
        jne     .LBB0_33
        mov     eax, 16384
        test    edi, 16384
        jne     .LBB0_33
        mov     eax, 32768
        test    di, di
        js      .LBB0_33
        mov     eax, 65536
        test    edi, 65536
        jne     .LBB0_33
        mov     eax, 131072
        test    edi, 131072
        jne     .LBB0_33
        mov     eax, 262144
        test    edi, 262144
        jne     .LBB0_33
        mov     eax, 524288
        test    edi, 524288
        jne     .LBB0_33
        mov     eax, 1048576
        test    edi, 1048576
        jne     .LBB0_33
        mov     eax, 2097152
        test    edi, 2097152
        jne     .LBB0_33
        mov     eax, 4194304
        test    edi, 4194304
        jne     .LBB0_33
        mov     eax, 8388608
        test    edi, 8388608
        jne     .LBB0_33
        mov     eax, 16777216
        test    edi, 16777216
        jne     .LBB0_33
        mov     eax, 33554432
        test    edi, 33554432
        jne     .LBB0_33
        mov     eax, 67108864
        test    edi, 67108864
        jne     .LBB0_33
        mov     eax, 134217728
        test    edi, 134217728
        jne     .LBB0_33
        mov     eax, 268435456
        test    edi, 268435456
        jne     .LBB0_33
        mov     eax, 536870912
        test    edi, 536870912
        jne     .LBB0_33
        mov     eax, 1073741824
        test    edi, 1073741824
        jne     .LBB0_33
        mov     eax, -2147483648
        test    edi, edi
        je      .LBB0_32
.LBB0_33:
        xor     eax, edi
        ret
.LBB0_32:
        xor     eax, eax
        ret

