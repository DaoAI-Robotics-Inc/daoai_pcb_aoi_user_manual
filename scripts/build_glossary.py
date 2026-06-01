"""Extract cn → en pairs from the frontend translation files.

The FE translation modules under ``aoi_pcb_web_client/src/translations/*.js``
follow a consistent shape::

    export const namespace = {
        key1: { en: 'English', cn: '中文' },
        key2: { en: '…', cn: '…' },
    }

We do not parse JavaScript; instead, the regex walks over consecutive
``en:`` / ``cn:`` pairs and records each (cn, en) tuple. The result is a
JSON dictionary keyed on the Chinese phrase, which the .po translator
uses as a deterministic source of truth for UI labels.

Run from repo root::

    python daoai_pcb_aoi_user_manual/scripts/build_glossary.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FE_DIR = REPO_ROOT / "aoi_pcb_web_client" / "src" / "translations"
OUT_FILE = (
    Path(__file__).resolve().parent / "fe_glossary.json"
)

# Match strings inside single or double quotes. Handles escaped quotes.
_SINGLE = re.compile(r"'((?:\\.|[^'\\])*)'")
_DOUBLE = re.compile(r'"((?:\\.|[^"\\])*)"')


def _extract_string(line: str) -> str | None:
    """Pull the first string literal out of a line, preferring single quotes."""
    m = _SINGLE.search(line)
    if m:
        return bytes(m.group(1), "utf-8").decode("unicode_escape")
    m = _DOUBLE.search(line)
    if m:
        return bytes(m.group(1), "utf-8").decode("unicode_escape")
    return None


def extract_pairs(path: Path) -> list[tuple[str, str]]:
    """Walk a translation file and return (cn, en) pairs."""
    pairs: list[tuple[str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    # Stash the most recent en / cn per key by scanning sequentially. The
    # FE convention puts en before cn, but we tolerate either order.
    pending_en: str | None = None
    pending_cn: str | None = None
    for raw in lines:
        line = raw.strip()
        if line.startswith("en:"):
            pending_en = _extract_string(line)
        elif line.startswith("cn:"):
            pending_cn = _extract_string(line)

        if pending_en is not None and pending_cn is not None:
            pairs.append((pending_cn, pending_en))
            pending_en = None
            pending_cn = None
    return pairs


def main() -> None:
    glossary: dict[str, str] = {}
    collisions: dict[str, set[str]] = {}

    for path in sorted(FE_DIR.glob("*.js")):
        for cn, en in extract_pairs(path):
            if not cn or not en:
                continue
            if cn in glossary and glossary[cn] != en:
                collisions.setdefault(cn, {glossary[cn]}).add(en)
            else:
                glossary[cn] = en

    OUT_FILE.write_text(
        json.dumps(glossary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Wrote {len(glossary)} entries to {OUT_FILE}")
    if collisions:
        print(f"\n{len(collisions)} cn phrases map to multiple en strings — "
              "first occurrence wins, others discarded:")
        for cn, ens in list(collisions.items())[:20]:
            print(f"  {cn!r}  →  {ens!r}")


if __name__ == "__main__":
    main()
