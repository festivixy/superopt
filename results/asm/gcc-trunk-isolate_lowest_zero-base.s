# compiler: gcc (Compiler-Explorer-Build-gcc-6add1e29e28d21850e81857811528280aa23fbe6-binutils-2.44) 17.0.0 20260728 (experimental) via godbolt.org (id cgsnapshot)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cgsnapshot/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
"isolate_lowest_zero":
        test    dil, 1
        je      .L5
        xor     ecx, ecx
.L3:
        add     ecx, 1
        cmp     ecx, 32
        je      .L10
        mov     eax, 1
        sal     eax, cl
        test    eax, edi
        jne     .L3
        ret
.L10:
        xor     eax, eax
        ret
.L5:
        mov     eax, 1
        ret
