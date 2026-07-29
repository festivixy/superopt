	.file	"avg_floor.c"
	.text
	.p2align 4
	.globl	avg_floor
	.def	avg_floor;	.scl	2;	.type	32;	.endef
	.seh_proc	avg_floor
avg_floor:
	.seh_endprologue
	movl	%ecx, %ecx
	movl	%edx, %edx
	leaq	(%rcx,%rdx), %rax
	shrq	%rax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
