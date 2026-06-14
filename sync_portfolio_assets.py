# -*- coding: utf-8 -*-
"""从桌面精确同步图片到 assets/portfolio/（按路径优先级，避免同名文件放错）。"""
from __future__ import annotations

import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
PORT = BASE / "assets" / "portfolio"
DESKTOP = BASE.parent

SEARCH_ROOTS = [
    DESKTOP / "毕设项目",
    DESKTOP / "软件素材",
    DESKTOP / "作品集",
    DESKTOP / "作品集-投递版-综合岗",
    DESKTOP / "作品集-投递版",
    DESKTOP / "学校文档",
]

MAPPING: list[tuple[str, str, tuple[str, ...]]] = [
    ("looptrace-home.png", "首页.png", ("惜食小站", "原型图")),
    ("looptrace-list.png", "智能购物清单.png", ("惜食小站", "原型图")),
    ("looptrace-mall.png", "碳积分商城.png", ("惜食小站", "原型图")),
    ("looptrace-rank.png", "企业黑红榜.png", ("惜食小站", "原型图")),
    ("looptrace-recycle.png", "智能回收.png", ("惜食小站", "原型图")),
    ("looptrace-product.png", "商品详情.png", ("惜食小站", "原型图")),
    ("looptrace-order.png", "订单管理.png", ("惜食小站", "原型图")),
    ("looptrace-trace.png", "整改追溯系统.png", ("惜食小站", "原型图")),
    ("looptrace-challenge.png", "环保挑战中心.png", ("惜食小站", "原型图")),
    ("looptrace-bill.png", "环境账单详情.png", ("惜食小站", "原型图")),
    ("looptrace-profile.png", "个人主页.png", ("惜食小站", "原型图")),
    ("looptrace-shop.png", "商城.png", ("惜食小站", "原型图")),
    ("looptrace-contribute.png", "循环贡献.png", ("惜食小站", "原型图")),
    ("looptrace-confirm.png", "确认订单.png", ("惜食小站", "原型图")),
    ("looptrace-settings.png", "设置.png", ("惜食小站", "原型图")),
    ("looptrace-poster.jpg", "2220048 秦艺榕 基于微信小程序“惜食小站”珍惜粮食与积分兑换系统的设计与开发 作品海报.jpg", ("毕业设计",)),
    ("looptrace-poster.jpg", "2220048 秦艺榕 基于微信小程序“惜食小站”珍惜粮食与积分兑换系统的设计与开发 作品海报.jpg", ("01-设计稿",)),
    ("health-food-login.png", "2220048_秦艺榕__列表页.JPG", ("UI设计稿",)),
    ("health-food-home-general.png", "2220048_秦艺榕_首页.png", ("UI设计稿",)),
    ("health-food-home-ai.png", "2220048_秦艺榕_作业1.png", ("UI设计稿",)),
    ("health-food-home-nutritionist.png", "2220048_秦艺榕_作业2.png", ("UI设计稿",)),
    ("health-food-profile.png", "2220048_秦艺榕_我的.png", ("UI设计稿",)),
    # health-food-logo / cover / bubble / rank：桌面无对应源文件，保留仓库版本不覆盖
    ("medical-home.jpg", "首页.jpg", ("健康医疗网站", "低保")),
    ("medical-home.jpg", "首页.jpg", ("健康医疗网站", "高保")),
    ("medical-home.jpg", "首页.jpg", ("new-doctor",)),
    ("medical-guide.jpg", "指导网页.jpg", ("健康医疗",)),
    ("medical-hospital.jpg", "医院列表.jpg", ("健康医疗",)),
    ("medical-about.png", "关于我们.png", ("健康医疗网站",)),
    ("medical-help.png", "帮助.png", ("健康医疗",)),
    ("medical-donation.png", "捐赠.png", ("健康医疗",)),
    ("medical-contact.png", "联系我们.png", ("健康医疗",)),
    ("medical-register.jpg", "注册.jpg", ("健康医疗",)),
    ("medical-login-web.jpg", "登录网页.jpg", ("健康医疗",)),
    ("health-pathway.jpg", "网页展板.jpg", ("C1 秦艺榕",)),
    ("health-pathway.jpg", "网页展板.jpg", ("12-团队Web",)),
    ("web-house-sample.jpg", "house-gb.jpg", ("house", "static", "img")),
    ("brand-logo-main.png", "2220048 秦艺榕 名字logo.png", ("01-设计稿",)),
    ("brand-logo-alt.png", "2220048 秦艺榕 名字logo-01.png", ("01-设计稿",)),
    ("brand-logo-restored.png", "2220048 秦艺榕 名字logo-01.png", ("01-设计稿",)),
    # peking-opera-cover：桌面 Web 截图易误配 C4D 图，保留仓库/投递版版本
]

