**Review of the current manuscript — 16 September 2026**

**Update after the review:** Findings 1 and 2 below have been resolved in `heights.tex`: the former F7 height-7 polynomial has been moved to height 9, and the first replacement supplied by the author has been inserted at height 7. Both newly supplied candidates were checked and are smooth of height 7; their coefficient traces are `(0,0,0,0,0,0,4)` and `(0,0,0,0,0,0,1)`. Results are in `review_checks/replacement_checks.json`. The review below and its original JSONL results describe the pre-correction manuscript. The original two equations are preserved in `review_checks/original_f7_rows.json` so the historical checks remain reproducible.

I read all active text in `main.tex` and its six included sections, the bibliography, and the existing reviewer-response files. Findings below refer to source line numbers before any manuscript changes. The manuscript itself has not been edited.

The most consequential findings are in the F7 example table: the row labeled height 7 computes to height 9, and the row labeled height 9 is singular. These are separate issues. The current height-7 row is smooth and can supply the height-9 example, but a smooth height-7 example is still needed to substantiate the table's all-heights claim.

I independently checked smoothness of all 33 displayed quartics and their height-1 coefficients. I also recomputed the full height recurrence through height 10 for every F5 and F7 entry, using exact integer arithmetic. I did **not** recompute higher heights over F11 or F13, as requested. I could not inspect a compiled PDF: the repository contains only LaTeX sources and no TeX engine is installed here. Thus the layout comments below are source-level findings, not a visual typesetting review.

**Definite errors affecting the examples**

