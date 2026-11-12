#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
ASSETS = SITE / 'assets'

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
COPY_EXTENSIONS = {'.html', '.css', '.js', '.svg', '.json', '.txt', '.xml'}


def copy_static_assets():
    SITE.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)

    for path in ROOT.iterdir():
        if path.is_dir():
            continue
        if path.suffix.lower() in COPY_EXTENSIONS:
            shutil.copy2(path, SITE / path.name)

    for path in ROOT.iterdir():
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            if path.name.lower().endswith('.gif'):
                # GIFs are not ideal for static Pages; keep original if already present.
                shutil.copy2(path, ASSETS / path.name)
                continue

            dest = ASSETS / path.name
            try:
                with Image.open(path) as img:
                    img = ImageOps.exif_transpose(img)
                    img = img.convert('RGB') if img.mode not in ('RGB', 'L', 'RGBA') else img
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    max_dim = 1600
                    if max(img.size) > max_dim:
                        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                    if path.suffix.lower() in {'.png', '.webp'}:
                        img.save(dest, optimize=True, quality=78)
                    else:
                        img.save(dest, format='JPEG', quality=72, optimize=True)
            except Exception:
                # Fall back to a plain copy if Pillow cannot process the file.
                shutil.copy2(path, dest)

    # Copy the main HTML file if it exists at the root.
    index_file = ROOT / 'index.html'
    if index_file.exists():
        shutil.copy2(index_file, SITE / 'index.html')

    # Ensure CSS is also in the output folder if present.
    for css_file in ROOT.glob('*.css'):
        shutil.copy2(css_file, SITE / css_file.name)


if __name__ == '__main__':
    copy_static_assets()
    print(f'Built optimized Pages site in {SITE}')