RUN_SCREEN_ORDER = [
    "屏幕截图 2026-05-25 215127.png",
    "屏幕截图 2026-05-25 215216.png",
    "屏幕截图 2026-05-25 215233.png",
    "屏幕截图 2026-05-25 215346.png",
    "屏幕截图 2026-05-25 215428.png",
    "屏幕截图 2026-05-25 215504.png",
    "屏幕截图 2026-05-25 215528.png",
    "屏幕截图 2026-05-25 215542.png",
    "屏幕截图 2026-05-25 215615.png",
    "屏幕截图 2026-05-25 215659.png",
    "屏幕截图 2026-05-25 220247.png",
]

RUN_HINTS = ("惜食小站", "运行截图", "作品截图", "03-毕设-惜食小站", "03-设计素材", "毕业设计")


def score_path(path: Path, hints: tuple[str, ...], filename: str) -> int:
    if path.name != filename and path.name.lower() != filename.lower():
        return -1
    if "node_modules" in path.parts or "个人主页" in path.parts:
        return -1
    text = str(path)
    score = sum(10 for h in hints if h in text)
    if "效果图" in text and "原型图" in hints:
        score -= 5
    if any(x in text for x in ("\\dist\\", "/dist/", "\\frontend\\", "/frontend/", "rikxiniao", "MagicFace")):
        score -= 50
    if "app" in path.parts and "logo" in filename.lower():
        score -= 30
    return score


def find_best(filename: str, hints: tuple[str, ...]) -> Path | None:
    best: Path | None = None
    best_score = -1
    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        for path in root.rglob(filename):
            if not path.is_file():
                continue
            s = score_path(path, hints, filename)
            if s > best_score:
                best_score = s
                best = path
    return best


def find_run_screens() -> list[Path]:
    found: dict[str, Path] = {}
    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        for name in RUN_SCREEN_ORDER:
            if name in found:
                continue
            for path in root.rglob(name):
                if not path.is_file():
                    continue
                if not any(h in str(path) for h in RUN_HINTS):
                    continue
                found[name] = path
                break
    return [found[n] for n in RUN_SCREEN_ORDER if n in found]


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_file() and dst.stat().st_size == src.stat().st_size:
        return
    shutil.copy2(src, dst)


def main() -> int:
    if not any(r.is_dir() for r in SEARCH_ROOTS):
        print("[错误] 找不到桌面素材目录")
        return 1

    ok, missing = 0, []
    seen: set[str] = set()

    for dst_rel, filename, hints in MAPPING:
        if dst_rel in seen:
            continue
        src = find_best(filename, hints)
        if src:
            copy_file(src, PORT / dst_rel)
            print("OK", dst_rel, "<-", src.relative_to(DESKTOP))
            ok += 1
            seen.add(dst_rel)

    for dst_rel, filename, hints in MAPPING:
        if dst_rel not in seen:
            missing.append(f"{dst_rel} <= {filename}")

    run_dir = PORT / "looptrace-run"
    run_dir.mkdir(parents=True, exist_ok=True)
    screens = find_run_screens()
    for i, src in enumerate(screens, start=1):
        dst = run_dir / f"run-{i:02d}.png"
        copy_file(src, dst)
        print("OK", dst.relative_to(PORT), "<-", src.relative_to(DESKTOP))
        ok += 1
    if len(screens) < 11:
        missing.append(f"looptrace-run: {len(screens)}/11")

    print(f"\n完成: {ok} 个文件已同步")
    if missing:
        print(f"保留旧文件 / 未找到 {len(missing)} 项:")
        for m in missing:
            print(" ", m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
