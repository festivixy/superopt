# compiler: gcc (Compiler-Explorer-Build-gcc-6add1e29e28d21850e81857811528280aa23fbe6-binutils-2.44) 17.0.0 20260728 (experimental) via godbolt.org (id cgsnapshot)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cgsnapshot/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
"sign":
        mov     edx, edi
        xor     eax, eax
        sar     edx, 31
        or      edx, 1
        test    edi, edi
        cmovne  eax, edx
        ret
