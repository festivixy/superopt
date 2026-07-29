	.file	"smear_lowest_bit.c"
	.text
	.p2align 4
	.globl	smear_lowest_bit
	.def	smear_lowest_bit;	.scl	2;	.type	32;	.endef
	.seh_proc	smear_lowest_bit
smear_lowest_bit:
	.seh_endprologue
	movl	$-1, %eax
	movl	%ecx, %edx
	testl	%ecx, %ecx
	je	.L1
	testb	$1, %cl
	jne	.L7
	xorl	%ecx, %ecx
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L4:
	addl	$1, %ecx
	cmpl	$32, %ecx
	je	.L12
	movl	%r8d, %eax
	sall	%cl, %eax
	testl	%edx, %eax
	je	.L4
	subl	$1, %eax
	orl	%edx, %eax
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L12:
	movl	$-1, %eax
	ret
.L7:
	movl	%ecx, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
