# -*- coding: utf-8 -*-
import os, shutil

PORT = r"c:\Users\echo9\Desktop\个人主页\assets\portfolio"
ROOT = r"c:\Users\echo9\Desktop\作品集"

MAPPING = [
    # 环溯 LoopTrace
    (r"2220048 秦艺榕\原型图\首页.png", "looptrace-home.png"),
    (r"2220048 秦艺榕\原型图\智能购物清单.png", "looptrace-list.png"),
    (r"2220048 秦艺榕\原型图\碳积分商城.png", "looptrace-mall.png"),
    (r"2220048 秦艺榕\原型图\企业黑红榜.png", "looptrace-rank.png"),
    (r"2220048 秦艺榕\原型图\智能回收.png", "looptrace-recycle.png"),
    (r"2220048 秦艺榕\原型图\商品详情.png", "looptrace-product.png"),
    (r"2220048 秦艺榕\原型图\订单管理.png", "looptrace-order.png"),
    (r"2220048 秦艺榕\原型图\整改追溯系统.png", "looptrace-trace.png"),
    (r"2220048 秦艺榕\原型图\环保挑战中心.png", "looptrace-challenge.png"),
    (r"2220048 秦艺榕\原型图\环境账单详情.png", "looptrace-bill.png"),
    # 健康食途
    (r"健康食途app设计.jpg", "health-food-cover.jpg"),
    (r"健康食途.png", "health-food-logo.png"),
    (r"首页_状态 1.png", "health-food-home.png"),
    (r"登录页.png", "health-food-login.png"),
    (r"个人页_状态 1.png", "health-food-profile.png"),
    (r"冒泡.png", "health-food-bubble.png"),
    (r"排行榜_状态 1.png", "health-food-rank.png"),
    # 健康医疗网站
    (r"健康医疗网站.png", "medical-sitemap.png"),
    (r"首页.jpg", "medical-home.jpg"),
    (r"指导网页.jpg", "medical-guide.jpg"),
    (r"医院列表.jpg", "medical-hospital.jpg"),
    (r"关于我们.png", "medical-about.png"),
    (r"帮助.png", "medical-help.png"),
    (r"捐赠.png", "medical-donation.png"),
    (r"联系我们.png", "medical-contact.png"),
    (r"注册.jpg", "medical-register.jpg"),
    (r"登录网页.jpg", "medical-login-web.jpg"),
    # 健康之路
    (r"C1 秦艺榕 冷婷婷 陈艺璇\网页展板.jpg", "health-pathway.jpg"),
    # 房屋租赁
    (r"用户端打包\house\static\img\house-gb.jpg", "web-house-sample.jpg"),
    # 品牌
    (r"2220048 秦艺榕 名字logo.png", "brand-logo-main.png"),
    (r"UI设计\logo.png", "brand-logo-alt.png"),
    (r"UI设计\2220048 秦艺榕 名字logo-恢复的.png", "brand-logo-restored.png"),
]

os.makedirs(PORT, exist_ok=True)
for src_rel, dst in MAPPING:
    src = os.path.join(ROOT, src_rel)
    dst_path = os.path.join(PORT, dst)
    if os.path.exists(src):
        shutil.copy2(src, dst_path)
        print("OK", dst)
    else:
        print("MISSING", src_rel)
