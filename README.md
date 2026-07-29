# superopt

A superoptimizer for short, loop-free integer and bitwise routines. Hand it a
small function and it searches for the shortest equivalent program, then proves
there's nothing shorter. Not "a bit faster," but provably optimal under a fixed
instruction set. For the from-scratch version that assumes no background, read
[docs/explainer.md](docs/explainer.md).

## The idea

An ordinary compiler at `-O3` applies a big bag of heuristic rewrites. It makes
your code faster but never claims it found the best version. Superoptimization,
going back to Massalin in 1987, asks the harder question: out of *all* programs,
which is the shortest one that computes this function? The classic party trick
is rediscovering something like `x & -x` (isolate the lowest set bit) from
nothing, and certifying that no shorter sequence does the same job.

The catch is the word "equivalent." Two programs are equivalent only if they
agree on *every* input, and you can't check that by running them. A single
32-bit input already means four billion cases, and it gets worse fast with more
arguments. So instead of running anything, superopt encodes each program as a
bit-vector formula and hands it to the Z3 SMT solver, asking the question
backwards:

> Is there *any* input where these two programs disagree?

If Z3 says unsat (unsatisfiable), no such input exists, which means the programs
are equal everywhere. That's the proof. If it says sat, it hands back the exact
input where they differ, which is a gift when you're debugging. This backwards
framing is the whole foundation. Once it clicks for one pair of programs it
scales to all of them.

Finding the optimal program comes in two flavors. The brute-force version
enumerates programs by length (all of length 1, then 2, then 3) and asks Z3
"equivalent?" for each. The first length that matches is optimal by
construction. It's slow but obviously correct, which is exactly why it comes
first: it proves the interpreter, the encoder, and the equivalence check all
agree before anything clever gets layered on. The clever version is CEGIS
(counterexample-guided inductive synthesis, from Jha et al. 2010): synthesize a
program that works on a handful of example inputs, verify it against all inputs
with Z3, and feed any counterexample back as a new example. It converges fast
because every counterexample rules out a huge slice of wrong programs.

One thing that falls out of the SMT approach genuinely surprised me: a constant
isn't something you have to guess. In the formula it's just a free variable the
solver gets to pick, so Z3 can *solve* for the magic number that makes a program
correct, something brute-force enumeration could never stumble onto.

## Status and scope

Phases 1 through 4 and the independent fuzzer are done and verified:

- the reference interpreter,
- the Z3 encoder, cross-checked against the interpreter on 100,000 random cases,
- the equivalence checker, with counterexample extraction,
- brute-force search, which rediscovers `x & -x` for isolate-rightmost-bit and
  proves it optimal at length 2 (the de-risk milestone),
- a random-input fuzzer written without reusing the encoder,
- CEGIS constant synthesis (Phase 4a): the solver treats a program's constants as
  free bit-vector variables and solves for them, which recovered the magic number
  `0xAAAAAAAA` over all 32-bit inputs, something enumeration can never reach,
- component synthesis (Phase 4b): the Jha 2010 location-variable encoding, where
  the solver wires a fixed bag of operations into a program. It rediscovers
  `x & -x`, recovers a mask constant and even a shift amount on its own, and
  verifies the result over all inputs,
- the compiler gap study (Phase 5B): the same naive specs compiled with
  `gcc -O3` and `clang -O3` versus superopt's proven minimums, measured by
  a scripted counting rule. See [results/compiler_gap.md](results/compiler_gap.md).
- the latency cost model (Phase 5A): a second definition of optimal, minimum
  summed latency instead of instruction count, where `x * 9` flips from a
  single multiply to a two-op shift-and-add. See
  [results/cost_model.md](results/cost_model.md).
- the gap survey (Phase 5B, Stage A): the gap study extended from 3 benchmarks
  to 14, with the superopt column split into proven, best found, verified upper
  bound, or no result rather than a single assertion in all cases. Seven rows
  contain a proven floor at 32-bit with free constants. The floor certification
  frontier, where a 77-library sweep takes 20.7 seconds on one spec and fails
  to complete even in hours on another, is documented in the same document.

The suite runs 109 tests green by default with 3 deselected, and every
synthesized program clears both layers, the SMT proof and the independent
fuzzer.

One result is worth stating plainly. Full SWAR population count is the measured
ceiling of the component synthesizer. Even at 8-bit, with bit-vector locations,
symmetry breaking, and the shift amounts pinned so only the masks stay free, CEGIS
does not converge: the per-round synthesis cost explodes as counterexamples pile up,
running 0.06s, 0.1s, 3.9s, 11s, 27s over the first five examples and then falling off
a cliff. The two popcount rungs stay in the suite marked `slow`, deselected by
default and runnable with `pytest -m slow`, documenting both the target and the wall.
The `rotl5` floor sweep bears the same mark for the usual reason that it takes
20.7 seconds. The seven rungs that pass prove the technique end to end.

The gap study is now a fourteen-benchmark survey. The same naive specs go to
`gcc -O3` and `clang -O3` and to superopt, and the superopt column identifies the
tier of each number: seven proven minimums, four best found with no floor
certification, two verified upper bounds, and popcount's blank. The most clear-cut
result is that a naive bit scan loop outdoes both compilers in the same manner. On
clear-lowest-bit, smear-lowest-bit, turn-off-trailing-ones and isolate-lowest-zero
gcc preserves a loop of 14 to 19 instructions, while clang unrolls to 93 to 98;
superopt proves 2 or 3. isolate-rightmost-bit follows the same pattern with 14 and
97 against a proven 2. The honesty rows are also present: rotl5 and bswap32 map to
the compilers because x86 supports a rotate and a byte swap, but the IR does not;
times_nine maps to a tie by instruction count that the latency model interprets
differently. absval is a three-way tie at 3. Popcount lacks a superopt answer. The
numbers, the method, the tier hierarchy, and the assembly reading are in
[results/compiler_gap.md](results/compiler_gap.md). The remaining Phase 5 stretch
goal is neural-guided search.

Deliberately out of scope for now: floating point, memory and loads/stores,
loops and branches, and multi-output programs. Each one is its own research
project; the single-output, loop-free, integer case comes first.

## Run it

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -e ".[dev]"
pytest
```

`pytest` should report 109 passed, 3 deselected. The three marked `slow` are
the two popcount rungs and the `rotl5` floor sweep, which takes 20.7 seconds
on its own; run them with `pytest -m slow`.

## Notes

The study notes (superoptimization theory, SMT and bit-vectors,
equivalence-via-unsat, CEGIS, the Jha 2010 reading) live in a separate
repository, so the Obsidian auto-sync churn never clutters this one's history:

**→ [github.com/smiles0527/superopt-notes](https://github.com/smiles0527/superopt-notes)**

They're also checked out locally at `notes/` (gitignored here) as an Obsidian
vault. Edit them there; the `obsidian-git` plugin syncs them to the notes repo
on its own. A fresh clone of this project that wants the notes should also
`git clone` the notes repo into `notes/`. A clean, read-only snapshot lives
under [docs/notes/](docs/notes/), browsable on GitHub, alongside the
[plain-English explainer](docs/explainer.md) and the
[references](docs/references.md).

## Honest framing

The synthesis technique here (CEGIS, component-based encoding) isn't novel. It
goes back to Jha et al. 2010 and Solar-Lezama's sketching work, both cited in
the references. What's mine is the IR design, the encoder, the implementation,
and the evaluation.
