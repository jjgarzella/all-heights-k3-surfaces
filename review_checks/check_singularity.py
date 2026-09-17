"""Direct integer and mod-7 evaluations at the singular point in the F7 h=9 row."""
from math import prod
import json
from pathlib import Path

p = 7
# Preserve the original review finding after the manuscript table is corrected.
snapshot = json.loads(Path(__file__).with_name('original_f7_rows.json').read_text())
f = {tuple(e): c for e, c in snapshot['9']}
point = (0, 1, 5, 2)
derivatives = [
    {
        tuple(e[k] - (j == k) for k in range(4)): c * e[j]
        for e, c in f.items() if e[j]
    }
    for j in range(4)
]
values = [
    sum(c * prod(x ** a for x, a in zip(point, e)) for e, c in g.items())
    for g in [f] + derivatives
]
assert values == [2261, 630, 1134, 1078, 1260]
assert all(value % p == 0 for value in values)
print({"point": point, "integer_values": values, "mod_7": [v % p for v in values]})
