"""Walk all .rst files and produce a map of {basename: [resolved paths]}.

Useful for the capture script: given a target screenshot like ``home.png``,
look up where it actually lives under ``docs/source/`` so we save the
``.en.png`` next to it.
"""
import json
import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2] / "docs" / "source"

mapping: dict[str, set[str]] = {}
for rst in SOURCE.rglob("*.rst"):
    for m in re.finditer(
        r"^\.\.\s+(?:image|figure)::\s*(\S+)", rst.read_text(encoding="utf-8"), re.M
    ):
        ref = m.group(1)
        resolved = (rst.parent / ref).resolve()
        rel = resolved.relative_to(SOURCE).as_posix()
        mapping.setdefault(resolved.name, set()).add(rel)

print(json.dumps({k: sorted(v) for k, v in sorted(mapping.items())}, indent=2, ensure_ascii=False))
