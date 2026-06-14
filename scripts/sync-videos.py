# -*- coding: utf-8 -*-
"""Sync desktop portfolio videos into assets/videos/ for GitHub Pages."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = Path.home() / "Desktop"
DST = ROOT / "assets" / "videos"


def find_portfolio_dir() -> Path | None:
    for item in DESKTOP.iterdir():
        if not item.is_dir():
            continue
        if (item / "梨园之韵").is_dir() or (item / "信息可视化").is_dir():
            return item
    return None


def copy(src: Path, category: str, name: str) -> bool:
    if not src.is_file():
        print(f"SKIP missing: {src}")
        return False
    out_dir = DST / category
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / name
    shutil.copy2(src, out)
    mb = out.stat().st_size / (1024 * 1024)
    print(f"OK  {category}/{name} ({mb:.1f} MB)")
    return True


def first_existing(*paths: Path) -> Path | None:
    for p in paths:
        if p and p.is_file():
            return p
    return None


def main() -> int:
    portfolio = find_portfolio_dir()
    if not portfolio:
        print("ERROR: 未找到桌面「作品集」文件夹")
        return 1

    recovered = portfolio / "01-已恢复-视频资料"
    xishi_folder = None
    for item in DESKTOP.iterdir():
        if item.is_dir() and "惜食小站" in item.name and "2220048" in item.name:
            xishi_folder = item
            break

    copied = 0

    # xishixiaozhan
    xishi_sources = [
        recovered / "2220048 秦艺榕 作品展示视频（用户端）.mp4",
        ROOT / "assets" / "videos" / "xishixiaozhan" / "user-demo.mp4",
    ]
    admin_sources = [
        recovered / "2220048 秦艺榕 作品展示视频（管理端）.mp4",
        ROOT / "assets" / "videos" / "xishixiaozhan" / "admin-demo.mp4",
    ]
    if xishi_folder:
        xishi_sources = list(xishi_folder.glob("*.mp4")) + xishi_sources
        for f in xishi_folder.glob("*.mp4"):
            if "用户" in f.name:
                xishi_sources.insert(0, f)
            if "管理" in f.name:
                admin_sources.insert(0, f)

    user_src = first_existing(*[p for p in xishi_sources if isinstance(p, Path)])
    admin_src = first_existing(*[p for p in admin_sources if isinstance(p, Path)])
    if user_src:
        copied += copy(user_src, "xishixiaozhan", "user-demo.mp4")
    if admin_src:
        copied += copy(admin_src, "xishixiaozhan", "admin-demo.mp4")

    # peking-opera
    peking = [
        (portfolio / "梨园之韵" / "梨园之韵 最终成品.mp4", "final.mp4"),
        (portfolio / "信息可视化" / "京剧1.mp4", "opera-1.mp4"),
        (portfolio / "信息可视化" / "京剧2.mp4", "opera-2.mp4"),
        (portfolio / "信息可视化" / "京剧3.mp4", "opera-3.mp4"),
        (portfolio / "京剧修改后.mp4", "revised-full.mp4"),
        (portfolio / "京剧修改后_1.mp4", "revised-short.mp4"),
    ]
    for src, name in peking:
        copied += copy(src, "peking-opera", name)

    # campus-media
    campus = [
        (recovered / "2220048 秦艺榕 剧本视频.mp4", "script-video.mp4"),
        (portfolio / "梨园.mp4", "liyuan-short.mp4"),
    ]
    for src, name in campus:
        copied += copy(src, "campus-media", name)

    # c4d (from recovered folder)
    c4d_map = {
        "2220048 秦艺榕 滚动的水滴_1.mp4": "water-roll.mp4",
        "2220048 秦艺榕 滚动的水滴.mp4": "water-roll.mp4",
        "2220048 秦艺榕 游动的鱼.mp4": "swimming-fish.mp4",
        "2220048 秦艺榕 钟摆_1.mp4": "pendulum.mp4",
        "2220048 秦艺榕 钟摆.mp4": "pendulum.mp4",
        "2220048 秦艺榕时钟.mp4": "clock.mp4",
        "2220048 秦艺榕 切红肠.mp4": "cut-sausage.mp4",
        "2220048 秦艺榕 变速.mp4": "variable-speed.mp4",
        "2220048 秦艺榕 路径动画_1.mp4": "path-motion.mp4",
        "2220048 秦艺榕 路径动画.mp4": "path-motion.mp4",
        "2220048 秦艺榕 小球变形_1.mp4": "ball-morph.mp4",
        "2220048 秦艺榕 小球变形.mp4": "ball-morph.mp4",
        "2220048 秦艺榕 水滴滴落.mp4": "water-drop.mp4",
        "2220048 秦艺榕 生长动画.mp4": "growth.mp4",
        "220048 秦艺榕  小球抛物线.mp4": "parabola.mp4",
        "骨骼.mp4": "skeleton.mp4",
        "摩天轮.mp4": "ferris-wheel.mp4",
        "xiache.mp4": "get-off.mp4",
    }
    for src_name, out_name in c4d_map.items():
        src = first_existing(recovered / src_name, portfolio / "c4d动画合集" / src_name)
        if src:
            copied += copy(src, "c4d", out_name)

    print(f"\nSynced from: {portfolio}")
    print(f"Total copies: {copied}")
    print(f"Output: {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
