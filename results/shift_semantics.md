# Optimality Claims

Until now, the claim made in this research paper is that each proof conducted here establishes optimality of a program with respect to a single semantics, where specifically, a shifting operation saturates for shifts that are equal to or larger than the width, similarly to Z3's native semantics of bit-vector shifts. The correspondence, however, cannot hold true in the hardware implementation, where in the x86 architecture the shift amount will be reduced modulo the width before performing the operation; as a consequence, x >> 40 on 32-bit width corresponds to the operation of x >> 8. Therefore, an "optimal" program which depends on this semantics is indeed optimal in the Intermediate Representation but wrong on hardware.

Thus, the main question of this research is: out of all the programs which were proved to be optimal by this tool with previous semantics, which are still optimal under changed semantics and which are mere artifacts of the current mode?

## Two Modes

- ShiftMode.SATURATE (default, unchanged): results of SHL and LSHR shifting operations are 0 if the shift amount is greater than or equal to the width; ASHR results are filled entirely with copies of the sign bit. The name comes from the shift amount behaving as if it saturated at the width;
- ShiftMode.MASK (new): the shift amount is reduced by first calculating amount & (width − 1); only power of two widths are allowed. This parameter is keyword only, with the SATURATE as the default in all public code paths, including the interpreter, encoder, equivalence checker, synthesizer and fuzzer; consequently, the current test suite is unaffected and passes with this change.

## The Gate

An incorrect MASK-encoded shift would silently invalidate every result below; hence, the cross-checking encoder-vs-interpreter test runs in both modes: 1000 random programs checked against 100 random inputs per mode, complemented with the hand-picked set of over-width edge-cases. For example, ASHR(0x80, 9) on width 8 gives 0xC0 under MASK (due to the masking of shift to 1) and 0xFF under SATURATE. Symbolic verification confirmed that the MASK encoder is consistent with the independently developed oracle at widths 8, 16 and 32.

## Headline: Constant-free Absval is Saturation-only

One of the stranger programs found by this tool is the constant-free absval which is composed of three instructions and starts with ashr(x, x). It is sensible, since for negative x, the shift amount becomes so large, that saturation of the shift result provides all-ones sign-mask, similar to ashr(x, 31). All manipulation takes place in the saturation logic.

It has been established for both cases at width 32:

- SATURATE: the constant-free library (ASHR, XOR, SUB) synthesizes the three-instructions absval; the SMT checker confirms the result is correct according to the specification; independent fuzzer confirms correctness of the solution on 20,000 inputs.
- MASK: for the same library and specification the solver finds that the result is unsatisfiable: there are no ways to wire ASHR, XOR and SUB without constant to construct the absval without saturating the shift result.
- MASK with one free constant reinvents the classic three-instructions form: the constant chosen by the solver is 825,509,791 (rather than the 31); any number which masks to 31 suffices, so the constant of portable version is defined only modulo the mask. Both verification layers confirm the solution in mask mode.

Thus, the optimal length remains the same in both cases, but the zero-constant version cannot be used in other architecture: it is a sensible program only on an ISA which saturates. Thus, the constant is the penalty for x86 portability. One caveat checked explicitly in the tests is that the reference specification contains shifting by width − 1; hence, a number always less than width under any mode; consequently, the specification encodes the same function in both cases and the difference lies purely in the search space.

## Stability: All Other Results Persist

All previously proven affordable floors have been retested under MASK by using the exhaustive library sweeps, reproducing all known techniques under mask mode:

- clear_lowest_bit: 11 libraries at length 1 – holds; optimum under MASK: 2 instructions, same trick.
- smear_lowest_bit: 11 libraries at length 1 – holds; optimum under MASK: 2 instructions, same trick.
- turn_off_trailing_ones: 11 libraries at length 1 – holds; optimum under MASK: 2 instructions, same trick.
- isolate_rmb: 11 libraries at length 1 – holds; optimum under MASK: 2 instructions, same trick.
- absval: 77 libraries at length 2 – holds; optimum under MASK: 3 instructions (with the constant).

In each case, the length of the shortest program remains the same under MASK. This result is expected, since the two-instruction tricks contain no shifts at all and the absval optimum shifts only by an in-range constant. Nevertheless, the verification proves the claim.

## Open Question: No Mask Only Tricks Either

The remaining question to ask is whether there is any trick which is valid only under MASK; that is, can wrapping perform the same role in the trick that saturating performs for the absval. Four constant-free library-benchmark pairs were tested in both modes: (SUB, AND) for clear_lowest_bit; (SUB, OR) for smear_lowest_bit; (ADD, AND) for turn_off_trailing_ones; (SHL, LSHR, OR) for rotate_left_by_5. All 8 (library, mode) combinations turned out to be unsatisfiable: bit scan requires its literal and rotation requires its two shift amounts; neither can be calculated from the inputs. Though the result is negative, it answers the question.

## Limitations

The current evaluation considers the single semantic dimension only. The behavior of overflow, rotations, division semantics and widths that are not power of two have not been considered, and possibly contain the sought class of mode-specific programs. The impossibility claim covers the same set of programs that all floors of this project cover: they are valid for all programs built with the same multiset of operations, but do not necessarily prove impossibility of all programs of the same length constructed from some other set of operations.

In addition, MASK represents x86- and AArch64-like mask-based ISA; different behavior of the ISA implies the need for the dedicated mode.
