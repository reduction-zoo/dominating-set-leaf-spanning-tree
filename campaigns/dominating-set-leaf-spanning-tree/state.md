# Campaign state

Status: awaiting independent review. Date: 2026-09-22. Budget: 20 rounds authorized; 1 used, 19 remaining; 1 mechanism attempted.

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

Prepare is committed at `b8aaeaa`; candidate round 001 is committed at `537f518`. The prepared loop passed 11 source instances and 97 independently enumerated target outputs. Independent Verify passed all 44 connected labeled graphs through four vertices, 255 source instances and 598 recovered target outputs after checking 1,295,656 target edge subsets and 166,307 spanning trees. Next: commit verification and request a fresh-context registered review.

Experience extraction: none at initialization; no research finding exists yet.
