#!/usr/bin/env python3
import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path


NO_SOLUTION = {"status": "NO-SOLUTION"}


def graph(instance):
    if type(instance) is not dict or type(instance.get("n")) is not int:
        raise ValueError("instance must contain integer n")
    n = instance["n"]
    edges = instance.get("edges")
    if n < 1 or type(edges) is not list:
        raise ValueError("n must be positive and edges must be a list")
    normalized = []
    for edge in edges:
        if (
            type(edge) is not list
            or len(edge) != 2
            or any(type(v) is not int for v in edge)
            or not (0 <= edge[0] < edge[1] < n)
        ):
            raise ValueError("edges must be unique ordered vertex pairs")
        normalized.append(tuple(edge))
    if len(set(normalized)) != len(normalized):
        raise ValueError("edges must be unique")
    if not connected(n, normalized):
        raise ValueError("graph must be connected")
    return n, normalized


def connected(n, edges):
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        for vertex in adjacency[stack.pop()]:
            if vertex not in seen:
                seen.add(vertex)
                stack.append(vertex)
    return len(seen) == n


def source_witnesses(instance):
    n, edges = graph(instance)
    k = instance.get("k")
    if type(k) is not int or k < 0:
        raise ValueError("k must be a nonnegative integer")
    adjacency = [{v} for v in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    witnesses = []
    for size in range(min(k, n) + 1):
        for choice in itertools.combinations(range(n), size):
            if set().union(*(adjacency[v] for v in choice)) == set(range(n)):
                witnesses.append(choice)
    return witnesses


def valid_source_output(instance, output):
    witnesses = source_witnesses(instance)
    if output == NO_SOLUTION:
        return not witnesses
    if type(output) is not dict or set(output) != {"dominating_set"}:
        return False
    vertices = output["dominating_set"]
    return type(vertices) is list and tuple(vertices) in witnesses


def is_tree(n, edges):
    return len(edges) == n - 1 and connected(n, edges)


def leaf_count(n, edges):
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    return sum(value == 1 for value in degree)


def target_solutions(instance):
    n, edges = graph(instance)
    threshold = instance.get("K")
    if type(threshold) is not int or threshold < 0:
        raise ValueError("K must be a nonnegative integer")
    trees = [
        choice
        for choice in itertools.combinations(edges, n - 1)
        if is_tree(n, choice) and leaf_count(n, choice) >= threshold
    ]
    return [{"tree_edges": [list(edge) for edge in tree]} for tree in trees] or [NO_SOLUTION]


def valid_target_output(instance, output):
    solutions = target_solutions(instance)
    if output == NO_SOLUTION:
        return solutions == [NO_SOLUTION]
    if type(output) is not dict or set(output) != {"tree_edges"}:
        return False
    edges = output["tree_edges"]
    return type(edges) is list and output in solutions


def run_json(command, value):
    result = subprocess.run(
        command,
        input=json.dumps(value),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)} failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{' '.join(command)} returned invalid JSON") from error


def load_cases():
    return json.loads(Path(__file__).with_name("cases.json").read_text())


def self_test():
    cases = load_cases()
    for case in cases:
        witnesses = source_witnesses(case["source"])
        assert bool(witnesses) == case["has_solution"], case["name"]
        for witness in case.get("witnesses", []):
            assert valid_source_output(case["source"], {"dominating_set": witness}), case["name"]
        assert valid_source_output(case["source"], NO_SOLUTION) != case["has_solution"], case["name"]
    assert not valid_source_output(cases[4]["source"], {"dominating_set": []})
    assert not valid_source_output(cases[4]["source"], {"dominating_set": [1, 1]})

    target = {"n": 4, "edges": [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]], "K": 3}
    solutions = target_solutions(target)
    assert len(solutions) == 4
    assert all(valid_target_output(target, solution) for solution in solutions)
    assert not valid_target_output(target, {"tree_edges": [[0, 1], [1, 2], [2, 3]]})
    assert not valid_target_output(target, NO_SOLUTION)
    impossible = target | {"K": 5}
    assert target_solutions(impossible) == [NO_SOLUTION]
    assert valid_target_output(impossible, NO_SOLUTION)
    assert not valid_target_output(impossible, solutions[0])

    malformed = [
        {"n": 0, "edges": [], "k": 0},
        {"n": 2, "edges": [[0, 1], [0, 1]], "k": 1},
        {"n": 2, "edges": [], "k": 1},
        {"n": 2, "edges": [[0, 1]], "k": -1},
    ]
    for instance in malformed:
        try:
            source_witnesses(instance)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted malformed instance: {instance}")
    print(f"self-test passed: {len(cases)} source cases, 4 target trees, malformed and wrong outputs rejected")


def check_candidate(path):
    cases = load_cases()
    target_outputs = 0
    for case in cases:
        source = case["source"]
        target = run_json([sys.executable, path], source)
        graph(target)
        outputs = target_solutions(target)
        for target_output in outputs:
            assert valid_target_output(target, target_output)
            recovered = run_json(
                [sys.executable, path, "--extract"],
                {"source": source, "target_solution": target_output},
            )
            if not valid_source_output(source, recovered):
                raise AssertionError(f"{case['name']}: invalid recovery {recovered} from {target_output}")
            target_outputs += 1
    print(f"candidate passed: {len(cases)} source instances, {target_outputs} independently enumerated target outputs")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        check_candidate(args.candidate)


if __name__ == "__main__":
    main()
