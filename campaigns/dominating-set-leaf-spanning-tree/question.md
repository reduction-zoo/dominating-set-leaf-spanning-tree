# Dominating Set → Maximum Leaf Spanning Tree with a threshold

## Category

Construction open

## Source Definition

Given a finite simple connected graph and k, return at most k vertices whose closed neighborhoods cover the graph. The selected set need not be connected. Return NO-SOLUTION exactly when no such witness exists. Graphs, families and strings are explicit; numerical parameters use binary encodings.

## Target Definition

Given a connected simple graph and K, return a spanning tree with at least K degree-one vertices. A valid output is a witness satisfying these conditions, or NO-SOLUTION exactly when none exists.

## Required Result

Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.

## Acceptance

Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.

## Importance

The task makes an often-conflated connection between domination and leaf-rich network backbones precise.

## Difficulty

Difficulty is not yet established by a construction attempt. The complement-of-leaves identity concerns connected dominating sets. Ordinary dominating sets require an additional construction rather than the identity map.

## Openness

This is a rule-completion task from the imported catalog. The requested contribution is a complete, reproducible construction, proof and implementation; the existing hardness attribution is not presented as an unsolved complexity classification. The references are leads to check, not a verified solution.

## Literature Checked

2026-09-18

## Coverage

Import inventory review of the cited sources. Primary proofs have not been independently re-audited; availability of a complete reconstruction elsewhere remains unassessed.

## References

- [Problem-Reductions: Dominating Set → Maximum Leaf Spanning Tree with a threshold](https://github.com/CodingThrust/problem-reductions/issues/910): Upstream task and discussion checked on 2026-09-18. Reported reference: Garey & Johnson, *Computers and Intractability*, ND2, p.206
