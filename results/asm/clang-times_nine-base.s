# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
times_nine:
        lea     eax, [rdi + 8*rdi]
        ret

