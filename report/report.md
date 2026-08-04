# Superopt: a provably-optimal superoptimizer for short, loop-free integer and bitwise routines

## What this is about

Superopt takes a short, loop-free routine over integers and bit-vectors and returns
the shortest program that computes the same thing, along with a proof that no
shorter program exists. It is the latter aspect that sets superoptimization apart
from normal compilation. At optimization level -O3, an optimizing compiler tries
many rewriting tricks and stops when nothing more can be done; it does not
guarantee nor prove optimality. Superoptimization, as defined by Massalin in 1987,
asks a much more stringent question: among all programs that can be written in a
given fixed instruction set, which one is the shortest that computes a given
function?

In order to give an answer to this question, it is necessary to give a precise
definition of "the same function" and testing alone cannot be used for this purpose.
Two programs are equal if they compute the same result for every possible input.
With a single 32-bit input, there are already over four billion inputs and the
addition of a second input makes this even larger. Superopt does not execute code
during the search process. Instead, it encodes each program in bit-vector form and
hands both encodings to Z3, a satisfiability modulo theories (SMT) solver, in a
single query asking whether there is any possible input at which the programs
diverge. Z3 operates on formulas over fixed-width machine integers, not just
booleans.

We are asking whether there is an input on which the two programs disagree. Z3 will
return UNSAT (no such input exists) if the two programs are equivalent; otherwise
it returns SAT and gives an explicit counterexample.

All else follows from this. I have implemented the system myself, in Python and
Z3, in six phases. One result puts into perspective the scale of the difference:
for a simple function that clears the lowest set bit, gcc -O3 takes 18
instructions while clang -O3 takes 98, whereas superopt can compute it in 2
instructions, and shows that 1 is not enough.

## Background and prior work

Massalin (1987) pioneered the approach by exhaustive search of short sequences of
Motorola 68000 instructions, measuring their cycle count against the target function
and choosing the shortest one. This is a seminal point, the idea that a program can
be synthesized through exhaustive search, not merely transformed.

Counterexample-guided inductive synthesis, or CEGIS, comes from Solar-Lezama et
al. (2006; 2008). In the context of synthesis, two quantifiers define the goal: there
exists a program that for all inputs matches the specification. This is a difficult
thing to do in a solver, so CEGIS reduces it to two questions: a finite-synthesis
query that finds a program matching the specification on a given set of example
inputs (an existential problem), and a verification query that checks the
candidate against all inputs. In case of failure, the counterexample is added to
the set of examples and the loop repeats; usually it     converges quickly as each
counterexample excludes a family of candidates.

I have used the encoding suggested by Jha et al. (2010). The form of the encoding
enables the solver to choose from a fixed set of components plus one location
variable for each component output and input, where the input location represents
the index of the line from which the operand is taken. The solver chooses the wiring
connections and any unknown constant operands in a single query.

STOKE (Schkufza, Sharma and Aiken, 2013) is a good contrast in its own right. It
randomly walks over program space, scoring by a mixture of correctness and runtime
measurement, and drops the optimality proof.

There are two other sources to note which are not foundational. The benchmarks are
taken from Warren's Hacker's Delight, and the per-opcode latency weights in the
model are taken from Fog's instruction tables. See the references below and
docs/references.md for all the sources.

The techniques here are not novel. What is mine is the intermediate
representation, the encoder, the implementation, the soundness arguments for this
encoder, and all of the measurements below.

## The approach

Intermediate representation (IR) is the data structure used by the rest of the
system. A program in the IR is a straight-line sequence of fixed-width bit-vector
instructions with one output, no branches, no memory accesses, and no floating-point.
An operand is one of three fixed data types: an input register, a constant, or the
output of an earlier instruction. The semantics is evaluated by a simple Python
interpreter that masks every intermediate value to the register width.

The encoder maps a program from the IR to a Z3 bit-vector formula one opcode
at a time. The function equivalent(a, b) creates the query described above, with
UNSAT standing for equivalence and SAT standing for counterexample. Since an error in
the encoder would render all results useless, the encoder and interpreter are
checked against each other first: test_encoder_matches_interpreter generates 1,000
programs at random and executes each one on 100 random inputs (100,000 tests total)
to check that the encoder and the interpreter agree on every result and that every
opcode in the set is used at least once.

Phase 3 had to be as simple as possible and was very low-risk. The program
enumerator generated programs by increasing length and checked each one for
equivalence with the specification through exhaustive evaluation at 8-bit width
(256 inputs). The first match guarantees minimality through shortest-first search
of the search space. The program x & -x turned out to be optimal with length 2.

