#!/usr/bin/env python3
"""make.fun entry: "Sum up 24 November's world news in one image".

The entry image ships in this repository as base64 text
(assets/entry.png.b64) so it can travel through text-only channels.
Running this program decodes it and writes the original PNG bytes to
$ENTRY_OUTPUT_DIR/entry.png (default: /output/entry.png).

Standard library only, no network access, fully deterministic: every
run writes exactly the same bytes.
"""

import base64
import os
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "assets" / "entry.png.b64"


def main() -> None:
    out_dir = Path(os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    png_bytes = base64.b64decode(ASSET.read_bytes())
    (out_dir / "entry.png").write_bytes(png_bytes)


if __name__ == "__main__":
    main()
