# Preparation

## Independent oracles

`check.py` derives both oracles directly from the fixed definitions. For a
source graph it enumerates every vertex subset of size at most `min(k,n)` and
tests whether the union of its closed neighborhoods is the full vertex set.
Thus an enumerated subset is accepted exactly when it is a valid dominating-set
witness; `NO-SOLUTION` is accepted only when exhaustive enumeration is empty.

For a target graph it enumerates every `(n-1)`-edge subset, checks connectedness,
and counts degree-one vertices. A connected graph on `n` vertices with `n-1`
edges is a tree, so the returned objects are exactly all threshold-satisfying
spanning trees. `NO-SOLUTION` is returned only when that exhaustive list is empty.
The implementation uses uv-selected CPython 3.14.2 standard-library exact integers and no
candidate code or external solver. Exponential time is intentional and confines
this oracle to the explicit small domain; it is not part of F or G.

## Coverage and checks

`cases.json` contains 11 connected source instances on one through five vertices:
four negative and seven positive threshold cases, multiple distinct witnesses,
paths, a cycle, a star, the one-vertex/empty-edge boundary, `k=0`, and
`k=2^130`. The self-test also enumerates four leaf-rich spanning trees of `K4`,
rejects a subthreshold path and false `NO-SOLUTION`, accepts a conclusively
infeasible threshold, and rejects malformed, disconnected and negative-parameter
inputs.

Run from the repository root:

```sh
uv sync --locked
uv run python campaigns/dominating-set-leaf-spanning-tree/work/check.py --self-test
uv run python campaigns/dominating-set-leaf-spanning-tree/work/check.py --candidate campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py
```

The candidate command is intentionally pending until after this foundation is
committed. Candidate checks will report actual target-output counts. Finite tests
do not establish the required general theorem; they are regression and
counterexample evidence only. No random choices, numerical tolerances, solver
timeouts or inconclusive statuses occur.

The 2026-09-22 run passed as recorded in
[`evidence/prepare/self-test.txt`](evidence/prepare/self-test.txt).
