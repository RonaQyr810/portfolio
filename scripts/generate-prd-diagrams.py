#!/usr/bin/env python3
"""Extract Mermaid blocks from wildlife-rescue PRD and render to SVG."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_FILE = ROOT / "projects/wildlife-rescue/wireframes/野生动物收容救护平台-PRD-v4-极简8页版.md"
OUT_DIR = ROOT / "projects/wildlife-rescue/wireframes/diagrams"

DIAGRAMS = [
    ("5-0-business-flow", "5.0 业务流程泳道图"),
    ("5-1-workbench-flow", "5.1 救护工作台交互路径"),
    ("5-2-citizen-flow", "5.2 市民端交互流程"),
    ("5-3-admin-flow", "5.3 管理后台交互流程"),
    ("8-2-state-flow", "8.2 工单状态流转规则"),
]

NODE_LABEL_RE = re.compile(
    r'(<rect class="basic label-container"[^>]*y=")(-?[\d.]+)("[^>]*height=")(\d+)("[^>]*/>\s*'
    r'<g class="label"[^>]*transform="translate\([^,]+,\s*)(-?[\d.]+)(\)[^>]*>\s*'
    r'<rect/>\s*<foreignObject width="[^"]+" height=")(\d+)(">)(.*?)(</foreignObject>)',
    re.S,
)


def _extra_label_padding(br_count: int) -> int:
    """Mermaid often under-allocates foreignObject height for multi-line HTML labels."""
    if br_count >= 2:
        return 24
    if br_count == 1:
        return 12
    return 0


def fix_multiline_label_clipping(svg_path: Path) -> None:
    text = svg_path.read_text(encoding="utf-8")
    extra_bottom = 0.0

    def patch_label(match: re.Match[str]) -> str:
        nonlocal extra_bottom
        inner = match.group(10)
        br_count = inner.count("<br")
        extra = _extra_label_padding(br_count)
        if extra <= 0:
            return match.group(0)

        half = extra / 2
        extra_bottom = max(extra_bottom, half)

        rect_y = float(match.group(2)) - half
        rect_h = int(match.group(4)) + extra
        label_y = float(match.group(6)) - half
        fo_h = int(match.group(8)) + extra

        return (
            f"{match.group(1)}{rect_y:g}{match.group(3)}{rect_h}{match.group(5)}"
            f"{label_y:g}{match.group(7)}{fo_h}{match.group(9)}{inner}{match.group(11)}"
        )

    text = NODE_LABEL_RE.sub(patch_label, text)

    viewbox_match = re.search(
        r'viewBox="(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+)"',
        text,
    )
    if viewbox_match and extra_bottom:
        x, y, width, height = map(float, viewbox_match.groups())
        new_height = height + extra_bottom + 8
        old = viewbox_match.group(0)
        new = f'viewBox="{x:g} {y:g} {width:g} {new_height:g}"'
        text = text.replace(old, new, 1)

    svg_path.write_text(text, encoding="utf-8")


def main() -> int:
    if not MD_FILE.is_file():
        print(f"[错误] 找不到 PRD：{MD_FILE}", file=sys.stderr)
        return 1

    text = MD_FILE.read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
    if len(blocks) != len(DIAGRAMS):
        print(f"[错误] 期望 {len(DIAGRAMS)} 个 Mermaid 块，实际 {len(blocks)} 个", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for (slug, label), block in zip(DIAGRAMS, blocks):
        mmd = OUT_DIR / f"{slug}.mmd"
        svg = OUT_DIR / f"{slug}.svg"
        mmd.write_text(block.strip() + "\n", encoding="utf-8")
        print(f"渲染 {label} -> {svg.name}")
        width = "2400" if slug != "5-0-business-flow" else "1600"
        height = "1200" if slug != "5-0-business-flow" else "1400"
        subprocess.run(
            [
                "npx.cmd",
                "-y",
                "@mermaid-js/mermaid-cli@10.9.0",
                "-i",
                str(mmd),
                "-o",
                str(svg),
                "-b",
                "transparent",
                "--width",
                width,
                "--height",
                height,
            ],
            check=True,
            cwd=str(ROOT),
            shell=True,
        )
        fix_multiline_label_clipping(svg)

    print(f"完成，共 {len(DIAGRAMS)} 张 SVG -> {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
