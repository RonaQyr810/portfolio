# -*- coding: utf-8 -*-
"""对比桌面素材与官网 assets，输出差异报告。"""
from __future__ import annotations

from pathlib import Path

DESKTOP = Path.home() / "Desktop"
SITE = Path(__file__).resolve().parents[1]
PORT = SITE / "assets" / "portfolio"
VID = SITE / "assets" / "videos"

ROOTS = [
    DESKTOP / "作品集",
    DESKTOP / "毕设项目",
    DESKTOP / "软件素材",
    DESKTOP / "作品集-投递版-综合岗",
]


def find_all(name: str) -> list[Path]:
    hits = []
    for root in ROOTS:
        if not root.is_dir():
            continue
        for p in root.rglob(name):
            if p.is_file() and "node_modules" not in p.parts:
                hits.append(p)
    return hits


def main() -> None:
    print("=== 同名文件冲突（可能导致图片放错）===")
    for name in [
        "首页.png", "首页.jpg", "logo.png", "登录页.png",
    ]:
        hits = find_all(name)
        if len(hits) > 1:
            print(f"\n{name} ({len(hits)} 处):")
            for h in hits[:8]:
                print(" ", h.relative_to(DESKTOP))

    print("\n=== 官网视频 vs 桌面源 ===")
    expected = {
        "campus-media/shizhu.mp4": ["拾筑.mp4"],
        "campus-media/ui-defense.mp4": ["录屏文件.mp4", "UI设计答辩", "录屏"],
        "campus-media/script-video.mp4": ["剧本视频.mp4", "剧本.mp4"],
        "web-dev/flask-house.mp4": ["Flask功能演示", "flask-house.mp4", "FlaskVideo", "网页录屏"],
        "web-dev/web-group.mp4": ["web-group.mp4", "网页录屏"],
        "web-dev/health-pathway.mp4": ["健康之路", "录屏文件.mp4"],
        "ae-effects/mg-intro.mp4": ["mg开头", "mg标题"],
    }
    for dst, keywords in expected.items():
        out = VID / dst
        ok = out.is_file()
        size = f"{out.stat().st_size/1024/1024:.1f}MB" if ok else "MISSING"
        print(f"{dst}: {size}")
        if not ok:
            for root in ROOTS:
                if not root.is_dir():
                    continue
                for mp4 in root.rglob("*.mp4"):
                    if any(k in mp4.name for k in keywords):
                        print("  candidate:", mp4.relative_to(DESKTOP))


if __name__ == "__main__":
    main()
