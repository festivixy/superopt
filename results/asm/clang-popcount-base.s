# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64
# fetched: 2026-07-22 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
popcount:
        mov     eax, edi
        and     eax, 1
        mov     ecx, edi
        shr     ecx
        and     ecx, 1
        bt      edi, 2
        adc     ecx, eax
        mov     eax, edi
        shr     eax, 3
        and     eax, 1
        bt      edi, 4
        adc     eax, ecx
        mov     ecx, edi
        shr     ecx, 5
        and     ecx, 1
        bt      edi, 6
        adc     ecx, eax
        mov     eax, edi
        shr     eax, 7
        and     eax, 1
        bt      edi, 8
        adc     eax, ecx
        mov     ecx, edi
        shr     ecx, 9
        and     ecx, 1
        bt      edi, 10
        adc     ecx, eax
        mov     eax, edi
        shr     eax, 11
        and     eax, 1
        bt      edi, 12
        adc     eax, ecx
        mov     ecx, edi
        shr     ecx, 13
        and     ecx, 1
        bt      edi, 14
        adc     ecx, eax
        mov     eax, edi
        shr     eax, 15
        and     eax, 1
        bt      edi, 16
        adc     eax, ecx
        mov     ecx, edi
        shr     ecx, 17
        and     ecx, 1
        bt      edi, 18
        adc     ecx, eax
        mov     eax, edi
        shr     eax, 19
        and     eax, 1
        bt      edi, 20
        adc     eax, ecx
        mov     ecx, edi
        shr     ecx, 21
        and     ecx, 1
        bt      edi, 22
        adc     ecx, eax
        mov     eax, edi
        shr     eax, 23
        and     eax, 1
        bt      edi, 24
        adc     eax, ecx
        mov     ecx, edi
        shr     ecx, 25
        and     ecx, 1
        bt      edi, 26
        adc     ecx, eax
        mov     edx, edi
        shr     edx, 27
        and     edx, 1
        bt      edi, 28
        adc     edx, ecx
        mov     eax, edi
        shr     eax, 29
        and     eax, 1
        bt      edi, 30
        adc     eax, edx
        shr     edi, 31
        add     eax, edi
        ret

