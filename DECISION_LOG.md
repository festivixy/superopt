# Decision log

Why each non-obvious choice was made. Newest entry first.

## The shift-semantics study

- **The default remains SATURATE, as it is aligned with the Z3 semantics for the purpose of the byte-by-byte consistency of the default code path of the encoder.** MASK is the opt-in parameter per run.
- **Mask enforces the power of two widths, since amount & (width − 1) equals amount mod width only in such cases.** All benchmarks use the widths which are power of two, and allowing other widths without testing is dangerous.
- **Comprehensive cross-checking is retained as the sole safeguard.** An incorrectly encoded MASK shift would silently poison the impossibility claims made in this paper.

## Phase 5B, Stage A: the gap survey

- **Superopt's column is graded because one column was stating four different things.** With three benchmarks, every row was either proven or had its popcount field empty, giving one honest label. With fourteen rows this was not the case anymore. The grading is made from: proven (synthesis plus a completed component-library floor sweep at 32-bit with free constants), best found (synthesis plus both verification layers, no completed floor), verified upper bound (a hand-built IR program analyzed exhaustively at small widths and fuzzed at 32, with no minimality claim), and no result. Seven rows are proven, four are best found, two are verified upper bound, and one is no result. The label is recorded as data in the SUPEROPT dictionary in scripts/compiler_gap.py file, ensuring that regeneration agrees with the table, not diverges into a narrative.
- **Verified upper bound rows don't have SMT layer because this is a structural deficiency.** The equivalent() function compares two IR programs. Bswap32 and flp2 contain only one chain, a hand-built IR chain that references a naive Python loop with branches that are not supported in IR. Without a second formula for the other side of the query these two rows are analyzed exhaustively at widths 8 and 16, as well as fuzzed at 32-bit. As a result, the label is "verified upper bound" and contains no implications about proving. The tests test_flp2_upper_bound_verified and test_bswap32_upper_bound_verified check this; the latter additionally fixes four 32-bit directed vectors to prevent silent regressions in wiring.
- **The benchmark menu was chosen based on expected outcomes, not expected wins.** Eleven new rows were introduced to ensure that the table contained cases that could possibly be lost: times_nine, bswap32, and rotl5 were chosen because x86 has lea, bswap, and rol instructions, but IR lacks them; avg_floor and avg_ceil were chosen under the assumption of a tie. The survey that would contain only cases where synthesizer wins is not a survey. Expected outcomes were formulated before measurement and taken as hypotheses; rotl5 and bswap32 matched the predictions, sign exceeded the predictions by one instruction against clang and two against gcc, and flp2 appeared as a near-tie, not as a compiler dominant outcome as originally expected.
- **IR specification program is used as an SMT oracle. The Python benchmark function is an independent reference point.** Every new row gives two reference points that play different roles. The Python function found in superopt/benchmarks folder is a naive algorithm. Its copy, line-for-line, in results/c folder is used by the fuzzer as the reference to compare against. IR spec Program in tests/test_survey.py file is the thing that will be proved to be equivalent to a synthesized program with equivalent() because the proof requires a formula. The bridging step is to write a test that evaluates the IR spec program against every 8-bit input against the Python function and then fuzzes the 32-bit version (test_*_spec_matches_benchmark). Without this step SMT layer would prove equivalence between a synthesized program and IR spec that is not yet proven, which means proof of an incorrect object.
- **Naive specification with an undefined case returns a value produced by the corresponding trick in both languages.** The construction smear_lowest_bit is an example. The expression x | (x-1) maps zero to all-ones; a loop that scans for a set bit and fails to find one could return any value. Choosing all-ones in both the Python specification and C implementation makes the trick equivalent to the specification and ensures that both sides of the comparison describe the same function. Choosing zero would make the trick subtly differ from the specification in what it returns in the empty scan case and thus would alter the thing that was proven by the floor sweep and what was compiled by GCC. Every benchmark with an empty scan case received identical treatment.
- **Four floor sweeps were tried but didn't succeed to certify and were dropped, not marked as slow.** The sweep of isolate_lowest_zero at length 2 or less (77 libraries) ran for hours; the sweeps of sign, avg_floor, and avg_ceil at length 3 or less (363 libraries each) took more than 35 minutes. Commit 30c9cb3 drops these four, and the rows become best found. A test that never succeeded cannot support the label "proven", and retaining this label with the slow marker would have meant shipping an assertion that never happened. Two possible workarounds that were tried and rejected were pre-seeding with 16 examples per call (it increased difficulty and left the sweep unfinished in 10 minutes), and querying Z3 with exists-forall (yielded unknown at a 60-second timeout on ADD-bearing pair libraries, scratchpad forall_floor.py, and unknown is not a floor).
- **Certification cost is a property of the specification, not of the number of libraries.** Three sweeps of exactly 77 libraries were performed: absval's sweep runs within the default suite, rotl5's requires 20.7 seconds and is labeled slow, and isolate_lowest_zero's sweep didn't finish in hours. Same code path, same width and same constant budget were used. The working hypothesis is that near-solution density affects refutation effort: a library is easy to refute if the first counterexample rules it out, and hard if it passes every finite example set through many CEGIS rounds before ultimate unsat. Libraries with four free constants (ADD/AND-family) are flexible. Therefore, a row's grade cannot be predicted prior to running the sweep.
- **The folklore minimum trick is a sidebar, not a row because IR cannot express it.** The expression y + ((x-y) & ((x-y) >> 31)) is wrong in case of overflow. The test test_folklore_min_trick_is_wrong detects this with the fuzzer and manually picks the case x = INT_MIN, y = 1, where the trick gives 1 while the correct result is INT_MIN. The original plan supposed equivalent() to return the counterexample, and this would mean a proof of wrongness. But this is impossible because signed minimum needs comparisons or branches, which are not present in IR by CLAUDE.md scope; therefore there is no IR spec that can be used as the other side of the query. The layer that should catch folklore mistakes is absent for this function, and the independent fuzzer catches the mistake instead. This is an argument for having two layers and also shows a real cost imposed by the IR's scope.

