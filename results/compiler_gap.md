# The compiler gap

What this measures, in one sentence: given the same naive algorithm, how many
instructions `-O3` emits versus the proven minimum superopt finds.

## Method

Both sides start from the same naive source. superopt reads the Python reference
spec; gcc and clang get a line-for-line naive C translation of that same spec.
The point isn't to hand a compiler the trick and watch it copy it back. The
question is who recovers the trick from the dumb form, so both sides have to
start dumb.

The count is every instruction in the function body except `ret`, applied by
`scripts/compiler_gap.py` and checked by `tests/test_compiler_gap.py`. The
benchmarks compile to leaf functions with no prologue, so the body is
unambiguous and the rule can't drift from one benchmark to the next by being
applied by eye.

There are two compiler columns, not one. The baseline `x86-64` column is the
headline. The `-march=x86-64-v3` column is here because that feature level turns
on BMI1 and POPCNT, and with those the ISA can absorb a whole trick into a
single instruction: `blsi` for isolate-rightmost-bit, `popcnt` for population
count. That's a hardware story, not a code-generation one, so both columns
appear and neither hides the other.

superopt's number is IR instructions with constants free, which is the project's
definition of optimal. A superopt count lands in the table only with both layers
behind it: the SMT proof that it equals the spec on every input, and a pass from
the independent fuzzer.

Versions: local gcc is `gcc (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht
Sanders, r8) 13.2.0`; clang is 22.1.0, fetched from Compiler Explorer. The local
gcc snapshots use the MinGW/Windows ABI and the godbolt clang snapshots use
SysV, which changes which registers hold the arguments but not the instruction
counts, so it doesn't affect the comparison.

<!-- gap-table:begin -->
| benchmark | gcc -O3 base | gcc -O3 v3 | clang -O3 base | clang -O3 v3 | superopt (proven minimum) |
|---|---|---|---|---|---|
| absval | 3 | 3 | 3 | 3 | **3** (proven) |
| isolate_rmb | 14 | 14 | 97 | 97 | **2** (proven) |
| popcount | 11 | 25 | 79 | 24 | no result (frontier) |

Local gcc: `gcc (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r8) 13.2.0`. Counting rule: every
instruction in the function body except `ret`; applied by
`scripts/compiler_gap.py`, tested in `tests/test_compiler_gap.py`.
<!-- gap-table:end -->

## Reading the rows

### isolate_rmb

Neither compiler recovers `x & -x` from the naive loop. gcc keeps the loop: a
14-instruction scan that walks bit positions looking for the first set bit. Base
and v3 both land at 14, but they aren't the same 14. The baseline shifts with
`sall %cl`; v3 swaps in the BMI2 `shlx`, so the v3 build does use the newer
instructions, it just spends them inside the same loop instead of collapsing it
to `blsi`. clang goes the other way and fully unrolls, 97 instructions, a
`mov`/`test`/`jne` block per bit position. superopt returns 2, `neg` then
`and`, which is `x & -x`. The length-2 optimum is the original Phase 3 milestone,
`test_isolate_rmb_rediscovers_two_instruction_trick` with the length-1 floor from
`test_no_single_instruction_program_matches_isolate_rmb`, both 8-bit and
constant-free. `test_no_isolate_rmb_program_of_length_one_or_less` now carries the
floor at 32-bit with free constants, sweeping every single-op component library
and getting unsat, the same component-exhaustion argument the absval row uses.
That component-library floor is stronger than the Phase 3 enumeration because it
covers constants and runs at the full width.

### absval

This one's a tie. gcc and clang both go branchless and both land at 3, and
superopt's proven minimum is also 3. The compilers use the same shape: `mov`,
`neg`, then `cmovs`, a conditional move on the sign flag, identical across base
and v3 for both. They don't use the sar/xor/sub form at all.

superopt finds a different 3-op program, and it's constant-free. The wiring is
`ashr(x, x)`, then `x xor r0`, then `r1 sub r0`. The first instruction is the
interesting one. Shifting `x` arithmetically by `x` itself builds the sign mask.
Split it by the value of `x`. For `x` from 0 to 31 the shift amount is in range,
and since `x < 2^x` every set bit shifts off the low end, so the result is 0. For `x`
of 32 and up the shift is over-width, and the IR's ASHR saturates a non-negative
value to 0, so those land at 0 too. A negative `x` saturates the other way: its
shift amount read as unsigned is at least 2^31, well past the width, so the
arithmetic shift fills with all-ones. That gives 0 for non-negative inputs and -1
for negative ones, which is exactly the mask the classic `(x ^ mask) - mask`
absolute-value trick wants, without ever naming the constant 31.

One caveat, and it matters. That saturating over-width shift is the IR's
semantics, matching Z3's `bvashr`. x86's `sar` masks the shift amount mod 32
instead, so the variant breaks on x86 at both ends. A negative `x` would shift by
`x & 31` rather than saturate, and the mask comes out wrong. A non-negative `x` of
32 and up breaks too: `x = 32` masks to a shift of 0, so `sar` returns 32 where
the IR gives 0. The variant is correct in the project's IR and proven there; it
just isn't x86-portable. The optimality claim is scoped to the project's
instruction set either way, which is what the CLAUDE.md definition of optimal says.
`test_synthesizes_branchless_absval_at_32_bit`
verifies the 3-op program over all 32-bit inputs, and
`test_no_absval_program_of_length_two_or_less` sweeps every one-op and two-op
component library and gets unsat everywhere, so 3 is the proven floor.

### popcount

The honest row, where superopt has no answer and the compilers spread out. gcc
base keeps the loop but compacts it hard, 11 instructions running the naive
32-iteration shift-mask-add. It's a rolled loop, not the SWAR bit-twiddle and not
`popcnt`. gcc v3 doesn't reach for `popcnt` either; it vectorizes, 25 AVX2
instructions that broadcast `x` across a vector, shift each lane by a different
amount, mask, and add-reduce. clang base fully unrolls into a 79-instruction
`bt`/`adc` carry chain, testing each bit and folding it into an accumulator
through the carry flag. clang v3 does the AVX2 thing more tightly, 24
instructions. So even at v3, with `popcnt` sitting in the ISA, neither compiler
recognizes the idiom from this naive loop.

superopt has no converged result here. Full SWAR popcount is the measured
frontier of the component synthesizer, recorded in the Phase 4b DECISION_LOG
entry: the per-round synthesis cost explodes as counterexamples accumulate and
the loop never finishes. The two popcount rungs stay in the suite marked `slow`,
deselected by default, documenting the wall rather than hiding it.

## Limits

One local compiler, gcc MinGW 13.2.0, with clang supplied as checked-in Compiler
Explorer snapshots. No MSVC. Three benchmarks, not a suite. And the whole table
counts instructions, which isn't latency: a 3-instruction sequence with a slow
multiply can lose to a longer one built from cheap shifts. That second reading
exists now, in `results/cost_model.md`: the compiler columns above still count
instructions, and it's the cost doc that runs the comparison the other way.
