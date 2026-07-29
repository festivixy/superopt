	.file	"turn_off_trailing_ones.c"
	.text
	.p2align 4
	.globl	turn_off_trailing_ones
	.def	turn_off_trailing_ones;	.scl	2;	.type	32;	.endef
	.seh_proc	turn_off_trailing_ones
turn_off_trailing_ones:
	.seh_endprologue
	movl	%ecx, %eax
	andl	$1, %ecx
	je	.L2
	xorl	%edx, %edx
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %edx
	xorl	%ecx, %eax
	cmpl	$32, %edx
	je	.L2
	shlx	%edx, %r8d, %ecx
	testl	%eax, %ecx
	jne	.L3
.L2:
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
