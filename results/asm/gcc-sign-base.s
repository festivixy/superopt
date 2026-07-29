	.file	"sign.c"
	.text
	.p2align 4
	.globl	sign
	.def	sign;	.scl	2;	.type	32;	.endef
	.seh_proc	sign
sign:
	.seh_endprologue
	xorl	%eax, %eax
	testl	%ecx, %ecx
	je	.L1
	movl	%ecx, %eax
	sarl	$31, %eax
	orl	$1, %eax
.L1:
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
