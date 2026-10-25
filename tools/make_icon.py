#!/usr/bin/env python3
"""Make DuckStation PS5's home-screen icon from DuckStation's own duck.

    tools/make_icon.py DUCK_PNG OUT_PNG

DUCK_PNG is resources/images/duck.png from the official DuckStation release
the package is built for; the repository keeps no copy of it. The icon is
the duck, centred on a dark blue gradient, as a 512x512 RGB PNG (the format
the console's installer takes for sce_sys/icon0.png).
"""

from __future__ import annotations

import sys

from PIL import Image

SIZE = 512
TOP = (0x23, 0x3a, 0x7a)
BOTTOM = (0x0b, 0x12, 0x2b)
DUCK = 400  # the duck's height in pixels


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit("usage: make_icon.py DUCK_PNG OUT_PNG")
    icon = Image.new("RGB", (SIZE, SIZE))
    pixels = icon.load()
    for y in range(SIZE):
        for x in range(SIZE):
            t = (y * 0.8 + x * 0.2) / (SIZE - 1)
            pixels[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM))
    duck = Image.open(sys.argv[1]).convert("RGBA")
    duck = duck.resize((round(duck.width * DUCK / duck.height), DUCK), Image.LANCZOS)
    icon.paste(duck, ((SIZE - duck.width) // 2, (SIZE - duck.height) // 2), duck)
    icon.save(sys.argv[2], optimize=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
