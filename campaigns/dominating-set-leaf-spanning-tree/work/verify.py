#!/usr/bin/env python3
import argparse
import itertools
import json
import subprocess
import sys


NO_SOLUTION = {"status": "NO-SOLUTION"}


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


def connected_graphs(limit):
    for n in range(1, limit + 1):
        possible = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [possible[index] for index in range(len(possible)) if mask >> index & 1]
            if connected(n, edges):
                yield n, edges


def valid_graph(instance):
    if type(instance) is not dict or type(instance.get("n")) is not int or instance["n"] < 1:
        return False
    n = instance["n"]
    edges = instance.get("edges")
    if type(edges) is not list:
        return False
    tuples = []
    for edge in edges:
        if type(edge) is not list or len(edge) != 2 or any(type(v) is not int for v in edge):
            return False
        u, v = edge
        if not 0 <= u < v < n:
            return False
        tuples.append((u, v))
    return len(tuples) == len(set(tuples)) and connected(n, tuples)


def source_witnesses(source):
    n = source["n"]
    adjacency = [{vertex} for vertex in range(n)]
    for u, v in source["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    for size in range(min(source["k"], n) + 1):
        for choice in itertools.combinations(range(n), size):
            if all(any(vertex in adjacency[picked] for picked in choice) for vertex in range(n)):
                yield choice


def valid_source_output(source, output):
    witnesses = list(source_witnesses(source))
    if output == NO_SOLUTION:
        return not witnesses
    if type(output) is not dict or set(output) != {"dominating_set"}:
        return False
    vertices = output["dominating_set"]
    return type(vertices) is list and tuple(vertices) in witnesses


def tree_and_leaves(n, edges):
    if len(edges) != n - 1 or not connected(n, edges):
        return None
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    return sum(value == 1 for value in degree)


def solve_target_family(targets, sample_limit=3):
    first = targets[0]
    n = first["n"]
    edges = [tuple(edge) for edge in first["edges"]]
    thresholds = {target["K"] for target in targets}
    samples = {threshold: [] for threshold in thresholds}
    subset_count = 0
    tree_count = 0
    for choice in itertools.combinations(edges, n - 1):
        subset_count += 1
        leaves = tree_and_leaves(n, choice)
        if leaves is None:
            continue
        tree_count += 1
        for threshold in thresholds:
            if leaves >= threshold and len(samples[threshold]) < sample_limit:
                samples[threshold].append({"tree_edges": [list(edge) for edge in choice]})
    return {threshold: values or [NO_SOLUTION] for threshold, values in samples.items()}, subset_count, tree_count


def run_json(command, value):
    result = subprocess.run(command, input=json.dumps(value), text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)} failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{' '.join(command)} returned invalid JSON") from error


def verify(candidate):
    cases = []
    graph_count = 0
    for n, edges in connected_graphs(4):
        graph_count += 1
        sources = [
            {"n": n, "edges": [list(edge) for edge in edges], "k": k}
            for k in [*range(n + 1), 1 << 130]
        ]
        targets = [run_json([sys.executable, candidate], source) for source in sources]
        for target in targets:
            if not valid_graph(target) or type(target.get("K")) is not int or target["K"] < 0:
                raise AssertionError(f"illegal target: {target}")
        groups = {}
        for index, target in enumerate(targets):
            key = (target["n"], tuple(map(tuple, target["edges"])))
            groups.setdefault(key, []).append(index)
        solved = {}
        for indices in groups.values():
            family = [targets[index] for index in indices]
            outputs, subsets, trees = solve_target_family(family)
            for index in indices:
                solved[index] = outputs[targets[index]["K"]]
            cases.append((subsets, trees))
        for index, source in enumerate(sources):
            source_exists = bool(list(source_witnesses(source)))
            target_exists = solved[index] != [NO_SOLUTION]
            if source_exists != target_exists:
                raise AssertionError(f"existence mismatch: {source} -> {targets[index]}")
            for target_output in solved[index]:
                recovered = run_json(
                    [sys.executable, candidate, "--extract"],
                    {"source": source, "target_solution": target_output},
                )
                if not valid_source_output(source, recovered):
                    raise AssertionError(
                        f"invalid recovery: source={source}, target={targets[index]}, "
                        f"output={target_output}, recovered={recovered}"
                    )
                cases.append(target_output)
    instance_count = sum(n + 2 for n, _ in connected_graphs(4))
    output_count = sum(type(item) is dict for item in cases)
    subset_count = sum(item[0] for item in cases if type(item) is tuple)
    tree_count = sum(item[1] for item in cases if type(item) is tuple)
    print(
        f"verification passed: {graph_count} connected graphs, {instance_count} source instances, "
        f"{output_count} target outputs exercised, {subset_count} edge subsets and "
        f"{tree_count} spanning trees independently checked"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    verify(parser.parse_args().candidate)


if __name__ == "__main__":
    main()
