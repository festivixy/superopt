# Two definitions of optimal

Phases 3 and 4 have locked down one definition of "optimal": the minimal
instruction count with the constants still unconstrained (CLAUDE.md, section
7). It continues to be the principal definition. This document proposes a
second definition, the minimal latency, and describes a benchmark in which the
two definitions lead to different results. The multiplication of x by 9 takes
one instruction counted by instruction count, and two instructions counted by
latency: two operation shift-and-add.

## Weights

Every opcode has an associated latency weight. The weight is 3 for
multiplication, and the weight is 1 for everything else. Weights are taken from
Agner Fog's instruction tables (agner.org/optimize) for Intel Alder Lake.
There, a 32-bit IMUL has latency 3, and ALU and shift operations have latency
1. The precise numbers in this table do not matter for the main conclusion: the
main conclusion applies to any architecture in which multiplication has latency
at least 2 (including the mainstream x86 and ARM cores I checked). Weights
reflect the latency of a single sequential dependency chain, ignoring the
effect of throughput, instruction level parallelism, and macro-op fusion, which
are considered by a real-world scheduler but are not visible in a straight-line
code routine.

## Proving cost-optimality

Cost of a program is the sum of the opcode weights, the same thing as the
weight of the opcode multiset in the program. This equality follows from the
encoder premises: the Jha component-connection encoding connects every library
component to the program exactly once, and the location variables are unique
and occupy the corresponding slots. Therefore, the cost of the synthesized
program is equal to the weight of the library. Any optimal program does not
contain dead code, and removal of any unused instruction makes the program
cheaper without changing the functionality. Thus, the cheapest program
corresponds to some opcode multiset, and synthesize_min_cost enumerates opcode
multisets in the increasing weight order, using the Phase 4b component
synthesizer on each of them. The first multiset that gives the synthesized
verified program is the optimal multiset, as any lighter multiset has already
been tried and found unsatisfiable. This is an example of iterative deepening
by weight rather than by length, performed at 32-bit precision with free
constants.

Zero-length programs have cost 0, so they would provide a win. They are not
considered by the sweep, though: `_libraries_by_cost` starts with one-component
libraries, so synthesize_min_cost explicitly excludes the empty program from
the search. This exclusion is legitimate if and only if the specification
requires at least one instruction. Verification of this requirement is the task
of the tests rather than the sweep itself. The identity check checks whether
the bare input satisfies the specification, and thus anticipates
counterexamples; the non-constancy check executes the specification on two
inputs and makes sure that the outputs are different, thus excluding any
constant pass-through. All three tests,
test_length_optimal_times_nine_is_the_multiply,
test_cost_optimal_times_nine_is_shift_add, and
test_the_two_definitions_disagree_on_times_nine, perform both checks before
making any statements below.

## The flip: x*9

For length optimality, x * 9 requires one instruction: mul(x, 9), with cost 3.
The solver finds the constant 9 in a one-component multiply library with a free
constant.

For latency optimality, x * 9 requires two instructions: shl(x, 3) followed by
add(x, r0), so x + (x << 3) = 9x, with cost 2. The solver finds the shift
amount 3 as a free constant in the two-component shift-and-add library that the
sweep reaches at weight 2. In this case, two cheap instructions outperform one
costly multiplication.

Both programs are verified twice: with the SMT proof that the program is equal
to the specification for all 32-bit inputs, and with an independent fuzzer that
checks for equivalence across 20,000 random cases. The difference is clear and
obvious: minimal number of instructions prefers multiplication, while minimal
latency prefers the shift-and-add combination.

A cross-benchmark perspective is provided below:

| benchmark | length-optimal | latency-optimal | flip? |
|---|---|---|---|
| isolate_rmb | 2 instructions, cost 2 | identical program | no |
| absval | 3 instructions, cost 3 | identical program | no |
| popcount | no result (frontier) | no cost claim | — |
| x*9 | 1 instruction (mul), cost 3 | 2 instructions (shl, add), cost 2 | yes |

## The old benchmarks do not flip

As the only operation with weight greater than 1 is multiplication, any program
that does not contain multiplication has cost equal to its length. The Phase 5B
floors therefore serve as double-duty constraint: a program with cost less than
c has fewer than c instructions regardless of its actual operations. The
necessity of the multiply-free constraint is thus confined to the reverse
direction: it is what makes the cost of the known program equal to its floor.

In isolate_rmb, the optimum is neg followed by and: two weight-1 instructions,
and the cost is 2. The test test_no_isolate_rmb_program_of_length_one_or_less
that searches all one-operation libraries at 32-bit precision with free
constants finds no solution, so there is no one-operation or cost-1 program,
and 2 is both the cost floor and the length floor. For absval, the optimum is
the three-instruction sequence: ashr(x, x), x xor r0, r1 sub r0, all weight-1,
with the cost of 3. The test test_no_absval_program_of_length_two_or_less that
searches all one- and two-operation libraries similarly finds no solution, so 3
is the floor in both metrics. Both benchmarks do not flip, as their optimum
does not use multiplication. The popcount benchmark has no converged result and
thus has no corresponding cost claim, maintaining the honesty of the length
table.

## Honest framing

Cost-aware superoptimization is known technique. In his 1987 paper, Massalin
superoptimized cycle counts, not instruction counts. STOKE (Schkufza, Sharma,
Aiken, ASPLOS 2013) optimized measured runtime directly using a random walk
approach. Strength reduction, that is, replacement of multiplications with
shift-and-adds, is compiler lore, preceding this work. The current sweep uses
iterative deepening by weight applied to the Jha 2010 component encoding used
by the rest of the project. The current contribution includes the
implementation, the formal soundness argument for this particular encoder, and
the corresponding measurements, each verified by SMT proofs and fuzzers prior
to reporting.
