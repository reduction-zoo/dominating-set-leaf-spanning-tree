# Executable contract

## Instances and outputs

A source instance is a JSON object `{"n": n, "edges": [[u,v],...], "k": k}`.
Vertices are the integers `0,...,n-1`; `n >= 1`; every edge is listed once with
`u < v`; the graph is simple and connected; and `k` is a nonnegative integer.
The integer has no machine-word bound. A source output is exactly
`{"dominating_set": [v,...]}` with distinct vertices whose closed neighborhoods
cover every vertex and whose length is at most `k`, or
`{"status": "NO-SOLUTION"}` exactly when no such set exists.

A target instance has the same graph fields and a nonnegative integer `K`. A
target output is exactly `{"tree_edges": [[u,v],...]}`, listing a spanning tree
whose number of degree-one vertices is at least `K`, or the same `NO-SOLUTION`
object exactly when no such tree exists. In the one-vertex tree the sole vertex
has degree zero, hence there are zero leaves under the fixed degree-one definition.

JSON integers are exact. Their decimal text length and binary encoding length
are within constant factors, so polynomial bounds in either representation agree.
The empty graph is outside both legal instance domains; empty edge sets and empty
tree outputs occur for the legal one-vertex boundary case.

## Candidate commands

`python3 algorithm.py` reads one source instance from standard input and writes
one target instance to standard output. `python3 algorithm.py --extract` reads
`{"source": ..., "target_solution": ...}` and writes one source output. Each
process is stateless; diagnostics use standard error and failures return nonzero.

The independent checker validates both instance domains and both output
relations directly. `python3 check.py --candidate PATH` runs the two candidate
commands, exhaustively solves each constructed target in the finite test suite,
and exercises recovery on every enumerated valid target output.
