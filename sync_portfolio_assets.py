# -*- coding: utf-8 -*-
"""从桌面「作品集」文件夹同步图片到 assets/portfolio/"""
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent
PORT = BASE / "assets" / "portfolio"
ROOT = BASE.parent / "作品集"

MAPPING = [
    # 环溯 LoopTrace（惜食小站）
    ("2220048 秦艺榕/原型图/首页.png", "looptrace-home.png"),
    ("2220048 秦艺榕/原型图/智能购物清单.png", "looptrace-list.png"),
    ("2220048 秦艺榕/原型图/碳积分商城.png", "looptrace-mall.png"),
    ("2220048 秦艺榕/原型图/企业黑红榜.png", "looptrace-rank.png"),
    ("2220048 秦艺榕/原型图/智能回收.png", "looptrace-recycle.png"),
    ("2220048 秦艺榕/原型图/商品详情.png", "looptrace-product.png"),
    ("2220048 秦艺榕/原型图/订单管理.png", "looptrace-order.png"),
    ("2220048 秦艺榕/原型图/整改追溯系统.png", "looptrace-trace.png"),
    ("2220048 秦艺榕/原型图/环保挑战中心.png", "looptrace-challenge.png"),
    ("2220048 秦艺榕/原型图/环境账单详情.png", "looptrace-bill.png"),
    # 健康食途
    ("健康食途app设计.jpg", "health-food-cover.jpg"),
    ("健康食途.png", "health-food-logo.png"),
    ("首页_状态 1.png", "health-food-home.png"),
    ("登录页.png", "health-food-login.png"),
    ("个人页_状态 1.png", "health-food-profile.png"),
    ("冒泡.png", "health-food-bubble.png"),
    ("排行榜_状态 1.png", "health-food-rank.png"),
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
    # 房屋租赁
    ("用户端打包/house/static/img/house-gb.jpg", "web-house-sample.jpg"),
    # 品牌
    ("2220048 秦艺榕 名字logo.png", "brand-logo-main.png"),
    ("UI设计/logo.png", "brand-logo-alt.png"),
    ("UI设计/2220048 秦艺榕 名字logo-恢复的.png", "brand-logo-restored.png"),
)


def find_file(name: str) -> Path | None:
    """在作品集目录递归查找文件名（兼容子文件夹重组）。"""
    if not ROOT.is_dir():
        return None
    direct = ROOT / name.replace("/", "\\")
    if direct.is_file():
        return direct
    target = Path(name).name
    for path in ROOT.rglob(target):
        if path.is_file():
            return path
    return None


def main():
    if not ROOT.is_dir():
        print(f"[错误] 找不到作品集文件夹: {ROOT}")
        return 1
    PORT.mkdir(parents=True, exist_ok=True)
    ok, missing = 0, 0
    for src_rel, dst in MAPPING:
        src = find_file(src_rel)
        dst_path = PORT / dst
        if src:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst_path)
            print("OK", dst)
            ok += 1
        else:
            print("MISSING", src_rel)
            missing += 1
    print(f"\n完成: {ok} 成功, {missing} 未找到")
    return 0 if missing == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
