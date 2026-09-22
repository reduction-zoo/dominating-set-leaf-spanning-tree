# Round 001 — closed-neighborhood incidence construction

## Plan

Gap: the complement-of-leaves identity directly represents connected dominating
sets, while the source permits a disconnected dominating set.

Mechanism: treat Dominating Set as Set Cover. Build one set vertex `s_v` and one
element vertex `e_u` per source vertex, join `s_v` to `e_u` exactly when `v`
dominates `u`, join a root to every set vertex, and give the root one pendant
neighbor. The pendant should force the root to be internal. A leaf-rich tree
should then have at most `k` other internal vertices; replace each internal
element vertex by its corresponding source vertex and retain every internal set
vertex. This is intended to dominate all source vertices within the same count.

For unbounded encoded `k`, use `k' = min(k,n)` and threshold `2n+1-k'`, preserving
the source answer while keeping the target threshold legal. The full candidate
must handle every valid target tree and valid target `NO-SOLUTION`, not only a
canonical tree.

The shared experience collection was searched on 2026-09-22 for domination,
leaves, spanning trees and connected domination; no matching entry was found.

First discriminating check: implement both maps and run the committed exhaustive
candidate checker over all 11 injected source instances and every target tree it
enumerates. A failure will distinguish construction/recovery defects from the
already-passing oracle foundation. A pass supports finite behavior only and
leaves the general counting/recovery proof and literature status to audit.

## Evidence and diagnosis

The candidate loop passed all 11 prepared source cases and all 97 valid target
outputs independently enumerated for their constructed instances; see
[`candidate-check.txt`](candidate-check.txt). This includes positive and negative
source cases, target `NO-SOLUTION`, distinct target trees, the one-vertex source
boundary and `k=2^130`.

The general proof in [`../../work/proof.md`](../../work/proof.md) confirms the
mechanism. Any threshold-satisfying target tree has at most `k'+1` internal
vertices; the pendant makes the root one of them. Each leaf element vertex is
adjacent to an internal set vertex, while each internal element vertex can be
replaced by its own source vertex. These choices dominate all source vertices
and use at most the remaining `k'` internal vertices. Valid target
`NO-SOLUTION` is sound by the explicit forward tree built from any source
witness. No normalization of the target tree is assumed.

Primary-source search on 2026-09-22 found that Garey and Johnson's ND2 catalog
states a transformation from Dominating Set but does not print the construction,
and Caro, West and Yuster state the connected-domination/maximum-leaf identity.
The inspected sources did not establish that this exact two-layer incidence
construction is novel. It is best described as an independently derived direct
specialization of the standard Set Cover incidence idea, with low expected
novelty but useful completeness for the requested search-output contract.

- Garey and Johnson, *Computers and Intractability*, ND2, p. 206:
  <https://perso.limos.fr/~palafour/PAPERS/PDF/Garey-Johnson79.pdf>
- Caro, West and Yuster, *Connected Domination and Spanning Trees with Many
  Leaves*: <https://math.haifa.ac.il/raphy/papers/conndom.pdf>

Outcome: supported. Finite execution and the general proof agree; no candidate
defect or unresolved lemma remains before broader verification.

## Next action

Run independent verification on broader generated source families and alternate
target outputs, then request isolated review if it passes.

Experience extraction: none. The mechanism is a complete campaign-specific
construction, while its reusable ingredients are standard incidence and
connected-domination facts; no distinct new failure pattern or general lemma was
identified for the shared collection.
