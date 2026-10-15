# Clarify Algorithm 1 and code/data availability; revise manuscript exposition

Algorithm 1 now explicitly names the modulo-p² coefficient ring and its F_p output. A code/data availability section provides package versions, source links, defining-polynomial and validation-file locations, dependencies, rerun commands, and the limits of the available records.

The retained Astra revisions correct Witt addition and the Teichmüller-coordinate explanation, specify quasi-F-split module linearity, distinguish the Frobenius trace from a splitting, and restrict computational matrix iteration to F_p. They also require a finite-height bound in the algorithm inputs, include the h=b endpoint, repair the Fermat example, and clarify NTT bounds/padding, WICS empty cases and complexities, and packed-exponent arithmetic. Height-stratification and exact/tail heuristic formulas remain corrected, and matrix-construction timings match the existing table. Notation, bibliography fields, caption references, and PDF destinations are also improved. The inherited F7 example repairs are preserved.

[changes.md](changes.md) records before/after text, feedback provenance, and stable change IDs. At the author’s request, C09, C12, C20, C30, C44, C45, C50, C51, C52, and C56 were reverted in full; only the last edits in C05 and C17 were reverted. The PR description reflects the remaining changes. The branch starts from `astra-review` at `f98cae2`, which contains `main` at `e3f0b52`.

Validation: the manuscript builds successfully. Prior independent checks confirmed smoothness and ordinary/nonordinary coefficients for all 33 examples and all 22 full-height labels over F5/F7; these reverts do not change the example polynomials. The retained NTT bound was independently checked. Higher heights over F11/F13 and GPU performance were not recomputed.

Original benchmark trials and sampling logs remain unavailable in the repository. The actual GPU arithmetic mode, timing protocol, and sampling/throughput denominator still need supporting records. The restored precision, frequency, waiting-time, speedup, and controlled-reduction claims are not claimed as resolved by this PR.
