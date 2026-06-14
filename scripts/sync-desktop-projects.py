# -*- coding: utf-8 -*-
"""????????????? projects/ ??"""
from __future__ import annotations

import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DESKTOP = BASE.parent

SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".next",
    "ios",
    "Pods",
    ".vercel",
}


def desktop_dir(name: str) -> Path:
    direct = DESKTOP / name
    if direct.is_dir():
        return direct
    for path in DESKTOP.iterdir():
        if path.is_dir() and name in path.name:
            return path
    return direct


def copy_tree_filtered(src: Path, dst: Path, *, extra_skip: set[str] | None = None) -> int:
    skip = SKIP_DIRS | (extra_skip or set())
    if not src.is_dir():
        print("[??] ???:", src)
        return 0
    if dst.exists():
        shutil.rmtree(dst)
    count = 0

    def _ignore(_dir: str, names: list[str]) -> set[str]:
        return {n for n in names if n in skip}

    shutil.copytree(src, dst, ignore=_ignore)
    count = sum(1 for _ in dst.rglob("*") if _.is_file())
    return count


def copy_files(src_dir: Path, dst_dir: Path, names: tuple[str, ...]) -> int:
    if not src_dir.is_dir():
        print("[??] ???:", src_dir)
        return 0
    dst_dir.mkdir(parents=True, exist_ok=True)
    ok = 0
    for name in names:
        src = src_dir / name
        if src.is_file():
            shutil.copy2(src, dst_dir / name)
            print("OK", dst_dir.relative_to(BASE) / name)
            ok += 1
    return ok


def sync_voice_draw() -> None:
    src = desktop_dir("??????")
    dst = BASE / "projects" / "voice-draw" / "app"
    copy_files(src, dst, ("index.html", "styles.css"))
    js_src, js_dst = src / "js", dst / "js"
    if js_src.is_dir():
        if js_dst.exists():
            shutil.rmtree(js_dst)
        shutil.copytree(js_src, js_dst)
        print("OK voice-draw/app/js/", len(list(js_dst.glob("*.js"))), "files")


def sync_smart_c_cleaner() -> None:
    src = desktop_dir("????") / "smart-c-cleaner"
    dst = BASE / "projects" / "smart-c-cleaner" / "src"
    n = copy_tree_filtered(src, dst)
    if n:
        print("OK smart-c-cleaner/src/", n, "files")


def sync_wildlife_wireframes() -> None:
    roots = [
        DESKTOP / "???" / "04-????" / "??????????-H5????",
        desktop_dir("???") / "04-????" / "??????????-H5????",
    ]
    src = next((p for p in roots if p.is_dir()), None)
    if src is None:
        print("[??] ???????????")
        return
    dst = BASE / "projects" / "wildlife-rescue" / "wireframes"
    dst.mkdir(parents=True, exist_ok=True)
    for name in (
        "??????????-H5???-v4-8??.html",
        "??????????-H5???.html",
        "??????????-PRD-v4-??8??.md",
    ):
        f = src / name
        if f.is_file():
            shutil.copy2(f, dst / name)
            print("OK wildlife-rescue/wireframes/", name)


def main() -> int:
    print("???? ->", BASE / "projects")
    print("-" * 40)
    sync_voice_draw()
    sync_smart_c_cleaner()
    sync_wildlife_wireframes()
    print("-" * 40)
    print("?????? python sync_portfolio_assets.py ???????")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
