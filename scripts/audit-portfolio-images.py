# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
refs = set()
for p in ROOT.rglob("*"):
    if p.suffix not in {".html", ".js"} or "node_modules" in p.parts:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    refs.update(re.findall(r'(?:src|href)=["\'](?:\.\./)*assets/portfolio/([^"\']+)["\']', text))
    refs.update(re.findall(r"src:\s*['\"]assets/portfolio/([^'\"]+)['\"]", text))

missing, tiny, svg_broken = [], [], []
for r in sorted(refs):
    rel = r.split("?")[0]
    path = ROOT / "assets" / "portfolio" / rel.replace("assets/portfolio/", "")
    if not path.exists():
        missing.append(rel)
        continue
    size = path.stat().st_size
    if size < 500:
        tiny.append((rel, size))
    if path.suffix == ".svg":
        raw = path.read_bytes()
        if b"?" in raw or b"\xef\xbf\xbd" in raw or sum(1 for b in raw if b > 127) > 20:
            try:
                raw.decode("ascii")
            except UnicodeDecodeError:
                svg_broken.append(rel)

print("MISSING:", len(missing))
for x in missing:
    print(" ", x)
print("TINY:", len(tiny))
for x, s in tiny:
    print(" ", s, x)
print("SVG_CHECK:", len(svg_broken))
for x in svg_broken:
    print(" ", x)
