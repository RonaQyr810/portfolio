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
                "1400",
                "--height",
                "900",
            ],
            check=True,
            cwd=str(ROOT),
            shell=True,
        )

    print(f"完成，共 {len(DIAGRAMS)} 张 SVG -> {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