Phase 4 replaces the enumerator with the component encoding and the CEGIS loop. As
a result, the power of the search increases. In the resulting formula,
an unknown constant is a free bit-vector variable that the solver can assign.
Consequently, it becomes possible to find the values that are impossible to guess
by an enumeration, such as 0xAAAAAAAA in case of x & C with C free. This is a very
good argument in favor of using a solver in building a superoptimizer.

There are two layers that ensure that the results are sound. The program must
clear two layers in order to be optimal: the SMT proof and a random-input fuzzer
that tests the generated program against the original Python benchmark.
These layers make different mistakes deliberately: if the encoder fails to
translate an opcode correctly, then the SMT proof will prove a wrong program
equivalent to a wrong formula, and the fuzzer will catch this mistake by running
the program directly.

## Implementation walk

Most of the implementation is straightforward. There are four important pieces.

The first piece is the wiring, in superopt/cegis.py. Each component gets an output
location and one input location per operand. The well-formed constraint ensures that
the output locations are a proper permutation of lines so that every line is defined
exactly once, and each input location points to something earlier in the chain so
that acyclicity is enforced. In addition to that, a separate constraint binds each
component input to the value on its line. Here a hidden mistake may reside: an
incorrect constraint may return an incorrect or no answer. Locations are encoded in
small bit-vectors using unsigned comparison constraints (ULT, UGE) instead of full
comparison on integers in order to stay in the theory of bit-vectors that Z3 can
efficiently solve.

The second piece that requires attention is in superopt/encode.py. A Z3 BitVecRef
has Python >> operator that performs arithmetic shift and preserves the sign bit,
so a logical shift right has to be done by LShR(). The two agree on inputs where
the sign bit is zero, hence an easy-to-miss bug in the minimality claim for a
shifting program.

The third is the method of showing the lower bound, which is separate from
minimization itself. Showing that a length-2 program is optimal implies showing that
there is no length-1 program that computes the same function, and the component
encoding supplies this argument. Since every component is used exactly once, a
library of size k results in programs of exactly k instructions. Thus checking all
libraries of size k checks all programs of length k. With 11 opcodes there are 11
libraries of size one, 77 of size two, and 363 of size three. Checking all of
them at 32-bit width with free constants and getting UNSAT for each one is what
"proven" stands for in the table below.

The fourth and final piece is latency and it is the basis of the cost model. The
cost of a program is the sum of its opcode weights, which is the weight of its
opcode multiset. An optimal program has no dead code, since removing an unused
instruction would give a cheaper program computing the same function. Thus we
enumerate opcode multisets in increasing weight and run the component synthesizer on
each one. The first success is cost-optimal; lighter multisets have been proven
irrelevant. See superopt/cost.py where this is implemented as a weight-order
iterative deepening. Programs of length zero are filtered out and the behavior
tested.

## Evaluation

Fourteen benchmarks were measured.

| Benchmark | gcc -O3 base | gcc -O3 v3 | clang -O3 base | clang -O3 v3 | superopt |
|-|-|-|-|-|-|
| absval | 3 | 3 | 3 | 3 | 3 (proven) |
| avg_ceil | 4 | 4 | 5 | 5 | 4 (best found) |
| avg_floor | 4 | 4 | 4 | 4 | 4 (best found) |
| bswap32 | 2 | 2 | 2 | 2 | 9 (verified upper bound) |
| clear_lowest_bit | 18 | 16 | 98 | 98 | 2 (proven) |
| flp2 | 13 | 14 | 93 | 93 | 12 (verified upper bound) |
| isolate_lowest_zero | 14 | 15 | 96 | 96 | 3 (best found) |
| isolate_rmb | 14 | 14 | 97 | 97 | 2 (proven) |
| popcount | 11 | 25 | 79 | 24 | no result (frontier) |
| rotl5 | 2 | 1 | 2 | 1 | 3 (proven) |
| sign | 6 | 6 | 5 | 5 | 4 (best found) |
| smear_lowest_bit | 19 | 17 | 97 | 97 | 2 (proven) |
| times_nine | 1 | 1 | 1 | 1 | 1 (proven) |
| turn_off_trailing_ones | 14 | 12 | 96 | 96 | 2 (proven) |

