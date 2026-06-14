# -*- coding: utf-8 -*-
import os
import re
from collections import defaultdict

ROOT = r"c:\Users\echo9\Desktop\作品集"
OUT_MD = os.path.join(ROOT, "作品集分类整理.md")
OUT_HTML = r"c:\Users\echo9\Desktop\个人主页\classification.html"

SKIP_DIRS = {
    "node_modules", "__pycache__", ".git", ".vs", ".idea",
    "dist", "build", ".bin", "FileContentIndex", "v17", "inspectionProfiles",
}

# Classification rules: (category_id, category_name, patterns for path/name)
RULES = [
    ("resume", "简历与个人资料", [
        r"简历", r"演员资料", r"模特", r"演员", r"个人写真", r"社会实践考核",
        r"假期留宿", r"临时住宿", r"认识实习",
    ]),
    ("live", "直播运营与传媒实践", [
        r"直播", r"校招", r"主播", r"带货", r"暑期班", r"广告用语",
    ]),
    ("ui", "UI/UX 产品设计", [
        r"原型图", r"效果图", r"健康食途", r"惜食小站", r"环溯", r"LoopTrace",
        r"登录页", r"个人页", r"排行榜", r"冒泡", r"讨论区", r"状态 1",
        r"app设计", r"xmind", r"系统功能结构",
    ]),
    ("web", "Web 开发与编程", [
        r"web", r"Web", r"flask", r"Flask", r"house\.sql", r"healthy",
        r"new-doctor", r"用户端打包", r"\.html$", r"\.py$", r"\.sql$",
        r"网页录屏", r"项目部署", r"软件需求规格", r"房屋租赁", r"指导网页",
        r"首页\.jpg", r"医院列表", r"捐赠", r"帮助", r"关于我们", r"联系我们",
        r"注册\.jpg", r"登录网页",
    ]),
    ("video", "视频动画与三维制作", [
        r"\.mp4$", r"\.avi$", r"\.aep$", r"\.prproj$", r"\.c4d$",
        r"京剧", r"梨园", r"信息可视化", r"c4d动画", r"ae/", r"ae\\",
        r"赛博", r"mg开头", r"mg标题", r"wanshp", r"剧本", r"拾筑",
        r"录屏文件",
    ]),
    ("visual", "品牌视觉与平面设计", [
        r"logo", r"Logo", r"LOGO", r"海报", r"美甲", r"文人四友",
        r"UI设计", r"画布", r"\.psd$", r"\.ai$", r"非遗", r"手工DIY",
        r"绿芯科技", r"创业计划",
    ]),
    ("course", "课程作业与学术报告", [
        r"实验报告", r"课程设计", r"设计报告", r"设计书", r"可行性分析",
        r"调研报告", r"课题规划", r"创新创业", r"项目实战", r"实训文件",
        r"实验九", r"数字图像处理", r"数字合成", r"web应用开发",
        r"无穷级数", r"\.pptx$", r"\.doc$", r"\.docx$", r"\.pdf$",
    ]),
    ("work", "实习与工作项目", [
        r"和光同坤", r"CEO", r"投融资",
    ]),
    ("archive", "压缩包与备份", [
        r"\.zip$", r"\.rar$", r"\.7z$", r"healthy\.zip",
    ]),
    ("misc", "素材杂项与待整理", [
        r"杂七杂八", r"一堆", r"微信图片", r"副本", r"测试\.pptx",
        r"最终ppt", r"~\\$",
    ]),
]

CATEGORY_META = {
    "resume": ("八", "简历与个人资料", "个人简历、写真、演员模卡、社会实践等个人展示材料"),
    "live": ("七", "直播运营与传媒实践", "校招直播、带货运营、直播流程策划与数据统计"),
    "ui": ("二", "UI/UX 产品设计", "APP 原型、界面设计、交互稿、功能结构文档"),
    "web": ("三", "Web 开发与编程", "网站项目源码、数据库、HTML 页面、部署文档"),
    "video": ("四", "视频动画与三维制作", "AE/PR/C4D 工程、成片视频、信息可视化作品"),
    "visual": ("五", "品牌视觉与平面设计", "LOGO、海报、PPT 视觉、文创设计"),
    "course": ("一", "课程作业与学术报告", "实验报告、课程设计、调研分析、创业计划书"),
    "work": ("六", "实习与工作项目", "实习相关产出（如有）"),
    "archive": ("九", "压缩包与备份", "项目打包压缩文件"),
    "misc": ("十", "素材杂项与待整理", "零散素材、截图、待归档文件"),
}


