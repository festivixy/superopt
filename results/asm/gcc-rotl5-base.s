	.file	"rotl5.c"
	.text
	.p2align 4
	.globl	rotl5
	.def	rotl5;	.scl	2;	.type	32;	.endef
	.seh_proc	rotl5
rotl5:
	.seh_endprologue
	movl	%ecx, %eax
	roll	$5, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