Notes:
- In the superopt column, there are four labels: proven: a full floor sweep at 32-bit width with free constants found UNSAT for all smaller libraries; best found: a program found and verified in both layers but the floor sweep not completed; verified upper bound: a hand-crafted IR program was exhaustively evaluated at small widths and fuzzed at 32-bit width without proving optimality; no result: the synthesizer did not converge.

Findings:
- There are five benchmarks where the pattern of a naive loop for bit-operation is not optimized away by either compiler, but superopt finds a two- or three-instruction program, proven minimal in four of the five cases (such as x & -x at length 2; isolate_lowest_zero remains best found). The result suggests a general deficiency of compilers in handling some loop patterns.
- Some cases go to the side of the compilers, since x86 supports rotate and byte-swap operations, so they can beat the IR on those particular tasks.
- The cost model (opcode weights) is different from the minimal instruction count and gives different results for the optimal program.

More details in two documents: results/compiler_gap.md (method, assembly reading, floor certification) and results/cost_model.md (weights, soundness of weight-order sweep, benchmark comparisons).

## What broke and what it taught

The most valuable mistake in the experiment was a one-line error.
In phase 4b, the width of the location variables was chosen as `(n_lines - 1).bit_length()`, enough for every line index but not for the exclusive bound to which the indexes are compared against. If the library's line count was a power of two, the constant in `ULT(var, n_lines)` rounded to zero at this width, since no unsigned value can be less than zero; consequently, the well-formedness constraint becomes unsatisfiable and `synthesize` returns `None`.

That is possible because `None` is a valid answer. It means no program of the requested shape exists, exactly what a floor sweep expects from every library. The most frequently met configuration in the sweeps is one input, one constant and two operations occupying 4 lines; that made the single-operation stage of every floor sweep vacuously unsatisfiable, and the floors of absval, isolate_rmb and times_nine, together with the weight-1 stage of the cost sweep, rested partly on thin air.

There is no assertion in the suite that can detect that, but the signal came from timing: floor stages finished in 0.02 seconds. In a pipeline whose output is a proof, a negative result arriving implausibly fast requires investigation. The fix was the one-line change
`loc_width = max(1, n_lines.bit_length())` (commit 9780477), along with a regression test asserting the positive direction, since no assertion about `None` can distinguish a true negative from a false one;
`test_synthesizes_when_line_count_is_a_power_of_two` synthesizes `x & (x-1)` from the 4-line configuration that had been failing. Then the default suite was rerun fully and passed green, since the sweeps now actually ran solver work but returned `None` from every library, and so the published claims survived re-validation on genuine evidence. A later commit (75f4d0d) dropped a workaround in three survey tests, where an implementer had raised `n_constants` from 1 to 2 after finding that 1 "does not work", which incidentally moved the line count to 5 and bypassed the bug.

The second limit is a matter of scale rather than of correctness. Full SWAR population count is the end of the component synthesizer. At 8 bits, even with bit-vector locations, symmetry breaking on interchangeable components and the shift amounts fixed so that only the masks are left free, the CEGIS loop did not converge: per-round synthesis cost grows as counterexamples accumulate, reaching 0.06s, 0.1s, 3.9s, 11s and 27s on the first five examples and then rising above any useful budget, since each round needs to find one wiring correct on all accumulated inputs at once. The two popcount rungs are included in the suite, labeled `slow` and deselected by default.

The third discovery goes against my expectations that the cost of a floor sweep should track the number of libraries in it. Three sweeps involving exactly 77 libraries, following the same code path at the same width and with the same constant budget, behave completely differently: absval finishes inside the default suite, rotl5 takes 20.7 seconds and is labeled `slow`, and isolate_lowest_zero runs for hours without finishing. The sweeps for sign, avg_floor and avg_ceil, featuring 363 libraries each, were still running after 35 minutes. These four floor tests were deleted (commit 30c9cb3) and their rows downgraded to best found, since a test never seen to pass cannot ship as an assertion. Two alternatives were tested and ruled out first: pre-seeding each sweep with 16 random examples increased the per-call cost and still failed to finish in 10 minutes, and the doubly-quantified query posed to Z3 directly returned `unknown` at a 60-second timeout on the libraries with ADD, which is not a floor. The spread itself is the result, since it makes certification cost a function of the specification rather than of the size of the search space, and so a row's tier cannot be predicted in advance. The hypothesis is near-solution density, since libraries selected from the ADD and AND families contain four free constants and can stay consistent with many example sets before finally becoming unsatisfiable, but the rounds per library remain uninstrumented.

