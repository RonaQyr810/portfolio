# -*- coding: utf-8 -*-
"""从桌面「作品集」同步视频到 assets/videos/。"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = Path.home() / "Desktop"
DST = ROOT / "assets" / "videos"

SEARCH_ROOTS = [
    DESKTOP / "作品集",
    DESKTOP / "作品集-投递版-综合岗",
    DESKTOP / "毕设项目",
    DESKTOP / "软件素材",
    DESKTOP / "学校文档",
]


def copy(src: Path, category: str, name: str) -> bool:
    if not src.is_file():
        return False
    out = DST / category / name
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.is_file() and out.stat().st_size == src.stat().st_size:
        print(f"SKIP same {category}/{name}")
        return False
    shutil.copy2(src, out)
    mb = out.stat().st_size / (1024 * 1024)
    print(f"OK  {category}/{name} ({mb:.1f} MB) <- {src.name}")
    return True


def first_matching(*patterns: tuple[tuple[str, ...], str]) -> Path | None:
    best: Path | None = None
    best_score = -1
    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        for hints, filename in patterns:
            for path in root.rglob(filename):
                if not path.is_file() or "node_modules" in path.parts or "个人主页" in path.parts:
                    continue
                score = sum(10 for h in hints if h in str(path))
                if score > best_score:
                    best_score = score
                    best = path
    return best


def main() -> int:
    if not (DESKTOP / "作品集").is_dir():
        print("ERROR: 未找到桌面「作品集」文件夹")
        return 1

    copied = 0

    def put(category: str, name: str, *pattern_list: tuple[tuple[str, ...], str]) -> None:
        nonlocal copied
        src = first_matching(*pattern_list)
        if src and copy(src, category, name):
            copied += 1

    put("xishixiaozhan", "user-demo.mp4",
        (("03-毕设-惜食小站", "演示视频"), "2220048 秦艺榕 作品展示视频（用户端）.mp4"),
        (("01-视频动画",), "2220048 秦艺榕 作品展示视频（用户端）.mp4"))
    put("xishixiaozhan", "admin-demo.mp4",
        (("03-毕设-惜食小站", "演示视频"), "2220048 秦艺榕 作品展示视频（管理端）.mp4"),
        (("01-视频动画",), "2220048 秦艺榕 作品展示视频（管理端）.mp4"))

    for name, patterns in [
        ("final.mp4", ((("梨园之韵",), "梨园之韵 最终成品.mp4"),)),
        ("opera-1.mp4", ((("信息可视化",), "京剧1.mp4"),)),
        ("opera-2.mp4", ((("信息可视化",), "京剧2.mp4"),)),
        ("opera-3.mp4", ((("信息可视化",), "京剧3.mp4"),)),
        ("revised-full.mp4", ((("信息可视化",), "京剧修改后.mp4"),)),
        ("revised-short.mp4", ((("信息可视化",), "京剧修改后_1.mp4"),)),
    ]:
        put("peking-opera", name, *patterns)

    campus = [
        ("shizhu.mp4", (("08-传媒影像", "拾筑"), "拾筑.mp4"), (("08-传媒影像",), "拾筑.mp4")),
        ("script-video.mp4", (("01-视频动画",), "2220048 秦艺榕 剧本视频.mp4"), (("08-传媒影像",), "2220048 秦艺榕 剧本视频.mp4")),
        ("ui-defense.mp4",
         (("12-团队Web",), "录屏文件.mp4"),
         (("03-课程与项目", "录屏"), "录屏文件.mp4"),
         (("UI设计",), "录屏文件.mp4")),
        ("liyuan-short.mp4", (("06-视频精选", "梨园"), "梨园.mp4"), (("梨园",), "梨园.mp4")),
    ]
    for item in campus:
        put("campus-media", item[0], *item[1:])

    web = [
        ("flask-house.mp4", (("12-团队Web", "Flask"), "FlaskVideo-2220048.mp4"), (("web小组",), "2220048 秦艺榕 网页录屏.mp4")),
        ("web-group.mp4", (("01-视频动画",), "2220048 秦艺榕 网页录屏.mp4"),),
        ("health-pathway.mp4", (("09-课程动画",), "C1 秦艺榕 冷婷婷 陈艺璇.mp4"), (("C1 秦艺榕",), "C1 秦艺榕 冷婷婷 陈艺璇.mp4")),
    ]
    for item in web:
        put("web-dev", item[0], *item[1:])

    c4d_map = {
        "2220048 秦艺榕 滚动的水滴.mp4": "water-roll.mp4",
        "2220048 秦艺榕 游动的鱼.mp4": "swimming-fish.mp4",
        "2220048 秦艺榕 钟摆.mp4": "pendulum.mp4",
        "2220048 秦艺榕时钟.mp4": "clock.mp4",
        "2220048 秦艺榕 切红肠.mp4": "cut-sausage.mp4",
        "2220048 秦艺榕 变速.mp4": "variable-speed.mp4",
        "2220048 秦艺榕 路径动画.mp4": "path-motion.mp4",
        "2220048 秦艺榕 小球变形.mp4": "ball-morph.mp4",
        "2220048 秦艺榕 水滴滴落.mp4": "water-drop.mp4",
        "2220048 秦艺榕 生长动画.mp4": "growth.mp4",
        "220048 秦艺榕  小球抛物线.mp4": "parabola.mp4",
        "骨骼.mp4": "skeleton.mp4",
        "摩天轮.mp4": "ferris-wheel.mp4",
        "xiache.mp4": "get-off.mp4",
    }
    seen: set[str] = set()
    for src_name, out_name in c4d_map.items():
        if out_name in seen:
            continue
        put("c4d", out_name, (("01-视频动画",), src_name), (("09-课程动画",), src_name))
        seen.add(out_name)

    put("ae-effects", "mg-intro.mp4", (("01-视频动画",), "2220048 秦艺榕.mp4"))
    put("ae-effects", "composite-2.mp4", (("01-视频动画",), "2220048 秦艺榕_1.mp4"))

    print(f"\nTotal copies: {copied}")
    print(f"Output: {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
