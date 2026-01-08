Reviewer 1: Consider a K3 surface X over a finite field F_q. Its Artin-Mazur height is an
integer h between 1 and 10, or +infinity, which determines the Newton polygon
of X, and hence the point counts of X over extensions of F_q (i.e. its zeta
function). The question then arises whether every value of h can be realized
over a fixed finite field F_q. The answer is known to be "yes" over F_2, F_3,
and over large enough finite fields in any characteristic, but not in
general. The paper under review presents an algorithmic approach to also answer
"yes" (as expected) in the cases of F_5 and F_7, by drawing quartic K3 surfaces
at random and computing their heights. The cases F_11 and F_13 are partially
treated as well, even though the computations have ultimately been too
expensive in those cases. This is a welcome contribution to the explicit study
of K3 surfaces, which is a dynamic research topic.

The paper has two main parts. The first part (sections 2 and 3) presents an
algorithm from a preprint of Kawakami-Takamatsu-Yoshikawa [17] to compute h, as
well as a modification to it (precomputing the matrix of a certain linear
operator that has to be iterated). The second part (sections 4 to 6) presents
the authors' effort to implement this algorithm using GPUs (accessed through a
Julia interface), the rationale being that running the experiments on
traditional CPUs would be too slow.

The main issue is that I am not completely convinced that the authors are
always implementing the right algorithms or using the right tools for their
problem. For example:

- In Algorithm 1, why are you lifting the polynomial all the way to ZZ? It
seems to me that lifting to ZZ/p^2 ZZ would be enough. This would avoid the
problem of coefficient explosion that is the main focus of Section 5. See
e.g. Algorithm 3.1 in arXiv:2504.01834. What about the nmod_mpoly type in
FLINT for instance?

- In Section 4, it is quite clear that Algorithm 7 is the correct way to
compute u(Delta*m) when m is a monomial. (Figure 1 even suggests that using
GPUs is not vital with this algorithm). But is it necessary to compute the
whole matrix? If polynomials you manipulate stay sparse, then you could
compute u(Delta*m) only for the monomials m that actually occur in g at some
point during Algorithm 3 (and that match with some monomial of Delta).

- In Section 4, I understand that you thought of Algorithm 7 only after the
implementation work was done (cf. Section 7). Still, this algorithm is much
more efficient than Algorithms 5 and 6, so I wonder whether those should be
presented in such detail in the final version of your paper.

- In Section 6, I am not sure what the timings in Figure 3 refer to. Are you
referring to matrix-vector products (as in Algorithm 4) or matrix-matrix
products? Are you multiplying sparse or dense matrices? Are you multiplying
in characteristic 0 or directly mod p? Have you tried using FLINT's nmod_mat
type for instance?

Assuming the above comments make sense, I would encourage the authors to

(1) implement the above on traditional CPUs (for instance in FLINT or Magma) to
figure out if practical bottlenecks are still present;

(2) assuming they are, to discuss GPU replacements; and

(3) to re-run their computations using Algorithm 7, and maybe present the
relative costs of powering, evaluating u(Delta*m) for a monomial m, and
matrix-vector products in their experiments.

I realize that this is substantial work, however, such a rewrite is necessary
in my opinion to pass the acceptance bar.

More minor comments follow.

- p.4, Remark 2.12: (1) and (2) simply make no sense to me. F is a map of sets
from R to R. (3) does make sense though, because you can give the set R
different R-module structures.

- p.4, Definition 2.13: what do you mean by "split"? Same question for
"module-finite".

- p.4 L26: I think I^[m] is well-defined only when m is a power of p and R has
characteristic p. Otherwise, it will depend on the chosen set of generators.

- p.4, Theorem 2.16: this is the first time you use "weakly ordinary". If you
wish to define this term, it's better to do it outside of a theorem
statement.

- p.4, Definition 2.17: I was wondering whether R n-quasi-F-split implies that
R is (n+1)-squasi-F-split. Is this true?

- p.5, Definition 3.1: it would be helpful to say which ring Delta_1(f) belongs
to.

- p.5, Remark 3.4: as above, is it really necessary to lift all the way to
characteristic zero?

- p.5 L55: I don't recognize perspective (3) which would be a map S ->
F_*S. The set you describe generates F_*S as an S-module, and u lies in
Hom_S(F_*S, S).

- p.8, Definition 4.3: why are you calling this "weak integer decompositions"
and not just "partitions" for instance? You want to assume d_i nonnegative.

    - Alex: Too lazy to libgen a book to find a reputable definition of integer partitions, but generally order doesn't matter for partitions - (1, 1, 0) and (1, 0, 1) are the same partition. Order matters to us, so we use weak integer compositions.

- p.11, Algorithm 7, line 8: can you add a few words explaining why you write =
and not += here?

    - Alex: Probably should change to +=

- p.13, section 5.1.3: what are the "twiddle factors" you are referring to?

    - Alex: Suggested edit: "... too big to fit root of unity power tables and inputs ..."
            "... and don't cache the root of unity power tables. Because ..."
    The vocabulary "twiddle factors" should make sense to a reader who we assume 
    understands the FFT, and I honestly disagree with the reviewer here. If they 
    understand the FFT but not "twiddle factors", then a 2-second google search should 
    give them all the information they need.

