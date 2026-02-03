# Response to Reviewer 1:

>> Reviewer 1: Consider a K3 surface X over a finite field F_q. Its Artin-Mazur height is an
>> integer h between 1 and 10, or +infinity, which determines the Newton polygon
>> of X, and hence the point counts of X over extensions of F_q (i.e. its zeta
>> function). The question then arises whether every value of h can be realized
>> over a fixed finite field F_q. The answer is known to be "yes" over F_2, F_3,
>> and over large enough finite fields in any characteristic, but not in
>> general. The paper under review presents an algorithmic approach to also answer
>> "yes" (as expected) in the cases of F_5 and F_7, by drawing quartic K3 surfaces
>> at random and computing their heights. The cases F_11 and F_13 are partially
>> treated as well, even though the computations have ultimately been too
>> expensive in those cases. This is a welcome contribution to the explicit study
>> of K3 surfaces, which is a dynamic research topic.
>> 
>> The paper has two main parts. The first part (sections 2 and 3) presents an
>> algorithm from a preprint of Kawakami-Takamatsu-Yoshikawa [17] to compute h, as
>> well as a modification to it (precomputing the matrix of a certain linear
>> operator that has to be iterated). The second part (sections 4 to 6) presents
>> the authors' effort to implement this algorithm using GPUs (accessed through a
>> Julia interface), the rationale being that running the experiments on
>> traditional CPUs would be too slow.
>> 
>> The main issue is that I am not completely convinced that the authors are
>> always implementing the right algorithms or using the right tools for their
>> problem. For example:
>> 
>> - In Algorithm 1, why are you lifting the polynomial all the way to ZZ? It
>> seems to me that lifting to ZZ/p^2 ZZ would be enough. This would avoid the
>> problem of coefficient explosion that is the main focus of Section 5. See
>> e.g. Algorithm 3.1 in arXiv:2504.01834. What about the nmod_mpoly type in
>> FLINT for instance?

We would like to thank Reviewer 1 for pointing this out, not lifting to ZZ/p^2 ZZ was a clear oversight in our approach. Please see below for the changes we made.

>> 
>> - In Section 4, it is quite clear that Algorithm 7 is the correct way to
>> compute u(Delta*m) when m is a monomial. (Figure 1 even suggests that using
>> GPUs is not vital with this algorithm). But is it necessary to compute the
>> whole matrix? If polynomials you manipulate stay sparse, then you could
>> compute u(Delta*m) only for the monomials m that actually occur in g at some
>> point during Algorithm 3 (and that match with some monomial of Delta).

It is not strictly necessary to compute the whole matrix. For example, our algorithms for computing the matrix of a \mapsto u(\delta a) can easily be made sparse. However, we found this was not necessary for our computation (finding K3 surfaces of all heights) in characteristic 5 and 7. Sparse computations may offer a speedup, but we have found that this step is not the bottleneck of the computation, even in characteristic 11.

In fact, we have a work in progress that implements similar algorithms to the ones presented here. There, calculating this matrix may sometimes be the bottleneck. In that work, we have implemented a sparse version and it has led to a nice speedup.

One can also ask to use a sparse multiplication/powering algorithm for the computation of Delta_1. We do this by default on the CPU using FLINT. However, on the GPU the choice is not as clear. In Summer 2024, some preliminary experiments suggested that sparse GPU implementations may actually be worse than a dense GPU algorithms for our problem size.

Perhaps there are some variants of this problem where a sparse GPU algorithm provides significant speedups. We recognize this as future work.

>> 
>> - In Section 4, I understand that you thought of Algorithm 7 only after the
>> implementation work was done (cf. Section 7). Still, this algorithm is much
>> more efficient than Algorithms 5 and 6, so I wonder whether those should be
>> presented in such detail in the final version of your paper.

We agree that section 4 needs improvement. In our revision, we have chosen to remove Algorithm 6 and keep Algorithm 5. There are two main reasons that led us to this choice:

