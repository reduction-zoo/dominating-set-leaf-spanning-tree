#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


candidate = Path(__file__).resolve().parents[4] / "campaigns/dominating-set-leaf-spanning-tree/work/algorithm.py"
source = '{"n":1,"edges":[],"k":' + "9" * 5000 + "}"
payloads = [
    ([], source),
    (["--extract"], '{"source":' + source + ',"target_solution":{"status":"NO-SOLUTION"}}'),
]
for args, payload in payloads:
    result = subprocess.run(
        [sys.executable, str(candidate), *args],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "Exceeds the limit (4300 digits)" in result.stderr
print("reproduced: forward and extraction modes reject a legal 5000-digit k")
