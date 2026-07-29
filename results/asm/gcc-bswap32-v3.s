	.file	"bswap32.c"
	.text
	.p2align 4
	.globl	bswap32
	.def	bswap32;	.scl	2;	.type	32;	.endef
	.seh_proc	bswap32
bswap32:
	.seh_endprologue
	movl	%ecx, %eax
	bswap	%eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0"
