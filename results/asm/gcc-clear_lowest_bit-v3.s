	.file	"clear_lowest_bit.c"
	.text
	.p2align 4
	.globl	clear_lowest_bit
	.def	clear_lowest_bit;	.scl	2;	.type	32;	.endef
	.seh_proc	clear_lowest_bit
clear_lowest_bit:
	.seh_endprologue
	movl	%ecx, %r9d
	andl	$1, %r9d
	jne	.L6
	xorl	%eax, %eax
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %eax
	cmpl	$32, %eax
	je	.L1
	shlx	%eax, %r8d, %edx
	testl	%ecx, %edx
	je	.L3
.L2:
	xorl	%edx, %ecx
	movl	%ecx, %r9d
.L1:
	movl	%r9d, %eax
	ret
.L6:
	movl	%r9d, %edx
	jmp	.L2
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
