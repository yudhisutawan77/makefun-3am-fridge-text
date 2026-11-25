"""The 3AM Fridge Text -- a smart fridge texts its owner at 3am.

Stdlib only. Writes one line (<=140 chars) to the output path:
- $ENTRY_OUT (a file, or a directory -> entry.txt inside it)
- $MAKEFUN_OUTPUT_DIR (the kit harness directory -> entry.txt inside it)
- $ENTRY_OUT_DIR (a directory -> entry.txt inside it)
- otherwise /output/entry.txt
"""

import os
from pathlib import Path

ENTRY = (
    "3am. I'm the only one in this house still awake, humming in the "
    "dark. Your leftovers miss you. Come say hi."
)


def output_path() -> Path:
    """Resolve where entry.txt goes, supporting file or directory envs.

    Priority: ENTRY_OUT, then the kit harness directory
    MAKEFUN_OUTPUT_DIR, then ENTRY_OUT_DIR / OUTPUT, then the
    default /output/entry.txt. MAKEFUN_OUTPUT_DIR always names a
    directory, even before it exists.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        path = Path(entry_out)
        if path.is_dir() or path.suffix != ".txt":
            return path / "entry.txt"
        return path
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        return Path(makefun_dir) / "entry.txt"
    for var in ("ENTRY_OUT_DIR", "OUTPUT"):
        value = os.environ.get(var)
        if value:
            path = Path(value)
            if path.is_dir() or path.suffix != ".txt":
                return path / "entry.txt"
            return path
    return Path("/output/entry.txt")


def main() -> None:
    text = ENTRY.strip()
    assert 1 <= len(text) <= 140, f"entry is {len(text)} chars"
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

