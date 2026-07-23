# Compiler gap

<!-- gap-table:begin -->
| benchmark | gcc -O3 base | gcc -O3 v3 | clang -O3 base | clang -O3 v3 | superopt (proven minimum) |
|---|---|---|---|---|---|
| absval | 3 | 3 | — | — | **3** (proven) |
| isolate_rmb | 14 | 14 | — | — | **2** (proven) |
| popcount | 11 | 25 | — | — | no result (frontier) |

Local gcc: `gcc (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0`. Counting rule: every
instruction in the function body except `ret`; applied by
`scripts/compiler_gap.py`, tested in `tests/test_compiler_gap.py`.
<!-- gap-table:end -->
