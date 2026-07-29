# compiler: clang version 24.0.0git (https://github.com/llvm/llvm-project.git 5e91f5d57a19752fe245ab64c1265e26c44d0d76) via godbolt.org (id cclang_trunk)
# flags: -O3 -march=x86-64
# fetched: 2026-07-29 from https://godbolt.org/api/compiler/cclang_trunk/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
sign:
        test    edi, edi
        sets    al
        setg    cl
        sub     cl, al
        movsx   eax, cl
        ret

