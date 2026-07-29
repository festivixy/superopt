	.file	"isolate_lowest_zero.c"
	.text
	.p2align 4
	.globl	isolate_lowest_zero
	.def	isolate_lowest_zero;	.scl	2;	.type	32;	.endef
	.seh_proc	isolate_lowest_zero
isolate_lowest_zero:
	.seh_endprologue
	testb	$1, %cl
	je	.L5
	xorl	%eax, %eax
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %eax
	cmpl	$32, %eax
	je	.L10
	shlx	%eax, %r8d, %edx
	testl	%ecx, %edx
	jne	.L3
.L1:
	movl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	xorl	%edx, %edx
	movl	%edx, %eax
	ret
.L5:
	movl	$1, %edx
	jmp	.L1
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
