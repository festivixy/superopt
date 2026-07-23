	.file	"absval.c"
	.text
	.p2align 4
	.globl	absval
	.def	absval;	.scl	2;	.type	32;	.endef
	.seh_proc	absval
absval:
	.seh_endprologue
	movl	%ecx, %eax
	negl	%eax
	cmovs	%ecx, %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
