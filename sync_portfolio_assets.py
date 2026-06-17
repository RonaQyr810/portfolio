# -*- coding: utf-8 -*-
"""从桌面精确同步图片到 assets/portfolio/（按路径优先级，避免同名文件放错）。"""
from __future__ import annotations

import shutil
import subprocess
import sys
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

MIRROR_BASE = DESKTOP / "作品集" / "00-投递版本"
MIRROR_SUBPATH = Path("07-在线作品集-个人主页") / "assets" / "portfolio"
MIRROR_DELIVERY_NAMES = ("作品集-投递版-综合岗", "作品集-投递版-产品经理岗")

# 桌面重组后 DocWala / 健康食途封面等仅保留在投递版镜像中
MIRROR_FALLBACK: tuple[str, ...] = (
    "medical-home.jpg",
    "medical-guide.jpg",
    "medical-hospital.jpg",
    "medical-about.png",
    "medical-help.png",
    "medical-donation.png",
    "medical-contact.png",
    "medical-register.jpg",
    "medical-login-web.jpg",
    "medical-sitemap.png",
    "health-pathway.jpg",
    "health-food-cover.jpg",
    "health-food-bubble.png",
    "health-food-logo.png",
    "health-food-rank.png",
    "health-food-home.png",
    "health-food-login.png",
    "health-food-profile.png",
    "peking-opera-cover.png",
    "moyan-cover.png",
    "brand-logo-main.png",
    "brand-logo-restored.png",
)

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
    ("looptrace-poster.jpg", "2220048 秦艺榕 基于微信小程序“惜食小站”珍惜粮食与积分兑换系统的设计与开发 作品海报.jpg", ("03-毕设-惜食小站",)),
    # health-food-home-general / home-ai / home-nutritionist：仅保留在仓库/投递版镜像，
    # 勿映射到 UI 课作业素材（2220048_作业*.png 等为英语/音乐模板，非健康食途）
    # health-food-login / profile / logo / cover / bubble / rank：从投递版镜像同步
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
    ("web-house-sample.jpg", "2220048_秦艺榕_列表页截图.png", ("12-团队Web", "页面截图")),
    # brand-logo-*：桌面源 PNG 为 EFS 加密，改由 mirror + scripts/fix-brand-logos.py 处理
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

RUN_HINTS = (
    "惜食小站",
    "运行截图",
    "作品截图",
    "03-毕设-惜食小站",
    "03-设计素材",
    "惜食小站-作品截图",
    "毕业设计",
)


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


def mirror_roots() -> list[Path]:
    roots: list[Path] = []
    for name in MIRROR_DELIVERY_NAMES:
        p = MIRROR_BASE / name / MIRROR_SUBPATH
        if p.is_dir():
            roots.append(p)
    return roots


def sync_from_mirror(seen: set[str]) -> tuple[int, list[str]]:
    ok = 0
    synced: list[str] = []
    for root in mirror_roots():
        for rel in MIRROR_FALLBACK:
            if rel in seen:
                continue
            src = root / rel
            if not src.is_file():
                continue
            copy_file(src, PORT / rel)
            print("OK (mirror)", rel, "<-", src.relative_to(DESKTOP))
            ok += 1
            seen.add(rel)
            synced.append(rel)
        lixiang_src = root / "lixiang"
        if lixiang_src.is_dir():
            for src in lixiang_src.glob("*.png"):
                dst = PORT / "lixiang" / src.name
                before = dst.stat().st_size if dst.is_file() else -1
                copy_file(src, dst)
                if not dst.is_file() or dst.stat().st_size != before:
                    print("OK (mirror)", dst.relative_to(PORT), "<-", src.name)
                    ok += 1
    return ok, synced


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

    mirror_ok, mirror_synced = sync_from_mirror(seen)
    ok += mirror_ok
    missing = [m for m in missing if not m.split(" <= ")[0].split(":")[0] in mirror_synced]

    fix_script = BASE / "scripts" / "fix-brand-logos.py"
    if fix_script.is_file():
        import subprocess
        print("\n运行品牌 LOGO 后处理 …")
        subprocess.run([sys.executable, str(fix_script)], check=False)

    print(f"\n完成: {ok} 个文件已同步")
    if missing:
        print(f"保留旧文件 / 未找到 {len(missing)} 项:")
        for m in missing:
            print(" ", m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