First, we would like ot note that even the most naive algorithm (i.e. Algorithm 5) on the GPU gives a significant speedup. Indeed, this speedup was sufficient to solve the existence of K3 surfaces in characteristic 5, and perhaps characteristic 7. We find this very interesting and worth sharing through the paper.

Second, algorithm 5's writeup is relatively short compared to algorithm 6.

>> 
>> - In Section 6, I am not sure what the timings in Figure 3 refer to. Are you
>> referring to matrix-vector products (as in Algorithm 4) or matrix-matrix
>> products? Are you multiplying sparse or dense matrices? Are you multiplying
>> in characteristic 0 or directly mod p? Have you tried using FLINT's nmod_mat
>> type for instance?

In our revision, we have tried to improve Figure 3 to highlight that:

* These are matrix-matrix products
* They are dense matrices
* They are multiplying in characteristic p. The time is taken by doing an integer/floating point MATMUL and then reducing modulo p.
* FLINT uses single-threaded BLAS for multiplication in this case, via its Oscar.jl wrapper. We have highlighted this in the figure.

>> 
>> Assuming the above comments make sense, I would encourage the authors to
>> 
>> (1) implement the above on traditional CPUs (for instance in FLINT or Magma) to
>> figure out if practical bottlenecks are still present;
>> 
>> (2) assuming they are, to discuss GPU replacements; and
>> 
>> (3) to re-run their computations using Algorithm 7, and maybe present the
>> relative costs of powering, evaluating u(Delta*m) for a monomial m, and
>> matrix-vector products in their experiments.
>> 
>> I realize that this is substantial work, however, such a rewrite is necessary
>> in my opinion to pass the acceptance bar.

We would like to thank Reviewer 1 for these suggestions. At the same time, we would like to mention that we had already done much of this work. However, these may not have been communicated clearly in the paper.

For example, all of our GPU algorithms have a CPU implementation that uses FLINT via Oscar.jl. The only instance where FLINT was not used was for CPU matrix multiplication, where we used Julia's built-in matrix multiplication. This calls the same BLAS library that FLINT uses, but with more threads by default.

The one thing we had not implemented was the lift modulo p^2 instead of the lift to ZZ, which affects the computation of \Delta_1 only. We have addressed this in our revision by providing:

* A (FLINT via Oscar) CPU version of Delta_1 that lifts modulo p^2
* An FFT-based GPU implementation of an "incremental multiplication" algorithm. Namely, if we wish to compute g^d, it computes d = n * d_1 + d\_2 for d_1 as large as possible so that g^{d_1} does not overflow the prime in our "multimodular" (now single-modular) algorithm. Since we can now use only one prime, we use the Goldilocks prime to achieve fast reductions and FFTs.

Our FLINT CPU times are comparable to the times for ZZ, which was expected: the coefficient explosion does not trigger until p=11, while the explosion in the number of terms can already be seen at p=5. p=7 took such a significant amount of time that we found it was unnecessary to time Delta_1 on the CPU for p=11.

On the other hand, the incremental multiplication algorithm gives no discernible difference for p=5 (since we only needed one prime anyways here). For p=7, it provides a small speedup. For p=11 and p=13, incremental multiplication gives an incredible 1.5 orders of magnitude speedup. With this algorithm, we actually found a height h=6 K3 surface in characteristic p=11. Once again, we would like to thank Reviewer 1 for this suggestion.

Furthermore, we have added a section to the introduction that explains the algorithm's bottlenecks with timings. The polynomial powering section has also been updated to describe the incremental multiplication algorithm, instead of multimodular FFT.

>> 
>> More minor comments follow.
>> 
>> - p.4, Remark 2.12: (1) and (2) simply make no sense to me. F is a map of sets
>> from R to R. (3) does make sense though, because you can give the set R
>> different R-module structures.

We have tried to clarify this in the revised exposition.  

