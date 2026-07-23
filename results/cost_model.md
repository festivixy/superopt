# Two definitions of optimal

Phases 3 and 4 pinned "optimal" to one meaning: the fewest instructions, with
constants free (CLAUDE.md section 7). That's the headline and it stays the
headline. This doc adds a second meaning, the lowest summed latency, and points
the synthesizer at a benchmark where the two disagree. On `x * 9`, counting
instructions picks a single multiply and counting latency picks a two-op
shift-and-add. Same spec, same proof machinery, two different winners.

## The weights

Every opcode carries a latency weight. Multiply weighs 3, everything else weighs
1. The numbers come from Agner Fog's instruction tables (agner.org/optimize) for
Intel Alder Lake, where a 32-bit `IMUL` has latency 3 and the ALU and shift
operations have latency 1. The exact table doesn't matter much for the result:
the flip survives on any core where multiply costs at least 2, which is every
mainstream x86 and ARM part I know of. This weighting models the latency of one
serial dependency chain and nothing else. It ignores throughput, instruction-level
parallelism, and macro-op fusion, all of which a real scheduler cares about and
none of which a single straight-line routine exposes.

## How cost-optimality is proven

A program's cost is the sum of its instruction weights, which is the total weight
of its opcode multiset. That identity leans on a premise from the encoder: the
Jha component-connection encoding wires every library component into the
program exactly once, the location variables are distinct and exactly fill the
component slots, so a synthesized program's cost always equals its library's
total weight. An optimal program has no dead code, since dropping an
unused instruction leaves a cheaper program computing the same thing. So the
cheapest program is realized by some multiset of components, and `synthesize_min_cost`
sweeps those multisets in nondecreasing weight order, calling the Phase 4b
component synthesizer on each. The first multiset that yields a verified program
gives the minimum cost, because every lighter multiset was already tried and
came back unsat. It's iterative deepening on weight instead of length, and it
runs at 32 bits with the constants left free for the solver to pick.

Zero-instruction programs cost 0, so they'd win outright if the sweep ever
considered them. It doesn't: `_libraries_by_cost` starts at one component, so
`synthesize_min_cost` structurally excludes the empty program before the search
begins. That's only safe if the spec truly needs an instruction, and confirming
that is the tests' job, not the sweep's. The identity check asks whether the
bare input already equals the spec and expects a counterexample; the
non-constancy check runs the spec on two inputs and confirms the outputs
differ, which kills any constant pass-through. All three flip tests,
`test_length_optimal_times_nine_is_the_multiply`,
`test_cost_optimal_times_nine_is_shift_add`, and
`test_the_two_definitions_disagree_on_times_nine`, run both checks before
making any claim below.

## The flip: x*9

Length-optimal `x * 9` is one instruction: `mul(x, 9)`, cost 3. The solver finds
the 9 on its own, from a one-component multiply library with a single free
constant.

Cost-optimal `x * 9` is two instructions: `shl(x, 3)` then `add(x, r0)`, which is
`x + (x << 3) = 9x`, cost 2. The solver finds the shift amount 3 the same way,
from a free constant. Two cheap operations beat one expensive one, 2 against 3.

Both programs are verified twice over. The SMT proof shows each equals the spec
on every 32-bit input, and the independent fuzzer agrees on 20,000 random cases.
The flip is real and it's plain: minimum instruction count picks the multiply,
minimum latency picks the shift-and-add.

Here's the same comparison across every benchmark in the suite:

| benchmark | length-optimal | latency-optimal | flip? |
|---|---|---|---|
| isolate_rmb | 2 instructions, cost 2 | same program | no |
| absval | 3 instructions, cost 3 | same program | no |
| popcount | no result (frontier) | no cost claim | — |
| x*9 | 1 instruction (mul), cost 3 | 2 instructions (shl, add), cost 2 | yes |

## The old benchmarks don't flip

Only multiply has a weight above 1, so for any MUL-free program the cost equals
the length exactly. That makes the Phase 5B floors do double duty. A program of
cost below `c` has fewer than `c` instructions, since every op weighs at least
1, and that holds no matter what ops are used, so a length floor at `c` is
always a cost floor at `c` too. What needs the multiply-free condition is the
other side: it's what makes the known program's own cost equal its length, so
that program meets the floor exactly instead of just sitting above it.

isolate_rmb's optimum is `neg` then `and`, two weight-1 instructions, cost 2.
`test_no_isolate_rmb_program_of_length_one_or_less` sweeps every one-op library
at 32 bits with free constants and gets unsat, so nothing of length one or cost
one exists, and 2 is the cost floor as well as the length floor. absval's optimum
is the three-instruction `ashr(x, x)`, `x xor r0`, `r1 sub r0`, all weight-1,
cost 3. `test_no_absval_program_of_length_two_or_less` sweeps every one-op and
two-op library and gets unsat, so 3 is the floor both ways. Neither benchmark
flips, because neither optimum spends a multiply. popcount has no converged
result at all, so it gets no cost claim, the same honest blank it already carries
in the length table.

## Honest framing

Cost-aware superoptimization is old ground. Massalin's 1987 superoptimizer
counted cycles, not instructions. STOKE (Schkufza, Sharma, Aiken, ASPLOS 2013)
optimized measured runtime directly with a random walk. Strength reduction,
turning a multiply into shifts and adds, is compiler folklore older than any of
this. The sweep here is iterative deepening by weight, adapted to the Jha 2010
component encoding the rest of the project already uses. Mine is the
implementation, the soundness argument as written for this encoder, and the
measurements, each one verified by the SMT proof and the fuzzer before it's
reported.
