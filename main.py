#!/usr/bin/env python3
"""make.fun entry: "Sum up 24 November's world news in one image".

The finished picture lives next to this program at assets/entry.png.
A run simply places a copy of it where the harness looks for the
entry: $ENTRY_OUTPUT_DIR/entry.png (default: /output/entry.png).

Standard library only, no network access, fully deterministic:
the output bytes are the asset bytes, unchanged, every run.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "assets" / "entry.png"


def place_entry() -> Path:
    target_dir = Path(os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(PICTURE, target)
    return target


if __name__ == "__main__":
    place_entry()
