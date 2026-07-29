	.file	"avg_ceil.c"
	.text
	.p2align 4
	.globl	avg_ceil
	.def	avg_ceil;	.scl	2;	.type	32;	.endef
	.seh_proc	avg_ceil
avg_ceil:
	.seh_endprologue
	movl	%edx, %edx
	movl	%ecx, %ecx
	leaq	1(%rdx,%rcx), %rax
	shrq	%rax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
