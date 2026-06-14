# -*- coding: utf-8 -*-
"""从桌面多个文件夹同步图片到 assets/portfolio/"""
from __future__ import annotations

from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent
PORT = BASE / "assets" / "portfolio"
DESKTOP = BASE.parent

# 桌面素材可能分布在多个目录（整理后结构）
SEARCH_ROOTS = [
    DESKTOP / "作品集",
    DESKTOP / "毕设项目",
    DESKTOP / "软件素材",
    DESKTOP / "作品集-投递版-综合岗",
    DESKTOP / "作品集-投递版",
    DESKTOP / "学校文档",
]

MAPPING = [
    # 环溯 LoopTrace（惜食小站）
    ("2220048 秦艺榕/原型图/首页.png", "looptrace-home.png"),
    ("首页.png", "looptrace-home.png"),
    ("2220048 秦艺榕/原型图/智能购物清单.png", "looptrace-list.png"),
    ("智能购物清单.png", "looptrace-list.png"),
    ("2220048 秦艺榕/原型图/碳积分商城.png", "looptrace-mall.png"),
    ("碳积分商城.png", "looptrace-mall.png"),
    ("2220048 秦艺榕/原型图/企业黑红榜.png", "looptrace-rank.png"),
    ("企业黑红榜.png", "looptrace-rank.png"),
    ("2220048 秦艺榕/原型图/智能回收.png", "looptrace-recycle.png"),
    ("智能回收.png", "looptrace-recycle.png"),
    ("2220048 秦艺榕/原型图/商品详情.png", "looptrace-product.png"),
    ("商品详情.png", "looptrace-product.png"),
    ("2220048 秦艺榕/原型图/订单管理.png", "looptrace-order.png"),
    ("订单管理.png", "looptrace-order.png"),
    ("2220048 秦艺榕/原型图/整改追溯系统.png", "looptrace-trace.png"),
    ("整改追溯系统.png", "looptrace-trace.png"),
    ("2220048 秦艺榕/原型图/环保挑战中心.png", "looptrace-challenge.png"),
    ("环保挑战中心.png", "looptrace-challenge.png"),
    ("2220048 秦艺榕/原型图/环境账单详情.png", "looptrace-bill.png"),
    ("环境账单详情.png", "looptrace-bill.png"),
    ("2220048 秦艺榕/原型图/个人主页.png", "looptrace-profile.png"),
    ("个人主页.png", "looptrace-profile.png"),
    ("2220048 秦艺榕/原型图/商城.png", "looptrace-shop.png"),
    ("商城.png", "looptrace-shop.png"),
    ("2220048 秦艺榕/原型图/循环贡献.png", "looptrace-contribute.png"),
    ("循环贡献.png", "looptrace-contribute.png"),
    ("2220048 秦艺榕/原型图/确认订单.png", "looptrace-confirm.png"),
    ("确认订单.png", "looptrace-confirm.png"),
    ("2220048 秦艺榕/原型图/设置.png", "looptrace-settings.png"),
    ("设置.png", "looptrace-settings.png"),
    # 健康食途
    ("健康食途app设计.jpg", "health-food-cover.jpg"),
    ("健康食途.png", "health-food-logo.png"),
    ("首页_状态 1.png", "health-food-home.png"),
    ("登录页.png", "health-food-login.png"),
    ("个人页_状态 1.png", "health-food-profile.png"),
    ("冒泡.png", "health-food-bubble.png"),
    ("排行榜_状态 1.png", "health-food-rank.png"),
    ("讨论区_状态 1.png", "health-food-discuss.png"),
    # 健康医疗网站
    ("健康医疗网站.png", "medical-sitemap.png"),
    ("首页.jpg", "medical-home.jpg"),
    ("指导网页.jpg", "medical-guide.jpg"),
    ("医院列表.jpg", "medical-hospital.jpg"),
    ("关于我们.png", "medical-about.png"),
    ("帮助.png", "medical-help.png"),
    ("捐赠.png", "medical-donation.png"),
    ("联系我们.png", "medical-contact.png"),
    ("注册.jpg", "medical-register.jpg"),
    ("登录网页.jpg", "medical-login-web.jpg"),
    # 健康之路
    ("C1 秦艺榕 冷婷婷 陈艺璇/网页展板.jpg", "health-pathway.jpg"),
    ("网页展板.jpg", "health-pathway.jpg"),
    # 房屋租赁
    ("用户端打包/house/static/img/house-gb.jpg", "web-house-sample.jpg"),
    ("house-gb.jpg", "web-house-sample.jpg"),
    # 品牌（源 PNG 可能损坏，线上封面已改用 SVG）
    ("2220048-秦艺榕/04-演示与设计/2220048 秦艺榕 名字logo.png", "brand-logo-main.png"),
    ("2220048 秦艺榕 名字logo.png", "brand-logo-main.png"),
    ("UI设计/logo.png", "brand-logo-alt.png"),
    ("logo.png", "brand-logo-alt.png"),
    ("projects/rikxiniao/app/logo.png", "brand-logo-alt.png"),
]


def find_file(name: str) -> Path | None:
    """在桌面多个目录递归查找文件。"""
    target = Path(name.replace("\\", "/")).name
    rel_path = name.replace("\\", "/")

    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        direct = root / rel_path.replace("/", "\\")
        if direct.is_file():
            return direct
        for path in root.rglob(target):
            if path.is_file():
                return path
    return None


def main() -> int:
    existing_roots = [r for r in SEARCH_ROOTS if r.is_dir()]
    if not existing_roots:
        print("[错误] 找不到桌面素材目录（作品集 / 毕设项目 / 软件素材 等）")
        return 1

    PORT.mkdir(parents=True, exist_ok=True)
    ok, missing, seen_dst = 0, 0, set()

    for src_rel, dst in MAPPING:
        if dst in seen_dst:
            continue
        src = find_file(src_rel)
        if not src:
            continue
        dst_path = PORT / dst
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst_path)
        print("OK", dst, "<-", src.parent.name + "/" + src.name)
        ok += 1
        seen_dst.add(dst)

    for src_rel, dst in MAPPING:
        if dst in seen_dst:
            continue
        print("MISSING", src_rel)
        missing += 1

    print(f"\n完成: {ok} 成功, {missing} 未找到（已有文件保留不变）")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
