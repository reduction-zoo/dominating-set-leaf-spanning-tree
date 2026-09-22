# Reduction and proof

## Construction

Let the legal source instance be a connected simple graph `G=(V,E)` with
`V={0,...,n-1}` and nonnegative integer `k`. Put `k'=min(k,n)`. Construct `H`
with vertices

- a root `r` and its pendant neighbor `p`;
- a set vertex `s_v` for every `v` in `V`; and
- an element vertex `e_u` for every `u` in `V`.

Add `rp`, every edge `r s_v`, and `s_v e_u` exactly when `u` belongs to the
closed neighborhood of `v` in `G`. Set the target threshold to
`K=2n+1-k'`. This is the forward map F implemented by `algorithm.py`.

For a valid target tree `T`, the recovery map G returns `NO-SOLUTION` when that
is the target output. Otherwise it returns the source vertices corresponding to
all set vertices of degree at least two in `T`, together with every `u` whose
element vertex `e_u` has degree at least two in `T`. Duplicate source vertices
are removed.

## Legality and completeness

`H` is simple and connected: every set vertex is adjacent to `r`, every element
vertex has at least its diagonal edge to its same-index set vertex, and `p` is
adjacent to `r`. Since `0 <= k' <= n`, `K >= n+1`, so the target instance is
legal.

Suppose `D` is a dominating set of `G` with `|D| <= k`. Its size is also at most
`k'`: if `k<n` this is immediate, while if `k>=n`, `V` itself is an available
witness of size `n=k'`. Choose a dominating witness of size at most `k'`. Form a
tree using `rp`, all `n` edges `r s_v`, and, for each `u`, one edge `s_v e_u`
with `v` chosen from the witness to dominate `u`. It is connected and has
`2n+1` edges on `2n+2` vertices, hence is a spanning tree. The pendant, every
element vertex, and every set vertex outside the witness are leaves, giving at
least `1+n+(n-|D|) >= 2n+1-k'=K` leaves.

Consequently, if a valid target output is `NO-SOLUTION`, the source has no
dominating set of size at most `k`; otherwise the preceding construction would
be a valid target witness. Recovery may therefore return source `NO-SOLUTION`.

## Soundness for every target tree

Let `T` be any spanning tree of `H` with at least `K` leaves. It has `2n+2`
vertices, so it has at most

`(2n+2)-K = k'+1`

non-leaf vertices. The edge `rp` must occur because `p` has no other neighbor.
The root must also have an edge toward a set vertex to connect the remaining
vertices. Thus `r` has degree at least two and is a non-leaf. The tree has at
most `k'` other non-leaf vertices.

Consider any source vertex `u`. If `e_u` is a non-leaf, recovery includes `u`,
which dominates itself. If `e_u` is a leaf, its unique tree neighbor is some
`s_v`. A tree on `2n+2 >= 4` vertices cannot have adjacent leaves, so `s_v` is a
non-leaf and recovery includes `v`. By construction of the incidence edge,
`v` dominates `u` in `G`. Hence the recovered set dominates every source vertex.
It contains at most one source vertex for each non-root non-leaf of `T`, after
deduplication, so its size is at most `k' <= k`. This argument uses no canonical
form of `T` and covers every valid target tree.

Together with the `NO-SOLUTION` argument, for every legal source input and every
valid target output, G returns a valid source output.

## Complexity and encoding size

If `G` has `n` vertices and `m` edges, `H` has `2n+2` vertices and
`1+2n+2m` edges: one pendant edge, `n` root edges, and
`sum_v |N_G[v]| = n+2m` incidence edges. F constructs these in `O(n^2+m)` time
as implemented by its direct pair scan; a linear adjacency-list implementation
would not improve the polynomial claim. Exact comparison of `k` with `n` costs
polynomial time in their bit lengths. The output length is
`O((n+m) log n + log n)`, hence polynomial in the source encoding; the possibly
huge source `k` is not copied.

G scans the `2n+1` tree edges, then the two vertex layers, in `O(n)` arithmetic
operations on `O(log n)`-bit identifiers. Its output has at most `n` identifiers
and length `O(n log n)`. Both subprocess modes are deterministic and reconstruct
all layer identifiers from the source, with no retained state or oracle calls.
Before JSON input parsing, both modes disable CPython's process-local decimal
integer digit cap, so legal encoded integers are not truncated or rejected.

## Evidence boundary

The executable checks are finite regression evidence, not a proof. The argument
above is the general correctness claim. The construction is the standard
set-cover incidence idea specialized to closed neighborhoods; its precise
literature attribution and novelty assessment remain subject to independent
review. Garey and Johnson's ND2 catalog records a Dominating Set transformation
without printing its construction, while Caro, West and Yuster give the
connected-domination/maximum-leaf identity used for context:

- <https://perso.limos.fr/~palafour/PAPERS/PDF/Garey-Johnson79.pdf>
- <https://math.haifa.ac.il/raphy/papers/conndom.pdf>

The exact rule and every-valid-output recovery proof stated here were derived in
this campaign; no novelty claim is made for the underlying incidence idea.
