	.file	"turn_off_trailing_ones.c"
	.text
	.p2align 4
	.globl	turn_off_trailing_ones
	.def	turn_off_trailing_ones;	.scl	2;	.type	32;	.endef
	.seh_proc	turn_off_trailing_ones
turn_off_trailing_ones:
	.seh_endprologue
	movl	%ecx, %edx
	movl	%ecx, %eax
	andl	$1, %edx
	je	.L2
	xorl	%ecx, %ecx
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %ecx
	xorl	%edx, %eax
	cmpl	$32, %ecx
	je	.L2
	movl	%r8d, %edx
	sall	%cl, %edx
	testl	%eax, %edx
	jne	.L3
.L2:
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
