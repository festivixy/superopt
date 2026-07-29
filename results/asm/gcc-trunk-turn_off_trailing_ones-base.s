# compiler: gcc (Compiler-Explorer-Build-gcc-6add1e29e28d21850e81857811528280aa23fbe6-binutils-2.44) 17.0.0 20260728 (experimental) via godbolt.org (id cgsnapshot)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cgsnapshot/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
"turn_off_trailing_ones":
        mov     eax, edi
        xor     ecx, ecx
        jmp     .L2
.L4:
        add     ecx, 1
        xor     eax, edx
        cmp     ecx, 32
        je      .L3
.L2:
        mov     edx, 1
        sal     edx, cl
        test    edx, eax
        jne     .L4
.L3:
        ret