## Phase 4b correction: the location-width bug

- **Location variables had one bit too little, leading to satisfiable queries being unsatisfiable.** The loc_width parameter was computed as (n_lines - 1).bit_length(), which allows all line index values, but not the exclusive upper bound against which they are compared. When n_lines itself is a power of two, ULT(var, n_lines) casts n_lines to zero at that width, and no value is less than unsigned zero. The well-formedness constraint becomes unsatisfiable, and synthesize returns None. The fix is setting loc_width = max(1, n_lines.bit_length()) in superopt/cegis.py, commit 9780477.
- **The stealth of the bug lies in None being a legitimate answer.** synthesize returning None means that no program of the given shape exists, and that is the expected outcome of a floor sweep for any library tried. The most common library, 1 input + 1 constant + 2 operations (4 lines, a power of two), triggers vacuous unsatisfiability at every single-op floor stage, including the cost sweep's weight-1 stage, partially voiding the evidence behind the absval, isolate_rmb, and times_nine floors.
- **Timing reveals the defect.** A survey implementer noted that n_constants = 1 "does not work" and bumped it to 2, hence making the line count 5 and avoiding the bug without knowing about it. The actual clue was floor stages running in 0.02 seconds. The lesson is that, in a proof pipeline, an unusually quick negative result deserves investigation.
- **The regression test confirms the positive case at the power-of-two line count.** test_synthesizes_when_line_count_is_a_power_of_two synthesizes x & (x-1) from a two-op library with one free constant, the exact 4-line configuration that failed before, and asserts that a program returns and proves equivalent. Emphasizing the positive direction is appropriate in this case because the failure mode was a false negative, and no assertion about None could have caught it.
- **All published claims withstand re-validation.** After the fix, the whole default suite was rerun and stayed green: the sweeps that used to short circuit now do genuine solver work and return None for every library, empirically confirming the absval, isolate_rmb, and times_nine floors instead of relying on the encodings. The numerical results in results/compiler_gap.md and results/cost_model.md stay intact. Commit 75f4d0d reverses the n_constants=2 workaround in three survey tests to restore the intended one constant; no part of the pipeline would detect the invalid floor otherwise.

## Phase 5A: the latency cost model

- **"Optimal" gains a second definition, and both are reported.** Minimum
  instruction count stays the headline (CLAUDE.md section 7); minimum
  summed latency is the alternate, with per-op weights from Agner Fog's
  instruction tables (agner.org/optimize) for Intel Alder Lake: mul 3,
  everything else 1. The report compares both on the same benchmarks, as
  section 7 requires.
- **Cost-optimality is proven by sweeping libraries in weight order.** A
  program's cost equals its op multiset's total weight, and an optimal
  program has no dead code, so CEGIS over multisets in nondecreasing
  weight order makes the first synthesized program cost-optimal at 32-bit
  with constants free. Zero-instruction programs cost 0 and are excluded
  by the identity and non-constancy checks, like the Phase 5B floors.
- **x*9 is the flip.** Length picks mul-by-9 (1 instruction, cost 3);
  latency picks shift-3-add (2 instructions, cost 2). The solver finds
  the 9 and the 3 itself. The old benchmarks don't flip: their optimal
  programs are MUL-free, so the existing floors already carry the cost
  claims.

## Phase 5B: the compiler gap study

