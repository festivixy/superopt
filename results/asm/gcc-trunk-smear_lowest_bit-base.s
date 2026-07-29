# compiler: gcc (Compiler-Explorer-Build-gcc-6add1e29e28d21850e81857811528280aa23fbe6-binutils-2.44) 17.0.0 20260728 (experimental) via godbolt.org (id cgsnapshot)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cgsnapshot/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
"smear_lowest_bit":
        test    edi, edi
        je      .L2
        test    dil, 1
        jne     .L6
        xor     ecx, ecx
.L4:
        add     ecx, 1
        cmp     ecx, 32
        je      .L2
        mov     eax, 1
        sal     eax, cl
        test    eax, edi
        je      .L4
        sub     eax, 1
        or      eax, edi
        ret
.L6:
        mov     eax, edi
        ret
.L2:
        mov     eax, -1
        ret
