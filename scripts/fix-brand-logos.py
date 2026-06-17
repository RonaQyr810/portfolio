# -*- coding: utf-8 -*-
"""从桌面投递版镜像同步品牌 LOGO，并生成变体封面。"""
from __future__ import annotations

import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT = ROOT / "assets" / "portfolio"
DESKTOP = ROOT.parent

MIRROR_ROOTS = [
    DESKTOP / "作品集" / "00-投递版本" / name / "07-在线作品集-个人主页" / "assets" / "portfolio"
    for name in ("作品集-投递版-综合岗", "作品集-投递版-产品经理岗")
]

PS_POST = r"""
Add-Type -AssemblyName System.Drawing
$port = '{port}'
$main = Join-Path $port 'brand-logo-main.png'
$alt = Join-Path $port 'brand-logo-alt.png'
$cover = Join-Path $port 'brand-logo-cover.png'
if (-not (Test-Path $main)) {{ exit 1 }}
$src = [System.Drawing.Image]::FromFile($main)
$x=120; $y=1820; $w=2240; $h=1550
$rect = New-Object System.Drawing.Rectangle $x, $y, $w, $h
$altBmp = New-Object System.Drawing.Bitmap $w, $h
$gAlt = [System.Drawing.Graphics]::FromImage($altBmp)
$gAlt.Clear([System.Drawing.Color]::White)
$gAlt.DrawImage($src, (New-Object System.Drawing.Rectangle 0,0,$w,$h), $rect, [System.Drawing.GraphicsUnit]::Pixel)
$altBmp.Save($alt, [System.Drawing.Imaging.ImageFormat]::Png)
$gAlt.Dispose(); $altBmp.Dispose()
$outW=1600; $outH=1000
$canvas = New-Object System.Drawing.Bitmap $outW, $outH
$g = [System.Drawing.Graphics]::FromImage($canvas)
$g.Clear([System.Drawing.Color]::FromArgb(247,244,240))
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$srcRect = New-Object System.Drawing.Rectangle 120, 120, 2240, 1650
$destH = 900; $destW = [int]($destH * ($srcRect.Width / $srcRect.Height))
$destX = ($outW - $destW) / 2; $destY = ($outH - $destH) / 2
$destRect = New-Object System.Drawing.Rectangle $destX, $destY, $destW, $destH
$g.DrawImage($src, $destRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
$canvas.Save($cover, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $canvas.Dispose(); $src.Dispose()
"""


def is_png(path: Path) -> bool:
    with path.open("rb") as f:
        return f.read(8) == b"\x89PNG\r\n\x1a\n"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        f.seek(16)
        return struct.unpack(">II", f.read(8))


def mirror_file(name: str) -> Path | None:
    for root in MIRROR_ROOTS:
        path = root / name
        if path.is_file() and is_png(path):
            return path
    return None


def write_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    shutil.copyfile(src, dst)


def build_derivatives() -> None:
    script = PS_POST.format(port=str(PORT).replace("'", "''"))
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        check=False,
    )


def main() -> int:
    copied = 0
    for dst_name, src in {
        "brand-logo-main.png": mirror_file("brand-logo-main.png"),
        "brand-logo-restored.png": mirror_file("brand-logo-restored.png"),
    }.items():
        if not src:
            print("MISSING", dst_name)
            continue
        write_copy(src, PORT / dst_name)
        w, h = png_size(PORT / dst_name)
        print(f"OK {dst_name} <- {src.relative_to(DESKTOP)} ({w}x{h})")
        copied += 1

    if copied:
        build_derivatives()
        for name in ("brand-logo-alt.png", "brand-logo-cover.png"):
            path = PORT / name
            if path.is_file() and is_png(path):
                print(f"OK {name} {png_size(path)}")
            else:
                print("WARN", name, "not generated")

    print("Done")
    return 0 if copied else 1


if __name__ == "__main__":
    raise SystemExit(main())