- **Both sides start from the same naive spec.** superopt reads the Python
  spec; gcc and clang get a line-for-line naive C translation. Comparing my
  optimal output against a compiler that was handed the trick would be
  meaningless; the question is who recovers the trick from the naive form.
- **The counting rule is "every body instruction except ret," by script.**
  Prologue-free leaf functions make the body unambiguous, and putting the
  rule in `scripts/compiler_gap.py` with a parser test keeps it from being
  applied by eye, differently per benchmark.
- **Baseline x86-64 is the headline; -march=x86-64-v3 is the honesty
  column.** With BMI1 and POPCNT the ISA absorbs whole tricks (`blsi`,
  `popcnt`), which is a hardware story, not a code-generation one. Both
  columns appear so neither story hides the other.
- **The absval lower bound comes from exhausting component libraries, not
  the Phase 3 enumerator.** The enumerator is constant-free and 8-bit; the
  claim is at 32-bit with constants. Since the Jha encoding wires every
  library component, sweeping all 11 one-op and 66 two-op multisets with
  free constants and getting unsat everywhere proves no program of length
  one or two computes absval at width 32. The same argument now backs the
  isolate_rmb row at 32-bit, where sweeping every single-op library with free
  constants proves no one-instruction program isolates the rightmost bit.
- **The 32-bit absval synthesis returned a constant-free wiring, so the
  "solver finds 31" assertion was dropped.** I expected the solver to pick
  the shift amount 31 for `ashr(x, 31)`. It found something better: a 3-op
  program with no constants at all, `ashr(x, x)` then `x xor r0` then
  `r1 sub r0`. Shifting `x` by `x` builds the sign mask because a
  non-negative `x` shifts to 0 and a negative `x`, read as an unsigned shift
  amount at least 2^31, saturates the arithmetic shift to all-ones, matching
  the over-width shift semantics logged in Phase 1. That's IR/Z3 behavior,
  not x86's, since `sar` masks the shift amount mod 32, so the test asserts
  length, equivalence, and a fuzz pass instead of a specific constant.

## Phase 4b: component synthesis

- **The wiring is encoded with Jha 2010 location variables.** Each operation gets an integer output line and one input line per operand. Well-formedness keeps the output lines a permutation (one component per line) and forces every input to read a strictly-earlier line (acyclicity), and a connection constraint ties each input to the value on the line it points at. The solver picks the wiring and the constants together, and a decoder reads the model back into a `Program`. The technique is Jha et al. 2010, not novel here; the implementation and evaluation are.
- **Location variables are bit-vectors, not integers.** Integer locations force Z3 to mix linear-integer and bit-vector reasoning, which is slow. Small fixed-width `BitVec` locations make the whole query one bit-vector problem it can bit-blast, with unsigned comparisons (`ULT`, `UGE`) since the indices are non-negative. The fast rungs are the canary: a signed/unsigned slip breaks acyclicity and `x & -x` stops synthesizing.
- **Symmetry is broken on interchangeable parts.** Identical opcodes are ordered by line, and commutative operations have their two input locations ordered. Both are non-lossy (any valid program has exactly one labeling that obeys them), and they stop the solver re-deriving the same wiring under every relabeling.
- **A `Library` can pin constants via `fixed_constants`.** Structural constants like shift amounts are provided rather than searched, while the genuinely magic constants stay free. This keeps the headline, the solver discovering the masks, and shrinks the search (popcount from six unknown bytes to three).
- **The headline target moved from CTZ to popcount.** Count-trailing-zeros via a De Bruijn sequence indexes a 32-entry table, which is a memory load and out of scope, so SWAR population count replaced it: pure arithmetic and bitwise work with real magic masks and no table.
- **Full SWAR popcount is recorded as the measured frontier, not forced.** Even with every lever, CEGIS does not converge on it. The per-round synthesis cost explodes as counterexamples accumulate (0.06s, 0.1s, 3.9s, 11s, 27s over five examples, then a cliff), because each round must find one wiring correct on all accumulated inputs at once. The two popcount rungs are marked `slow` and deselected by default; the seven rungs that pass prove the technique end to end.

## Phase 4a: constant synthesis

- **A constant is a free variable the solver picks, not a value to enumerate.** A `Hole` in a sketch encodes to a free `BitVec`, so the solver solves for the constant that makes the program correct. This recovered `0xAAAAAAAA` over all 32-bit inputs, which brute-force enumeration could never reach. It is the real insight the project exists to show.
- **CEGIS splits the doubly-quantified synthesis query.** "There exists a program such that for all inputs it matches the spec" is too hard to ask Z3 directly, so the loop alternates: finite-synthesis finds constants fitting a few example inputs (an easy existential), `equivalent` verifies over all inputs (the Phase 2 proof), and any counterexample is folded back as a new example. It converges in a few rounds.
- **Finite-synthesis `unsat` means no program exists at all, not just none for these examples.** If no constants fit even the current handful of examples, none fit every input, so the loop returns `None` rather than spinning.
- **Sketch and spec arity and width are checked up front.** A mismatch is a programming error, not a synthesis failure, so it raises rather than producing a misleading `None`.