1. **The F7 height-7 row has height 9.** [heights.tex:224](./heights.tex#L224).

   For this exact displayed polynomial, the coefficients tested at heights 1 through 9 are
   \[
   (0,0,0,0,0,0,0,0,4)\in\mathbb F_7^9.
   \]
   I checked the result using both matrix iteration and a separate direct multiply-and-trace implementation. I additionally checked the powering calculation against a separate exact packed-integer convolution. The quartic is smooth, so its Artin–Mazur height is 9 under the cited criterion. Relabeling it supplies height 9, but leaves height 7 missing.

2. **The F7 height-9 row is singular.** [heights.tex:232](./heights.tex#L232).

   At \(P=[0:1:5:2]\), direct evaluation gives
   \[
   f(P)=f_{x_1}(P)=f_{x_2}(P)=f_{x_3}(P)=f_{x_4}(P)=0\pmod7.
   \]
   With the displayed coefficients interpreted as integers, the five evaluations are respectively
   \[
   (2261,630,1134,1078,1260)=7(323,90,162,154,180).
   \]
   Hence the displayed projective hypersurface is not a smooth quartic K3 surface. Its quasi-F-split recurrence does return 9, but that does not establish the stated smoothness claim. If a resolution is intended, its properties and the transfer of height require an explicit argument; the straightforward repair is to use the smooth polynomial currently labeled 7 here and supply a replacement for 7.

   The remaining 32 displayed quartics passed the following exact geometric smoothness certificate: their four cubic partial derivatives, multiplied by all degree-6 monomials, span the entire 220-dimensional space of degree-9 forms. Consequently their Jacobian ideals have no projective zero even over the algebraic closure. All F5 height labels agree with the recomputation, as do the F7 recurrence labels other than the row labeled 7.

**Definite mathematical corrections in the exposition**

3. **The sign in the Witt addition formula is reversed.** [algorithm_outline.tex:213](./algorithm_outline.tex#L213).

   The formula must be
   \[
   S_1=X_1+Y_1-\frac{(X_0+Y_0)^p-X_0^p-Y_0^p}{p}.
   \]
   This follows immediately from \(S_0^p+pS_1=X_0^p+pX_1+Y_0^p+pY_1\). The later positive cross-term formula for \(\Delta_1\) is consistent with its definition as \([f]-\sum[t]\); do **not** change that formula's sign as well. The proof of the proposition at line 456 should use the corrected subtraction.

4. **The claimed identification of \(W_2(S)\) is false.** [algorithm_outline.tex:467](./algorithm_outline.tex#L467).

   For \(S=\mathbb F_p[x_1,\ldots,x_n]\), one does not have
   \(W_2(S)=(\mathbb Z/p^2\mathbb Z)[x_1,\ldots,x_n]\).
   Here \(S\) is not perfect. For example, in \(W_2(S)\),
   \(p(a,b)=(0,a^p)\), so \(\ker(p)=V(S)\) while \(pW_2(S)=V(S^p)\); these differ. In the polynomial ring over \(\mathbb Z/p^2\mathbb Z\), the kernel and image of multiplication by \(p\) coincide.

   Suggested replacement: “Although \(\Delta_1\) is defined using \(W_2(S)\), the coefficient-lift formula lets us compute it in \((\mathbb Z/p^2\mathbb Z)[x_1,\ldots,x_n]\).” This preserves the valid computational approach.

5. **The warning about ordinary p-adic digits and Witt coordinates is incorrect.** [algorithm_outline.tex:104](./algorithm_outline.tex#L104).

   The proposed correction \((c_0,c_1^p,c_2^{p^2},\ldots)\) cannot distinguish it from \((c_0,c_1,c_2,\ldots)\) over \(\mathbb F_p\), where these powers are identical. The missing distinction is between ordinary integer representatives and Teichmüller representatives. For a perfect field, a Witt vector \((a_0,a_1,\ldots)\) corresponds to
   \[
   \sum_{i\ge0}p^i[a_i^{p^{-i}}].
   \]
   For example, in \(W_2(\mathbb F_3)\cong\mathbb Z/9\), \((2,0)\) corresponds to the Teichmüller representative 8, whereas the ordinary integer 2 corresponds to \((2,1)\). The cited [Kim exposition](https://web.stanford.edu/~dkim04/blog/witt-vectors/) explicitly uses Teichmüller representatives.

6. **The quasi-F-split definition omits essential module-linearity.** [algorithm_outline.tex:341](./algorithm_outline.tex#L341).

   Specify a **\(W_n(R)\)-linear** map
   \(\phi:F_*W_n(R)\to R\), where \(R\) has its module structure via truncation, **such that the displayed diagram commutes**. The prose currently gives an untwisted domain and says only “a map.” Without linearity, the splitting condition loses its intended content. Also define the height to be \(\infty\) if no such positive integer exists. Compare [Kawakami–Takamatsu–Yoshikawa, Definition 2.5](https://arxiv.org/html/2204.10076v3#S2.SS2).

7. **The map \(u\) is not itself a splitting of Frobenius.** [algorithm_outline.tex:547](./algorithm_outline.tex#L547).

   A projection to the coefficient of a nonconstant basis monomial sends 1 to 0. In particular, the selected \(u\) has \(u(1)=0\), whereas a splitting must send 1 to 1. Call it the Frobenius trace or a generator of the relevant Hom module. One gets an actual splitting by composing it with multiplication by \((x_1\cdots x_n)^{p-1}\). Also distinguish projection to \(x^I S^p\) from coefficient projection to \(S^p\): an identification of that summand with \(S^p\) is being used.

8. **The computational map is not k-linear over an arbitrary perfect field.** [algorithm_outline.tex:559](./algorithm_outline.tex#L559), [algorithm_outline.tex:582](./algorithm_outline.tex#L582), [multiply_then_split.tex:33](./multiply_then_split.tex#L33).

   Identifying \(S^p\) with \(S\) takes p-th roots of coefficients as well as variable exponents. In conventional notation,
   \[
   u(c\mathbf x^{\mathbf a})=
   c^{1/p}\mathbf x^{(\mathbf a-(p-1)\mathbf1)/p}
   \]
   for surviving terms. Thus \(u(cg)=c^{1/p}u(g)\). The algorithms leave coefficients unchanged and use ordinary matrix powers, which are correct over \(\mathbb F_p\), the setting of the implementation. State that restriction explicitly for the algorithms and matrix discussion. Over general perfect fields one needs the Frobenius twist and a semilinear iteration.

9. **Fedder's criterion needs a homogeneous or local hypothesis.** [algorithm_outline.tex:309](./algorithm_outline.tex#L309).

   The stated test at \(\mathfrak m=(x_1,\ldots,x_n)\) does not characterize global F-splitness of an arbitrary nonhomogeneous polynomial. For instance, over \(\mathbb F_p\), \(f=x(x-1)^p\) has a nonzero coefficient of \(x^{p-1}\) in \(f^{p-1}\), yet its quotient ring is nonreduced at \(x=1\) and cannot be F-split. Restrict to homogeneous nonzero \(f\), as needed here, or formulate the local result. The cited [Ma–Polstra text](https://www.math.purdue.edu/~ma326/F-singularitiesBook.pdf) states the local theorem as Theorem 2.5 and the graded version as Remark 2.8.

10. **Ghost identities must be universal polynomial identities.** [algorithm_outline.tex:30](./algorithm_outline.tex#L30), [algorithm_outline.tex:54](./algorithm_outline.tex#L54).

    Having fixed characteristic p, the ghost map is \((a_0,a_1,\ldots)\mapsto(a_0,a_0^p,\ldots)\), and its higher coordinates cannot determine the higher addition and multiplication polynomials. State that there are unique integer polynomials satisfying the displayed identities **over the universal integer polynomial ring**, then evaluate them in R. This makes the subsequent definition unambiguous. See [Rabinoff's construction](https://arxiv.org/html/1409.7445).

11. **Verschiebung is an additive homomorphism.** [algorithm_outline.tex:128](./algorithm_outline.tex#L128).

    Say “homomorphism of additive groups,” not simply “homomorphism” in a paragraph otherwise discussing ring maps. On \(W(\mathbb F_p)=\mathbb Z_p\), it is multiplication by p, which is not multiplicative.

12. **The introductory generality is too broad.** [intro.tex:1](./intro.tex#L1), [intro.tex:19](./intro.tex#L19).

    An arbitrary variety does not automatically have the one-dimensional Artin–Mazur formal group underlying the height used here; one must specify the cohomological degree and hypotheses. Likewise, remove “and in fact for any surfaces” from the height-1/ordinary and infinite-height/supersingular discussion. The one-dimensional K3 argument does not extend to all surfaces as stated. Starting with K3 surfaces and then describing the applicable Calabi–Yau generalization is safer and clearer.

13. **Smoothness/properness must be part of the geometric terminology.** [intro.tex:11](./intro.tex#L11), [intro.tex:60](./intro.tex#L60), [algorithm_outline.tex:320](./algorithm_outline.tex#L320), [algorithm_outline.tex:599](./algorithm_outline.tex#L599).

    The definition of a K3 surface should include smoothness and properness (and the usual geometric connectedness hypothesis). A “quartic K3 surface” is a **smooth** quartic in projective 3-space. A homogeneous degree-n equation in n variables need not define a smooth Calabi–Yau variety. Distinguish the possibly singular algebraic input from the smooth geometric object whose Artin–Mazur height is asserted.

14. **A cutoff does not by itself certify infinite height.** [algorithm_outline.tex:613](./algorithm_outline.tex#L613), [algorithm_outline.tex:625](./algorithm_outline.tex#L625), [multiply_then_split.tex:59](./multiply_then_split.tex#L59).

    For an arbitrary chosen b, the output after exhausting the loop is “height greater than b,” not necessarily infinity. Either require b to be a known upper bound on all finite heights of the admissible inputs, or return a distinct cutoff status. For smooth quartic K3 surfaces b=10 suffices. The theorem at line 638 can say \(h\le b\), since the loop does test h=b. Also qualify the introductory “guaranteed to run h−1 times” at [intro.tex:137](./intro.tex#L137) by finite height within the cutoff.

15. **The Fermat worked example has the wrong product degree and skips an operation.** [algorithm_outline.tex:673](./algorithm_outline.tex#L673).

    After cubing the lift and subtracting the cubes of individual terms, divide by 3 and reduce modulo 3. Here \(\deg g=8\), \(\deg\Delta_1(g)=24\), and \(\deg(g\Delta_1(g))=32\), not 24. Then \((32-8)/3=8\) explains the trace degree.

    The statement about exponents being multiples of four does not justify vanishing after the trace: pre-trace exponent 8 becomes exponent 2. A short correct verification is available. Set \(X_i=x_i^4\); then \(g=(X_1+\cdots+X_4)^2\). The only possible surviving output is \(x_1^2x_2^2x_3^2x_4^2\), with coefficient
    \[
    \frac{1}{3}\frac{8!}{(2!)^4}=840\equiv0\pmod3.
    \]
    The cubed individual terms contribute nothing to this coefficient. Hence the first trace is zero and all later iterates remain zero.

16. **The cyclotomic extension degree has the wrong argument.** [algorithm_outline.tex:498](./algorithm_outline.tex#L498).

    The ring introduced is \(\mathbb Z[\zeta_{q-1}]\), so its fraction field has degree \(\varphi(q-1)\), not \(\varphi(q)=p^{e-1}(p-1)\). Also specify a prime above p and a residue-field identification when describing the cyclotomic lift. These choices matter when there is more than one prime above p.

17. **The height stratification inequality is reversed.** [heights.tex:37](./heights.tex#L37).

    The closed nested loci are \(M_i=\{X:h(X)\ge i\}\), with \(M_1=M\). A locus defined by \(h\le i\) grows as i increases and cannot be cut out inside \(M_{i-1}\) as described. Replace the internally contradictory phrase “locus of height i such that h≤i” with the definition above.

18. **The frequency heuristic has an off-by-one error and conflates exact and tail probabilities.** [heights.tex:53](./heights.tex#L53), [heights.tex:78](./heights.tex#L78).

    Under the paper's own codimension-one heuristic,
    \[
    \Pr(H\ge h)\approx p^{-(h-1)},\qquad
    \Pr(H=h)\approx p^{-(h-1)}-p^{-h}=\frac{p-1}{p^h}
    \]
    for finite heights 1 through 10, with the final tail interpreted as the supersingular locus. In particular, the ordinary probability is about \(1-1/p\), not \(1/p\). The claims of agreement with \(1/5^h\) and \(1/7^h\) “to three digits” require the actual counts and a precise denominator. They might describe a differently conditioned statistic, but are not compatible with the stated unconditioned heuristic.

    Consequently, revisit the sample-size and waiting-time discussion. If throughput counts all random surfaces, the heuristic waiting count for **exactly** height 10 is \(p^{10}/(p-1)\); \(p^9\) is the count for height at least 10. If throughput instead counts only nonordinary inputs, condition the probability accordingly. Discarding cheap height-1 cases without defining the throughput denominator mixes the two models.

19. **Lang–Weil needs geometric irreducibility and a base field.** [heights.tex:8](./heights.tex#L8).

    State that X is geometrically irreducible and defined over \(\mathbb F_p\). Irreducibility over \(\mathbb F_p\) alone does not give the leading coefficient 1 uniformly along extensions. For example, \(\operatorname{Spec}\mathbb F_{p^2}\) has zero points for odd extension degree and two for even degree. See [Kedlaya's precise statement](https://kskedlaya.org/weil-cohom/chapter-8.html). The same geometric qualification belongs in the heuristic if it is intended to model a single component.

20. **The NTT coefficient bound uses p instead of p².** [polymul.tex:186](./polymul.tex#L186).

    Working modulo \(13^2\), reduced coefficients can be as large as 168, not 12. The stated elementary bound becomes
    \[
    2^{28}(13^2-1)^2=7{,}576{,}322{,}310{,}144,
    \]
    still comfortably below the Goldilocks prime. Thus the numerical argument is repairable without changing its conclusion. At line 168, the unsafe threshold is “greater than or equal to” the NTT prime, since a coefficient equal to q also wraps to zero.

21. **The Float32 explanation confuses precision loss with overflow.** [matmul.tex:10](./matmul.tex#L10), [matmul.tex:17](./matmul.tex#L17).

    Set \(\ell=2^{24}\), the upper endpoint through which **every** nonnegative integer is exactly representable in Float32. This is not the largest integer representable by that type. Integer multiplication is exact only when the exact product is representable, and a dot-product argument must bound intermediate sums too. With inputs in \(\{0,\ldots,N-1\}\) and accumulation from zero, a sufficient length bound is
    \[
    o=\left\lfloor\frac{2^{24}}{(N-1)^2}\right\rfloor.
    \]
    The manuscript's extra −1 is conservative, not dangerous, but is not the claimed maximum. The corresponding bounds are 4,194,304; 1,048,576; 466,033; 167,772; and 116,508. All five matrix dimensions in the manuscript are correct and remain within these limits. Explain the actual accumulation precision/math mode used: [NVIDIA's floating-point documentation](https://docs.nvidia.com/cuda/floating-point/index.html) and [cuBLAS compute modes](https://docs.nvidia.com/cuda/cublas/index.html) distinguish datatype from arithmetic mode. For these small coefficients some reduced input formats may also be exact, but that requires its own argument.

22. **Dehomogenization is injective only at a fixed degree.** [polymul.tex:53](./polymul.tex#L53).

    Replace “injective on homogeneous elements” with “injective on each fixed-degree homogeneous component.” Otherwise the homogeneous polynomials 1 and \(x_n\) are a counterexample. The intended implementation already knows the degree, so this is a statement correction.

23. **A matching tuple is incorrect.** [multiply_then_split.tex:404](./multiply_then_split.tex#L404).

    Replace \((8,7,0,1)\) with \((8,5,2,1)\), obtained by adding \((5,5,0,0)\) to \((3,0,2,1)\). The printed tuple does not satisfy the required residue condition.

24. **The count of terms of Δ is an upper bound, not an equality.** [multiply_then_split.tex:178](./multiply_then_split.tex#L178).

    Use \(\ell_\Delta\le\binom{n(p^2-p+1)-1}{n-1}\). Terms can be absent or cancel. Similarly, statements that \(\Delta_1(f)\) has degree pd should allow that it can be zero: “is homogeneous of degree pd, possibly zero” avoids the degree-of-zero issue.

**Claims needing qualification, evidence, or fuller algorithm specifications**

25. **The cone/projective height identification needs an additional citation.** [algorithm_outline.tex:377](./algorithm_outline.tex#L377).

    [Yobuko's Theorem 4.5](https://arxiv.org/html/1704.05604) identifies the Artin–Mazur height with the geometric quasi-F-split height of a Calabi–Yau variety. It does not alone establish equality with the height of its affine homogeneous coordinate ring. Add the cone/section-ring result, or cite a result that explicitly incorporates it, such as [Kawakami–Takamatsu–Yoshikawa, Theorem 5.16](https://arxiv.org/html/2204.10076v3#S5.SS3). Check numbering against the version actually cited. Also state the needed positive dimension and field hypotheses.

26. **The Taelman attribution needs a hypothesis check.** [intro.tex:46](./intro.tex#L46).

    The realization theorem in [Taelman 2016](https://arxiv.org/pdf/1507.08547) assumes a potential semistable reduction property. The manuscript cites it as an unconditional existence argument without mentioning that hypothesis. This is a citation gap, not a claim that all-heights existence is false. An unconditional replacement for finite heights in p≥5 is [Ito, Theorem 6.4](https://arxiv.org/pdf/1612.05382), taking Picard number 2; the cited explicit examples already address p=2,3. Treat infinite height separately as needed.

27. **The cited ToricControlledReduction complexity is not \(O(p^{1/2})\).** [heights.tex:133](./heights.tex#L133).

    The [Costa–Harvey–Kedlaya paper](https://arxiv.org/html/1806.00368) describes quasi-linear dependence on p and explicitly says a square-root improvement is not attempted there. Cite the actual algorithm/version supporting a different bound, or change the assertion to the bound in the cited source. The qualitative expectation that its scaling will eventually win can remain, but should rest on the correct comparison.

28. **The general matrix-construction complexity omits output initialization.** [multiply_then_split.tex:224](./multiply_then_split.tex#L224), [multiply_then_split.tex:452](./multiply_then_split.tex#L452).

    Initializing the dense \(\ell_{d'}\times\ell_d\) matrix costs \(\Theta(\ell_{d'}\ell_d)\). Include this term or say that the stated bounds count entry generation after allocation/initialization. For very sparse Δ in the general setup, it cannot be ignored. State that n is fixed and hash lookup is expected constant time if those are the computational assumptions. The WICS binomial factor is bounded independently of p for fixed n in the Calabi–Yau specialization, not in the unrestricted d,n,p problem.

29. **Specify empty cases in the general WICS setup.** [multiply_then_split.tex:106](./multiply_then_split.tex#L106), [multiply_then_split.tex:365](./multiply_then_split.tex#L365).

    Set \(S_{d'}=0\) for negative as well as nonintegral d′. Define \(\operatorname{wics}(t,n)=\varnothing\) when t is negative or nonintegral, or guard those inputs explicitly. The phrase “because the division is exact” in the corollary's proof assumes a nonempty/integral case and should acknowledge that.

30. **The NTT algorithm needs its correctness conditions stated.** [polymul.tex:84](./polymul.tex#L84).

    Specify k≥0, positive moduli, the coefficient-lift convention defining \(\tilde f\), the NTT prime q, the fixed Kronecker base, and the zero-padding rule. Require the transform length L to divide q−1 and exceed the encoded degree of the product being computed. Otherwise an NTT computes cyclic convolution. A constant transform length in the main loop and smaller initial transforms are reasonable, but explain how the auxiliary polynomial is padded and transformed at the final loop length. The bare call `steps()` should state which problem-shape parameters determine its cached output.

31. **Bitpacking arithmetic needs no-carry/no-borrow conditions.** [multiply_then_split.tex:464](./multiply_then_split.tex#L464).

    Packed integer addition equals componentwise tuple addition only if fields have room for every intermediate exponent sum; subtraction similarly needs nonnegative componentwise differences. State the chosen field width condition and which coordinate occupies the most significant field for the claimed lexicographic comparison. This is an implementation precondition, not evidence that the existing implementation is wrong.

32. **The moduli/sampling description omits the smooth open subset.** [heights.tex:64](./heights.tex#L64).

    Projectivize the nonzero quartic forms, restrict to the smooth locus, then discuss the action of the algebraic group \(\mathrm{PGL}_4\). Quotienting the finite set of rational equations by \(\mathrm{PGL}_4(\mathbb F_p)\) describes rational coordinate-change orbits; it is not by itself a construction of the moduli space. Explain how smoothness was checked, whether singular samples were counted in frequency estimates, and how automorphisms affect the sampling distribution. This is especially relevant given finding 2.

33. **The benchmark figures disagree and need one consistent measurement description.** [intro.tex:180](./intro.tex#L180), [intro.tex:197](./intro.tex#L197), [multiply_then_split.tex:518](./multiply_then_split.tex#L518).

    The introduction gives matrix-construction times 0.037/0.343 seconds on CPU and about 0.0001 seconds on GPU for p=5,7. The table gives WICS CPU times 0.028/0.277 and GPU times 0.0024/0.025. The GPU differences are factors of 24 and 250, so this is not ordinary rounding. If the measurements differ in caching, transfers, synchronization, inputs, hardware, or software version, say so; otherwise update them together. Distinguish per-input latency from throughput under eight concurrent CPU callers and specify whether ordinary inputs are included. Record warmup, GPU synchronization, what each timer includes, and sample counts. The repo's existing data-availability TODO remains relevant.

34. **The quoted speedup magnitudes are inconsistent.** [intro.tex:208](./intro.tex#L208), [heights.tex:125](./heights.tex#L125).

    The explicit numbers give \(43/0.94\approx45.7\) times faster at p=11 and \(43/4.5\approx9.56\) times faster at p=13. Write those two factors, rather than alternately claiming 1.5 or two orders of magnitude. Clarify the comparison baseline and whether full zeta-function computation is being compared with height-only computation.

35. **The p=7 waiting-time arithmetic switches denominators.** [heights.tex:103](./heights.tex#L103).

    \(7^9/180\approx224{,}186.71\) seconds, whereas \(7^9/185\approx218{,}127.61\) seconds. The printed value uses 185 despite displaying 180. Fix this after resolving the probability/throughput conditioning in finding 18.

36. **The hardware comparison is too categorical.** [matmul.tex:4](./matmul.tex#L4).

    “Floating point types are faster than integer data types,” the factor-of-two claim, and “Int64 multiplication is not [supported in hardware]” need a specific architecture and operation. Matrix-library support, native instruction throughput, tensor-core throughput, and synthesized multi-instruction integer arithmetic are different issues. State the measured behavior on the actual GPUs and distinguish a lack of a particular native instruction from a lack of GPU execution support.

**Grammar, vocabulary, notation, and LaTeX fixes**

These are smaller changes; the first group includes genuine notation/cross-reference errors.

| Location | Current issue | Suggested change |
|---|---|---|
| [intro.tex:140](./intro.tex#L140) | Δ is called a “summand” of a multiplication | “factor” |
| [algorithm_outline.tex:102](./algorithm_outline.tex#L102) | \(\mathbb Z_p\) called the p-adic numbers | “p-adic integers” |
| [algorithm_outline.tex:150](./algorithm_outline.tex#L150) | Unspecified limit of truncated Witt rings | Write the inverse limit \(\varprojlim_n W_n(R)\) |
| [algorithm_outline.tex:423](./algorithm_outline.tex#L423) | Definition ends without punctuation | Add a period after \(\operatorname{coeff}(m)=a\) |
| [algorithm_outline.tex:444](./algorithm_outline.tex#L444) | Polynomial lift said to lie “in W(k)” | “in \(W(k)[x_1,\ldots,x_n]\)” |
| [algorithm_outline.tex:458](./algorithm_outline.tex#L458) | \(S_1\) called the “first Witt polynomial” | “the addition polynomial \(S_1\)” (the Witt polynomials were named \(\omega_n\)) |
| [algorithm_outline.tex:508](./algorithm_outline.tex#L508) | Algorithm label precedes its caption | Move `\label{alg:calc:delta1}` immediately after `\caption` |
| [algorithm_outline.tex:610](./algorithm_outline.tex#L610) | Lowercase caption beginning “quasi-” differs from the matrix algorithm caption | Choose one capitalization consistently |
| [algorithm_outline.tex:673](./algorithm_outline.tex#L673) | “We raise g^3 in the integers, and subtract by…” | “We cube the lift of g over the integers and subtract the cube of each term…” |
| [multiply_then_split.tex:91](./multiply_then_split.tex#L91) | Wrong input \(\Delta_1(f)\) | \(\Delta_1(f^{p-1})\) |
| [multiply_then_split.tex:138](./multiply_then_split.tex#L138) | “c.f.” | “cf.” or simply “see” |
| [multiply_then_split.tex:139](./multiply_then_split.tex#L139) | “The weak integer compositions … is the set” | “The set of weak integer compositions … is …” |
| [multiply_then_split.tex:154](./multiply_then_split.tex#L154) | Dimension uses k after defining degree d | \(\lvert\operatorname{wics}(d,n)\rvert\) |
| [multiply_then_split.tex:357](./multiply_then_split.tex#L357) | Undecorated B | \(B_d\) |
| [multiply_then_split.tex:366](./multiply_then_split.tex#L366) | `sum` typeset as three mathematical variables | Use `\operatorname{sum}` in both occurrences, including line 419 |
| [multiply_then_split.tex:382](./multiply_then_split.tex#L382) | “and δ a monomial” | “and let δ be a monomial” |
| [multiply_then_split.tex:390](./multiply_then_split.tex#L390) | An exponent tuple said to belong to a monomial basis | Say its corresponding monomial does not belong to \(B_{16}\) |
| [multiply_then_split.tex:428](./multiply_then_split.tex#L428) | Undefined \(M_d\) in function arguments | \(B_d\) |
| [multiply_then_split.tex:470](./multiply_then_split.tex#L470) | “addition and subtraction … reduces” | “reduce” |
| [multiply_then_split.tex:479](./multiply_then_split.tex#L479) | “performing the insides of the loop” | “executing the loop body” |
| [multiply_then_split.tex:501](./multiply_then_split.tex#L501) | “the fastest practically” | “the fastest in practice” |
| [multiply_then_split.tex:509](./multiply_then_split.tex#L509) | Figure label precedes caption | Move label immediately after caption at line 528 |
| [polymul.tex:8](./polymul.tex#L8) | “mass parallelization” | “massive parallelism” or “parallel execution” |
| [polymul.tex:19](./polymul.tex#L19) | “non-inclusive upper bound” | “strict upper bound” |
| [polymul.tex:77](./polymul.tex#L77) | “multiplying to an accumulator” | “multiplying the accumulator by …” (also line 103) |
| [polymul.tex:117](./polymul.tex#L117) | “section” for a numbered reference | “Section”; use subsection where that is the intended unit |
| [polymul.tex:183](./polymul.tex#L183) | “n−1 degree polynomials” | “polynomials of degree n−1” |
| [polymul.tex:211](./polymul.tex#L211) | “less total multiplications” | “fewer multiplications” |
| [matmul.tex:12](./matmul.tex#L12) | “floating points” | “floating-point types” |
| [matmul.tex:55](./matmul.tex#L55) | “Fedder type criterion” | “Fedder-type criterion” |
| [matmul.tex:59](./matmul.tex#L59) | Hardcoded “Figure 3” | This is Figure 2 among active figures; add a label and use `\ref` |
| [matmul.tex:60](./matmul.tex#L60) | Julia/FLINT “respectively” does not follow table's FLINT/Julia column order | Reorder or name each column explicitly |
| [heights.tex:100](./heights.tex#L100) | “a height = 10 example” | “an example of height 10” (also line 106) |
| [heights.tex:135](./heights.tex#L135) | “our algorithms … beat it” | “outperform our implementation” |
| [main.bib:278](./main.bib#L278) | Two `note` fields in the OpenBLAS entry | Merge URL/access date into one field; duplicate fields can trigger BibTeX diagnostics |
| [main.bib:158](./main.bib#L158) | Author names contain “Dr.” | Remove honorifics from bibliography author fields |

Optional style improvements: “We briefly overview” → “We briefly describe” (intro:117); “big finite field” → “large finite field” (intro:49); “memory overhead of communication” → “data-transfer overhead” (intro:192); “a large amount of unnecessary terms” → “many unnecessary terms” (multiply_then_split:132). Standardize `NVIDIA`, `cuBLAS`, `OpenBLAS`, `OSCAR`, and Calabi–Yau punctuation throughout. Use a consistent choice of “term” (coefficient included) versus “monomial” (usually coefficient 1); the algorithms currently blur these. The final tables list defining polynomials, so “Defining polynomial f” would be more precise than “Equation,” unless “=0” is supplied.

All active `\ref` and `\cite` keys resolve to defined labels/entries; there are no duplicate active labels. That check does not detect the before-caption counter errors listed above.

**Reproducibility and limits of the checks**

The [review_checks directory](./review_checks) contains the independent Python/NumPy checkers and recorded results. They parse the displayed equations directly from `heights.tex`, check that every term has total degree 4, and perform exact modular arithmetic. The full-height checker uses repeated multiplication by the original quartic modulo p², then extracts Δ and iterates its matrix. The exceptional F7 row was also checked by a separate direct residue-slice recurrence that does not construct a matrix. These checks do not use the authors' Julia packages or GPU code.

To rerun the intended scope from the repo root:

```bash
python3 review_checks/check_examples.py
python3 review_checks/check_heights.py 5 7
python3 review_checks/independent_recurrence.py
python3 review_checks/check_singularity.py
```

`check_examples.py` covers geometric smoothness and the ordinary/nonordinary coefficient for all 33 entries. `check_heights.py 5 7` covers higher heights only for F5 and F7. For the two smooth supersingular entries, vanishing through height 10 certifies infinity using the K3 finite-height bound. The singular row's computed value is reported only as its quasi-F-split recurrence value. Recorded runtimes are incidental verification timings, not controlled benchmarks or a comparison with the manuscript's performance results.
