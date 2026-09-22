#!/usr/bin/env python3
import argparse
import json
import sys


NO_SOLUTION = {"status": "NO-SOLUTION"}


def construct(source):
    n = source["n"]
    source_edges = {tuple(edge) for edge in source["edges"]}
    edges = [[0, 1]]
    edges.extend([0, 2 + vertex] for vertex in range(n))
    for dominator in range(n):
        for element in range(n):
            if dominator == element or tuple(sorted((dominator, element))) in source_edges:
                edges.append([2 + dominator, 2 + n + element])
    return {"n": 2 * n + 2, "edges": edges, "K": 2 * n + 1 - min(source["k"], n)}


def extract(source, target_solution):
    if target_solution == NO_SOLUTION:
        return NO_SOLUTION
    n = source["n"]
    degree = [0] * (2 * n + 2)
    for u, v in target_solution["tree_edges"]:
        degree[u] += 1
        degree[v] += 1
    dominating_set = {vertex for vertex in range(n) if degree[2 + vertex] >= 2}
    dominating_set.update(vertex for vertex in range(n) if degree[2 + n + vertex] >= 2)
    return {"dominating_set": sorted(dominating_set)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true")
    args = parser.parse_args()
    sys.set_int_max_str_digits(0)
    value = json.load(sys.stdin)
    output = extract(value["source"], value["target_solution"]) if args.extract else construct(value)
    json.dump(output, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
