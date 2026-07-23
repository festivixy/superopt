	.file	"popcount.c"
	.text
	.p2align 4
	.globl	popcount
	.def	popcount;	.scl	2;	.type	32;	.endef
	.seh_proc	popcount
popcount:
	.seh_endprologue
	movl	$1, %eax
	vmovd	%eax, %xmm2
	vpbroadcastd	%xmm2, %ymm2
	vmovd	%ecx, %xmm0
	vpbroadcastd	%xmm0, %ymm0
	vpsrlvd	.LC0(%rip), %ymm0, %ymm1
	vpsrlvd	.LC2(%rip), %ymm0, %ymm3
	vpand	%ymm2, %ymm1, %ymm1
	vpand	%ymm2, %ymm3, %ymm3
	vpaddd	%ymm3, %ymm1, %ymm1
	vpsrlvd	.LC3(%rip), %ymm0, %ymm3
	vpsrlvd	.LC4(%rip), %ymm0, %ymm0
	vpand	%ymm2, %ymm3, %ymm3
	vpand	%ymm2, %ymm0, %ymm0
	vpaddd	%ymm0, %ymm3, %ymm0
	vpaddd	%ymm0, %ymm1, %ymm1
	vmovdqa	%xmm1, %xmm0
	vextracti128	$0x1, %ymm1, %xmm1
	vpaddd	%xmm1, %xmm0, %xmm0
	vpsrldq	$8, %xmm0, %xmm1
	vpaddd	%xmm1, %xmm0, %xmm0
	vpsrldq	$4, %xmm0, %xmm1
	vpaddd	%xmm1, %xmm0, %xmm0
	vmovd	%xmm0, %eax
	vzeroupper
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 32
.LC0:
	.long	0
	.long	1
	.long	2
	.long	3
	.long	4
	.long	5
	.long	6
	.long	7
	.align 32
.LC2:
	.long	8
	.long	9
	.long	10
	.long	11
	.long	12
	.long	13
	.long	14
	.long	15
	.align 32
.LC3:
	.long	24
	.long	25
	.long	26
	.long	27
	.long	28
	.long	29
	.long	30
	.long	31
	.align 32
.LC4:
	.long	16
	.long	17
	.long	18
	.long	19
	.long	20
	.long	21
	.long	22
	.long	23
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
