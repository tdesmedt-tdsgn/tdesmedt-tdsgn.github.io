#!/usr/bin/env python3
"""Generate the default Open Graph image (public/og.png), 1200x630."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public' / 'og.png'

BG = (23, 21, 18)        # warm near-black
FG = (234, 231, 224)     # off-white
MUTED = (162, 157, 146)
ACCENT = (224, 149, 107) # copper

SERIF_CANDIDATES = [
    '/System/Library/Fonts/Supplemental/Iowan Old Style.ttc',
    '/System/Library/Fonts/Supplemental/Palatino.ttc',
    '/System/Library/Fonts/Supplemental/Georgia.ttf',
    '/System/Library/Fonts/Supplemental/Times New Roman.ttf',
]
SANS_CANDIDATES = [
    '/System/Library/Fonts/SFNS.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
]


def load_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


def main() -> None:
    img = Image.new('RGB', (1200, 630), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 1200, 8], fill=ACCENT)  # top rule

    kicker = load_font(SANS_CANDIDATES, 30)
    name = load_font(SERIF_CANDIDATES, 96)
    tagline = load_font(SANS_CANDIDATES, 38)

    d.text((90, 150), 'AI · ENGINEERING LEADERSHIP · SHIPPING', font=kicker, fill=ACCENT)
    d.text((84, 220), 'Tom De Smedt', font=name, fill=FG)
    d.text(
        (90, 370),
        'Notes on AI, engineering leadership, and\nshipping — with working code.',
        font=tagline,
        fill=MUTED,
        spacing=14,
    )
    d.text((90, 540), 'tdesmedt-tdsgn.github.io', font=kicker, fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, 'PNG')
    print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
