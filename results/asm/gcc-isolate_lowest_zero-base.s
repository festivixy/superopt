	.file	"isolate_lowest_zero.c"
	.text
	.p2align 4
	.globl	isolate_lowest_zero
	.def	isolate_lowest_zero;	.scl	2;	.type	32;	.endef
	.seh_proc	isolate_lowest_zero
isolate_lowest_zero:
	.seh_endprologue
	movl	%ecx, %edx
	testb	$1, %cl
	je	.L5
	xorl	%ecx, %ecx
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %ecx
	cmpl	$32, %ecx
	je	.L10
	movl	%r8d, %eax
	sall	%cl, %eax
	testl	%edx, %eax
	jne	.L3
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	xorl	%eax, %eax
	ret
.L5:
	movl	$1, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
