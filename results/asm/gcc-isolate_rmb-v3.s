	.file	"isolate_rmb.c"
	.text
	.p2align 4
	.globl	isolate_rmb
	.def	isolate_rmb;	.scl	2;	.type	32;	.endef
	.seh_proc	isolate_rmb
isolate_rmb:
	.seh_endprologue
	movl	%ecx, %edx
	andl	$1, %edx
	jne	.L1
	xorl	%eax, %eax
	movl	$1, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %eax
	cmpl	$32, %eax
	je	.L7
	shlx	%eax, %r8d, %edx
	testl	%ecx, %edx
	je	.L3
.L1:
	movl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	xorl	%edx, %edx
	movl	%edx, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
