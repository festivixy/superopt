# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64-v3
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
smear_lowest_bit:
        test    edi, edi
        je      .LBB0_1
        xor     eax, eax
        test    dil, 1
        jne     .LBB0_33
        mov     eax, 1
        test    dil, 2
        jne     .LBB0_33
        mov     eax, 3
        test    dil, 4
        jne     .LBB0_33
        mov     eax, 7
        test    dil, 8
        jne     .LBB0_33
        mov     eax, 15
        test    dil, 16
        jne     .LBB0_33
        mov     eax, 31
        test    dil, 32
        jne     .LBB0_33
        mov     eax, 63
        test    dil, 64
        jne     .LBB0_33
        mov     eax, 127
        test    dil, dil
        js      .LBB0_33
        mov     eax, 255
        test    edi, 256
        jne     .LBB0_33
        mov     eax, 511
        test    edi, 512
        jne     .LBB0_33
        mov     eax, 1023
        test    edi, 1024
        jne     .LBB0_33
        mov     eax, 2047
        test    edi, 2048
        jne     .LBB0_33
        mov     eax, 4095
        test    edi, 4096
        jne     .LBB0_33
        mov     eax, 8191
        test    edi, 8192
        jne     .LBB0_33
        mov     eax, 16383
        test    edi, 16384
        jne     .LBB0_33
        mov     eax, 32767
        test    di, di
        js      .LBB0_33
        mov     eax, 65535
        test    edi, 65536
        jne     .LBB0_33
        mov     eax, 131071
        test    edi, 131072
        jne     .LBB0_33
        mov     eax, 262143
        test    edi, 262144
        jne     .LBB0_33
        mov     eax, 524287
        test    edi, 524288
        jne     .LBB0_33
        mov     eax, 1048575
        test    edi, 1048576
        jne     .LBB0_33
        mov     eax, 2097151
        test    edi, 2097152
        jne     .LBB0_33
        mov     eax, 4194303
        test    edi, 4194304
        jne     .LBB0_33
        mov     eax, 8388607
        test    edi, 8388608
        jne     .LBB0_33
        mov     eax, 16777215
        test    edi, 16777216
        jne     .LBB0_33
        mov     eax, 33554431
        test    edi, 33554432
        jne     .LBB0_33
        mov     eax, 67108863
        test    edi, 67108864
        jne     .LBB0_33
        mov     eax, 134217727
        test    edi, 134217728
        jne     .LBB0_33
        mov     eax, 268435455
        test    edi, 268435456
        jne     .LBB0_33
        mov     eax, 536870911
        test    edi, 536870912
        jne     .LBB0_33
        mov     eax, edi
        and     eax, 1073741824
        xor     eax, 2147483647
.LBB0_33:
        or      eax, edi
        ret
.LBB0_1:
        mov     eax, -1
        ret

