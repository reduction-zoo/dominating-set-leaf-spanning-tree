#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


candidate = Path(__file__).resolve().parents[4] / "campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py"


def invoke(args, payload):
    result = subprocess.run(
        [sys.executable, str(candidate), *args],
        input=payload,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


for digits in (4301, 5000, 10000):
    source = '{"n":1,"edges":[],"k":' + "9" * digits + "}"
    assert invoke([], source) == {
        "n": 4,
        "edges": [[0, 1], [0, 2], [2, 3]],
        "K": 2,
    }
    extraction = (
        '{"source":'
        + source
        + ',"target_solution":{"tree_edges":[[0,1],[0,2],[2,3]]}}'
    )
    assert invoke(["--extract"], extraction) == {"dominating_set": [0]}

print("passed: 4301-, 5000-, and 10000-digit k accepted in both modes")
