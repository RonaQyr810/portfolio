# -*- coding: utf-8 -*-
"""Patch 日薪喵 bundle for portfolio local demo."""
import re
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "projects/rikxiniao/app"
FILES = list((APP / "assets").glob("*.js")) if (APP / "assets").is_dir() else []
if (APP / "bundle.js").is_file():
    FILES.append(APP / "bundle.js")

CLOUD_PATTERNS = [
    "http://192.168.10.157:8787",
    "https://192.168.10.157:8787",
]


ASSET_PATH_PATCHES = [
    ("/logo.png", "./logo.png"),
    ("/favicon.png", "./favicon.png"),
    ("/icon-192.png", "./icon-192.png"),
    ("/icon-512.png", "./icon-512.png"),
]


def patch_file(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    for url in CLOUD_PATTERNS:
        text = text.replace(url, "")
    text = re.sub(r"http://192\.168\.\d+\.\d+:8787", "", text)
    for old, new in ASSET_PATH_PATCHES:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("patched", path.name)
        return True
    return False


def main():
    for f in FILES:
        patch_file(f)

if __name__ == "__main__":
    main()
