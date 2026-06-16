# -*- coding: utf-8 -*-
"""Sync 日薪喵 web build from Desktop/cat 2/dist -> projects/rikxiniao/app."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DESKTOP = BASE.parent
APP = BASE / "projects" / "rikxiniao" / "app"

KEEP_IN_APP = {"icons.svg", "favicon.svg"}

CLOUD_PATTERNS = [
    "http://192.168.10.157:8787",
    "https://192.168.10.157:8787",
]

PET_NAME_PATCHES = [
    (
        "className: `input-field pet-name-input`, value: g7.name, onChange: (e97) => _7({ name: e97.target.value }), maxLength: 12",
        "className: `input-field pet-name-input`, value: g7.name, onChange: (e97) => _7({ name: e97.target.value }), onKeyDown: (e97) => { if (e97.key === `Enter`) { e97.preventDefault(); y7 && v7(); } }, maxLength: 12",
    ),
    (
        "className:`input-field pet-name-input`,value:g.name,onChange:e=>_({name:e.target.value}),maxLength:12",
        "className:`input-field pet-name-input`,value:g.name,onChange:e=>_({name:e.target.value}),onKeyDown:e=>{if(e.key===`Enter`){e.preventDefault();y&&v();}},maxLength:12",
    ),
]

ONBOARDING_PATCHES = [
    (
        "className: `input-field`, maxLength: 12, value: Ke5, onChange: (e97) => Je5(e97.target.value)",
        "className: `input-field`, maxLength: 12, value: Ke5, onChange: (e97) => Je5(e97.target.value), onKeyDown: (e97) => { if (e97.key === `Enter`) { e97.preventDefault(); wt4(); } }",
    ),
    (
        "className:`input-field`,maxLength:12,value:Ke,onChange:e=>Je(e.target.value)",
        "className:`input-field`,maxLength:12,value:Ke,onChange:e=>Je(e.target.value),onKeyDown:e=>{if(e.key===`Enter`){e.preventDefault();wt();}}",
    ),
]


def find_cat_dist() -> Path | None:
    direct = DESKTOP / "cat 2" / "dist"
    if direct.is_dir():
        return direct
    for path in DESKTOP.iterdir():
        if not path.is_dir():
            continue
        if "cat" in path.name.lower():
            dist = path / "dist"
            if dist.is_dir() and (dist / "index.html").is_file():
                return dist
    return None


def patch_bundle(path: Path) -> bool:
    if not path.is_file() or path.suffix != ".js":
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    for url in CLOUD_PATTERNS:
        text = text.replace(url, "")
    text = re.sub(r"https?://192\.168\.\d+\.\d+:8787", "", text)
    for old, new in PET_NAME_PATCHES + ONBOARDING_PATCHES:
        if old in text:
            text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("patched", path.relative_to(APP))
        return True
    return False


def parse_dist_index(dist_index: Path) -> dict[str, list[str]]:
    html = dist_index.read_text(encoding="utf-8")
    return {
        "module": re.findall(r'<script[^>]+src="(\./assets/[^"]+\.js)"', html),
        "preload": re.findall(r'<link[^>]+href="(\./assets/[^"]+\.js)"', html),
        "styles": re.findall(r'<link[^>]+href="(\./assets/[^"]+\.css)"', html),
    }


def write_html(target: Path, assets: dict[str, list[str]], *, entry_name: str) -> None:
    module = assets["module"][0] if assets["module"] else "./assets/index.js"
    preloads = assets["preload"]
    styles = assets["styles"]
    entry_pattern = entry_name.replace(".", r"\.")
    preload_lines = "\n".join(
        f'    <link rel="modulepreload" crossorigin href="{href}">' for href in preloads
    )
    style_lines = "\n".join(
        f'    <link rel="stylesheet" crossorigin href="{href}">' for href in styles
    )
    html = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <script>
      (function () {{
        var path = location.pathname;
        if (!/\\/{entry_pattern}$/i.test(path) && !path.endsWith('/')) {{
          location.replace(path + '.html' + location.search + location.hash);
        }}
      }})();
    </script>
    <script>
      try {{ localStorage.removeItem('salary-pet-cloud-token'); }} catch (e) {{}}
    </script>
    <base href="./" />
    <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
    <link rel="apple-touch-icon" href="./favicon.svg" />
    <link rel="manifest" href="./manifest.json" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
    <meta name="theme-color" content="#4A90E2" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="default" />
    <meta name="apple-mobile-web-app-title" content="日薪喵" />
    <title>日薪喵 - 每秒收入计算器</title>
{preload_lines}
{style_lines}
    <script type="module" crossorigin src="{module}"></script>
  </head>
  <body>
    <div id="root"></div>
    <div id="overlay-root"></div>
  </body>
</html>
"""
    target.write_text(html, encoding="utf-8")
    print("OK", target.relative_to(BASE))


def write_manifest(app_dir: Path) -> None:
    manifest = {
        "name": "日薪喵",
        "short_name": "日薪喵",
        "description": "实时显示每秒收入的可爱桌宠",
        "start_url": "./play.html",
        "display": "standalone",
        "background_color": "#4A90E2",
        "theme_color": "#4A90E2",
        "orientation": "portrait",
        "icons": [
            {
                "src": "./favicon.svg",
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            }
        ],
    }
    (app_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("OK manifest.json")


def sync() -> int:
    dist = find_cat_dist()
    if dist is None:
        print("[跳过] 未找到桌面 cat 2/dist")
        return 0

    print("源目录:", dist)
    APP.mkdir(parents=True, exist_ok=True)

    for item in APP.iterdir():
        if item.name in KEEP_IN_APP:
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    copied = 0
    for src in dist.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(dist)
        if rel.parts and rel.parts[0] == "index.html":
            continue
        dst = APP / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    print("OK assets/", copied, "files")

    assets = parse_dist_index(dist / "index.html")
    write_html(APP / "play.html", assets, entry_name="play.html")
    write_html(APP / "index.html", assets, entry_name="index.html")
    write_manifest(APP)

    if not (APP / "favicon.svg").is_file():
        legacy = BASE / "assets" / "portfolio" / "rikxiniao-cover.svg"
        if legacy.is_file():
            shutil.copy2(legacy, APP / "favicon.svg")
            print("OK favicon.svg <- portfolio cover")

    patched = sum(1 for js in (APP / "assets").glob("*.js") if patch_bundle(js))
    print("patched bundles:", patched)
    return 0


def main() -> int:
    return sync()


if __name__ == "__main__":
    raise SystemExit(main())
