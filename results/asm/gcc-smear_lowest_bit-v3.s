	.file	"smear_lowest_bit.c"
	.text
	.p2align 4
	.globl	smear_lowest_bit
	.def	smear_lowest_bit;	.scl	2;	.type	32;	.endef
	.seh_proc	smear_lowest_bit
smear_lowest_bit:
	.seh_endprologue
	movl	$-1, %eax
	testl	%ecx, %ecx
	je	.L1
	testb	$1, %cl
	jne	.L7
	xorl	%eax, %eax
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L4:
	addl	$1, %eax
	cmpl	$32, %eax
	je	.L12
	shlx	%eax, %r8d, %edx
	testl	%ecx, %edx
	je	.L4
	leal	-1(%rdx), %eax
	orl	%ecx, %eax
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
