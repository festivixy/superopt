# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64-v3
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
isolate_lowest_zero:
        mov     eax, 1
        test    dil, 1
        je      .LBB0_32
        mov     eax, 2
        test    dil, 2
        je      .LBB0_32
        mov     eax, 4
        test    dil, 4
        je      .LBB0_32
        mov     eax, 8
        test    dil, 8
        je      .LBB0_32
        mov     eax, 16
        test    dil, 16
        je      .LBB0_32
        mov     eax, 32
        test    dil, 32
        je      .LBB0_32
        mov     eax, 64
        test    dil, 64
        je      .LBB0_32
        mov     eax, 128
        test    dil, dil
        jns     .LBB0_32
        mov     eax, 256
        test    edi, 256
        je      .LBB0_32
        mov     eax, 512
        test    edi, 512
        je      .LBB0_32
        mov     eax, 1024
        test    edi, 1024
        je      .LBB0_32
        mov     eax, 2048
        test    edi, 2048
        je      .LBB0_32
        mov     eax, 4096
        test    edi, 4096
        je      .LBB0_32
        mov     eax, 8192
        test    edi, 8192
        je      .LBB0_32
        mov     eax, 16384
        test    edi, 16384
        je      .LBB0_32
        mov     eax, 32768
        test    di, di
        jns     .LBB0_32
        mov     eax, 65536
        test    edi, 65536
        je      .LBB0_32
        mov     eax, 131072
        test    edi, 131072
        je      .LBB0_32
        mov     eax, 262144
        test    edi, 262144
        je      .LBB0_32
        mov     eax, 524288
        test    edi, 524288
        je      .LBB0_32
        mov     eax, 1048576
        test    edi, 1048576
        je      .LBB0_32
        mov     eax, 2097152
        test    edi, 2097152
        je      .LBB0_32
        mov     eax, 4194304
        test    edi, 4194304
        je      .LBB0_32
        mov     eax, 8388608
        test    edi, 8388608
        je      .LBB0_32
        mov     eax, 16777216
        test    edi, 16777216
        je      .LBB0_32
        mov     eax, 33554432
        test    edi, 33554432
        je      .LBB0_32
        mov     eax, 67108864
        test    edi, 67108864
        je      .LBB0_32
        mov     eax, 134217728
        test    edi, 134217728
        je      .LBB0_32
        mov     eax, 268435456
        test    edi, 268435456
        je      .LBB0_32
        mov     eax, 536870912
        test    edi, 536870912
        je      .LBB0_32
        mov     eax, 1073741824
        test    edi, 1073741824
        je      .LBB0_32
        not     edi
        and     edi, -2147483648
        mov     eax, edi
.LBB0_32:
        ret

