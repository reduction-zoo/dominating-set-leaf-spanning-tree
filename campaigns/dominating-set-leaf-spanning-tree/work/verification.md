# Verification

Candidate: round 001 commit `537f518`, `work/algorithm.py` and `work/proof.md`.

`verify.py` is independent of both the prepared checker and the candidate. It
generates every connected labeled simple graph on one through four vertices and
tests each with `k=0,...,n` and `k=2^130`. It solves Dominating Set by exhaustive
vertex-subset enumeration. For each actual target graph emitted by the candidate,
it exhausts all edge subsets of tree size, checks connectivity and leaf count,
and thereby concludes witness existence or `NO-SOLUTION`. It sends up to three
distinct qualifying trees per positive target, and the exact `NO-SOLUTION`
answer per negative target, through the candidate's separate extraction process.
Recovered outputs are checked directly against independently enumerated source
witnesses.

It separately sends a raw legal 5,000-digit `k` through both forward and
extraction subprocesses, exceeding CPython's default 4,300-digit parser limit.

The 2026-09-22 run passed on 44 graphs and 255 source instances. It exercised 598
valid target outputs after checking 1,295,656 candidate edge subsets and 166,307
spanning trees independently.

Run from the repository root:

```sh
uv run python campaigns/dominating-set-leaf-spanning-tree/work/verify.py \
  --candidate campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py
```

The retained result is in [`evidence/verify/exhaustive-n4.txt`](evidence/verify/exhaustive-n4.txt).
This finite check covers all source graph shapes through four vertices, boundary
and representative large encoded thresholds, alternate valid target witnesses and
conclusive negative targets. It does not establish correctness beyond that finite
domain; the every-valid-output theorem is in `proof.md`. Runtime and size-growth
bounds are proved rather than benchmarked, and no practical performance claim is
made.
