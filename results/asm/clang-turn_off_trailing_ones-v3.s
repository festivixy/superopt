# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64-v3
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
turn_off_trailing_ones:
        mov     eax, edi
        test    al, 1
        jne     .LBB0_1
        ret
.LBB0_1:
        test    al, 2
        jne     .LBB0_3
        and     eax, -2
        ret
.LBB0_3:
        test    al, 4
        jne     .LBB0_5
        and     eax, -4
        ret
.LBB0_5:
        test    al, 8
        jne     .LBB0_7
        and     eax, -8
        ret
.LBB0_7:
        test    al, 16
        jne     .LBB0_9
        and     eax, -16
        ret
.LBB0_9:
        test    al, 32
        jne     .LBB0_11
        and     eax, -32
        ret
.LBB0_11:
        test    al, 64
        jne     .LBB0_13
        and     eax, -64
        ret
.LBB0_13:
        test    al, al
        js      .LBB0_15
        and     eax, -128
        ret
.LBB0_15:
        test    eax, 256
        jne     .LBB0_17
        and     eax, -256
        ret
.LBB0_17:
        test    eax, 512
        jne     .LBB0_19
        and     eax, -512
        ret
.LBB0_19:
        test    eax, 1024
        jne     .LBB0_21
        and     eax, -1024
        ret
.LBB0_21:
        test    eax, 2048
        jne     .LBB0_23
        and     eax, -2048
        ret
.LBB0_23:
        test    eax, 4096
        jne     .LBB0_25
        and     eax, -4096
        ret
.LBB0_25:
        test    eax, 8192
        jne     .LBB0_27
        and     eax, -8192
        ret
.LBB0_27:
        test    eax, 16384
        jne     .LBB0_29
        and     eax, -16384
        ret
.LBB0_29:
        test    ax, ax
        js      .LBB0_31
        and     eax, -32768
        ret
.LBB0_31:
        test    eax, 65536
        jne     .LBB0_33
        and     eax, -65536
        ret
.LBB0_33:
        test    eax, 131072
        jne     .LBB0_35
        and     eax, -131072
        ret
.LBB0_35:
        test    eax, 262144
        jne     .LBB0_37
        and     eax, -262144
        ret
.LBB0_37:
        test    eax, 524288
        jne     .LBB0_39
        and     eax, -524288
        ret
.LBB0_39:
        test    eax, 1048576
        jne     .LBB0_41
        and     eax, -1048576
        ret
.LBB0_41:
        test    eax, 2097152
        jne     .LBB0_43
        and     eax, -2097152
        ret
.LBB0_43:
        test    eax, 4194304
        jne     .LBB0_45
        and     eax, -4194304
        ret
.LBB0_45:
        test    eax, 8388608
        jne     .LBB0_47
        and     eax, -8388608
        ret
.LBB0_47:
        test    eax, 16777216
        jne     .LBB0_49
        and     eax, -16777216
        ret
.LBB0_49:
        test    eax, 33554432
        jne     .LBB0_51
        and     eax, -33554432
        ret
.LBB0_51:
        test    eax, 67108864
        jne     .LBB0_53
        and     eax, -67108864
        ret
.LBB0_53:
        test    eax, 134217728
        jne     .LBB0_55
        and     eax, -134217728
        ret
.LBB0_55:
        test    eax, 268435456
        jne     .LBB0_57
        and     eax, -268435456
        ret
.LBB0_57:
        test    eax, 536870912
        jne     .LBB0_59
        and     eax, -536870912
        ret
.LBB0_59:
        mov     ecx, eax
        and     ecx, -1073741824
        xor     edx, edx
        test    eax, 1073741824
        cmove   edx, ecx
        mov     eax, edx
        ret

