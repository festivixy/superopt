# compiler: gcc (Compiler-Explorer-Build-gcc-6add1e29e28d21850e81857811528280aa23fbe6-binutils-2.44) 17.0.0 20260728 (experimental) via godbolt.org (id cgsnapshot)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cgsnapshot/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
"clear_lowest_bit":
        mov     esi, edi
        and     esi, 1
        jne     .L6
        xor     ecx, ecx
.L3:
        add     ecx, 1
        cmp     ecx, 32
        je      .L1
        mov     eax, 1
        sal     eax, cl
        test    eax, edi
        je      .L3
.L2:
        mov     esi, edi
        xor     esi, eax
.L1:
        mov     eax, esi
        ret
.L6:
        mov     eax, esi
        jmp     .L2