In particular, we may identify R with the set R^p = {r^p | r \in R}, where the "raising to the p" is a formal decoration. Formally, this is a ring isomorphic to R. Now, we may define the map of sets R^p \to R, r^p \mapsto r^p, where the latter uses multiplication in the ring R. This map is a ring homomorphism by the freshman's dream. When we undo the identification R^p \isom R, it identifies with the Frobenius.

We may also identify the ring R with R^1/p, the set of formal pth roots of elements in R, in an exactly analogous way. When we apply the previous construction to that, we find that (R^1/p)^p is just R under the map r^1/p^p \mapsto r, removing both symbols.

>> 
>> - p.4, Definition 2.13: what do you mean by "split"? Same question for
>> "module-finite".

We have added clarifications to the paper. 

Here, split means to map back such that the composition is identity. Module-finite refers to a finitely generated as a module, in contrast to finitely generated as an algebra "finite type" or "algebra-finite". This is a commutative-algebra-ism.

>> 
>> - p.4 L26: I think I^[m] is well-defined only when m is a power of p and R has
>> characteristic p. Otherwise, it will depend on the chosen set of generators.

The definition has been changed to use p^e.

>> 
>> - p.4, Theorem 2.16: this is the first time you use "weakly ordinary". If you
>> wish to define this term, it's better to do it outside of a theorem
>> statement.

Since this term never comes up in the rest of the paper, we omit it.

>> 
>> - p.4, Definition 2.17: I was wondering whether R n-quasi-F-split implies that
>> R is (n+1)-squasi-F-split. Is this true?

It is! This is good to include, and an explanation has been added.

>> 
>> - p.5, Definition 3.1: it would be helpful to say which ring Delta_1(f) belongs
>> to.

Added.

>> 
>> - p.5, Remark 3.4: as above, is it really necessary to lift all the way to
>> characteristic zero?

No, see above.

>> - p.5 L55: I don't recognize perspective (3) which would be a map S ->
>> F_*S. The set you describe generates F_*S as an S-module, and u lies in
>> Hom_S(F_*S, S).

This was a typo. It was supposed to be (2), which has now changed to (1) with other edits.

>> 
>> - p.8, Definition 4.3: why are you calling this "weak integer decompositions"
>> and not just "partitions" for instance? You want to assume d_i nonnegative.

"Weak integer compositions" is term from the enumerative combinatorics literature. A composition is an ordered partition, and a weak composition allows entries to be zero. "Integer" here is in the same sense as integer partitions (as opposed to, say, set partitions or partitions of elements in some ring).


>> 
>> - p.11, Algorithm 7, line 8: can you add a few words explaining why you write =
>> and not += here?
>> 

This was a typo. We note that in some cases, the algorithm still seems to work when it has an "=", indicating that there is at most one matching term. This seems to deserve further consideration, but is out of scope for this project. Namely, understanding this is unlikely to give a speedup big enough to compute K3 surfaces with higher heights.

>> 
>> - p.13, section 5.1.3: what are the "twiddle factors" you are referring to?
>> 
>> 
>> - p.13 L31: what do you mean by "because of the precision of Barrett reduction"?
>> 

The corresponding section has been edited to describe incremental multiplication rather than multimodular FFT.

>> 
>> - p.13 L46: "We know this computation will be correct because FLINT uses
>> GMP". What do you mean by this? FLINT only uses GMP for its integer type, and
>> GMP could contain bugs too, as far as I know.

This has been removed. At the time, we meant to say "this computation won't overflow as FLINT uses GMP."

>> 
>> - p.16, Theorem 7.1: O() is an asymptotic notation. What is going to infinity
>> here? Is X defined over QQ?

One may interpret this as p is going to infinity, which tacitly assumes that X is defined over QQ and we are implicitly lifting/reducing mod p. 

