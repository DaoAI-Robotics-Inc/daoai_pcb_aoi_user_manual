"""Merge a JSON {msgid: msgstr} mapping into one or more .po files.

The translator workflow is::

    1. Write translations to a JSON file like:
       { "foo.po": { "中文 msgid": "English msgstr", ... }, ... }
    2. Run ``python apply_translations.py <translations.json>``.

The script reads each .po, fills in the matching msgids, and writes the file
back. msgids without a translation entry stay empty. Header metadata is
preserved; the file's fuzzy header marker is cleared the first time we add
a real translation.

Run from repo root::

    python daoai_pcb_aoi_user_manual/scripts/apply_translations.py \\
        daoai_pcb_aoi_user_manual/scripts/translations/example.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import polib

REPO_ROOT = Path(__file__).resolve().parents[2]
LOCALE_ROOT = (
    REPO_ROOT
    / "daoai_pcb_aoi_user_manual"
    / "docs"
    / "source"
    / "locale"
    / "en"
    / "LC_MESSAGES"
)


def apply_to_po(po_path: Path, mapping: dict[str, str]) -> tuple[int, int, list[str]]:
    """Apply the mapping to one .po file.

    Returns ``(filled, total_empty, unmatched_msgids)``.
    """
    po = polib.pofile(str(po_path), encoding="utf-8")

    # Strip the fuzzy header marker once we're committing translations.
    if "fuzzy" in po.metadata_is_fuzzy:
        po.metadata_is_fuzzy = []

    filled = 0
    unmatched: list[str] = []
    for entry in po:
        if entry.obsolete:
            continue
        # Fill empty msgstrs AND overwrite fuzzy ones. Fuzzy entries carry a
        # stale translation from a prior catalog update; sphinx ignores them at
        # build time, so they render the original Chinese unless we replace.
        if entry.msgid in mapping and (
            not entry.msgstr or "fuzzy" in entry.flags
        ):
            entry.msgstr = mapping[entry.msgid]
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")
            filled += 1

    for cn_text in mapping:
        if not any(e.msgid == cn_text for e in po):
            unmatched.append(cn_text)

    total_empty = sum(1 for e in po if not e.msgstr and not e.obsolete)

    po.save(str(po_path))
    return filled, total_empty, unmatched


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: apply_translations.py <translations.json>", file=sys.stderr)
        sys.exit(1)

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    summary: list[str] = []
    for rel_path, mapping in payload.items():
        po_path = LOCALE_ROOT / rel_path
        if not po_path.exists():
            print(f"  SKIP (missing): {rel_path}")
            continue
        filled, remaining, unmatched = apply_to_po(po_path, mapping)
        summary.append(
            f"{rel_path}: filled {filled} of {filled + remaining} (remaining {remaining})"
        )
        if unmatched:
            summary.append(
                f"  WARN: {len(unmatched)} msgid(s) in JSON not found in .po — "
                "could be a typo, an obsolete entry, or whitespace mismatch:"
            )
            for cn in unmatched[:5]:
                summary.append(f"    {cn!r}")
            if len(unmatched) > 5:
                summary.append(f"    ... and {len(unmatched) - 5} more")

    print("\n".join(summary))


if __name__ == "__main__":
    main()
