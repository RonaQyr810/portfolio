# -*- coding: utf-8 -*-
"""同步项目卡片封面 PNG（立相 / 墨演 / 同声传译 / 梨园）。"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = Path(r"C:\Users\echo9\Desktop")
PORT = ROOT / "assets" / "portfolio"


def copy_if_found(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_file() and dst.stat().st_size == src.stat().st_size:
        return False
    shutil.copy2(src, dst)
    print(f"OK {dst.relative_to(ROOT)} <- {src.name}")
    return True


def main() -> int:
    portfolio = DESKTOP / "\u4f5c\u54c1\u96c6"
    copied = 0

    lixiang_candidates = [
        portfolio / "00-\u6295\u9012\u7248\u672c" / "\u4f5c\u54c1\u96c6-\u6295\u9012\u7248-\u7efc\u5408\u5c97" / "07-\u5728\u7ebf\u4f5c\u54c1\u96c6-\u4e2a\u4eba\u4e3b\u9875" / "assets" / "portfolio" / "lixiang",
        portfolio / "00-\u6295\u9012\u7248\u672c" / "\u4f5c\u54c1\u96c6-\u6295\u9012\u7248-\u4ea7\u54c1\u7ecf\u7406\u5c97" / "07-\u5728\u7ebf\u4f5c\u54c1\u96c6-\u4e2a\u4eba\u4e3b\u9875" / "assets" / "portfolio" / "lixiang",
    ]
    for lixiang_screens in lixiang_candidates:
        if not lixiang_screens.is_dir():
            continue
        for name in ("splash.png", "home.png", "login.png", "scan.png", "astro.png", "astro-detail.png", "profile.png"):
            src = lixiang_screens / name
            if copy_if_found(src, PORT / "lixiang" / name):
                copied += 1

    for p in portfolio.rglob("linguo-logo*.png"):
        if p.is_file() and "node_modules" not in p.parts:
            if copy_if_found(p, PORT / "linguo-cover.png"):
                copied += 1
            break

    for p in portfolio.rglob("peking-opera-cover.png"):
        if p.is_file() and "07-" in str(p):
            if copy_if_found(p, PORT / "peking-opera-cover.png"):
                copied += 1
            break

    for p in portfolio.rglob("moyan-cover.png"):
        if p.is_file() and "portfolio" in str(p):
            if copy_if_found(p, PORT / "moyan-cover.png"):
                copied += 1
            break

    print(f"Done: {copied} cover(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