However, it may also be interpreted in a more casual sense: there exists an expression for which p^{r - 1/2} (possibly with some constant) is the dominant term, In other words, of all the terms in the expression, this one has the largest norm. Such notation shows up, for example, when one prints out elements of power series rings in Oscar.jl (there, one is using the x-adic norm).

Both are fine interpretations of the big O notation here.

>> 
>> - p.16 L46: do you have a sense of why ToricControlledReduction becomes a
>> faster way to compute the Newton polygon as p grows?

It's complexity in p is p^1/2, while this algorithm is exponential.

>> 
>> - p.17 and following: can you check using the code of [11] that your examples
>> indeed have the correct Newton polygons?
>> 

Please note that ToricControlledReduction only supports p=11 and p=13. Instead, we checked this against a forthcoming project of the second author, the first author, Mellberg, and Huang, which implements a similar algorithm to ToricControlledReduction.

This revealed that some of the examples in our tables for p=5 and p=7 were not smooth, so we updated the tables with other examples that are smooth. According to this, the Newton polygons are all correct.

# Response to Reviewer 2:

>> 
>> Reviewer 2: The article under review is of a computational nature.
>> 
>> It provides explicit equations of curves over the fields F5 and F7
>> for each possible value of Artin-Mazur height h in 1..10.
>> 
>> These equations are found by random search on equations,
>> and the authors take advantage of an explicit criterion
>> of the literature that permits the computation of the height of
>> a given Calabi-Yau surface equation.
>> 
>> ## Background
>> 
>> We may ignore the details, the point is that the criterion
>> is reduced to the following simple iterative process for an
>> equation f in variables $x,y,z,t$:
>> 
>> - compute g=f^(p-1) mod p
>> - compute a p-shift D = (f^p-\sum f_i^p)/p
>> - until g is in (exponents exceed p in each variable)
>> replace g by red(g*D),
>> where red(g) is a projection to exponents = (p-1) mod p.
>> 
>> The number of loops plus one gives the height of the surface.
>> 
>> This algorithm (the quasi-F-split Fedder's criterion)
>> is developed and proven in reference 17, and its authors
>> employed it to produce curves in characteristic 3.
>> 
>> However, when implemented in its stated form, it is no longer applicable for
>> bruteforce computations in larger characteristic.
>> 
>> ## Contributions
>> 
>> This is where the article under review enters the scene.
>> I see three clear contributions in it.
>> 
>> 1. Algorithmically, the authors identify two main bottlenecks
>> and investigate better implementations of the process.
>> Instead of doing complete and independent computations
>> at each step, they find it very useful to precompute
>> the linear map g->red(g*D) (Section 3), and to filter the
>> exponents in order to avoid the computation in the kernel
>> of the reduction (Section 4).
>> They also consider algorithmic ideas like bitpacking
>> the exponents and using FFT to accelerate the initial powering of
>> the equation.
>> 2. They benchmark the efficiency of both CPU and GPU hardware for this task.
>> The interesting conclusion is that the GPU speedup suffices to
>> run a massive computation. The other algorithmic optimizations
>> are noticeable, but on a smaller scale.
>> 3. They obtain complete tables of examples of surfaces of all possible
>> heights in characteristic 5 and 7, and partial tables of height <=5
>> for primes 11 and 13.
>> These tables would have been completely out of reach without the improvements
>> of the paper.
>> 
>> I can add another contribution: the authors have written a nice introduction
>> to the problem and the algorithmic criterion developed in Reference 17:
>> in fact the latter adopts a much more general perspective, and does not
>> state the algorithm in an easy to understand form.
>> 
>> I was really interested in reading the paper, which is well written, in
>> particular the introduction.
>> 
>> I definitely think that the results and the methods are worth publishing
>> in a journal like JSC.
>> 
>> ## Weakness
>> 
>> My main concern with the paper is that, except in the three lines abstract,
>> the real contribution regarding the algorithmic criterion is not clear.
>> 
>> The mathematical discourse of Section 2 (which I very much
>> enjoyed, by the way) draws the reader's attention away
>> from the real topic of the article, which is purely computational.
>> 
>> I think it would be much better to explain much sooner (before Section 2)
>> to the reader the real content
>> 
>> - that the article reconsiders an algorithm introduced in Reference 17
>> - that when properly demystified this algorithm amounts to a recursive
>> procedure involving only four mathematical operations:
>> powering,shift,multiplication,reduction
>> (I prefer the term reduction instead of splitting because it
>> captures more adequatly the computation involved).

We are concerned that the term "reduction" may be confusing. We regularly speak of reduction mod p, and more generally reduction modulo an ideal I of a ring. Much literature in the area uses similar terminologies. This operation is not a reduction in that sense, and we do not wish to overload the word. 

In the revised version of the paper, we continue to refer to this as "splitting" to match the matematical origins. However, we are open to other suggestions for a word that better captures the computation.

>> - (the precise -- ie algorithmic -- definitions of the shift and
>> the reduction can be given here without reference to the mathematical
>> background)
>> - that powering and shift are computed once for each curve, while
>> multiplication and reduction occur in a loop of length h-1
>> (hence less than 10)
>> - that a naive implementation of these on full degree equations results
>> in disastrous timings
>> 
>> To make things clear: a reader may ask why so much emphasis is put
>> on general Witt vectors and
>> quasi-F-split maps in Section 2, since these concepts only matter for
>> the design and the proof of Algorithm 3.
>> However this algorithm is not improved by the paper under review
>> in any mathematical way. Its proof is not given either.
>> 
>> It is of course very interesting to explain that the shift corresponds
>> to the addition on length 2 Witt vectors and that the reduction
>> is a projection on the component S^p which is enough
>> to capture the splitting of the Frobenius, central to Algorithm 3.
>> 
>> But I suggest making it clear that Section 2 contains
>> background which is essential to the understanding of the criterion,
>> but not to its implementation.
>> 
>> Also the final criterion must be stated in Section 2, at least in
>> mathematical terms, since it clearly belongs to the background
>> taken from Reference 17.
>> 
>> This comprises Proposition 3.2, the beginning of Section 3.2 with
>> a clear definition of the reduction map, with Definition 4.2 and
>> the important remark make on page 7 line 24 (the effect of u on
>> any polynomial...).
>> 
>> Once all this mathematical stuff is settled, we can proceed with
>> Section 3 and the naive implementation of the criterion, starting
>> with the small remark of Section 3.4,
>> then the naive implementations of the two steps and Algorithm 4.
>> 
>> Sections 3.4 and 4 should be merged in my opinion, as optimizations
>> of the reduction step. Section 5 is fine.

We appreciate Reviewer 2's comments, and believe that they will help make the article more accessible.

In particular, we agree with Reviewer 2 about our mathematical vs. algorithmic computations. Our paper was written with both experts in the F-singularities literature and computer algebra experts in mind - hence the extra background. 

In our revision, we have attempted to address these issues by expanding the introduction and reorganizing the paper.

* The introduction now contains a section which describes the algorithmic bottlenecks and gives timings.
* We decided to merge much of Section 3 into Section 2, Section 3.2, the above mentioned remark, and Definition 4.2, as described above.
* The remaining material in Section 3 has been merged more tidily into Section 4. Thus section 4 has a slightly bigger scope now, and Section 3 has been removed.

>> The paper lacks a proper conclusion (what next on the topic, on the
>> experience of programming and using GPU, on software for Witt vectors...?)
>> 
>> ## Small typographic remarks
>> 
>> Numbers refer to the left margin.
>> 
>> p4.17: please make the definition more readable by adding
>> a reformulation of the splitting

Added, Reviewer 1 also asked for this.

>> 
>> p5.25: link to remark 2.11

Added.

>> 
>> p16.8: final dot

We believe this feedback was about the end of the paragraph before Heuristic 7.2. We added a semicolon to the end of that paragraph.