# Dominating Set → Maximum Leaf Spanning Tree with a threshold

**Status:** `ready_for_expert_review` · **Research model:** `gpt-6-astra` · **Submitted:** 2026-09-22

The public campaign supplies deterministic polynomial-time construction and recovery for the fixed Dominating Set to Maximum Leaf Spanning Tree with a threshold contract. Every valid target output recovers a valid source output, including NO-SOLUTION where applicable.

## Construction

A closed-neighborhood incidence graph with a universal root and one pendant vertex converts non-leaves into a dominating set. The leaf threshold is 2n+1-min(k,n). The public archive contains the complete every-output decoder and states its provenance and scope limits.

## Evidence

- **Mathematical correctness and recovery: Written proof; independent agent review advanced.** The general proof covers the fixed endpoint semantics and every valid target output. The registered reviewer found no remaining blocking correctness gap. Human expert acceptance remains pending. ([evidence](campaigns/dominating-set-leaf-spanning-tree/reviews/002/review.md))
- **Construction and recovery complexity: Written polynomial bounds.** Polynomial runtime and encoding-size bounds for both maps are stated and proved in the research archive. They are not formally certified or claimed optimal. ([evidence](campaigns/dominating-set-leaf-spanning-tree/work/proof.md))
- **Executable verification: Finite checks passed.** Verification covered 255 source instances, 598 recoveries, 1,295,656 edge subsets and 166,307 spanning trees. Independent follow-up advanced after repairing arbitrary-size integer parsing. The archive contains executable construction/recovery, a general proof with polynomial bounds, independent review, and an inspected manuscript. Human maintainer review remains pending. These finite checks supplement rather than replace the general proof. ([evidence](campaigns/dominating-set-leaf-spanning-tree/work/verification.md))
- **Formal certification and maintainer acceptance: Pending / not performed.** The repository records source-specific attribution and limitations. No Lean certification, human expert acceptance or upstream integration is recorded. ([evidence](campaigns/dominating-set-leaf-spanning-tree/state.md))

## Reproduce

Run from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/dominating-set-leaf-spanning-tree/work/check.py --candidate campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py
uv run --locked python campaigns/dominating-set-leaf-spanning-tree/work/verify.py --candidate campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py
```

The finite checks exercise the executable construction and recovery maps. The general claim rests on the written proof.

## Artifacts

- [Fixed question](campaigns/dominating-set-leaf-spanning-tree/question.md)
- [Campaign state](campaigns/dominating-set-leaf-spanning-tree/state.md)
- [Manuscript](campaigns/dominating-set-leaf-spanning-tree/work/paper/manuscript.pdf)
- [Construction and recovery](campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py)
- [General proof](campaigns/dominating-set-leaf-spanning-tree/work/proof.md)
- [Independent review](campaigns/dominating-set-leaf-spanning-tree/reviews/002/review.md)
- [Verification evidence](campaigns/dominating-set-leaf-spanning-tree/work/verification.md)

## Scope

The registered independent agent review advanced this result to expert review. The board records it as a submitted solution; no Lean checking, human expert acceptance, or upstream integration is claimed.
