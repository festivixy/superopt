# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64-v3
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
flp2:
        test    edi, edi
        js      .LBB0_1
        mov     eax, 1073741824
        cmp     edi, 1073741823
        ja      .LBB0_32
        mov     eax, 536870912
        cmp     edi, 536870911
        ja      .LBB0_32
        mov     eax, 268435456
        cmp     edi, 268435455
        ja      .LBB0_32
        mov     eax, 134217728
        cmp     edi, 134217727
        ja      .LBB0_32
        mov     eax, 67108864
        cmp     edi, 67108863
        ja      .LBB0_32
        mov     eax, 33554432
        cmp     edi, 33554431
        ja      .LBB0_32
        mov     eax, 16777216
        cmp     edi, 16777215
        ja      .LBB0_32
        mov     eax, 8388608
        cmp     edi, 8388607
        ja      .LBB0_32
        mov     eax, 4194304
        cmp     edi, 4194303
        ja      .LBB0_32
        mov     eax, 2097152
        cmp     edi, 2097151
        ja      .LBB0_32
        mov     eax, 1048576
        cmp     edi, 1048575
        ja      .LBB0_32
        mov     eax, 524288
        cmp     edi, 524287
        ja      .LBB0_32
        mov     eax, 262144
        cmp     edi, 262143
        ja      .LBB0_32
        mov     eax, 131072
        cmp     edi, 131071
        ja      .LBB0_32
        mov     eax, 65536
        cmp     edi, 65535
        ja      .LBB0_32
        mov     eax, 32768
        cmp     edi, 32767
        ja      .LBB0_32
        mov     eax, 16384
        cmp     edi, 16383
        ja      .LBB0_32
        mov     eax, 8192
        cmp     edi, 8191
        ja      .LBB0_32
        mov     eax, 4096
        cmp     edi, 4095
        ja      .LBB0_32
        mov     eax, 2048
        cmp     edi, 2047
        ja      .LBB0_32
        mov     eax, 1024
        cmp     edi, 1023
        ja      .LBB0_32
        mov     eax, 512
        cmp     edi, 511
        ja      .LBB0_32
        mov     eax, 256
        cmp     edi, 255
        ja      .LBB0_32
        mov     eax, 128
        cmp     edi, 127
        ja      .LBB0_32
        mov     eax, 64
        cmp     edi, 63
        ja      .LBB0_32
        mov     eax, 32
        cmp     edi, 31
        ja      .LBB0_32
        mov     eax, 16
        cmp     edi, 15
        ja      .LBB0_32
        mov     eax, 8
        cmp     edi, 7
        ja      .LBB0_32
        mov     eax, 4
        cmp     edi, 3
        ja      .LBB0_32
        cmp     edi, 2
        mov     eax, 2
        cmovb   eax, edi
.LBB0_32:
        ret
.LBB0_1:
        mov     eax, -2147483648
        ret

