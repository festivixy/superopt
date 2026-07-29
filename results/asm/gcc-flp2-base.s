	.file	"flp2.c"
	.text
	.p2align 4
	.globl	flp2
	.def	flp2;	.scl	2;	.type	32;	.endef
	.seh_proc	flp2
flp2:
	.seh_endprologue
	movl	%ecx, %edx
	testl	%ecx, %ecx
	js	.L5
	movl	$31, %ecx
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	subl	$1, %ecx
	jb	.L7
	movl	%r8d, %eax
	sall	%cl, %eax
	testl	%edx, %eax
	je	.L3
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	xorl	%eax, %eax
	ret
.L5:
	movl	$-2147483648, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
