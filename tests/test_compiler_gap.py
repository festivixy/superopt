from __future__ import annotations

from scripts.compiler_gap import count_instructions

FIXTURE = """\
\t.file\t"absval.c"
\t.text
\t.globl\tabsval
\t.def\tabsval;\t.scl\t2;\t.type\t32;\t.endef
absval:
\tmovl\t%ecx, %eax
\tnegl\t%eax
\tcmovs\t%ecx, %eax
\tret
\t.ident\t"GCC: 13.2.0"
"""

CLANG_STYLE = """\
# compiler: clang 18.1.0
# flags: -O3 -march=x86-64
absval:
\tmovl\t%edi, %eax
\tnegl\t%eax
\tcmovsl\t%edi, %eax
\tretq
.Lfunc_end0:
\t.size\tabsval, .Lfunc_end0-absval
"""


def test_counts_instructions_and_skips_ret():
    assert count_instructions(FIXTURE) == 3


def test_counts_clang_style_with_comment_header_and_retq():
    assert count_instructions(CLANG_STYLE) == 3


def test_empty_asm_counts_zero():
    assert count_instructions("\t.text\nlabel:\n\n") == 0