- p.13 L31: what do you mean by "because of the precision of Barrett reduction"?

    - Alex: Not sure how to justify this without a long derivation, and even the original authors of this variation of Barrett reduction (https://arxiv.org/pdf/2209.01290) don't explain why moduli are limited to less than 2^62, they just claim they have the fastest 2^62 bit Barrett reduction.

- p.13 L46: "We know this computation will be correct because FLINT uses
GMP". What do you mean by this? FLINT only uses GMP for its integer type, and
GMP could contain bugs too, as far as I know.

    - Alex: I don't agree with the reviewer's sentiment to not trust GMP. How do we know to trust anything on our computers if cosmic rays can lead to nondeterministic CPU behavior?

- p.16, Theorem 7.1: O() is an asymptotic notation. What is going to infinity
here? Is X defined over QQ?

- p.16 L46: do you have a sense of why ToricControlledReduction becomes a
faster way to compute the Newton polygon as p grows?

- p.17 and following: can you check using the code of [11] that your examples
indeed have the correct Newton polygons?


Reviewer 2: The article under review is of a computational nature.

It provides explicit equations of curves over the fields F5 and F7
for each possible value of Artin-Mazur height h in 1..10.

These equations are found by random search on equations,
and the authors take advantage of an explicit criterion
of the literature that permits the computation of the height of
a given Calabi-Yau surface equation.

## Background

We may ignore the details, the point is that the criterion
is reduced to the following simple iterative process for an
equation f in variables $x,y,z,t$:

- compute g=f^(p-1) mod p
- compute a p-shift D = (f^p-\sum f_i^p)/p
- until g is in (exponents exceed p in each variable)
replace g by red(g*D),
where red(g) is a projection to exponents = (p-1) mod p.

The number of loops plus one gives the height of the surface.

This algorithm (the quasi-F-split Fedder's criterion)
is developed and proven in reference 17, and its authors
employed it to produce curves in characteristic 3.

However, when implemented in its stated form, it is no longer applicable for
bruteforce computations in larger characteristic.

## Contributions

This is where the article under review enters the scene.
I see three clear contributions in it.

1. Algorithmically, the authors identify two main bottlenecks
and investigate better implementations of the process.
Instead of doing complete and independent computations
at each step, they find it very useful to precompute
the linear map g->red(g*D) (Section 3), and to filter the
exponents in order to avoid the computation in the kernel
of the reduction (Section 4).
They also consider algorithmic ideas like bitpacking
the exponents and using FFT to accelerate the initial powering of
the equation.
2. They benchmark the efficiency of both CPU and GPU hardware for this task.
The interesting conclusion is that the GPU speedup suffices to
run a massive computation. The other algorithmic optimizations
are noticeable, but on a smaller scale.
3. They obtain complete tables of examples of surfaces of all possible
heights in characteristic 5 and 7, and partial tables of height <=5
for primes 11 and 13.
These tables would have been completely out of reach without the improvements
of the paper.

I can add another contribution: the authors have written a nice introduction
to the problem and the algorithmic criterion developed in Reference 17:
in fact the latter adopts a much more general perspective, and does not
state the algorithm in an easy to understand form.

I was really interested in reading the paper, which is well written, in
particular the introduction.

I definitely think that the results and the methods are worth publishing
in a journal like JSC.

## Weakness

My main concern with the paper is that, except in the three lines abstract,
the real contribution regarding the algorithmic criterion is not clear.

The mathematical discourse of Section 2 (which I very much
enjoyed, by the way) draws the reader's attention away
from the real topic of the article, which is purely computational.

I think it would be much better to explain much sooner (before Section 2)
to the reader the real content

- that the article reconsiders an algorithm introduced in Reference 17
- that when properly demystified this algorithm amounts to a recursive
procedure involving only four mathematical operations:
powering,shift,multiplication,reduction
(I prefer the term reduction instead of splitting because it
captures more adequatly the computation involved).
- (the precise -- ie algorithmic -- definitions of the shift and
the reduction can be given here without reference to the mathematical
background)
- that powering and shift are computed once for each curve, while
multiplication and reduction occur in a loop of length h-1
(hence less than 10)
- that a naive implementation of these on full degree equations results
in disastrous timings

To make things clear: a reader may ask why so much emphasis is put
on general Witt vectors and
quasi-F-split maps in Section 2, since these concepts only matter for
the design and the proof of Algorithm 3.
However this algorithm is not improved by the paper under review
in any mathematical way. Its proof is not given either.

It is of course very interesting to explain that the shift corresponds
to the addition on length 2 Witt vectors and that the reduction
is a projection on the component S^p which is enough
to capture the splitting of the Frobenius, central to Algorithm 3.

But I suggest making it clear that Section 2 contains
background which is essential to the understanding of the criterion,
but not to its implementation.

Also the final criterion must be stated in Section 2, at least in
mathematical terms, since it clearly belongs to the background
taken from Reference 17.

This comprises Proposition 3.2, the beginning of Section 3.2 with
a clear definition of the reduction map, with Definition 4.2 and
the important remark make on page 7 line 24 (the effect of u on
any polynomial...).

Once all this mathematical stuff is settled, we can proceed with
Section 3 and the naive implementation of the criterion, starting
with the small remark of Section 3.4,
then the naive implementations of the two steps and Algorithm 4.

Sections 3.4 and 4 should be merged in my opinion, as optimizations
of the reduction step. Section 5 is fine.

The paper lacks a proper conclusion (what next on the topic, on the
experience of programming and using GPU, on software for Witt vectors...?)

## Small typographic remarks

Numbers refer to the left margin.

p4.17: please make the definition more readable by adding
a reformulation of the splitting

p5.25: link to remark 2.11

p16.8: final dot
    - Alex: can't find it