def should_skip_dir(name):
    return name in SKIP_DIRS or name.startswith(".")


def classify(rel_path, name):
    full = rel_path.replace("\\", "/")
    text = f"{full}/{name}" if full != "." else name
    ext = os.path.splitext(name)[1].lower()
    if ext in (".zip", ".rar", ".7z", ".tar", ".gz"):
        return "archive"
    for cat_id, _, patterns in RULES:
        if cat_id == "archive":
            continue
        for p in patterns:
            if re.search(p, text, re.I):
                return cat_id
    return "misc"


def human_size(n):
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n/1024:.1f} KB"
    if n < 1024 * 1024 * 1024:
        return f"{n/1024/1024:.1f} MB"
    return f"{n/1024/1024/1024:.2f} GB"


def scan():
    items = defaultdict(list)
    stats = defaultdict(lambda: {"count": 0, "size": 0})
    total_files = 0
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir == ".":
            rel_dir = ""

        for fn in filenames:
            if fn.startswith("~$"):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                sz = os.path.getsize(fp)
            except OSError:
                continue
            rel = os.path.join(rel_dir, fn) if rel_dir else fn
            cat = classify(rel_dir, fn)
            ext = os.path.splitext(fn)[1].lower()
            is_dep = any(x in rel.replace("\\", "/") for x in [
                "node_modules/", "healthy-serve/healthy/node_modules",
                "new-doctor(3)/", "__pycache__/",
            ])
            entry = {
                "path": rel.replace("\\", "/"),
                "name": fn,
                "size": sz,
                "ext": ext,
                "is_dep": is_dep,
            }
            items[cat].append(entry)
            if not is_dep:
                stats[cat]["count"] += 1
                stats[cat]["size"] += sz
            total_files += 1
            total_size += sz

    return items, stats, total_files, total_size


