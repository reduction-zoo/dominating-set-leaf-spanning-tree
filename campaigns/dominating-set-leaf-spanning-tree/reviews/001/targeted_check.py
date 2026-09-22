#!/usr/bin/env python3
import itertools
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / "campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py"


def run(args, value):
    result = subprocess.run(
        [sys.executable, str(CANDIDATE), *args],
        input=json.dumps(value),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def connected(n, edges):
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        for v in adjacency[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def dominates(source, vertices):
    covered = set(vertices)
    for u, v in source["edges"]:
        if u in vertices:
            covered.add(v)
        if v in vertices:
            covered.add(u)
    return covered == set(range(source["n"])) and len(vertices) <= source["k"]


def qualifying_trees(target):
    n = target["n"]
    for edges in itertools.combinations(target["edges"], n - 1):
        if not connected(n, edges):
            continue
        degree = [0] * n
        for u, v in edges:
            degree[u] += 1
            degree[v] += 1
        if sum(d == 1 for d in degree) >= target["K"]:
            yield edges, degree


def main():
    cycle = {"n": 4, "edges": [[0, 1], [1, 2], [2, 3], [0, 3]], "k": 2}
    target = run([], cycle)
    count = 0
    for edges, degree in qualifying_trees(target):
        count += 1
        output = {"tree_edges": [list(edge) for edge in edges]}
        recovered = run(["--extract"], {"source": cycle, "target_solution": output})
        assert dominates(cycle, set(recovered["dominating_set"]))

    assert count > 0

    clique = {
        "n": 4,
        "edges": [list(edge) for edge in itertools.combinations(range(4), 2)],
        "k": 2,
    }
    clique_target = run([], clique)
    element_tree = [[0, 1], [0, 2], [2, 6], [2, 7], [2, 8], [2, 9], [3, 6], [4, 6], [5, 6]]
    degree = [0] * clique_target["n"]
    for u, v in element_tree:
        degree[u] += 1
        degree[v] += 1
    assert connected(clique_target["n"], element_tree)
    assert sum(d == 1 for d in degree) >= clique_target["K"]
    assert degree[6] >= 2
    recovered = run(
        ["--extract"],
        {"source": clique, "target_solution": {"tree_edges": element_tree}},
    )
    assert dominates(clique, set(recovered["dominating_set"]))

    cycle["k"] = 0
    assert not any(qualifying_trees(run([], cycle)))
    assert run(["--extract"], {"source": cycle, "target_solution": {"status": "NO-SOLUTION"}}) == {
        "status": "NO-SOLUTION"
    }
    print(f"passed: {count} qualifying cycle trees; explicit element-layer decoding; k=0 infeasible")


if __name__ == "__main__":
    main()
