# compiler: clang 22.1.0 via godbolt.org (id cclang2210)
# flags: -O3 -march=x86-64-v3
# fetched: 2026-07-22 from https://godbolt.org/api/compiler/cclang2210/compile
# Compilation provided by Compiler Explorer at https://godbolt.org/
.LCPI0_0:
        .long   24
        .long   25
        .long   26
        .long   27
        .long   28
        .long   29
        .long   30
        .zero   4
.LCPI0_1:
        .long   1
        .long   0
        .long   2
        .long   3
        .long   4
        .long   5
        .long   6
        .long   7
.LCPI0_2:
        .long   16
        .long   17
        .long   18
        .long   19
        .long   20
        .long   21
        .long   22
        .long   23
.LCPI0_3:
        .long   8
        .long   9
        .long   10
        .long   11
        .long   12
        .long   13
        .long   14
        .long   15
.LCPI0_4:
        .long   1
popcount:
        vmovd   xmm0, edi
        vpbroadcastd    ymm0, xmm0
        vpsrlvd ymm1, ymm0, ymmword ptr [rip + .LCPI0_0]
        vpsrlvd ymm2, ymm0, ymmword ptr [rip + .LCPI0_1]
        vpsrlvd ymm3, ymm0, ymmword ptr [rip + .LCPI0_2]
        vpsrlvd ymm4, ymm0, ymmword ptr [rip + .LCPI0_3]
        vpbroadcastd    ymm5, dword ptr [rip + .LCPI0_4]
        vpand   ymm4, ymm4, ymm5
        vpand   ymm3, ymm3, ymm5
        vpand   ymm2, ymm2, ymm5
        vpaddd  ymm2, ymm2, ymm3
        vpand   ymm1, ymm1, ymm5
        vpsrld  ymm0, ymm0, 31
        vpblendd        ymm0, ymm1, ymm0, 128
        vpaddd  ymm0, ymm4, ymm0
        vpaddd  ymm0, ymm2, ymm0
        vextracti128    xmm1, ymm0, 1
        vpaddd  xmm0, xmm0, xmm1
        vpshufd xmm1, xmm0, 238
        vpaddd  xmm0, xmm0, xmm1
        vpshufd xmm1, xmm0, 85
        vpaddd  xmm0, xmm0, xmm1
        vmovd   eax, xmm0
        vzeroupper
        ret