## Phase 3: brute-force search

- **Candidates are matched by exhaustive interpretation, not the SMT checker.** At 8-bit the input space is 256 values, so running a candidate through the interpreter on every input is a complete, exact check. SMT-against-a-spec over all 32-bit inputs is the Phase 4 job.
- **Enumeration searches no constants.** Operands come only from inputs and earlier results. A constant operand would multiply the space by 2^width per constant, which is intractable, and it's exactly the limitation CEGIS removes in Phase 4 by solving for constants. The `x & -x` target needs none.
- **Shortest-first makes the first match provably optimal.** Every shorter length is fully enumerated first, so the first match has minimum instruction count. Dead-code and commutative-duplicate pruning are non-lossy: a program with an unused instruction has a shorter equivalent found earlier, and `f(a,b)` equals `f(b,a)` for commutative ops.
- **Length-0 programs handle identity.** A pass-through output (a bare input) is tried before length 1, so an identity spec resolves to the zero-instruction program instead of a one-instruction equivalent.

## Phase 2: encoder and equivalence

- **Each opcode maps to the matching Z3 bit-vector op.** Fixed-width `BitVec` arithmetic already wraps mod 2^width, so that wrap is the masking and the encoder adds no explicit mask. Constants are `BitVecVal(c, width)`, width spelled out, never an implicit Python int.
- **LSHR must use `LShR`, not `>>`.** On a Z3 `BitVecRef` the `>>` operator is arithmetic (sign-propagating), so logical shift right needs the explicit `LShR()`. This is the one line where a wrong choice produces confidently-wrong "optimal" results that pass casual testing.
- **Equivalence is proved by an UNSAT check.** `equivalent` asserts the two outputs differ and asks Z3; `unsat` means no input can make them differ, so they agree on every input. A proof over the whole symbolic domain, not a sample.
- **The proof relies on shared input variables.** Both programs are encoded with inputs named `in0, in1, ...`, and Z3 interns by name, so the two output expressions share the same variables. If the encoder ever namespaced inputs per program, the check would compare independent variables and report false counterexamples. There's no runtime guard for this, so the `x+x` vs `x<<1` test is the regression canary.

## Phase 1: interpreter

- **Bit width is enforced by masking every intermediate with `(1 << width) - 1`.** The interpreter models a fixed-width register, so arithmetic wraps like hardware rather than growing into an unbounded Python int.
- **ASHR sign-extends, LSHR does not.** ASHR reinterprets a sign-bit-set value as a negative int and then shifts; LSHR works on the masked non-negative value. Getting these backwards is a silent bug that only shows on sign-bit-set inputs.
- **An over-width shift (amount at or past the width) returns a fixed result.** SHL and LSHR return 0; ASHR returns all-ones or 0 depending on the sign bit. This matches Z3's native bvshl/bvlshr/bvashr, so the encoder and interpreter agree without special-casing, and it avoids constructing a multi-gigabit Python int once the width scales to 32.

## Phase 0: project scaffold

- **`Op` is a `StrEnum`.** Programs print and serialise as readable text
  (`add`, `lshr`), which keeps enumerator output and test failures legible.
- **`Operand` is a tagged union of three frozen dataclasses** (`InputRef`,
  `Const`, `ResultRef`) instead of one dataclass with a `kind` string. The
  type checker then forces the interpreter and encoder to handle all three
  operand kinds explicitly, rather than guessing.
- **Constants are operands, not an opcode.** A `Const` holds a concrete value
  now and becomes a free variable the solver fills during synthesis (Phase 4).
  That is why `CONST` is dropped from the `Op` enum that the file map listed.
- **`Program.output` is an `Operand`, not an instruction index.** This lets a
  program's output be a result, a pass-through input, or a constant, so the
  zero-instruction identity program is representable.
- **`interp.execute(program, inputs)` drops the separate `width` argument** the
  plan sketched, in favour of `program.width`, to keep width single-sourced.

## Phase 0: Z3 hello-world

- **Why UNSAT proves equivalence.** Asserting the two expressions differ and getting `unsat` means no assignment of the input bits makes them differ. The solver reasons over the symbolic bit-vector instead of trying values, so `unsat` is a statement about all 2^width inputs at once, equal everywhere. A `sat` result instead returns a concrete differing input. So the check is a proof, not evidence from sampling.
