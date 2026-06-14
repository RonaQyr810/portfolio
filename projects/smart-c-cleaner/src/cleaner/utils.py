from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def format_size(num_bytes: int) -> str:
    if num_bytes < 0:
        num_bytes = 0
    units = ("B", "KB", "MB", "GB", "TB")
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def expand_path(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path)))


def get_system_drive() -> Path:
    return Path(os.environ.get("SystemDrive", "C:") + "\\")


def empty_recycle_bin() -> tuple[bool, str]:
    flags = 0x00000001 | 0x00000002 | 0x00000004
    result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
    if result == 0:
        return True, "回收站已清空"
    return False, f"清空回收站失败，错误码: {result}"


def relaunch_as_admin() -> None:
    if is_admin():
        return
    params = " ".join(f'"{arg}"' for arg in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )
    sys.exit(0)
