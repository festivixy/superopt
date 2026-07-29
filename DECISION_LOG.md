# Decision log

Why each non-obvious choice was made. Newest entry first.

## Phase 5B, Stage A: the gap survey

- **The superopt column is graduated because a single column makes four separate claims.** With three benchmarks, there was exactly one label for every row. Now there are four: proven (with synthesis and both verification layers applied, plus a completed component-library floor sweep at 32-bit with free constants), best found (with synthesis and both verification layers applied, but with no completed floor), verified upper bound (a hand-built IR program tested exhaustively at widths 8 and 16, with a fuzz at 32, and no minimality claim), and no result. There are seven proven rows, four best found, two verified upper bound, and one with no result. The label is kept as data in the SUPEROPT dictionary in scripts/compiler_gap.py, guaranteeing that regeneration matches the table rather than veers off into prose.
- **The verified upper bound rows lack an SMT layer, and that is structural.** The equivalent() function takes two IR programs. Bswap32 and flp2 have just one chain, the hand-built IR sequence, whose reference implementation is a naive Python loop with branches that the IR cannot express. Since there is no second formula on the other side of the query, the two rows get a full exhaustive interpretation at widths 8 and 16, and a fuzz at 32. Hence, the label is "verified upper bound" and not any kind of "proven." The relevant tests are test_flp2_upper_bound_verified and test_bswap32_upper_bound_verified, the latter also fixing four directed 32-bit vectors to avoid silent regressions in the wiring.
- **The benchmark menu was chosen based on the expected outcome, not on the expected wins.** Eleven new rows were added to introduce deliberately unfavorable cases: times_nine, bswap32, and rotl5 were added especially because x86 has lea, bswap, and rol and the IR lacks them; avg_floor and avg_ceil were added in anticipation of a tie. A survey with only the cases where the synthesizer wins would not be a survey. The expectations were pre-registered as hypotheses; rotl5 and bswap32 met the prediction, sign beat the predicted instruction efficiency by one against clang and two against gcc, and flp2 was a near-tie rather than compiler favorite that was expected.
- **The IR spec program acts as an SMT oracle, whereas the Python benchmark stands alone.** Adding a new row yields two reference artifacts with different purposes. The Python function located at superopt/benchmarks/ does the naive thing, is replicated line-for-line in results/c/ for the compilers, and serves as a benchmark against which the fuzzer validates. The IR spec Program in tests/test_survey.py serves as the basis for the equivalence proofs by equivalent(), as the proof requires a formal formula. The link between the artifacts is a test that runs the IR spec on all 8-bit inputs against the Python function and then fuzzes the 32-bit version (test_*_spec_matches_benchmark). Without the link, the SMT layer would prove the synthesized program equivalent to the IR spec that is yet to be independently verified, proving the wrong proposition.
- **A naive spec with an undefined case produces the value from the trick in both languages.** The smear_lowest_bit function is an example: x | (x-1) produces all-ones from zero; a loop that checks for a set bit and finds none can return any value. Picking all-ones in both the Python spec and the C implementation makes the trick equivalent to the spec, thus putting both sides of the comparison on par. Picking zero would have silently altered what the floor sweep has shown and what gcc has compiled. Every benchmark with an empty-scan case got the same treatment.
- **Four floor sweeps were attempted but have failed to certify and were dropped rather than labeled slow.** The sweep for isolate_lowest_zero at length 2 or less (77 libraries) ran for hours; sign, avg_floor, and avg_ceil at length 3 or less (363 libraries each) took more than 35 minutes. Commit 30c9cb3 drops these four rows into the best found category. A test that has never passed cannot support the assertion of being proven, and keeping it with a slow mark implies an assertion unsupported by success. Two preliminary workarounds were attempted and rejected: pre-seeding 16 examples per call makes the finite synthesis problem harder and leaves the sweep unfinished at 10 minutes; asking Z3 for an exists-forall query directly returns unknown within 60 seconds timeout on ADD-bearing pair libraries (scratchpad forall_floor.py), and unknown is not a floor.
- **Certification cost is a property of the specification, not the library count.** Three sweeps of exactly 77 libraries have been done: absval runs within the default suite, rotl5 takes 20.7 seconds and is labeled slow, isolate_lowest_zero fails to finish in hours. The exact same code path, width, and constant budget were used. The working hypothesis, though never tested, is near-solution density: a library is relatively cheap to refute when the first counterexample invalidates it and expensive when it keeps fitting every finite example set in multiple CEGIS rounds before the ultimate unsat. ADD/AND family libraries with four free constants are the most flexible. The planning consequence is that the tier of a row cannot be determined in advance of the sweep run.
- **The folklore min trick is treated as a sidebar, not a row, as the IR cannot express it.** The expression y + ((x-y) & ((x-y) >> 31)) is wrong in the presence of overflow. The test_folklore_min_trick_is_wrong finds that with the fuzzer and manually picks the case of x = INT_MIN, y = 1, where the trick returns 1 but the correct answer is INT_MIN. The original plan was to have equivalent() return the counterexample, constituting thus the proof of wrongness. It does not, because signed minimum needs comparisons or branches, which the IR cannot express under CLAUDE.md scope; thus there is no IR spec to be the other side of the query. The layer intended to catch the folklore bugs is unavailable for this function, and the independent fuzzer catches the bug instead. That reinforces the reason why two layers are maintained and demonstrates the price of the IR scope limitation.

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