def project_summaries():
    return [
        {
            "name": "立相 MagicFace",
            "cat": "ui",
            "role": "产品规划与界面设计",
            "course": "和光同坤实习",
            "time": "2026",
            "files": "projects/lixiang/、assets/portfolio/lixiang/",
            "desc": "MediaPipe 面相匹配 iOS 应用，单人画像 / 双人适配度 / 3D 扫描演示。",
        },
        {
            "name": "日薪喵",
            "cat": "web",
            "role": "独立开发",
            "course": "个人项目",
            "time": "2026",
            "files": "projects/rikxiniao/",
            "desc": "实时收入桌宠，React + Electron + PWA 双端。",
        },
        {
            "name": "墨演 MoYan",
            "cat": "web",
            "role": "实训开发",
            "course": "七牛云×XE 实训营",
            "time": "2026",
            "files": "projects/moyan/",
            "desc": "AI 辅助剧本创作，小说转 YAML 剧本，Next.js + Monaco。",
        },
        {
            "name": "AI 视觉对话助手",
            "cat": "web",
            "role": "产品验证与原型",
            "course": "和光同坤实习",
            "time": "2026",
            "files": "projects/ai-vision/",
            "desc": "多模态视觉理解 + 对话交互原型（实习验证项目）。",
        },
        {
            "name": "AI 语音绘图工具",
            "cat": "web",
            "role": "独立开发",
            "course": "个人项目",
            "time": "2026",
            "files": "projects/voice-draw/",
            "desc": "纯语音控制 Web 绘图，Web Speech API + Canvas 原生 JavaScript。",
        },
        {
            "name": "Smart C Cleaner",
            "cat": "web",
            "role": "独立开发",
            "course": "个人项目",
            "time": "2026",
            "files": "projects/smart-c-cleaner/",
            "desc": "Windows 智能 C 盘清理工具，Python + Tkinter GUI 与命令行双模式。",
        },
        {
            "name": "环溯 LoopTrace · 惜食小站",
            "cat": "ui",
            "role": "课题规划设计（独立完成 15 页原型）",
            "course": "项目实战（虚拟现实与交互）",
            "time": "2025.07",
            "files": "2220048 秦艺榕/原型图/、系统功能结构设计.docx、惜食小站 PPT",
            "desc": "微信小程序可持续消费平台，含环境账单、智能购物清单、碳积分商城、企业红黑榜等模块。",
        },
        {
            "name": "健康食途",
            "cat": "ui",
            "role": "APP 功能规划与设计",
            "course": "创新创业综合实践",
            "time": "2025.01",
            "files": "设计书.docx、健康食途*.png/jpg/psd/xmind、商业计划 PPT",
            "desc": "智能健康饮食配送 APP，含开屏、登录、首页三板块、社区冒泡、排行榜等完整 UI。",
        },
        {
            "name": "健康之路 · 医疗预约平台",
            "cat": "web",
            "role": "可行性分析、调研、开发（团队协作）",
            "course": "Web 应用开发",
            "time": "2025.04",
            "files": "C1 秦艺榕 冷婷婷 陈艺璇/、healthy-serve/、网页展板.jpg",
            "desc": "上海市医疗资源预约与症状-科室智能匹配平台，Node.js + MySQL + HTML5。",
        },
        {
            "name": "健康医疗网站 (new-doctor)",
            "cat": "web",
            "role": "网站设计与页面开发",
            "course": "实习作品",
            "time": "2025",
            "files": "new-doctor/、健康医疗网站.png、医院列表/、各页面截图",
            "desc": "医疗健康服务平台，含医院列表、医生详情、预约、捐赠、帮助中心等页面。",
        },
        {
            "name": "房屋租赁可视化 Web",
            "cat": "web",
            "role": "Web 开发（小组作业）",
            "course": "Web 应用开发",
            "time": "2024",
            "files": "2220048 秦艺榕 web小组作业/、用户端打包/、首页.jpg",
            "desc": "Flask 房屋租赁信息管理与数据可视化系统，含源码、SQL 数据库与录屏演示。",
        },
        {
            "name": "梨园之韵 · 京剧信息可视化",
            "cat": "video",
            "role": "剪辑、动效、海报制作",
            "course": "信息可视化技术",
            "time": "2024-2025",
            "files": "梨园之韵/、信息可视化/、京剧*.mp4/ai/aep",
            "desc": "京剧文化主题信息可视化影像，AE/PR 完成剪辑与海报动画。",
        },
        {
            "name": "C4D / AE 动画练习",
            "cat": "video",
            "role": "三维与特效制作",
            "course": "数字合成与特效技术 / 三维模型设计",
            "time": "2024-2025",
            "files": "c4d动画合集/、ae/、赛博*.avi、mg*.avi、2220048 秦艺榕.mp4",
            "desc": "小球抛物线、游动的鱼、摩天轮、MG 片头、赛博朋克风格特效等练习与综合作品。",
        },
        {
            "name": "拾筑 · 非遗文化实训",
            "cat": "video",
            "role": "调研、剧本、视频制作",
            "course": "专业实训",
            "time": "2024",
            "files": "实训文件/、拾筑.mp4、剧本视频.mp4",
            "desc": "非物质文化遗产主题实训作品，含调研报告与剧本视频。",
        },
        {
            "name": "品牌 LOGO 与视觉设计",
            "cat": "visual",
            "role": "标志与视觉识别设计",
            "course": "UI 设计 / 个人品牌",
            "time": "2024-2025",
            "files": "UI设计/、名字logo*.png/psd、logo.png",
            "desc": "个人品牌 LOGO 及「文人四友」等课程视觉设计作品。",
        },
        {
            "name": "直播经济产业学院实践",
            "cat": "live",
            "role": "班长 / 直播主持人 / 账号运营",
            "course": "社会实践 + 直播课程",
            "time": "2025",
            "files": "社会实践考核表、校招直播流程、各主播任务表、演员资料",
            "desc": "辛江农业、佳农、来伊份等品类直播，校宣传主持人，137 小时社会实践。",
        },
    ]


