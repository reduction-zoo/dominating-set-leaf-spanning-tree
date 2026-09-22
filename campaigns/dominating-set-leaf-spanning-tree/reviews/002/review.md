# Independent follow-up review 002

## Decision: advance

Repair commit `7c08045` fixes the sole blocking finding from review 001 in both
candidate modes.  It does not change the graph construction or decoder, and it
introduces no new correctness, complexity, novelty, or significance issue.  The
candidate is eligible for expert review.

Review date: 2026-09-22.  Reviewed frozen HEAD:
`7c080453ce98250483091256debedd7c20a41abb`.

## Repair assessment

The previous defect was at `work/algorithm.py:39`: default CPython JSON parsing
rejected otherwise legal source values whose decimal encoding exceeded 4,300
digits.  The repaired `main` now calls `sys.set_int_max_str_digits(0)` before
`json.load`.  On the uv-selected CPython 3.14.2 runtime, the default is 4,300
and the configured value is 0, which disables the process-local conversion
limit.  Because forward construction and extraction share this `main`, the
repair covers the top-level source and the source nested in extraction input.

The independent check `reviews/002/integer_followup_check.py` sends raw JSON,
so its inputs are not pre-parsed by a caller subject to the same limit.  It
passed at the first value beyond the default boundary and at two larger sizes:

```text
passed: 4301-, 5000-, and 10000-digit k accepted in both modes
```

For forward mode, each value produced the exact legal one-vertex target with
`K=2`.  For extraction mode, each value used the valid unique spanning tree and
recovered `{"dominating_set":[0]}`.  This directly checks successful parsing,
the `min(k,n)` comparison, and recovery after parsing.  The committed
`work/verify.py:116-143` independently exercises a raw 5,000-digit value in
both modes, and `work/evidence/verify/integer-repair.txt` records the full
prepared and exhaustive suites passing after the repair.

The proof statement added at `work/proof.md:82-83` now matches the executable.
`work/verification.md` also correctly replaces the earlier overstatement
"arbitrarily large" with "representative large"; finite samples are regression
evidence, while totality follows from disabling the parser limit and exact
integer semantics.

## Consequences for the reduction

The repair occurs only at the common input boundary.  F still constructs the
same graph and threshold, and G still performs the same degree-based recovery.
Therefore the legality, completeness, every-valid-tree soundness, boundary-case,
and `NO-SOLUTION` arguments accepted in
`reviews/001/review.md` are unaffected and are reused here.

Parsing an `L`-digit integer and comparing it with `n` remains polynomial in
the input encoding length.  The large `k` is not copied to the target, so the
previous output-size bound is unchanged.  Removing a fixed implementation cap
does not introduce randomness, retained state, an oracle, or a non-polynomial
operation.  The setting is process-local and made before either mode reads
input.

The novelty and significance judgments from review 001 are also unaffected.
The underlying incidence construction remains known from Li and Toulouse's
Set Cover reduction, while the contribution here remains the explicit
every-valid-output search reduction and executable reconstruction required by
the fixed question.  The repair adds no theorem or practical-performance claim.
The prior literature URLs, theorem locations, search date, and stated coverage
gaps are reused without a redundant search.

## Isolation and route

This follow-up continued in the registered `research-reviewer` context that was
created with `fork_turns="none"`; the original fresh child-context boundary
therefore remained in force.  The model route was: **registered
research-reviewer, no explicit model override; backend identifier not exposed**.
Filesystem access was unrestricted and agent tools were available, so write
confinement and no-delegation were instruction-only rather than enforced by a
sandbox or tool denial.  No further agent was spawned and no agent tool was used
for delegation.  No structural depth cap was exposed.  All follow-up review
writes are confined to
`campaigns/dominating-set-leaf-spanning-tree/reviews/002`.
