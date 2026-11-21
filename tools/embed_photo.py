#!/usr/bin/env python3
"""Put your own photo in the hero arch.

    python tools/embed_photo.py path/to/photo.jpg

Needs Pillow (pip install pillow). The photo is cropped to the arch, shrunk
and embedded in assets/abhay-hero.svg, so no extra files are needed.
Portrait photos with the face in the upper half work best.
"""
import base64, io, pathlib, re, sys
from PIL import Image, ImageOps

if len(sys.argv) != 2:
    sys.exit(__doc__)
img = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert("RGB")
img = ImageOps.fit(img, (472, 592), centering=(0.5, 0.2))  # 2x the 236x296 arch
buf = io.BytesIO()
img.save(buf, "JPEG", quality=84, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()
tag = ('<image href="data:image/jpeg;base64,' + b64 + '" x="847" y="84" width="236" height="296" '
       'preserveAspectRatio="xMidYMin slice"/>')
svg = pathlib.Path(__file__).resolve().parent.parent / "assets" / "abhay-hero.svg"
s = svg.read_text(encoding="utf8")
s, n = re.subn(r"<!--PHOTO-->.*?<!--/PHOTO-->", lambda m: "<!--PHOTO-->" + tag + "<!--/PHOTO-->", s, flags=re.S)
if not n:
    sys.exit("Photo markers not found in abhay-hero.svg")
svg.write_text(s, encoding="utf8")
print("Done. Hero updated with your photo.")
