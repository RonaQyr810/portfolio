# -*- coding: utf-8 -*-
"""???????????????? projects/ ???"""
from __future__ import annotations

import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DESKTOP = BASE.parent
VOICE_DIR = "\u8bed\u97f3\u7ed8\u56fe\u5de5\u5177"  # ??????

VOICE_DST = BASE / "projects" / "voice-draw" / "app"
VOICE_FILES = ("index.html", "styles.css")
VOICE_JS = "js"


def desktop_dir(name: str) -> Path:
    direct = DESKTOP / name
    if direct.is_dir():
        return direct
    for path in DESKTOP.iterdir():
        if path.is_dir() and name in path.name:
            return path
    return direct


def copy_voice_draw() -> bool:
    voice_src = desktop_dir(VOICE_DIR)
    if not voice_src.is_dir():
        print("[??] ??????:", voice_src)
        return False

    VOICE_DST.mkdir(parents=True, exist_ok=True)
    for name in VOICE_FILES:
        src = voice_src / name
        if src.is_file():
            shutil.copy2(src, VOICE_DST / name)
            print("OK voice-draw/app/", name)

    js_src = voice_src / VOICE_JS
    js_dst = VOICE_DST / VOICE_JS
    if js_src.is_dir():
        if js_dst.exists():
            shutil.rmtree(js_dst)
        shutil.copytree(js_src, js_dst)
        print("OK voice-draw/app/js/", len(list(js_dst.glob("*.js"))), "files")
    return True


def main() -> int:
    print("?????? ->", BASE / "projects")
    print("-" * 40)
    copy_voice_draw()
    print("-" * 40)
    print("??: ?? python sync_portfolio_assets.py ???????")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
