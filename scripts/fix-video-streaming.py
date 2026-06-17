# -*- coding: utf-8 -*-
"""批量修复 assets/videos 中无法网页流式播放的 MP4（moov 在文件末尾）。"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VID = ROOT / "assets" / "videos"
REENCODE_MIN_MB = 45
CRF = "28"


def is_valid_mp4(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            head = handle.read(12)
        if len(head) >= 8 and head[4:8] == b"ftyp":
            return True
        with path.open("rb") as handle:
            chunk = handle.read(1024 * 1024)
        return b"ftyp" in chunk or b"moov" in chunk
    except OSError:
        return False


def is_faststart(path: Path) -> bool:
    try:
        data = path.read_bytes()
        moov, mdat = data.find(b"moov"), data.find(b"mdat")
        return moov > 0 and mdat > 0 and moov < mdat
    except OSError:
        return True


def fix_file(path: Path, ffmpeg: str) -> str:
    rel = path.relative_to(VID)
    if not is_valid_mp4(path):
        return f"SKIP invalid {rel}"
    if is_faststart(path):
        return f"OK   already {rel}"

    mb = path.stat().st_size / (1024 * 1024)
    tmp = path.with_suffix(".streamfix.tmp.mp4")
    if mb >= REENCODE_MIN_MB:
        subprocess.run(
            [
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(path),
                "-c:v", "libx264", "-preset", "medium", "-crf", CRF,
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart",
                str(tmp),
            ],
            check=True,
        )
        action = "REENC"
    else:
        subprocess.run(
            [
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(path),
                "-c", "copy",
                "-movflags", "+faststart",
                str(tmp),
            ],
            check=True,
        )
        action = "REMUX"
    tmp.replace(path)
    new_mb = path.stat().st_size / (1024 * 1024)
    ok = "OK" if is_faststart(path) else "FAIL"
    return f"{ok}  {action} {rel} ({mb:.1f} -> {new_mb:.1f} MB)"


def main() -> int:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ERROR: ffmpeg not found")
        return 1
    if not VID.is_dir():
        print(f"ERROR: missing {VID}")
        return 1

    results: list[str] = []
    for path in sorted(VID.rglob("*.mp4")):
        try:
            results.append(fix_file(path, ffmpeg))
        except subprocess.CalledProcessError as exc:
            results.append(f"ERR  {path.relative_to(VID)} ({exc})")

    print("\n".join(results))
    bad = [line for line in results if line.startswith(("SKIP", "ERR", "FAIL"))]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