The final item is a smaller failure with a sharp lesson. The branchless folklore trick for signed minimum, `y + ((x-y) & ((x-y) >> 31))`, is incorrect: in case of overflow, the sign mask is based on the wrapped value and the selection goes in the opposite direction, so that at `x = 0x80000000` and `y = 1`, the expression produces 1 instead of `INT_MIN`. I tried to prove this with `equivalent()`, because a counterexample returned by the solver is a proof of the incorrectness while the fuzzer's hit is just a witness, but I could not. The signed minimum requires a comparison or a branch operation, the IR lacks both and so there is no IR program to place on the other side of the query. The layer that usually catches mistakes of this kind fails exactly at the point where folklore is most likely to be wrong, and the independent fuzzer detected the defect instead (`test_folklore_min_trick_is_wrong`, 100,000 trials, plus the directed counterexample above). That is the strongest argument I have for having two verification layers, and a concrete example of the IR's limited scope.

## Honest framing and limits

The technique is not mine. CEGIS was invented by Solar-Lezama and colleagues, the
component-based encoding by Jha and colleagues, and cost-directed superoptimization goes back to Massalin and was extensively pursued by STOKE. What is mine is the IR, the interpreter, the encoder, the equivalence check, the soundness arguments as given for this encoder, the selection of benchmarks, and the numbers.

Scope is narrow by design: the IR has no comparisons, no branches, no memory, no floating point, and a single output. Each omission is a research problem in its own right, and the folklore minimum case above is a concrete bill for two of them.

Optimality is always relative to the instruction set. rotl5 is proven optimal at 3 but still loses to a compiler with a rotate instruction. The three-instruction absval program employs `ashr(x, x)`, which is correct under the saturating over-width shift semantics of the IR matching Z3's `bvashr`, unlike the `sar` of x86 that masks the amount modulo 32; the program is thus correct in the IR but not portable to hardware. Instruction count is also not latency. The gap table counts instructions, while the cost model counts weighted latency, and times_nine is the divergence point: on that row gcc emits a single `lea`, which has latency 1, so under the latency model the compiler's one instruction is better than either program superopt generated.

The measurements are performed on one machine. gcc is MinGW-W64 13.2.0 and runs locally, so its columns regenerate on each run of the script; clang 22.1.0 is included as 28 Compiler Explorer snapshots of a single build, so these columns change only when I refetch them. No MSVC build and no non-x86 target is measured. Fourteen benchmarks taken largely from *Hacker's Delight* feature a known bias towards functions with a short branchless form, which is the right bias to ask whether the compiler recovered an identity and the wrong one to estimate how often such code occurs in practice.

## Reproducibility

The suite is the artifact. A fresh checkout on Python 3.11 or newer reproduces all the above numbers:

```bash
git clone https://github.com/festivixy/superopt.git
cd superopt
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -e ".[dev]"
pytest
```

`pytest` will report 109 passed and 3 deselected tests. The three deselected tests are marked `slow`: the two popcount rungs, which record the frontier rather than pass fast, and the `rotl5` floor sweep, which takes 20.7 seconds on its own. `pytest -m slow` runs them.

## References

de Moura, Bjørner. *Z3: An Efficient SMT Solver*. TACAS 2008.
https://doi.org/10.1007/978-3-540-78800-3_24

Fog. *Instruction Tables*. Technical University of Denmark, updated 2025.
https://www.agner.org/optimize/instruction_tables.pdf

Jha, Gulwani, Seshia, Tiwari. *Oracle-Guided Component-Based Program
Synthesis*. ICSE 2010. https://doi.org/10.1145/1806799.1806833

Massalin. *Superoptimizer: A Look at the Smallest Program*. ASPLOS 1987.
https://dl.acm.org/doi/10.1145/36206.36194

Schkufza, Sharma, Aiken. *Stochastic Superoptimization*. ASPLOS 2013.
https://doi.org/10.1145/2451116.2451150

Solar-Lezama, Tancau, Bodík, Seshia, Saraswat. *Combinatorial Sketching for
Finite Programs*. ASPLOS 2006. https://doi.org/10.1145/1168857.1168907

Solar-Lezama. *Program Synthesis by Sketching*. PhD thesis, UC Berkeley, 2008.
https://people.csail.mit.edu/asolar/papers/thesis.pdf

Warren. *Hacker's Delight*, 2nd edition. Addison-Wesley, 2012. ISBN
978-0321842688.