def write_markdown(items, stats, total_files, total_size):
    lines = []
    lines.append("# 秦艺榕 · 作品集分类整理\n")
    lines.append(f"> 整理日期：2026年6月  |  文件夹：`作品集`  |  共 **{total_files}** 个文件，总大小 **{human_size(total_size)}**\n")
    lines.append("---\n")

    lines.append("## 总览\n")
    lines.append("| 序号 | 分类 | 文件数（不含依赖） | 大小 | 说明 |")
    lines.append("|------|------|-------------------|------|------|")
    order = ["course", "ui", "web", "video", "visual", "work", "live", "resume", "archive", "misc"]
    for cat_id in order:
        num, title, desc = CATEGORY_META[cat_id]
        s = stats[cat_id]
        lines.append(f"| {num} | {title} | {s['count']} | {human_size(s['size'])} | {desc} |")
    lines.append("")

    lines.append("## 核心项目一览\n")
    lines.append("| 项目名称 | 分类 | 你的角色 | 课程/场景 | 时间 | 关键文件位置 |")
    lines.append("|----------|------|----------|-----------|------|--------------|")
    for p in project_summaries():
        cat_name = CATEGORY_META[p["cat"]][1]
        lines.append(f"| {p['name']} | {cat_name} | {p['role']} | {p['course']} | {p['time']} | `{p['files']}` |")
    lines.append("")

    for cat_id in order:
        num, title, desc = CATEGORY_META[cat_id]
        lines.append(f"---\n\n## {num}、{title}\n")
        lines.append(f"{desc}\n")

        # group by top-level folder
        groups = defaultdict(list)
        for e in items[cat_id]:
            if e["is_dep"]:
                continue
            top = e["path"].split("/")[0] if "/" in e["path"] else "（根目录）"
            groups[top].append(e)

        if not groups:
            lines.append("*（无独立文件，或已归入依赖目录）*\n")
            continue

        dep_count = sum(1 for e in items[cat_id] if e["is_dep"])
        if dep_count:
            lines.append(f"> 另有 {dep_count} 个项目依赖文件（node_modules 等）已折叠，不逐条列出。\n")

        for group_name in sorted(groups.keys()):
            files = groups[group_name]
            group_size = sum(f["size"] for f in files)
            lines.append(f"### 📁 {group_name}（{len(files)} 个文件，{human_size(group_size)}）\n")
            lines.append("| 文件名 | 类型 | 大小 |")
            lines.append("|--------|------|------|")
            for f in sorted(files, key=lambda x: (-x["size"], x["name"]))[:40]:
                lines.append(f"| `{f['name']}` | {f['ext'] or '—'} | {human_size(f['size'])} |")
            if len(files) > 40:
                lines.append(f"| *... 另有 {len(files)-40} 个文件* | | |")
            lines.append("")

    lines.append("---\n\n## 整理建议\n")
    lines.append("建议将作品集按以下结构归档（可复制本分类创建子文件夹）：\n")
    lines.append("```")
    lines.append("作品集/")
    lines.append("├── 01-课程作业与学术报告/")
    lines.append("├── 02-UI与产品设计/")
    lines.append("│   ├── 环溯LoopTrace-惜食小站/")
    lines.append("│   └── 健康食途/")
    lines.append("├── 03-Web开发与编程/")
    lines.append("│   ├── 健康之路/")
    lines.append("│   ├── 健康医疗网站/")
    lines.append("│   └── 房屋租赁可视化/")
    lines.append("├── 04-视频动画与三维/")
    lines.append("│   ├── 梨园之韵-京剧可视化/")
    lines.append("│   ├── C4D动画练习/")
    lines.append("│   └── AE特效合成/")
    lines.append("├── 05-品牌视觉设计/")
    lines.append("├── 06-直播运营实践/")
    lines.append("├── 07-简历与个人资料/")
    lines.append("└── 08-素材杂项/")
    lines.append("```\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Wrote", OUT_MD)


