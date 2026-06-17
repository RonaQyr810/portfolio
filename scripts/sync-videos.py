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
    DESKTOP / "作品集" / "01-视频动画",
    DESKTOP / "作品集" / "01-视频动画" / "01-从主目录",
    DESKTOP / "作品集" / "01-视频动画" / "01-分类目录",
    DESKTOP / "作品集" / "信息可视化",
    DESKTOP / "作品集" / "梨园之韵",
    DESKTOP / "作品集-投递版-综合岗",
    DESKTOP / "毕设项目",
    DESKTOP / "软件素材",
    DESKTOP / "学校文档",
]


def is_valid_mp4(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            head = handle.read(12)
        if len(head) >= 8 and head[4:8] == b"ftyp":
            return True
        with path.open("rb") as handle:
            chunk = handle.read(1024 * 1024)
        return b"ftyp" in chunk or b"moov" in chunk
    except OSError:
        return False


def copy(src: Path, category: str, name: str) -> bool:
    if not src.is_file():
        return False
    if not is_valid_mp4(src):
        print(f"ERROR invalid mp4 {category}/{name} <- {src}")
        return False
    out = DST / category / name
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.is_file() and out.stat().st_size == src.stat().st_size and is_valid_mp4(out):
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
        (("01-视频动画",), "2220048 秦艺榕 作品展示视频（用户端）.mp4"),
        (("01-惜食环溯食项目",), "环溯小程序.mp4"),
        (("01-惜食环溯食项目",), "惜食环溯咨询系统录屏.mp4"))
    put("xishixiaozhan", "admin-demo.mp4",
        (("03-毕设-惜食小站", "演示视频"), "2220048 秦艺榕 作品展示视频（管理端）.mp4"),
        (("01-视频动画",), "2220048 秦艺榕 作品展示视频（管理端）.mp4"),
        (("01-惜食环溯食项目",), "惜食小站后台作品介绍.mp4"),
        (("01-惜食环溯食项目",), "惜食小站后台.mp4"))

    for name, patterns in [
        ("final.mp4", ((("梨园之韵",), "梨园之韵 最终成品.mp4"), (("梨园之韵",), "梨园之韵 最终成片.mp4"))),
    ]:
        put("peking-opera", name, *patterns)

    campus = [
        ("shizhu.mp4", (("08-传媒影像", "拾筑"), "拾筑.mp4"), (("08-传媒影像",), "拾筑.mp4")),
        ("script-video.mp4", (("01-视频动画",), "2220048 秦艺榕 剧本视频.mp4"), (("08-传媒影像",), "2220048 秦艺榕 剧本视频.mp4")),
        ("ui-defense.mp4",
         (("12-团队Web",), "录屏文件.mp4"),
         (("12-团队Web", "健康之路医疗网站"), "录屏文件.mp4"),
         (("03-课程与项目", "录屏"), "录屏文件.mp4"),
         (("UI设计",), "录屏文件.mp4")),
    ]
    for item in campus:
        put("campus-media", item[0], *item[1:])

    web = [
        ("flask-house.mp4",
         (("03-课程项目", "Flask"), "Flask功能演示.mp4"),
         (("03-课程项目",), "flask-house.mp4"),
         (("12-团队Web", "Flask"), "FlaskVideo-2220048.mp4"),
         (("web小组",), "2220048 秦艺榕 网页录屏.mp4")),
        ("web-group.mp4",
         (("03-代码项目", "文人四友"), "录屏文件.mp4"),
         (("12-团队Web", "文人四友"), "录屏文件.mp4"),
         (("03-代码项目",), "web-group.mp4"),
         (("03-课程项目",), "web-group.mp4"),
         (("01-视频动画",), "2220048 秦艺榕 网页录屏.mp4")),
        ("health-pathway.mp4",
         (("01-从主目录", "02-医疗与医生项目"), "录屏软件医疗网站设置.mp4"),
         (("02-医疗与医生项目",), "录屏软件医疗网站设置.mp4"),
         (("12-团队Web", "健康之路医疗网站"), "录屏文件.mp4"),
         (("03-课程项目", "健康之路"), "录屏文件.mp4")),
    ]
    for item in web:
        put("web-dev", item[0], *item[1:])

    c4d_home = DESKTOP / "作品集" / "01-视频动画" / "课程动画作业"
    c4d_entries = [
        ("2220048_秦艺榕_摩天轮.mp4", "ferris-wheel.mp4"),
        ("2220048_秦艺榕_滚动的水滴.mp4", "water-roll.mp4"),
        ("2220048_秦艺榕_游动的鱼.mp4", "swimming-fish.mp4"),
        ("2220048_秦艺榕_钟摆.mp4", "pendulum.mp4"),
        ("2220048_秦艺榕_闹钟.mp4", "clock.mp4"),
        ("2220048_秦艺榕_切红肠.mp4", "cut-sausage.mp4"),
        ("2220048_秦艺榕_变速.mp4", "variable-speed.mp4"),
        ("2220048_秦艺榕_路径动画.mp4", "path-motion.mp4"),
        ("2220048_秦艺榕_小球变形.mp4", "ball-morph.mp4"),
        ("2220048_秦艺榕_水滴滴落.mp4", "water-drop.mp4"),
        ("2220048_秦艺榕_生长动画.mp4", "growth.mp4"),
        ("2220048_秦艺榕_小球抛物线.mp4", "parabola.mp4"),
        ("2220048_秦艺榕_生气锤.mp4", "angry-hammer.mp4"),
        ("2220048_秦艺榕_小汽车.mp4", "small-car.mp4"),
        ("2220048_秦艺榕_变颜色.mp4", "color-change.mp4"),
        ("2220048_秦艺榕_传送射线可视.mp4", "ray-visual.mp4"),
        ("2220048_秦艺榕_交互.mp4", "interaction.mp4"),
        ("2220048_秦艺榕_UI交互.mp4", "ui-interaction.mp4"),
        ("2220048_秦艺榕_Ui交互 (1).MP4", "ui-interaction-demo.mp4"),
        ("2220048_秦艺榕_演示视频-1.mp4", "demo-1.mp4"),
        ("2220048_秦艺榕_演示视频-2.mp4", "demo-2.mp4"),
        ("2220048_秦艺榕_综合演示.mp4", "composite-demo.mp4"),
        ("2220048_秦艺榕_剧本视频.mp4", "script-video.mp4"),
        ("C1 秦艺榕 冷婷婷 陈艺璇.mp4", "team-c1.mp4"),
        ("录屏视频.mp4", "screen-record.mp4"),
        ("游动的鱼.mp4", "swimming-fish-alt.mp4"),
        ("秦艺榕_基于大数据的动漫分析.mp4", "anime-analysis.mp4"),
    ]
    c4d_legacy = {
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
        "骨骼.mp4": "angry-hammer.mp4",
        "摩天轮.mp4": "ferris-wheel.mp4",
        "xiache.mp4": "small-car.mp4",
    }
    seen: set[str] = set()
    for src_name, out_name in c4d_entries:
        if out_name in seen:
            continue
        direct = c4d_home / src_name
        if direct.is_file():
            if copy(direct, "c4d", out_name):
                copied += 1
        else:
            put("c4d", out_name, (("课程动画作业",), src_name), (("01-视频动画",), src_name), (("09-课程动画",), src_name))
        seen.add(out_name)
    for src_name, out_name in c4d_legacy.items():
        if out_name in seen:
            continue
        put("c4d", out_name, (("01-视频动画",), src_name), (("09-课程动画",), src_name), (("课程动画作业",), src_name))
        seen.add(out_name)

    put("ae-effects", "mg-intro.mp4", (("01-视频动画",), "2220048 秦艺榕.mp4"))
    put("ae-effects", "composite-2.mp4", (("01-视频动画",), "2220048 秦艺榕_1.mp4"))

    print(f"\nTotal copies: {copied}")
    print(f"Output: {DST}")

    invalid = [p.name for p in (DST / "peking-opera").glob("*.mp4") if not is_valid_mp4(p)]
    if invalid:
        print("\nWARN peking-opera 无效视频:", ", ".join(sorted(invalid)))
        print("     请将可播放的 MP4 导出到 桌面/作品集/梨园之韵/ 后再次运行本脚本")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
