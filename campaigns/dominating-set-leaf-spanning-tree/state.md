# Campaign state

Status: ready_for_expert_review. Date: 2026-09-22. Budget: 20 rounds authorized; 1 used, 19 remaining; 1 distinct mechanism attempted.

## Scope

[Fixed question](question.md). Deliver executable F/G, general correctness and complexity proofs, independent target-solving tests, registered independent review, and a compiled and visually inspected English Typst manuscript. Formal verification has not been requested. No construction claim exists at initialization.

## Capability probe — 2026-09-22

- Python: system Python 3.14.7 available; uv selected and locked CPython 3.14.2 for the project.
- uv: 0.12.7, available via local executable.
- Oracle solver: uv-selected CPython 3.14.2 standard-library exhaustive enumeration, available; no external dependency. Prepared self-test evidence is in [`work/preparation.md`](work/preparation.md).
- Lean: 4.34.0, available; the Lake version probe was interrupted by the command limit and Mathlib project availability remains pending. Formalization is not requested.
- Typst: 0.15.1, available at `/opt/homebrew/bin/typst`.
- External writing skill: available at `/Users/xiweipan/.agents/skills/how-to-technical-writing/SKILL.md` (also installed through the sci-brain plugin); read it at Write.
- Harness: Codex with native fresh-context subagents available; reviewer registration is `.codex/agents/research-reviewer.toml`. Main route reports GPT-5; no token-usage measurement is exposed, so none is recorded.

## Rounds

| Round | Mechanism or literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| 001 | Closed-neighborhood set/element incidence graph with forced-internal root | Prepared exhaustive candidate loop over every enumerated target output | Supported | [`rounds/001/round.md`](rounds/001/round.md) |

## Evidence and next action

Prepare is committed at `b8aaeaa`; candidate round 001 at `537f518`; verification at `c2c6f8a`; and the integer-boundary repair at `7c08045`. Review 001 (`728b2b8`) judged the graph construction and recovery sound but found CPython's default 4,300-digit JSON integer limit violated the contract. Focused review 002 (`b854146`) independently tested 4,301-, 5,000-, and 10,000-digit inputs in both modes and returned **advance**. The prepared loop passes 11 source instances and 97 target outputs. Independent Verify passes 44 connected graphs, 255 source instances and 598 recovered target outputs after checking 1,295,656 target edge subsets and 166,307 spanning trees. The English Typst [manuscript](work/paper/manuscript.typ) compiles to a five-page [PDF](work/paper/manuscript.pdf); every page was rendered and visually inspected after the final edit. Next: expert review; no publication or upstream action is authorized.

Experience closeout: 0 entries created, 0 updated, 0 pending. Round 001 yielded a complete campaign-specific reconstruction of a known incidence mechanism, not a distinct reusable finding requiring a shared entry.