def write_html(items, stats, total_files, total_size):
    projects = project_summaries()
    order = ["course", "ui", "web", "video", "visual", "work", "live", "resume", "archive", "misc"]

    cat_cards = ""
    for cat_id in order:
        num, title, desc = CATEGORY_META[cat_id]
        s = stats[cat_id]
        cat_cards += f"""
        <div class="cat-card" data-cat="{cat_id}">
          <span class="cat-num">{num}</span>
          <h3>{title}</h3>
          <p>{desc}</p>
          <div class="cat-meta"><span>{s['count']} 个文件</span><span>{human_size(s['size'])}</span></div>
        </div>"""

    project_rows = ""
    for p in projects:
        cat_name = CATEGORY_META[p["cat"]][1]
        project_rows += f"""
        <tr>
          <td><strong>{p['name']}</strong><br><small>{p['desc']}</small></td>
          <td>{cat_name}</td>
          <td>{p['role']}</td>
          <td>{p['course']}</td>
          <td>{p['time']}</td>
          <td><code>{p['files']}</code></td>
        </tr>"""

    file_sections = ""
    for cat_id in order:
        num, title, desc = CATEGORY_META[cat_id]
        groups = defaultdict(list)
        for e in items[cat_id]:
            if e["is_dep"]:
                continue
            top = e["path"].split("/")[0] if "/" in e["path"] else "（根目录）"
            groups[top].append(e)

        group_html = ""
        for gname in sorted(groups.keys()):
            files = groups[gname]
            rows = ""
            for f in sorted(files, key=lambda x: (-x["size"], x["name"]))[:30]:
                rows += f"<tr><td>{f['name']}</td><td>{f['ext'] or '—'}</td><td>{human_size(f['size'])}</td></tr>"
            more = f"<tr><td colspan='3' class='more'>... 另有 {len(files)-30} 个文件</td></tr>" if len(files) > 30 else ""
            group_html += f"""
            <details class="file-group">
              <summary>{gname}（{len(files)} 个文件）</summary>
              <table><thead><tr><th>文件名</th><th>类型</th><th>大小</th></tr></thead><tbody>{rows}{more}</tbody></table>
            </details>"""

        dep = sum(1 for e in items[cat_id] if e["is_dep"])
        dep_note = f"<p class='dep-note'>另有 {dep} 个项目依赖文件已折叠</p>" if dep else ""
        file_sections += f"""
        <section class="file-section" id="cat-{cat_id}" data-cat="{cat_id}">
          <h2>{num}、{title}</h2>
          <p class="section-desc">{desc}</p>
          {dep_note}
          {group_html or '<p class="empty">暂无独立文件</p>'}
        </section>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>作品集分类整理 · 秦艺榕</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{ --bg:#faf8f5; --card:#fff; --text:#2d2d3a; --muted:#6b6b7b; --accent:#c45c4a; --border:#e8e4df; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ font-family:'Noto Sans SC',sans-serif; background:var(--bg); color:var(--text); line-height:1.7; }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:40px 24px 80px; }}
    h1 {{ font-size:2rem; margin-bottom:8px; }}
    .subtitle {{ color:var(--muted); margin-bottom:32px; }}
    .back {{ display:inline-block; margin-bottom:24px; color:var(--accent); text-decoration:none; font-weight:500; }}
    .stats {{ display:flex; gap:24px; flex-wrap:wrap; margin-bottom:40px; }}
    .stat {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px 28px; }}
    .stat strong {{ display:block; font-size:1.8rem; color:var(--accent); }}
    .cat-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px; margin-bottom:48px; }}
    .cat-card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; cursor:pointer; transition:.2s; }}
    .cat-card:hover,.cat-card.active {{ border-color:var(--accent); box-shadow:0 4px 20px rgba(196,92,74,.12); }}
    .cat-num {{ font-size:.75rem; color:var(--accent); font-weight:600; }}
    .cat-card h3 {{ font-size:1rem; margin:6px 0; }}
    .cat-card p {{ font-size:.85rem; color:var(--muted); }}
    .cat-meta {{ display:flex; gap:12px; margin-top:10px; font-size:.8rem; color:var(--muted); }}
    h2 {{ font-size:1.4rem; margin:40px 0 12px; padding-bottom:8px; border-bottom:2px solid var(--border); }}
    .section-desc {{ color:var(--muted); margin-bottom:16px; }}
    table {{ width:100%; border-collapse:collapse; background:var(--card); border-radius:8px; overflow:hidden; margin-bottom:24px; font-size:.9rem; }}
    th,td {{ padding:10px 14px; text-align:left; border-bottom:1px solid var(--border); }}
    th {{ background:#f5f0ea; font-weight:600; }}
    code {{ font-size:.8rem; background:#f5f0ea; padding:2px 6px; border-radius:4px; word-break:break-all; }}
    .file-group {{ background:var(--card); border:1px solid var(--border); border-radius:8px; margin-bottom:10px; }}
    .file-group summary {{ padding:14px 18px; cursor:pointer; font-weight:500; }}
    .file-group table {{ margin:0; border-radius:0; }}
    .more {{ color:var(--muted); font-style:italic; }}
    .dep-note,.empty {{ color:var(--muted); font-size:.9rem; margin-bottom:12px; }}
    .filter-bar {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:24px; }}
    .filter-btn {{ padding:8px 18px; border:1px solid var(--border); background:var(--card); border-radius:100px; cursor:pointer; font-size:.85rem; }}
    .filter-btn.active {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
    .file-section.hidden {{ display:none; }}
    small {{ color:var(--muted); }}
  </style>
</head>
<body>
  <div class="wrap">
    <a href="index.html" class="back">← 返回个人主页</a>
    <h1>作品集分类整理</h1>
    <p class="subtitle">基于「作品集」文件夹全部 {total_files} 个文件自动扫描分类 · 总大小 {human_size(total_size)}</p>
    <div class="stats">
      <div class="stat"><strong>{total_files}</strong>总文件数</div>
      <div class="stat"><strong>{len([e for cat in items.values() for e in cat if not e['is_dep']])}</strong>有效文件（不含依赖）</div>
      <div class="stat"><strong>{len(projects)}</strong>核心项目</div>
      <div class="stat"><strong>10</strong>大分类</div>
    </div>

    <h2>分类总览</h2>
    <div class="cat-grid" id="catGrid">{cat_cards}</div>

    <h2>核心项目一览</h2>
    <table>
      <thead><tr><th>项目</th><th>分类</th><th>角色</th><th>课程/场景</th><th>时间</th><th>关键文件</th></tr></thead>
      <tbody>{project_rows}</tbody>
    </table>

    <h2>文件明细</h2>
    <div class="filter-bar" id="filterBar">
      <button class="filter-btn active" data-filter="all">全部</button>
      {"".join(f'<button class="filter-btn" data-filter="{c}">{CATEGORY_META[c][1]}</button>' for c in order)}
    </div>
    {file_sections}
  </div>
  <script>
    const cards = document.querySelectorAll('.cat-card');
    const sections = document.querySelectorAll('.file-section');
    const btns = document.querySelectorAll('.filter-btn');
    function filter(cat) {{
      btns.forEach(b => b.classList.toggle('active', b.dataset.filter === cat));
      cards.forEach(c => c.classList.toggle('active', cat === 'all' || c.dataset.cat === cat));
      sections.forEach(s => s.classList.toggle('hidden', cat !== 'all' && s.dataset.cat !== cat));
    }}
    btns.forEach(b => b.addEventListener('click', () => filter(b.dataset.filter)));
    cards.forEach(c => c.addEventListener('click', () => {{
      filter(c.dataset.cat);
      document.getElementById('cat-' + c.dataset.cat)?.scrollIntoView({{ behavior:'smooth' }});
    }}));
  </script>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote", OUT_HTML)


if __name__ == "__main__":
    items, stats, total_files, total_size = scan()
    write_markdown(items, stats, total_files, total_size)
    write_html(items, stats, total_files, total_size)
