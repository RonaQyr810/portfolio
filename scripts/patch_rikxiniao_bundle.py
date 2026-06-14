# -*- coding: utf-8 -*-
"""Patch 日薪喵 bundle for portfolio local demo."""
import re
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "projects/rikxiniao/app"
FILES = [APP / "assets/index-BSkfxrfo.js", APP / "bundle.js"]

CLOUD_PATTERNS = [
    "http://192.168.10.157:8787",
    "https://192.168.10.157:8787",
]


def patch_file(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    for url in CLOUD_PATTERNS:
        text = text.replace(url, "")
    text = re.sub(r"http://192\.168\.\d+\.\d+:8787", "", text)
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
