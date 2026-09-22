# Independent review 001

## Decision: revise

The graph-theoretic construction and every-valid-tree decoder are correct, but
the executable forward map is not defined on every legal source encoding.  The
repair is narrow: remove CPython's decimal-integer digit cap for this command and
add a raw JSON regression beyond the default limit.  Re-review can reuse the
graph proof, finite graph checks, and literature assessment below.

Reviewed candidate revision: `c2c6f8a` (candidate implementation and proof from
`537f518`, verification added at `c2c6f8a`).  Review date: 2026-09-22.

## Correctness

### Blocking finding

`work/contract.md:5-8,19-20` admits every nonnegative JSON integer `k` with no
machine-word bound.  `work/algorithm.py:39` parses it with the default CPython
JSON integer conversion.  On the locked CPython 3.14 runtime, a legal 5,000-digit
`k` is rejected by the interpreter's default 4,300-digit limit before
`construct` runs.  This contradicts the totality claim in `work/proof.md:73-76`
and means F is not a map on all legal source inputs.

The defect is reproduced by
`reviews/001/integer_boundary_check.py`:

```text
reproduced: forward and extraction modes reject a legal 5000-digit k
```

The existing evidence does not cover this boundary.  `work/verification.md:7`
uses only `2^130`, while line 29 calls that coverage "arbitrarily large encoded
thresholds".  One fixed large value is not arbitrary-length coverage.

Required correction and evidence: configure the candidate process to accept
unbounded decimal integers before `json.load`, retain exact comparison with
`n`, and add a subprocess regression using a raw JSON integer longer than 4,300
digits.  The same boundary should be exercised in extraction input because G
parses the embedded source through the same entry point.

### General construction and recovery audit

Apart from that encoding failure, the theorem in `work/proof.md` is sound.

- F produces a simple connected graph: `r` reaches every set vertex, each
  element vertex has its diagonal incidence edge, and `p` is pendant.  The
  threshold `K=2n+1-min(k,n)` is nonnegative and the output has `2n+2` vertices
  and `1+2n+2m` edges.
- Completeness holds for both threshold regimes.  A dominating set of size at
  most `min(k,n)` gives the stated tree with `p`, all element vertices, and all
  unused set vertices as leaves.  Thus target `NO-SOLUTION` validly implies
  source `NO-SOLUTION`.
- For any qualifying target tree, `r` is necessarily non-leaf: `rp` is forced
  and at least one root-to-set edge is needed to connect the other vertices.
  Hence at most `min(k,n)` non-root vertices are non-leaves.  For each source
  element `u`, either non-leaf `e_u` decodes `u`, or leaf `e_u` has a non-leaf
  set neighbor `s_v` whose incidence edge certifies that `v` dominates `u`.
  Mapping both layers to source labels and deduplicating cannot increase the
  number of non-root non-leaves.  This proves feasibility and the size bound for
  every valid target tree, not only canonical trees.
- `work/algorithm.py:22-32` implements that decoder exactly.  Validation of the
  target witness is not required inside G because the reduction contract gives
  G a valid target output as a precondition.
- The one-vertex boundary is covered: for `k=0`, H is a four-vertex path with
  only two leaves against `K=3`; for `k>=1`, its unique tree meets `K=2` and
  decodes `{0}`.  Negative targets and `k>n` are handled by the threshold cap.
- Once integer parsing is total, F is deterministic and polynomial: the direct
  pair scan is polynomial and its output is linear in `n+m` edges.  G scans the
  tree and two layers.  Vertex identifiers and the output have polynomial bit
  length.  No state, randomness, solver, or hidden oracle is used.

I did not rerun the full retained suites.  The targeted independent check
`reviews/001/targeted_check.py` enumerated all 24 qualifying target trees for a
four-cycle at `k=2`, checked each recovered set, exercised an explicit valid tree
whose element-layer vertex is non-leaf, and confirmed infeasibility at `k=0`:

```text
passed: 24 qualifying cycle trees; explicit element-layer decoding; k=0 infeasible
```

## Novelty

The underlying incidence construction is not novel.  Li and Toulouse,
*Variations of the maximum leaf spanning tree problem for bipartite graphs*,
Information Processing Letters 97(4), 129-132 (2006), gives in Section 2,
Theorem 2.1, a Set Cover reduction using the set-element incidence bipartite
graph plus an extra element adjacent to every set.  Its preceding Theorem 1.3
characterizes the relevant partite-set leaves.  Taking the sets to be the closed
neighborhoods of the source graph yields the core of the present construction.
Primary text: <https://doi.org/10.1016/j.ipl.2005.10.011> and an accessible copy
at <https://par.cse.nsysu.edu.tw/resource/paper/2006/060310/Variations%20of%20the%20maximum%20leaf%20spanning%20tree%20problem%20for%20bipartite%20graphs.pdf>.

Caro, West and Yuster, *Connected Domination and Spanning Trees with Many
Leaves*, SIAM Journal on Discrete Mathematics 13(2), 202-211 (2000), states in
the abstract and introduction the identity that maximum leaves equal graph
order minus minimum connected domination number.  This supports the
non-leaf/connected-domination step used by the candidate:
<https://doi.org/10.1137/S0895480199353780> and
<https://math.haifa.ac.il/raphy/papers/conndom.pdf>.

Garey and Johnson, *Computers and Intractability* (1979), ND2 at p. 206, records
Maximum Leaf Spanning Tree and its hardness/restrictions but does not print this
complete executable source-to-target rule on that page:
<https://perso.limos.fr/~palafour/PAPERS/PDF/Garey-Johnson79.pdf>.

The candidate's pendant vertex, total-leaf threshold, and decoder that maps
non-leaves from either incidence layer form a clean search-reduction packaging.
I did not locate that exact every-valid-output formulation in the checked
primary sources, but it is a direct refinement/composition of known ideas and
should not be presented as a new hardness result.  This is compatible with the
fixed question, which expressly accepts a reconstructed published construction.

Literature search date: 2026-09-22.  Queries covered Dominating Set to Maximum
Leaf Spanning Tree, Set Cover incidence reductions, and the connected
domination/maximum-leaf identity.  Coverage gaps: no exhaustive citation-graph
search, no full audit of all pre-2000 connected-domination reductions, and no
claim that the exact decoder is absent from theses, textbooks, or non-indexed
sources.  These gaps prevent a strong originality claim but do not undermine
the reconstruction contribution.

## Significance

Relative to the closest known results, the useful contribution is not a new
complexity classification.  It is a complete executable reduction for the
fixed search contract: explicit legal instance construction, correct handling
of `NO-SOLUTION`, and recovery from every qualifying spanning tree rather than
from one normalized witness.  That directly resolves the catalog's
ordinary-versus-connected domination ambiguity once the parser defect is fixed.

The constructed graph has `2n+2` vertices and `1+2n+2m` edges.  The current F
uses an `O(n^2+m)` membership scan although the output graph is sparse when G is
sparse; G is linear in the target tree size.  Target solving remains the
dominant NP-hard cost.  No practical speed claim is made, and the fixed question
has no stricter resource requirement, so this overhead is not a reason to stop.

## Isolation and route

This review ran as the registered `research-reviewer` with `fork_turns="none"`,
so a fresh child context was enforced.  The model route was: **registered
research-reviewer, no explicit model override; backend identifier not exposed**.
Filesystem access was unrestricted and agent tools were available; therefore
write confinement and no-delegation were instruction-only, not sandbox/tool
denial.  No further agent was spawned and no agent tool was used for delegation.
No structural depth cap was exposed.  All review writes are confined to
`campaigns/dominating-set-leaf-spanning-tree/reviews/001`.
