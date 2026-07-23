	.file	"popcount.c"
	.text
	.p2align 4
	.globl	popcount
	.def	popcount;	.scl	2;	.type	32;	.endef
	.seh_proc	popcount
popcount:
	.seh_endprologue
	xorl	%edx, %edx
	movl	%ecx, %r8d
	xorl	%ecx, %ecx
	.p2align 4,,10
	.p2align 3
.L2:
	movl	%r8d, %eax
	shrl	%cl, %eax
	addl	$1, %ecx
	andl	$1, %eax
	addl	%eax, %edx
	cmpl	$32, %ecx
	jne	.L2
	movl	%edx, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
