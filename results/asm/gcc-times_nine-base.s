	.file	"times_nine.c"
	.text
	.p2align 4
	.globl	times_nine
	.def	times_nine;	.scl	2;	.type	32;	.endef
	.seh_proc	times_nine
times_nine:
	.seh_endprologue
	leal	(%rcx,%rcx,8), %eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
